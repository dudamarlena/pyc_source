# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/neuro/AtlasStacker.py
# Compiled at: 2019-09-26 08:58:51
# Size of source mod 2**32: 8707 bytes
import pickle
from photonai.base.PhotonBase import Hyperpipe, PipelineElement, PipelineStacking
from sklearn.base import BaseEstimator
from sklearn.model_selection import ShuffleSplit
import numpy as np
import photonai.photonlogger.Logger as Logger

class RoiFilterElement(BaseEstimator):

    def __init__(self, roi_index):
        self.roi_index = roi_index

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return_data = X[self.roi_index]
        if isinstance(return_data, list):
            return_data = np.asarray(return_data)
        return return_data


class AtlasInfo:

    def __init__(self, atlas_name, roi_names, extraction_mode='mean', background_id=0, mask_threshold=None):
        self.atlas_name = atlas_name
        self.roi_names = roi_names
        self.extraction_mode = extraction_mode
        self.background_id = background_id
        self.mask_threshold = mask_threshold
        self.roi_names_runtime = []


class AtlasStacker(BaseEstimator):

    def __init__(self, atlas_info_object, hyperpipe_elements, best_config_metric=[], metrics=[]):
        self.atlas_info_object = atlas_info_object
        self.atlas_name = self.atlas_info_object.atlas_name
        self.hyperpipe_elements = hyperpipe_elements
        self.pipeline_fusion = None
        self.best_config_metric = best_config_metric
        self.metrics = metrics

    def generate_hyperpipes(self):
        if self.atlas_info_object.roi_names_runtime:
            self.rois = self.atlas_info_object.roi_names_runtime
            inner_pipe_list = {}
            for i in range(len(self.rois)):
                tmp_inner_pipe = Hyperpipe((self.atlas_name + '_' + str(self.rois[i])), optimizer='grid_search', inner_cv=ShuffleSplit(n_splits=1, test_size=0.2, random_state=3),
                  eval_final_performance=False,
                  verbose=(Logger().verbosity_level),
                  best_config_metric=(self.best_config_metric),
                  metrics=(self.metrics))
                roi_filter_element = RoiFilterElement(i)
                tmp_inner_pipe.filter_element = roi_filter_element
                for pipe_item in self.hyperpipe_elements:
                    tmp_inner_pipe += (PipelineElement.create)((pipe_item[0]), (pipe_item[1]), **pipe_item[2])

                inner_pipe_list[self.rois[i]] = tmp_inner_pipe

            self.pipeline_fusion = PipelineStacking('multiple_source_pipes', (inner_pipe_list.values()), voting=False)

    def fit(self, X, y=None):
        if not (self.pipeline_fusion or self.atlas_info_object.roi_names_runtime):
            raise BaseException('No ROIs could be received from Brain Atlas')
        else:
            if not self.pipeline_fusion:
                if self.atlas_info_object.roi_names_runtime:
                    self.generate_hyperpipes()
        self.pipeline_fusion.fit(X, y)
        return self

    def transform(self, X, y=None):
        return self.pipeline_fusion.transform(X, y)