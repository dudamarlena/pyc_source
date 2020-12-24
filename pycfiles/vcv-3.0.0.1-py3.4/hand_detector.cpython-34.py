# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vcv/hand_detector.py
# Compiled at: 2018-06-15 05:30:27
# Size of source mod 2**32: 6490 bytes
import numpy as np, os, cv2, six.moves.urllib as urllib, sys, tarfile, tensorflow as tf, zipfile, collections
from collections import defaultdict
from io import StringIO
from PIL import Image
import datetime, pdb, time as tm
from utils import label_map_util
from utils import visualization_utils as vis_util
from distutils.sysconfig import get_python_lib
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

class hand_detector:

    def __init__(self):
        self.site_package = get_python_lib()
        PATH_TO_CKPT = os.path.join(self.site_package, 'vcv/data/hdm41754')
        PATH_TO_LABELS = os.path.join('data', '/data1/mingmingzhao/hand_detector/data/hand_label_map.pbtxt')
        NUM_CLASSES = 1
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as (fid):
                self.serialized_graph = fid.read()
                od_graph_def.ParseFromString(self.serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        self.label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        self.categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)
        self.sess = None
        with self.detection_graph.as_default():
            self.sess = tf.Session(graph=self.detection_graph)

    def load_image_into_numpy_array(self, image):
        return np.array(image).reshape((120, 160, 3)).astype(np.uint8)

    def detect_hand(self, image):
        image = cv2.resize(image, (160, 120), interpolation=cv2.INTER_CUBIC)
        im_height = 120
        im_width = 160
        image_np = self.load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
        t1 = tm.time()
        boxes, scores, classes, num_detections = self.sess.run([boxes, scores, classes, num_detections], feed_dict={image_tensor: image_np_expanded})
        t2 = tm.time()
        hand_num, center_x, center_y, rect = self.get_hand_num(im_width, im_height, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores), self.category_index)
        return (hand_num, center_x, center_y, rect, t2 - t1)

    def get_hand_num(self, im_width, im_height, boxes, classes, scores, category_index, max_boxes_to_draw=2, min_score_thresh=0.5):
        hand_num = 0
        if scores is None:
            return hand_num
        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores[i] > min_score_thresh:
                hand_num = hand_num + 1
                continue

        center_x = 0
        center_y = 0
        rect = []
        if hand_num > 0:
            box = tuple(boxes[0].tolist())
            ymin, xmin, ymax, xmax = box
            left, right, top, bottom = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
            left = int(left)
            right = int(right)
            top = int(top)
            bottom = int(bottom)
            center_x = (left + right) / 2
            center_y = (right + bottom) / 2
            rect.append(np.array([left, top, right, bottom, scores[0]]))
        return (
         hand_num, center_x, center_y, rect)

    def test():
        hd3 = hand_detector()
        imf = os.path.join(self.site_package, 'vcv/data/test.jpg')
        print(imf)
        image = cv2.imread(imf)
        print(hd3.detect_hand(image))


def log2(message, of):
    print(message)
    of.write(message)


def draw_rect(img, savepath, left, top, right, bottom):
    cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 3)
    cv2.imwrite(savepath, img)
    return img


if __name__ == '__main__':
    dirname = '/data1/mingmingzhao/data_sets/hand_data/test_images/'
    dirname = '/data1/mingmingzhao/data_sets/hand_test_0614_child_1/'
    dirname = '/data1/mingmingzhao/data_sets/no_hand_data/'
    model_number = [
     1473, 41750, 42394, 43042, 43687]
    hd3 = hand_detector()
    hd3.test()
    ci = 0
    ch = 0
    ts = 0
    for f in os.listdir(dirname):
        if f.endswith('.jpg'):
            imf = os.path.join(dirname, f)
            print(imf)
            image = cv2.imread(imf)
            hand_num, center_x, center_y, rect, tc = hd3.detect_hand(image)
            if hand_num > 0:
                ch += 1
            if ci > 1:
                ts += tc
                print('%d/%d,%fs,%fs,%fHz avg' % (ch, ci, tc, ts / (ci - 1), (ci - 1) / ts))
            ci += 1
            continue