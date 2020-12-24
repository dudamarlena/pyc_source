# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/config/path_catlog.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 2463 bytes
import os

class DatasetCatalog:
    DATA_DIR = 'datasets'
    DATASETS = {'voc_2007_train':{'data_dir':'VOC2007', 
      'split':'train'}, 
     'voc_2007_val':{'data_dir':'VOC2007', 
      'split':'val'}, 
     'voc_2007_trainval':{'data_dir':'VOC2007', 
      'split':'trainval'}, 
     'voc_2007_test':{'data_dir':'VOC2007', 
      'split':'test'}, 
     'voc_2012_train':{'data_dir':'VOC2012', 
      'split':'train'}, 
     'voc_2012_val':{'data_dir':'VOC2012', 
      'split':'val'}, 
     'voc_2012_trainval':{'data_dir':'VOC2012', 
      'split':'trainval'}, 
     'voc_2012_test':{'data_dir':'VOC2012', 
      'split':'test'}, 
     'coco_2014_valminusminival':{'data_dir':'val2014', 
      'ann_file':'annotations/instances_valminusminival2014.json'}, 
     'coco_2014_minival':{'data_dir':'val2014', 
      'ann_file':'annotations/instances_minival2014.json'}, 
     'coco_2014_train':{'data_dir':'train2014', 
      'ann_file':'annotations/instances_train2014.json'}, 
     'coco_2014_val':{'data_dir':'val2014', 
      'ann_file':'annotations/instances_val2014.json'}}

    @staticmethod
    def get(name):
        if 'voc' in name:
            voc_root = DatasetCatalog.DATA_DIR
            if 'VOC_ROOT' in os.environ:
                voc_root = os.environ['VOC_ROOT']
            attrs = DatasetCatalog.DATASETS[name]
            args = dict(data_dir=(os.path.join(voc_root, attrs['data_dir'])),
              split=(attrs['split']))
            return dict(factory='VOCDataset', args=args)
        if 'coco' in name:
            coco_root = DatasetCatalog.DATA_DIR
            if 'COCO_ROOT' in os.environ:
                coco_root = os.environ['COCO_ROOT']
            attrs = DatasetCatalog.DATASETS[name]
            args = dict(data_dir=(os.path.join(coco_root, attrs['data_dir'])),
              ann_file=(os.path.join(coco_root, attrs['ann_file'])))
            return dict(factory='COCODataset', args=args)
        raise RuntimeError('Dataset not available: {}'.format(name))