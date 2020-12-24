# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/yolo.py
# Compiled at: 2020-03-29 10:33:01
# Size of source mod 2**32: 29919 bytes
import os, random, cv2, numpy as np, tensorflow as tf
import tensorflow.keras as K
from tensorflow.keras.layers import Input, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model
from tensorflow.python.ops import control_flow_ops
from notekeras.component.yolo import YoloModel
from notekeras.utils.image import boxes_iou_tf, boxes_giou_tf
from notekeras.utils.image import image_resize, boxes_iou_np, postprocess_boxes, nms
STRIDES = np.array([8, 16, 32])
IOU_LOSS_THRESH = 0.5

def get_anchors(index=1):
    """loads the anchors from a file"""
    if index == 0:
        anchors = '10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326'
    else:
        anchors = '1.25,1.625, 2.0,3.75, 4.125,2.875, 1.875,3.8125, 3.875,2.8125, 3.6875,7.4375, 3.625,2.8125, 4.875,6.1875, 11.65625,10.1875'
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)


class YoloBody:

    def __init__(self, anchors, num_classes, num_anchors=None, root='./', *args, **kwargs):
        self.anchors = anchors
        self.num_anchors = num_anchors or len(anchors)
        self.num_classes = num_classes
        self.input_shape = (416, 416)
        self.root = root
        self.yolo_model = self.predict_model = self.train_model = None
        self.build()

    def build(self):
        image_input = Input(shape=(None, None, 3))
        yolo_model = YoloModel((self.num_anchors // 3), (self.num_classes),
          inputs=image_input,
          as_model=True,
          name='Yolo',
          anchors=(self.anchors),
          layer_depth=10)
        self.yolo_model = Model(yolo_model.input, yolo_model.output)
        h, w = self.input_shape
        y_true = [
         Input(shape=(h // 32, w // 32, self.num_anchors // 3, self.num_classes + 5)),
         Input(shape=(h // 16, w // 16, self.num_anchors // 3, self.num_classes + 5)),
         Input(shape=(h // 8, w // 8, self.num_anchors // 3, self.num_classes + 5))]
        model_loss = Lambda(yolo_loss, output_shape=(1, ), name='yolo_loss', arguments={'anchors':self.anchors, 
         'num_classes':self.num_classes, 
         'ignore_thresh':0.5})([*self.yolo_model.output, *y_true])
        self.train_model = Model([self.yolo_model.input, *y_true], model_loss)
        feature_maps = self.yolo_model.output[::-1]
        bbox_tensors = []
        for i, fm in enumerate(feature_maps):
            bbox_tensor = self.decode(fm, index=i)
            bbox_tensors.append(bbox_tensor)

        self.predict_model = tf.keras.Model(self.yolo_model.input, bbox_tensors)
        feature_maps = self.yolo_model.output[::-1]
        bbox_tensors = []
        for i, fm in enumerate(feature_maps):
            bbox_tensor = self.decode(fm, index=i)
            bbox_tensors.append(fm)
            bbox_tensors.append(bbox_tensor)

        self.train_model2 = tf.keras.Model(self.yolo_model.input, bbox_tensors)

    def decode(self, conv_output, index=0):
        anchors = np.array(self.anchors).reshape([3, 3, 2])
        conv_shape = tf.shape(conv_output)
        batch_size = conv_shape[0]
        output_size = conv_shape[1]
        conv_output = tf.reshape(conv_output, (batch_size, output_size, output_size, 3, 5 + self.num_classes))
        conv_raw_dxdy = conv_output[:, :, :, :, 0:2]
        conv_raw_dwdh = conv_output[:, :, :, :, 2:4]
        conv_raw_conf = conv_output[:, :, :, :, 4:5]
        conv_raw_prob = conv_output[:, :, :, :, 5:]
        y = tf.tile(tf.range(output_size, dtype=(tf.int32))[:, tf.newaxis], [1, output_size])
        x = tf.tile(tf.range(output_size, dtype=(tf.int32))[tf.newaxis, :], [output_size, 1])
        xy_grid = tf.concat([x[:, :, tf.newaxis], y[:, :, tf.newaxis]], axis=(-1))
        xy_grid = tf.tile(xy_grid[tf.newaxis, :, :, tf.newaxis, :], [batch_size, 1, 1, 3, 1])
        xy_grid = tf.cast(xy_grid, tf.float32)
        pred_xy = (tf.sigmoid(conv_raw_dxdy) + xy_grid) * STRIDES[index]
        pred_wh = tf.exp(conv_raw_dwdh) * anchors[index] * STRIDES[index]
        pred_xywh = tf.concat([pred_xy, pred_wh], axis=(-1))
        pred_conf = tf.sigmoid(conv_raw_conf)
        pred_prob = tf.sigmoid(conv_raw_prob)
        return tf.concat([pred_xywh, pred_conf, pred_prob], axis=(-1))

    def predict_result(self, image_path=None, original_image=None):
        if original_image is None:
            if image_path is None:
                raise Exception('不能都为None')
        if original_image is None:
            original_image = cv2.imread(image_path)
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        image_data = image_resize(np.copy(original_image), self.input_shape)
        image_data = image_data[(np.newaxis, ...)].astype(np.float32)
        return (
         original_image, self.predict_model.predict(image_data))

    def predict_box(self, image_path=None, original_image=None):
        original_image, pred_box = self.predict_result(image_path, original_image=original_image)
        original_image_size = original_image.shape[:2]
        pred_box = [tf.reshape(x, (-1, tf.shape(x)[(-1)])) for x in pred_box]
        pred_box = tf.concat(pred_box, axis=0)
        boxes = postprocess_boxes(pred_box, original_image_size, self.input_shape[0], 0.3)
        boxes = nms(boxes, 0.45, method='nms')
        return (
         original_image, boxes)

    def train(self):
        trainset = Dataset('train')
        for image_data, target in trainset:
            self.train_model.evaluate(image_data, target[::-1])

    def load_weights(self, filepath, freeze_body=2):
        self.yolo_model.load_weights(filepath)
        print('Load weights success {}.'.format(filepath))
        if freeze_body in (1, 2):
            num = (
             20, len(self.yolo_model.layers) - 2)[(freeze_body - 1)]
            for i in range(num):
                self.yolo_model.layers[i].trainable = False

            print('Freeze the first {} layers of total {} layers.'.format(num, len(self.yolo_model.layers)))

    def debug(self):
        plot_model((self.yolo_model), to_file=(self.root + 'models/yolo-body.png'),
          show_shapes=True)
        plot_model((self.yolo_model), to_file=(self.root + 'models/yolo-body-expand.png'),
          show_shapes=True,
          expand_nested=True)
        plot_model((self.yolo_model), to_file=(self.root + 'models/yolo-train.png'),
          show_shapes=True)
        plot_model((self.yolo_model), to_file=(self.root + 'models/yolo-train-expand.png'),
          show_shapes=True,
          expand_nested=True)

    def yolo_eval(self, inputs, image_shape, max_boxes=20, score_threshold=0.6, iou_threshold=0.5):
        """Evaluate YOLO model on given input and return filtered boxes."""
        yolo_outputs = self.yolo_model.predict(inputs)
        print(yolo_outputs[0][0][0][0][0])
        num_layers = len(yolo_outputs)
        anchor_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]] if num_layers == 3 else [[3, 4, 5], [1, 2, 3]]
        input_shape = K.shape(yolo_outputs[0])[1:3] * 32
        boxes = []
        box_scores = []
        for l in range(num_layers):
            _boxes, _box_scores = self.yolo_eval_boxes_and_scores(yolo_outputs[l], self.anchors[anchor_mask[l]], input_shape, image_shape)
            boxes.append(_boxes)
            box_scores.append(_box_scores)

        boxes, box_scores = K.concatenate(boxes, axis=0), K.concatenate(box_scores, axis=0)
        mask = box_scores >= score_threshold
        max_boxes_tensor = K.constant(max_boxes, dtype='int32')
        out_boxes, out_scores, out_classes = [], [], []
        for c in range(self.num_classes):
            class_boxes = tf.boolean_mask(boxes, mask[:, c])
            class_box_scores = tf.boolean_mask(box_scores[:, c], mask[:, c])
            nms_index = tf.image.non_max_suppression(class_boxes,
              class_box_scores, max_boxes_tensor, iou_threshold=iou_threshold)
            class_boxes = K.gather(class_boxes, nms_index)
            class_box_scores = K.gather(class_box_scores, nms_index)
            classes = K.ones_like(class_box_scores, 'int32') * c
            out_boxes.append(class_boxes)
            out_scores.append(class_box_scores)
            out_classes.append(classes)

        out_boxes = K.concatenate(out_boxes, axis=0)
        out_scores = K.concatenate(out_scores, axis=0)
        out_classes = K.concatenate(out_classes, axis=0)
        return (
         out_boxes, out_scores, out_classes)

    def yolo_eval_boxes_and_scores(self, feats, anchors, input_shape, image_shape):
        """Process Conv layer output"""
        box_xy, box_wh, box_confidence, box_class_probs = yolo_head(feats, anchors, self.num_classes, input_shape)
        boxes = self.yolo_eval_correct_boxes(box_xy, box_wh, input_shape, image_shape)
        boxes = K.reshape(boxes, [-1, 4])
        box_scores = box_confidence * box_class_probs
        box_scores = K.reshape(box_scores, [-1, self.num_classes])
        return (boxes, box_scores)

    @staticmethod
    def yolo_eval_correct_boxes(box_xy, box_wh, input_shape, image_shape):
        """Get corrected boxes"""
        box_yx = box_xy[..., ::-1]
        box_hw = box_wh[..., ::-1]
        input_shape = K.cast(input_shape, K.dtype(box_yx))
        image_shape = K.cast(image_shape, K.dtype(box_yx))
        new_shape = K.round(image_shape * K.min(input_shape / image_shape))
        offset = (input_shape - new_shape) / 2.0 / input_shape
        scale = input_shape / new_shape
        box_yx = (box_yx - offset) * scale
        box_hw *= scale
        box_mins = box_yx - box_hw / 2.0
        box_maxes = box_yx + box_hw / 2.0
        boxes = K.concatenate([
         box_mins[..., 0:1],
         box_mins[..., 1:2],
         box_maxes[..., 0:1],
         box_maxes[..., 1:2]])
        boxes *= K.concatenate([image_shape, image_shape])
        return boxes


def yolo_head(feats, anchors, num_classes, input_shape, calc_loss=False):
    num_anchors = len(anchors)
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])
    grid_shape = K.shape(feats)[1:3]
    grid_height, grid_width = grid_shape[0], grid_shape[1]
    grid_x = K.tile(K.reshape(K.arange(0, stop=grid_width), [1, -1, 1, 1]), [grid_height, 1, 1, 1])
    grid_y = K.tile(K.reshape(K.arange(0, stop=grid_height), [-1, 1, 1, 1]), [1, grid_width, 1, 1])
    grid = K.concatenate([grid_x, grid_y])
    grid = K.cast(grid, feats.dtype)
    feats = K.reshape(feats, [-1, grid_height, grid_width, num_anchors, num_classes + 5])
    box_xy = (K.sigmoid(feats[..., :2]) + grid) / K.cast(grid_shape[::-1], feats.dtype)
    box_wh = K.exp(feats[..., 2:4]) * anchors_tensor / K.cast(input_shape[::-1], feats.dtype)
    if calc_loss is True:
        return (
         grid, feats, box_xy, box_wh)
    box_confidence = K.sigmoid(feats[..., 4:5])
    box_class_probs = K.sigmoid(feats[..., 5:])
    return (box_xy, box_wh, box_confidence, box_class_probs)


def box_iou(b1, b2):
    """Return iou tensor

    Parameters
    ----------
    b1: tensor, shape=(i1,...,iN, 4), xywh
    b2: tensor, shape=(j, 4), xywh

    Returns
    -------
    iou: tensor, shape=(i1,...,iN, j)

    """
    b1 = K.expand_dims(b1, -2)
    b1_xy = b1[..., :2]
    b1_wh = b1[..., 2:4]
    b1_wh_half = b1_wh / 2.0
    b1_mins = b1_xy - b1_wh_half
    b1_maxes = b1_xy + b1_wh_half
    b2 = K.expand_dims(b2, 0)
    b2_xy = b2[..., :2]
    b2_wh = b2[..., 2:4]
    b2_wh_half = b2_wh / 2.0
    b2_mins = b2_xy - b2_wh_half
    b2_maxes = b2_xy + b2_wh_half
    intersect_mins = K.maximum(b1_mins, b2_mins)
    intersect_maxes = K.minimum(b1_maxes, b2_maxes)
    intersect_wh = K.maximum(intersect_maxes - intersect_mins, 0.0)
    intersect_area = intersect_wh[(Ellipsis, 0)] * intersect_wh[(Ellipsis, 1)]
    b1_area = b1_wh[(Ellipsis, 0)] * b1_wh[(Ellipsis, 1)]
    b2_area = b2_wh[(Ellipsis, 0)] * b2_wh[(Ellipsis, 1)]
    iou = intersect_area / (b1_area + b2_area - intersect_area)
    return iou


def yolo_loss(args, anchors, num_classes, ignore_thresh=0.5, print_loss=False):
    """Return yolo_loss tensor

    Parameters
    ----------
    yolo_outputs: list of tensor, the output of yolo_body or tiny_yolo_body
    y_true: list of array, the output of preprocess_true_boxes
    anchors: array, shape=(N, 2), wh
    num_classes: integer
    ignore_thresh: float, the iou threshold whether to ignore object confidence loss

    args Lambda层的输入，即model_body.output和y_true的组合
    anchors 二维数组，结构是(9, 2)，即9个anchor box；
    num_classes 类别数
    ignore_thresh 过滤阈值
    print_loss 打印损失函数的开关
    Returns
    -------
    loss: tensor, shape=(1,)
    :param ignore_thresh:
    :param num_classes:
    :param args:
    :param anchors:
    :param print_loss:
    """
    num_layers = len(anchors) // 3
    y_pred = args[:num_layers]
    y_true = args[num_layers:]
    anchor_mask = [
     [
      6, 7, 8], [3, 4, 5], [0, 1, 2]]
    input_shape = K.cast(K.shape(y_pred[0])[1:3] * 32, K.dtype(y_true[0]))
    grid_shapes = [K.cast(K.shape(y_pred[l])[1:3], K.dtype(y_true[0])) for l in range(num_layers)]
    loss = 0
    batch_size = K.shape(y_pred[0])[0]
    batch_size2 = K.cast(batch_size, K.dtype(y_pred[0]))
    for l in range(num_layers):
        true_raw_xy = y_true[l][..., :2]
        true_raw_wh = y_true[l][..., 2:4]
        true_mask_object = y_true[l][..., 4:5]
        true_class_probs = y_true[l][..., 5:]
        grid, raw_pred, pred_xy, pred_wh = yolo_head((y_pred[l]), (anchors[anchor_mask[l]]),
          num_classes, input_shape, calc_loss=True)
        pred_raw_xy = raw_pred[..., 0:2]
        pred_raw_wh = raw_pred[..., 2:3]
        pred_mask_object = raw_pred[..., 4:5]
        pred_class_probs = raw_pred[..., 5:]
        pred_box = K.concatenate([pred_xy, pred_wh])
        true_raw_xy = true_raw_xy * grid_shapes[l][::-1] - grid
        true_raw_wh = K.log(true_raw_wh / anchors[anchor_mask[l]] * input_shape[::-1])
        true_raw_wh = K.switch(true_mask_object, true_raw_wh, K.zeros_like(true_raw_wh))
        box_loss_scale = 2 - y_true[l][..., 2:3] * y_true[l][..., 3:4]
        object_mask_bool = K.cast(true_mask_object, 'bool')
        ignore_mask = tf.TensorArray((K.dtype(y_true[0])), size=1, dynamic_size=True)

        def loop_body(b, ignore_mask):
            true_box = tf.boolean_mask(y_true[l][b, ..., 0:4], object_mask_bool[(b, ..., 0)])
            iou = box_iou(pred_box[b], true_box)
            best_iou = K.max(iou, axis=(-1))
            ignore_mask = ignore_mask.write(b, K.cast(best_iou < ignore_thresh, K.dtype(true_box)))
            return (b + 1, ignore_mask)

        _, ignore_mask = control_flow_ops.while_loop(lambda b, *args: b < batch_size, loop_body, [0, ignore_mask])
        ignore_mask = ignore_mask.stack()
        ignore_mask = K.expand_dims(ignore_mask, -1)
        loss_xy = true_mask_object * box_loss_scale * K.binary_crossentropy(true_raw_xy, pred_raw_xy, from_logits=True)
        loss_wh = true_mask_object * box_loss_scale * 0.5 * K.square(true_raw_wh - pred_raw_wh)
        loss_conf = K.binary_crossentropy(true_mask_object, pred_mask_object, from_logits=True) * (true_mask_object + (1 - true_mask_object) * ignore_mask)
        loss_class = true_mask_object * K.binary_crossentropy(true_class_probs, pred_class_probs, from_logits=True)
        loss_xy = K.sum(loss_xy) / batch_size2
        loss_wh = K.sum(loss_wh) / batch_size2
        loss_conf = K.sum(loss_conf) / batch_size2
        loss_class = K.sum(loss_class) / batch_size2
        loss += loss_xy + loss_wh + loss_conf + loss_class
        if print_loss:
            loss = tf.Print(loss, [loss, loss_xy, loss_wh, loss_conf, loss_class, K.sum(ignore_mask)], message='loss: ')

    return loss


class Dataset(object):

    def __init__(self, annotation_path, anchors=None, classes=None, repeat=5, batch_size=4):
        self.classes = classes
        self.batch_size = batch_size
        self.annotation_path = annotation_path
        self.anchors = np.array(anchors).reshape([3, 3, 2])
        self.num_classes = len(self.classes)
        self.data_aug = True
        self.input_size = [
         416, 416]
        self.output_size = [[52, 52], [26, 26], [13, 13]]
        self.train_input_sizes = [
         416]
        self.strides = np.array([8, 16, 32])
        self.anchor_per_scale = 3
        self.max_bbox_per_scale = 150
        self.annotations = []
        self.load_annotations()
        self.num_samples = len(self.annotations)
        self.num_batch = int(np.ceil(self.num_samples / self.batch_size))
        self.batch_count = 0
        self.dataset = self.build()
        self.dataset_iterator = self.dataset.repeat(repeat).batch(batch_size).as_numpy_iterator()

    def load_annotations(self):
        with open(self.annotation_path, 'r') as (f):
            txt = f.readlines()
            annotations = [line.strip() for line in txt if len(line.strip().split()[1:]) != 0]
        np.random.shuffle(annotations)
        self.annotations = annotations

    def __iter__(self):
        return self

    def build(self):
        self.train_input_size = random.choice(self.train_input_sizes)
        self.train_output_sizes = self.train_input_size // self.strides
        annotation_size = len(self.annotations)
        temp_size = [
         self.anchor_per_scale, 5 + self.num_classes]
        batch_image = np.zeros((annotation_size, *self.input_size, *(3, )), dtype=(np.float32))
        batch_label_sbbox = np.zeros((annotation_size, *self.output_size[0], *temp_size), dtype=(np.float32))
        batch_label_mbbox = np.zeros((annotation_size, *self.output_size[1], *temp_size), dtype=(np.float32))
        batch_label_lbbox = np.zeros((annotation_size, *self.output_size[2], *temp_size), dtype=(np.float32))
        batch_sbboxes = np.zeros((annotation_size, self.max_bbox_per_scale, 4), dtype=(np.float32))
        batch_mbboxes = np.zeros((annotation_size, self.max_bbox_per_scale, 4), dtype=(np.float32))
        batch_lbboxes = np.zeros((annotation_size, self.max_bbox_per_scale, 4), dtype=(np.float32))
        for num, annotation in enumerate(self.annotations):
            image, bboxes = self.parse_annotation(annotation)
            label_sbbox, label_mbbox, label_lbbox, sbboxes, mbboxes, lbboxes = self.preprocess_true_boxes(bboxes)
            batch_image[num, :, :, :] = image
            batch_label_sbbox[num, :, :, :, :] = label_sbbox
            batch_label_mbbox[num, :, :, :, :] = label_mbbox
            batch_label_lbbox[num, :, :, :, :] = label_lbbox
            batch_sbboxes[num, :, :] = sbboxes
            batch_mbboxes[num, :, :] = mbboxes
            batch_lbboxes[num, :, :] = lbboxes

        self.batch_count += 1
        batch_smaller_target = (batch_label_sbbox, batch_sbboxes)
        batch_medium_target = (batch_label_mbbox, batch_mbboxes)
        batch_larger_target = (batch_label_lbbox, batch_lbboxes)
        dataset_iterator = tf.data.Dataset.from_tensor_slices((
         batch_image, batch_smaller_target, batch_medium_target, batch_larger_target))
        return dataset_iterator

    @staticmethod
    def random_horizontal_flip(image, bboxes):
        if random.random() < 0.5:
            _, w, _ = image.shape
            image = image[:, ::-1, :]
            bboxes[:, [0, 2]] = w - bboxes[:, [2, 0]]
        return (image, bboxes)

    @staticmethod
    def random_crop(image, bboxes):
        if random.random() < 0.5:
            h, w, _ = image.shape
            max_bbox = np.concatenate([np.min((bboxes[:, 0:2]), axis=0), np.max((bboxes[:, 2:4]), axis=0)], axis=(-1))
            max_l_trans = max_bbox[0]
            max_u_trans = max_bbox[1]
            max_r_trans = w - max_bbox[2]
            max_d_trans = h - max_bbox[3]
            crop_xmin = max(0, int(max_bbox[0] - random.uniform(0, max_l_trans)))
            crop_ymin = max(0, int(max_bbox[1] - random.uniform(0, max_u_trans)))
            crop_xmax = max(w, int(max_bbox[2] + random.uniform(0, max_r_trans)))
            crop_ymax = max(h, int(max_bbox[3] + random.uniform(0, max_d_trans)))
            image = image[crop_ymin:crop_ymax, crop_xmin:crop_xmax]
            bboxes[:, [0, 2]] = bboxes[:, [0, 2]] - crop_xmin
            bboxes[:, [1, 3]] = bboxes[:, [1, 3]] - crop_ymin
        return (image, bboxes)

    @staticmethod
    def random_translate(image, bboxes):
        if random.random() < 0.5:
            h, w, _ = image.shape
            max_bbox = np.concatenate([np.min((bboxes[:, 0:2]), axis=0), np.max((bboxes[:, 2:4]), axis=0)], axis=(-1))
            max_l_trans = max_bbox[0]
            max_u_trans = max_bbox[1]
            max_r_trans = w - max_bbox[2]
            max_d_trans = h - max_bbox[3]
            tx = random.uniform(-(max_l_trans - 1), max_r_trans - 1)
            ty = random.uniform(-(max_u_trans - 1), max_d_trans - 1)
            M = np.array([[1, 0, tx], [0, 1, ty]])
            image = cv2.warpAffine(image, M, (w, h))
            bboxes[:, [0, 2]] = bboxes[:, [0, 2]] + tx
            bboxes[:, [1, 3]] = bboxes[:, [1, 3]] + ty
        return (image, bboxes)

    def parse_annotation(self, annotation):
        line = annotation.split()
        image_path = line[0]
        if not os.path.exists(image_path):
            raise KeyError('%s does not exist ... ' % image_path)
        image = cv2.imread(image_path)
        bboxes = np.array([list(map(int, box.split(','))) for box in line[1:]])
        if self.data_aug:
            image, bboxes = self.random_horizontal_flip(np.copy(image), np.copy(bboxes))
            image, bboxes = self.random_crop(np.copy(image), np.copy(bboxes))
            image, bboxes = self.random_translate(np.copy(image), np.copy(bboxes))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image, bboxes = image_resize(np.copy(image), [self.train_input_size, self.train_input_size], np.copy(bboxes))
        return (image, bboxes)

    def preprocess_true_boxes(self, bboxes):
        label = [np.zeros((self.train_output_sizes[i], self.train_output_sizes[i], self.anchor_per_scale, 5 + self.num_classes)) for i in range(3)]
        bboxes_xywh = [np.zeros((self.max_bbox_per_scale, 4)) for _ in range(3)]
        bbox_count = np.zeros((3, ))
        for bbox in bboxes:
            bbox_coor = bbox[:4]
            bbox_class_ind = bbox[4]
            onehot = np.zeros((self.num_classes), dtype=(np.float))
            onehot[bbox_class_ind] = 1.0
            uniform_distribution = np.full(self.num_classes, 1.0 / self.num_classes)
            deta = 0.01
            smooth_onehot = onehot * (1 - deta) + deta * uniform_distribution
            bbox_xywh = np.concatenate([(bbox_coor[2:] + bbox_coor[:2]) * 0.5, bbox_coor[2:] - bbox_coor[:2]], axis=(-1))
            bbox_xywh_scaled = 1.0 * bbox_xywh[np.newaxis, :] / self.strides[:, np.newaxis]
            iou = []
            exist_positive = False
            for i in range(3):
                anchors_xywh = np.zeros((self.anchor_per_scale, 4))
                anchors_xywh[:, 0:2] = np.floor(bbox_xywh_scaled[i, 0:2]).astype(np.int32) + 0.5
                anchors_xywh[:, 2:4] = self.anchors[i]
                iou_scale = boxes_iou_np(bbox_xywh_scaled[i][np.newaxis, :], anchors_xywh)
                iou.append(iou_scale)
                iou_mask = iou_scale > 0.3
                if np.any(iou_mask):
                    xind, yind = np.floor(bbox_xywh_scaled[i, 0:2]).astype(np.int32)
                    label[i][yind, xind, iou_mask, :] = 0
                    label[i][yind, xind, iou_mask, 0:4] = bbox_xywh
                    label[i][yind, xind, iou_mask, 4:5] = 1.0
                    label[i][yind, xind, iou_mask, 5:] = smooth_onehot
                    bbox_ind = int(bbox_count[i] % self.max_bbox_per_scale)
                    bboxes_xywh[i][bbox_ind, :4] = bbox_xywh
                    bbox_count[i] += 1
                    exist_positive = True

            if not exist_positive:
                best_anchor_ind = np.argmax((np.array(iou).reshape(-1)), axis=(-1))
                best_detect = int(best_anchor_ind / self.anchor_per_scale)
                best_anchor = int(best_anchor_ind % self.anchor_per_scale)
                xind, yind = np.floor(bbox_xywh_scaled[best_detect, 0:2]).astype(np.int32)
                label[best_detect][yind, xind, best_anchor, :] = 0
                label[best_detect][yind, xind, best_anchor, 0:4] = bbox_xywh
                label[best_detect][yind, xind, best_anchor, 4:5] = 1.0
                label[best_detect][yind, xind, best_anchor, 5:] = smooth_onehot
                bbox_ind = int(bbox_count[best_detect] % self.max_bbox_per_scale)
                bboxes_xywh[best_detect][bbox_ind, :4] = bbox_xywh
                bbox_count[best_detect] += 1

        label_sbbox, label_mbbox, label_lbbox = label
        sbboxes, mbboxes, lbboxes = bboxes_xywh
        return (label_sbbox, label_mbbox, label_lbbox, sbboxes, mbboxes, lbboxes)

    def __len__(self):
        return self.num_batch

    def __next__(self):
        batch_image, batch_smaller_target, batch_medium_target, batch_larger_target = self.dataset_iterator.next()
        return (batch_image, (batch_smaller_target, batch_medium_target, batch_larger_target))


def compute_loss(num_class, pred, conv, label, boxes, i=0, iou_loss_thresh=0.5, STRIDES=np.array([8, 16, 32])):
    conv_shape = tf.shape(conv)
    batch_size = conv_shape[0]
    output_size = conv_shape[1]
    input_size = STRIDES[i] * output_size
    conv = tf.reshape(conv, (batch_size, output_size, output_size, 3, 5 + num_class))
    conv_raw_conf = conv[:, :, :, :, 4:5]
    conv_raw_prob = conv[:, :, :, :, 5:]
    pred_xywh = pred[:, :, :, :, 0:4]
    pred_conf = pred[:, :, :, :, 4:5]
    label_xywh = label[:, :, :, :, 0:4]
    respond_bbox = label[:, :, :, :, 4:5]
    label_prob = label[:, :, :, :, 5:]
    giou = tf.expand_dims((boxes_giou_tf(pred_xywh, label_xywh)), axis=(-1))
    input_size = tf.cast(input_size, tf.float32)
    bbox_loss_scale = 2.0 - 1.0 * label_xywh[:, :, :, :, 2:3] * label_xywh[:, :, :, :, 3:4] / input_size ** 2
    giou_loss = respond_bbox * bbox_loss_scale * (1 - giou)
    iou = boxes_iou_tf(pred_xywh[:, :, :, :, np.newaxis, :], boxes[:, np.newaxis, np.newaxis, np.newaxis, :, :])
    max_iou = tf.expand_dims(tf.reduce_max(iou, axis=(-1)), axis=(-1))
    respond_bgd = (1.0 - respond_bbox) * tf.cast(max_iou < iou_loss_thresh, tf.float32)
    conf_focal = tf.pow(respond_bbox - pred_conf, 2)
    conf_loss = conf_focal * (respond_bbox * tf.nn.sigmoid_cross_entropy_with_logits(labels=respond_bbox, logits=conv_raw_conf) + respond_bgd * tf.nn.sigmoid_cross_entropy_with_logits(labels=respond_bbox, logits=conv_raw_conf))
    prob_loss = respond_bbox * tf.nn.sigmoid_cross_entropy_with_logits(labels=label_prob, logits=conv_raw_prob)
    giou_loss = tf.reduce_mean(tf.reduce_sum(giou_loss, axis=[1, 2, 3, 4]))
    conf_loss = tf.reduce_mean(tf.reduce_sum(conf_loss, axis=[1, 2, 3, 4]))
    prob_loss = tf.reduce_mean(tf.reduce_sum(prob_loss, axis=[1, 2, 3, 4]))
    return (
     giou_loss, conf_loss, prob_loss)