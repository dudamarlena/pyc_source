# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\datasets\pascal_voc.py
# Compiled at: 2019-12-31 04:09:01
# Size of source mod 2**32: 12708 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, pickle, subprocess, uuid
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np, pylab as pl, scipy.sparse
import datasets.imdb as imdb
import datasets.voc_eval as voc_eval
from model.config import cfg

class pascal_voc(imdb):

    def __init__(self, image_set, use_diff=False):
        name = 'voc_' + image_set
        if use_diff:
            name += '_diff'
        imdb.__init__(self, name)
        self._image_set = image_set
        self._devkit_path = self._get_default_path()
        self._data_path = os.path.join(cfg.TRAIN_DATA_PATH)
        self._classes = cfg.CLASSES
        self._class_to_ind = dict(list(zip(self.classes, list(range(self.num_classes)))))
        self._image_ext = '.jpg'
        self._image_index = self._load_image_set_index()
        self._roidb_handler = self.gt_roidb
        self._salt = str(uuid.uuid4())
        self._comp_id = 'comp4'
        self.config = {'cleanup':True, 
         'use_salt':True, 
         'use_diff':use_diff, 
         'matlab_eval':False, 
         'rpn_file':None}
        assert os.path.exists(self._data_path), 'Path does not exist: {}'.format(self._data_path)

    def image_path_at(self, i):
        """
        Return the absolute path to image i in the image sequence.
        """
        return self.image_path_from_index(self._image_index[i])

    def image_path_from_index(self, index):
        """
        Construct an image path from the image's "index" identifier.
        """
        image_path = os.path.join(self._data_path, 'Images', index + self._image_ext)
        assert os.path.exists(image_path), 'Path does not exist: {}'.format(image_path)
        return image_path

    def _load_image_set_index(self):
        """
        Load the indexes listed in this dataset's image set file.
        """
        image_set_file = os.path.join(self._data_path, 'ImageSets', 'Main', self._image_set + '.txt')
        assert os.path.exists(image_set_file), 'Path does not exist: {}'.format(image_set_file)
        with open(image_set_file) as (f):
            image_index = [x.strip() for x in f.readlines()]
        return image_index

    def _get_default_path(self):
        """
        Return the default path where PASCAL VOC is expected to be installed.
        """
        return os.path.join(cfg.DATA_DIR)

    def gt_roidb(self):
        """
        Return the database of ground-truth regions of interest.

        This function loads/saves from/to a cache file to speed up future calls.
        """
        gt_roidb = [self._load_pascal_annotation(index) for index in self.image_index]
        return gt_roidb

    def rpn_roidb(self):
        if self._image_set != 'test':
            gt_roidb = self.gt_roidb()
            rpn_roidb = self._load_rpn_roidb(gt_roidb)
            roidb = imdb.merge_roidbs(gt_roidb, rpn_roidb)
        else:
            roidb = self._load_rpn_roidb(None)
        return roidb

    def _load_rpn_roidb(self, gt_roidb):
        filename = self.config['rpn_file']
        print('loading {}'.format(filename))
        assert os.path.exists(filename), 'rpn data not found at: {}'.format(filename)
        with open(filename, 'rb') as (f):
            box_list = pickle.load(f)
        return self.create_roidb_from_box_list(box_list, gt_roidb)

    def _load_pascal_annotation(self, index):
        """
        Load image and bounding boxes info from XML file in the PASCAL VOC
        format.
        """
        filename = os.path.join(self._data_path, 'Annotations', index + '.xml')
        tree = ET.parse(filename)
        objs = tree.findall('object')
        if not self.config['use_diff']:
            non_diff_objs = [obj for obj in objs if int(obj.find('difficult').text) == 0]
            objs = non_diff_objs
        num_objs = len(objs)
        boxes = np.zeros((num_objs, 4), dtype=(np.uint16))
        gt_classes = np.zeros(num_objs, dtype=(np.int32))
        overlaps = np.zeros((num_objs, self.num_classes), dtype=(np.float32))
        seg_areas = np.zeros(num_objs, dtype=(np.float32))
        for ix, obj in enumerate(objs):
            bbox = obj.find('bndbox')
            x1 = float(bbox.find('xmin').text)
            y1 = float(bbox.find('ymin').text)
            x2 = float(bbox.find('xmax').text) - 1
            y2 = float(bbox.find('ymax').text) - 1
            cls = self._class_to_ind[obj.find('name').text.strip()]
            boxes[ix, :] = [x1, y1, x2, y2]
            gt_classes[ix] = cls
            overlaps[(ix, cls)] = 1.0
            seg_areas[ix] = (x2 - x1 + 1) * (y2 - y1 + 1)

        overlaps = scipy.sparse.csr_matrix(overlaps)
        return {'boxes':boxes, 
         'gt_classes':gt_classes, 
         'gt_overlaps':overlaps, 
         'flipped':False, 
         'seg_areas':seg_areas}

    def _get_comp_id(self):
        comp_id = self._comp_id + '_' + self._salt if self.config['use_salt'] else self._comp_id
        return comp_id

    def _get_voc_results_file_template(self):
        filename = self._get_comp_id() + '_det_' + self._image_set + '_{:s}.txt'
        path = os.path.join(self._devkit_path, 'results', 'VOC', 'Main', filename)
        return path

    def _write_voc_results_file(self, all_boxes, output_dir):
        for cls_ind, cls in enumerate(self.classes):
            if cls == '__background__':
                continue
            print('Writing {} VOC results file'.format(cls))
            filename = os.path.join(output_dir, cls + '_eval.txt')
            with open(filename, 'wt') as (f):
                for im_ind, index in enumerate(self.image_index):
                    dets = all_boxes[cls_ind][im_ind]
                    if dets == []:
                        continue
                    for k in range(dets.shape[0]):
                        f.write('{:s} {:.3f} {:.1f} {:.1f} {:.1f} {:.1f}\n'.format(index, dets[(k, -1)], dets[(k, 0)] + 1, dets[(k, 1)] + 1, dets[(k, 2)] + 1, dets[(k, 3)] + 1))

    def _do_python_eval(self, output_dir='output'):
        annopath = os.path.join(self._data_path, 'Annotations', '{:s}.xml')
        imagesetfile = os.path.join(self._data_path, 'ImageSets', 'Main', self._image_set + '.txt')
        cachedir = os.path.join(output_dir, 'annotations_cache')
        aps = []
        use_07_metric = True
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        for i, cls in enumerate(self._classes):
            if cls == '__background__':
                continue
            filename = os.path.join(output_dir, cls + '_eval.txt')
            rec, prec, ap = voc_eval(filename,
              annopath, imagesetfile, cls, cachedir, ovthresh=0.5, use_07_metric=use_07_metric,
              use_diff=(self.config['use_diff']))
            aps += [ap]
            pl.plot(rec, prec, lw=2, label=('{} (AP = {:.4f})'.format(cls, ap)))
            print('AP for {} = {:.4f}'.format(cls, ap))
            with open(os.path.join(output_dir, cls + '_pr.pkl'), 'wb') as (f):
                pickle.dump({'rec':rec,  'prec':prec,  'ap':ap}, f)

        pl.xlabel('Recall')
        pl.ylabel('Precision')
        plt.grid(True)
        pl.ylim([0.0, 1.05])
        pl.xlim([0.0, 1.05])
        pl.title('Precision-Recall')
        pl.legend(loc='lower left')
        plt.savefig(os.path.join(output_dir, 'PR.jpg'))
        print('Mean AP = {:.4f}'.format(np.mean(aps)))
        print('~~~~~~~~')
        print('Results:')
        for ap in aps:
            print('{:.3f}'.format(ap))

        print('{:.3f}'.format(np.mean(aps)))
        print('~~~~~~~~')

    def _do_matlab_eval(self, output_dir='output'):
        print('-----------------------------------------------------')
        print('Computing results with the official MATLAB eval code.')
        print('-----------------------------------------------------')
        path = os.path.join(cfg.ROOT_DIR, 'lib', 'datasets', 'VOCdevkit-matlab-wrapper')
        cmd = 'cd {} && '.format(path)
        cmd += '{:s} -nodisplay -nodesktop '.format(cfg.MATLAB)
        cmd += '-r "dbstop if error; '
        cmd += 'voc_eval(\'{:s}\',\'{:s}\',\'{:s}\',\'{:s}\'); quit;"'.format(self._devkit_path, self._get_comp_id(), self._image_set, output_dir)
        print('Running:\n{}'.format(cmd))
        status = subprocess.call(cmd, shell=True)

    def evaluate_detections(self, all_boxes, output_dir):
        self._write_voc_results_file(all_boxes, output_dir)
        self._do_python_eval(output_dir)

    def competition_mode(self, on):
        if on:
            self.config['use_salt'] = False
            self.config['cleanup'] = False
        else:
            self.config['use_salt'] = True
            self.config['cleanup'] = True


if __name__ == '__main__':
    import datasets.pascal_voc as pascal_voc
    d = pascal_voc('trainval', '2007')
    res = d.roidb