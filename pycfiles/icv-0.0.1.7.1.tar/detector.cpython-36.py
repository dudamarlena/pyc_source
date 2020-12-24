# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/detector/detector.py
# Compiled at: 2019-09-26 03:41:53
# Size of source mod 2**32: 2619 bytes
import torch, numpy as np
from ..utils import is_seq, is_file, is_str, labelmap_to_category_index
from abc import ABCMeta, abstractmethod
from .service.server import DetectorServer

class Detector(object):
    __metaclass__ = ABCMeta

    def __init__(self, categories=None, labelmap_path=None, iou_thr=0.5, score_thr=0.5, device=None):
        if not is_seq(categories):
            if not is_file(labelmap_path):
                raise AssertionError('param categories and param labelmap_path should input at_least one.')
        else:
            assert iou_thr > 0 and iou_thr < 1, 'param iou_thr should > 0 and < 1.'
            assert score_thr > 0 and score_thr < 1, 'param score_thr should > 0 and < 1.'
        self.categories = categories
        self.labelmap_path = labelmap_path
        self.iou_thr = iou_thr
        self.score_thr = score_thr
        self.device = device if device else torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self._labelmap()

    def _labelmap(self):
        if self.categories is not None:
            self.category_index = {id + 1:{'id':id + 1,  'name':label} for id, label in enumerate(self.categories)}
            self.category_name_index = {self.category_index[cat_id]['name']:self.category_index[cat_id] for cat_id in self.category_index}
        else:
            self.category_index = labelmap_to_category_index((self.labelmap_path), use_display_name=True)
            self.category_name_index = {self.category_index[cat_id]['name']:self.category_index[cat_id] for cat_id in self.category_index}

    def _warmup(self):
        self.inference(np.zeros((100, 100, 3), dtype=(np.uint8)))

    @abstractmethod
    def inference(self, image, is_show=False, save_path=None, score_thr=-1):
        pass

    @abstractmethod
    def inference_batch(self, images, save_dir=None, resize=None, score_thr=-1):
        pass

    @abstractmethod
    def start_server(self, port=9527, open_web=True, secret=None, upload_dir=None, debug=True, name='', default_params_score_thr=0.5):
        assert isinstance(port, int)
        if not secret is None:
            if not is_str(secret):
                raise AssertionError
        server = DetectorServer(self,
          secrect=secret,
          open_web=open_web,
          name=name,
          default_params_score_thr=default_params_score_thr)
        server.start_server(port=port, upload_dir=upload_dir, debug=debug)