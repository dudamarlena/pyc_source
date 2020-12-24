# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\_detection.py
# Compiled at: 2019-12-31 04:09:01
# Size of source mod 2**32: 26850 bytes
import os, sys, tempfile, cv2, numpy as np, rasterio, tensorflow as tf, yaml
from dotmap import DotMap
from geojson import Feature as geojsonFeature
from geojson import FeatureCollection
from geojson import Polygon, dump
from rasterio import transform
from rasterio.plot import reshape_as_image
from rasterio.windows import Window
from iobjectspy import Feature, FieldInfo, GeoLine, import_geojson
from iobjectspy._jsuperpy.data._util import get_output_datasource
from iobjectspy.ml.toolkit._toolkit import del_dir
from iobjectspy.ml.utils import datasetraster_to_numpy_array

class FasterRCNNEstimation(object):

    def __init__(self, model_path, cfg):
        self.model_path = model_path
        self.cfg = cfg
        self.load_model(model_path)

    def estimation_numpy(self, input_data, category_name, nms_thresh=0.3, score_thresh=0.5, **kwargs):
        """"
        进行影像数据目标检测
        """
        self.input_data = input_data
        self.category_name = category_name
        self.nms_thresh = nms_thresh
        self.score_thresh = score_thresh
        height = self.input_data.shape[0]
        blobs, im_scales = self._get_blobs(self.input_data)
        im_blob = blobs['data']
        blobs['im_info'] = np.array([im_blob.shape[1], im_blob.shape[2], im_scales[0]], dtype=(np.float32))
        _, scores, bbox_pred, rois = self.sess.run([self.score, self.prob, self.pred, self.rois], feed_dict={self.im_data: blobs['data'], 
         self.im_info: blobs['im_info']})
        self.sess.graph.finalize()
        boxes = rois[:, 1:5] / im_scales[0]
        scores = np.reshape(scores, [scores.shape[0], -1])
        bbox_pred = np.reshape(bbox_pred, [bbox_pred.shape[0], -1])
        box_deltas = bbox_pred
        pred_boxes = self._bbox_transform_inv(boxes, box_deltas)
        pred_boxes = self._clip_boxes(pred_boxes, self.input_data.shape)
        features = []
        for cls_ind, cls in enumerate(self.category_names[0:]):
            cls_ind += 1
            cls_boxes = pred_boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
            cls_scores = scores[:, cls_ind]
            dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
            keep = self.nms(dets)
            dets = dets[keep, :]
            inds = np.where(dets[:, -1] >= self.score_thresh)[0]
            if len(inds) > 0 and cls in self.category_name:
                for i in inds:
                    bbox = dets[i, :4]
                    x1 = round(float(bbox[0]), 4)
                    y1 = round(float(bbox[1]), 4)
                    x2 = round(float(bbox[2]), 4)
                    y2 = round(float(bbox[3]), 4)
                    polygon = Polygon([(x1, height - y2),
                     (
                      x2, height - y2),
                     (
                      x2, height - y1),
                     (
                      x1, height - y1),
                     (
                      x1, height - y2)])
                    features.append(geojsonFeature(geometry=polygon, properties={'category': cls}))

        return features

    def estimation_large_img(self, input_data, category_name, out_data, out_name, nms_thresh=0.3, score_thresh=0.5):
        """
            进行大幅影像数据目标检测
            """
        self.input_data = input_data
        self.category_name = category_name
        self.out_data = out_data
        self.out_name = out_name
        self.nms_thresh = nms_thresh
        self.score_thresh = score_thresh
        if isinstance(self.out_data, str):
            pardir_out_path = os.path.abspath(os.path.join(self.out_data, os.path.pardir))
            if not os.path.exists(pardir_out_path):
                os.makedirs(pardir_out_path)
        if self.tile_offset == self.blocksize:
            raise ValueError('tile_offset and blocksize is same!')
        else:
            if self.tile_offset > self.blocksize:
                raise ValueError('tile_offset is bigger than blocksize!')
            else:
                features = []
                with rasterio.open(self.input_data) as (ds):
                    width_block = ds.width // self.tile_offset
                    height_block = ds.height // self.tile_offset
                    try:
                        crs = ds.crs.data['init']
                        crs = {'type':'name',  'properties':{'name': crs}}
                    except:
                        crs = 'null'

                    p = 0
                    all_boxes = []
                    try:
                        one_pixel = ds.res[0]
                    except:
                        pass

                    for i in range(height_block):
                        for j in range(width_block):
                            all_boxes = self._get_bbox(ds, j, i, all_boxes)
                            p += 1
                            self._view_bar(p, height_block * width_block)

                    for cls_ind, cls in enumerate(self.category_name[0:]):
                        all_boxes_temp = []
                        for i in all_boxes:
                            if str(cls) == i[5]:
                                all_boxes_temp.append(i[0:5])

                        all_boxes_temp = np.array(all_boxes_temp)
                        if all_boxes_temp != np.array([]):
                            keep = self.nms(all_boxes_temp, one_pixel)
                            all_boxes_temp = all_boxes_temp[keep, :]
                        for bbox_score in all_boxes_temp:
                            polygon = Polygon([
                             [(float(bbox_score[0]), float(bbox_score[3])),
                              (
                               float(bbox_score[2]), float(bbox_score[3])),
                              (
                               float(bbox_score[2]), float(bbox_score[1])),
                              (
                               float(bbox_score[0]), float(bbox_score[1])),
                              (
                               float(bbox_score[0]), float(bbox_score[3]))]])
                            features.append(geojsonFeature(geometry=polygon, properties={'category':cls,  'score':bbox_score[4]}))

                    name = self.out_name.split('.')[0]
                    feature_collection = FeatureCollection(features, name=name, crs=crs)
                    temp_json_path = os.path.join(tempfile.mkdtemp(), 'temp') + '.json'
                    with open(temp_json_path, 'w') as (f):
                        dump(feature_collection, f)
                    out_datasource = get_output_datasource(self.out_data)
                    result = import_geojson(temp_json_path, out_datasource, self.out_name)
                    del_dir(os.path.abspath(os.path.join(temp_json_path, os.path.pardir)))
                    features.clear()
                    feature_collection.clear()
                    result = result[0] if (isinstance(result, list) and len(result) > 0) else result
                    out_datasource.close()
                self.close_model(self.sess)
                return result

    def estimation_img(self, input_data, category_name, out_data, out_name, nms_thresh=0.3, score_thresh=0.5):
        """
        进行影像数据目标检测
        """
        self.input_data = input_data
        self.category_name = category_name
        self.out_data = out_data
        self.out_name = out_name
        self.nms_thresh = nms_thresh
        self.score_thresh = score_thresh
        if isinstance(self.out_data, str):
            pardir_out_path = os.path.abspath(os.path.join(self.out_data, os.path.pardir))
            if not os.path.exists(pardir_out_path):
                os.makedirs(pardir_out_path)
        elif self._is_image_file():
            crs, image, transf = self._image_read(self.input_data)
        else:
            image = datasetraster_to_numpy_array(self.input_data)
            image = np.transpose(image, (1, 2, 0))
            image = image[:, :, (2, 1, 0)]
        height = image.shape[0]
        blobs, im_scales = self._get_blobs(image)
        im_blob = blobs['data']
        blobs['im_info'] = np.array([im_blob.shape[1], im_blob.shape[2], im_scales[0]], dtype=(np.float32))
        _, scores, bbox_pred, rois1 = self.sess.run([self.score, self.prob, self.pred, self.rois], feed_dict={self.im_data: blobs['data'], 
         self.im_info: blobs['im_info']})
        self.close_model(self.sess)
        boxes = rois1[:, 1:5] / im_scales[0]
        scores = np.reshape(scores, [scores.shape[0], -1])
        bbox_pred = np.reshape(bbox_pred, [bbox_pred.shape[0], -1])
        box_deltas = bbox_pred
        pred_boxes = self._bbox_transform_inv(boxes, box_deltas)
        pred_boxes = self._clip_boxes(pred_boxes, image.shape)
        features = []
        for cls_ind, cls in enumerate(self.category_names[0:]):
            cls_ind += 1
            cls_boxes = pred_boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
            cls_scores = scores[:, cls_ind]
            dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
            keep = self.nms(dets)
            dets = dets[keep, :]
            inds = np.where(dets[:, -1] >= self.score_thresh)[0]
            if len(inds) > 0 and str(cls) in self.category_name:
                if self._is_image_file():
                    for i in inds:
                        bbox = dets[i, :4]
                        if transf[0] == 1.0 and transf[1] == 0.0:
                            x1 = round(float(bbox[0]), 4)
                            y1 = round(float(bbox[1]), 4)
                            x2 = round(float(bbox[2]), 4)
                            y2 = round(float(bbox[3]), 4)
                            polygon = Polygon([(x1, height - y2),
                             (
                              x2, height - y2),
                             (
                              x2, height - y1),
                             (
                              x1, height - y1),
                             (
                              x1, height - y2)])
                            features.append(geojsonFeature(geometry=polygon, properties={'category': cls}))
                        else:
                            coord_min = transform.xy(transf, int(bbox[1]), int(bbox[0]))
                            coord_max = transform.xy(transf, int(bbox[3]), int(bbox[2]))
                            polygon = Polygon([
                             [(coord_min[0], coord_max[1]),
                              (
                               coord_max[0], coord_max[1]),
                              (
                               coord_max[0], coord_min[1]),
                              (
                               coord_min[0], coord_min[1]),
                              (
                               coord_min[0], coord_max[1])]])
                            features.append(geojsonFeature(geometry=polygon, properties={'category': cls}))

            else:
                for i in inds:
                    feature = Feature()
                    feature.add_field_info(FieldInfo('category', 'WTEXT'))
                    feature.set_values([cls])
                    bbox = dets[i, :4]
                    point_1 = input_data.image_to_xy(int(bbox[0]), int(bbox[3]))
                    point_2 = input_data.image_to_xy(int(bbox[2]), int(bbox[3]))
                    point_3 = input_data.image_to_xy(int(bbox[2]), int(bbox[1]))
                    point_4 = input_data.image_to_xy(int(bbox[0]), int(bbox[1]))
                    point_5 = input_data.image_to_xy(int(bbox[0]), int(bbox[3]))
                    feature.set_geometry(GeoLine([
                     point_1,
                     point_2,
                     point_3,
                     point_4,
                     point_5]))
                    features.append(feature)

        if self._is_image_file():
            name = self.out_name
            feature_collection = FeatureCollection(features, name=name, crs=crs)
            temp_json_path = os.path.join(tempfile.mkdtemp(), 'temp') + '.json'
            with open(temp_json_path, 'w') as (f):
                dump(feature_collection, f)
            out_datasource = get_output_datasource(self.out_data)
            result = import_geojson(temp_json_path, out_datasource, self.out_name)
            del_dir(os.path.abspath(os.path.join(temp_json_path, os.path.pardir)))
            result = result[0] if (isinstance(result, list) and len(result) > 0) else result
            out_datasource.close()
            return result
        out_datasource = get_output_datasource(self.out_data)
        out_datasource.write_features(features, self.out_name)
        out_datasource.close()

    def _get_bbox(self, ds, j, i, all_boxes):
        transf = ds.transform
        height = ds.height
        try:
            one_pixel = ds.res[0]
        except:
            pass

        block = np.zeros([3, self.blocksize, self.blocksize], dtype=(np.uint8))
        img = ds.read(window=(Window(j * self.tile_offset, i * self.tile_offset, self.blocksize, self.blocksize)))
        block[:, :img.shape[1], :img.shape[2]] = img[:3, :, :]
        block = reshape_as_image(block)
        block = cv2.cvtColor(block, cv2.COLOR_RGB2BGR)
        blobs, im_scales = self._get_blobs(block)
        im_blob = blobs['data']
        blobs['im_info'] = np.array([im_blob.shape[1], im_blob.shape[2], im_scales[0]], dtype=(np.float32))
        _, scores, bbox_pred, rois = self.sess.run([self.score, self.prob, self.pred, self.rois], feed_dict={self.im_data: blobs['data'], 
         self.im_info: blobs['im_info']})
        self.sess.graph.finalize()
        boxes = rois[:, 1:5] / im_scales[0]
        scores = np.reshape(scores, [scores.shape[0], -1])
        bbox_pred = np.reshape(bbox_pred, [bbox_pred.shape[0], -1])
        box_deltas = bbox_pred
        pred_boxes = self._bbox_transform_inv(boxes, box_deltas)
        pred_boxes = self._clip_boxes(pred_boxes, block.shape)
        for cls_ind, cls in enumerate(self.category_names[0:]):
            cls_ind += 1
            cls_boxes = pred_boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
            cls_scores = scores[:, cls_ind]
            dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
            keep = self.nms(dets, one_pixel)
            dets = dets[keep, :]
            inds = np.where(dets[:, -1] >= self.score_thresh)[0]
            if len(inds) > 0 and str(cls) in self.category_name:
                for s in inds:
                    bbox = dets[s, :5]
                    if transf.xoff == 0.0 and transf.yoff == 0.0:
                        xmin = round(float(bbox[0]), 4) + j * self.tile_offset
                        ymin = height - (round(float(bbox[3]), 4) + i * self.tile_offset)
                        xmax = round(float(bbox[2]), 4) + j * self.tile_offset
                        ymax = height - (round(float(bbox[1]), 4) + i * self.tile_offset)
                        score_single_bbox = round(float(bbox[4]), 4)
                    else:
                        coord_min = transform.xy(transf, bbox[1] + i * float(self.tile_offset), bbox[0] + j * float(self.tile_offset))
                        coord_max = transform.xy(transf, bbox[3] + i * float(self.tile_offset), bbox[2] + j * float(self.tile_offset))
                        xmin = coord_min[0]
                        ymin = coord_max[1]
                        xmax = coord_max[0]
                        ymax = coord_min[1]
                        score_single_bbox = bbox[4]
                    all_boxes.append([
                     xmin, ymin, xmax, ymax, score_single_bbox, str(cls)])

        return all_boxes

    def close_model(self, sess):
        """
        关闭模型
        :return:
        """
        sess.close()
        tf.reset_default_graph()

    def _get_blobs(self, im):
        """将影像以及ROI转换为网络输入"""
        blobs = {}
        blobs['data'], im_scale_factors = self._get_image_blob(im)
        return (
         blobs, im_scale_factors)

    def _get_image_blob(self, im):
        """Converts an image into a network input.
        Arguments:
          im (ndarray): a color image in BGR order
        Returns:
          blob (ndarray): a data blob holding an image pyramid
          im_scale_factors (list): list of image scales (relative to im) used
            in the image pyramid
        """
        im_orig = im.astype((np.float32), copy=True)
        im_orig -= np.array([[[102.9801, 115.9465, 122.7717]]])
        im_shape = im_orig.shape
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])
        processed_ims = []
        im_scale_factors = []
        for target_size in (600, ):
            im_scale = float(target_size) / float(im_size_min)
            if np.round(im_scale * im_size_max) > 1000:
                im_scale = float(1000) / float(im_size_max)
            im = cv2.resize(im_orig, None, None, fx=im_scale, fy=im_scale, interpolation=(cv2.INTER_LINEAR))
            im_scale_factors.append(im_scale)
            processed_ims.append(im)

        blob = self._im_list_to_blob(processed_ims)
        return (
         blob, np.array(im_scale_factors))

    def _im_list_to_blob(self, ims):
        """Convert a list of images into a network input.

        Assumes images are already prepared (means subtracted, BGR order, ...).
        """
        max_shape = np.array([im.shape for im in ims]).max(axis=0)
        num_images = len(ims)
        blob = np.zeros((num_images, max_shape[0], max_shape[1], 3), dtype=(np.float32))
        for i in range(num_images):
            im = ims[i]
            blob[i, 0:im.shape[0], 0:im.shape[1], :] = im

        return blob

    def _clip_boxes(self, boxes, im_shape):
        """Clip boxes to image boundaries."""
        boxes[:, 0::4] = np.maximum(boxes[:, 0::4], 0)
        boxes[:, 1::4] = np.maximum(boxes[:, 1::4], 0)
        boxes[:, 2::4] = np.minimum(boxes[:, 2::4], im_shape[1] - 1)
        boxes[:, 3::4] = np.minimum(boxes[:, 3::4], im_shape[0] - 1)
        return boxes

    def _bbox_transform_inv(self, boxes, deltas):
        if boxes.shape[0] == 0:
            return np.zeros((0, deltas.shape[1]), dtype=(deltas.dtype))
        boxes = boxes.astype((deltas.dtype), copy=False)
        widths = boxes[:, 2] - boxes[:, 0] + 1.0
        heights = boxes[:, 3] - boxes[:, 1] + 1.0
        ctr_x = boxes[:, 0] + 0.5 * widths
        ctr_y = boxes[:, 1] + 0.5 * heights
        dx = deltas[:, 0::4]
        dy = deltas[:, 1::4]
        dw = deltas[:, 2::4]
        dh = deltas[:, 3::4]
        pred_ctr_x = dx * widths[:, np.newaxis] + ctr_x[:, np.newaxis]
        pred_ctr_y = dy * heights[:, np.newaxis] + ctr_y[:, np.newaxis]
        pred_w = np.exp(dw) * widths[:, np.newaxis]
        pred_h = np.exp(dh) * heights[:, np.newaxis]
        pred_boxes = np.zeros((deltas.shape), dtype=(deltas.dtype))
        pred_boxes[:, 0::4] = pred_ctr_x - 0.5 * pred_w
        pred_boxes[:, 1::4] = pred_ctr_y - 0.5 * pred_h
        pred_boxes[:, 2::4] = pred_ctr_x + 0.5 * pred_w
        pred_boxes[:, 3::4] = pred_ctr_y + 0.5 * pred_h
        return pred_boxes

    def nms(self, dets, one_pixel=1):
        """nms过程,去除重复框"""
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]
        areas = (x2 - x1 + one_pixel) * (y2 - y1 + one_pixel)
        order = scores.argsort()[::-1]
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            w = np.maximum(0.0, xx2 - xx1 + one_pixel)
            h = np.maximum(0.0, yy2 - yy1 + one_pixel)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= self.nms_thresh)[0]
            order = order[(inds + 1)]

        return keep

    def _is_image_file(self):
        """
        输入数据是否为影像文件
        通过后缀名判断
        """
        data_is_image = True
        try:
            rasterio.open(self.input_data)
        except Exception as e:
            try:
                data_is_image = False
            finally:
                e = None
                del e

        return data_is_image

    def _image_read(self, path):
        with rasterio.open(path) as (ds):
            img = ds.read()
            transform = ds.transform
            try:
                crs = ds.crs.data['init']
                crs = {'type':'name',  'properties':{'name': crs}}
            except:
                crs = 'null'

        img = img[:3, :, :]
        img = reshape_as_image(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return (
         crs, img, transform)

    def _view_bar(self, num, total):
        rate = float(num) / float(total)
        rate_num = int(rate * 100)
        r = '\r[%s%s]%d%%,%d' % ('>' * rate_num, '-' * (100 - rate_num), rate_num, num)
        sys.stdout.write(r)
        sys.stdout.flush()

    def load_model(self, model_path):
        self.model_path = model_path
        self.sess = tf.Session()
        self.meta_graph_def = tf.saved_model.loader.load(self.sess, ['serve'], model_path)
        self.signature = self.meta_graph_def.signature_def
        im_data_tensor_name = self.signature['predict'].inputs['im_data'].name
        im_info_tensor_name = self.signature['predict'].inputs['im_info'].name
        score_tensor_name = self.signature['predict'].outputs['score'].name
        prob_tensor_name = self.signature['predict'].outputs['prob'].name
        pred_tensor_name = self.signature['predict'].outputs['pred'].name
        rois_tensor_name = self.signature['predict'].outputs['rois'].name
        self.im_data = self.sess.graph.get_tensor_by_name(im_data_tensor_name)
        self.im_info = self.sess.graph.get_tensor_by_name(im_info_tensor_name)
        self.score = self.sess.graph.get_tensor_by_name(score_tensor_name)
        self.prob = self.sess.graph.get_tensor_by_name(prob_tensor_name)
        self.pred = self.sess.graph.get_tensor_by_name(pred_tensor_name)
        self.rois = self.sess.graph.get_tensor_by_name(rois_tensor_name)
        with open(self.cfg) as (f):
            config_dict = yaml.load(f, Loader=(yaml.FullLoader))
        config = DotMap(config_dict)
        config.get('model').get('categorys').remove('__background__')
        self.category_names = config.get('model').get('categorys')
        self.blocksize = config.get('model').get('blocksize')
        self.tile_offset = config.get('model').get('tile_offset')
        config_categorys_num = len(config.get('model').get('categorys')) + 1
        tf.reset_default_graph()
        stds = np.tile(np.array([0.1, 0.1, 0.2, 0.2]), config_categorys_num)
        means = np.tile(np.array([0.0, 0.0, 0.0, 0.0]), config_categorys_num)
        self.pred *= stds
        self.pred += means