# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/neuro/atlas_mapping.py
# Compiled at: 2019-09-26 11:32:58
# Size of source mod 2**32: 9173 bytes
import json, os
from glob import glob
from typing import Union
import joblib
import matplotlib.pylab as plt
import numpy as np, pandas as pd
from nilearn import datasets, surface, plotting
from photonai.base import PipelineElement
from photonai.base.hyperpipe import Hyperpipe
from photonai.neuro.brain_atlas import BrainAtlas, AtlasLibrary
from photonai.neuro.neuro_branch import NeuroBranch
import photonai.photonlogger.logger as logger
from photonai.processing import ResultsHandler

class AtlasMapper:

    def __init__(self, create_surface_plots: bool=False):
        self.folder = None
        self.neuro_element = None
        self.original_hyperpipe_name = None
        self.roi_list = None
        self.atlas = None
        self.hyperpipe_infos = None
        self.hyperpipes_to_fit = None
        self.roi_indices = dict()
        self.best_config_metric = None
        self.create_surface_plots = create_surface_plots

    def generate_mappings(self, hyperpipe: Hyperpipe, neuro_element: Union[(NeuroBranch, PipelineElement)], folder: str):
        self.folder = folder
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        self.neuro_element = neuro_element
        self.original_hyperpipe_name = hyperpipe.name
        self.roi_list, self.atlas = self._find_brain_atlas(self.neuro_element)
        self.verbosity = hyperpipe.verbosity
        self.hyperpipe_infos = None
        self.best_config_metric = hyperpipe.optimization.best_config_metric
        hyperpipes_to_fit = dict()
        if len(self.roi_list) > 0:
            for roi_index, roi_name in enumerate(self.roi_list):
                self.roi_indices[roi_name] = roi_index
                copy_of_hyperpipe = hyperpipe.copy_me()
                new_pipe_name = copy_of_hyperpipe.name + '_Atlas_Mapper_' + roi_name
                copy_of_hyperpipe.name = new_pipe_name
                copy_of_hyperpipe.output_settings.project_folder = folder
                copy_of_hyperpipe.output_settings.overwrite_results = True
                copy_of_hyperpipe.output_settings.save_output = True
                hyperpipes_to_fit[roi_name] = copy_of_hyperpipe

        else:
            raise Exception('No Rois found...')
        self.hyperpipes_to_fit = hyperpipes_to_fit

    def _find_brain_atlas--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              list
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'roi_list'

 L.  64         6  LOAD_GLOBAL              list
                8  CALL_FUNCTION_0       0  '0 positional arguments'
               10  STORE_FAST               'atlas_obj'

 L.  65        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'neuro_element'
               16  LOAD_GLOBAL              NeuroBranch
               18  CALL_FUNCTION_2       2  '2 positional arguments'
               20  POP_JUMP_IF_FALSE    74  'to 74'

 L.  66        22  SETUP_LOOP          108  'to 108'
               24  LOAD_FAST                'neuro_element'
               26  LOAD_ATTR                elements
               28  GET_ITER         
             30_0  COME_FROM            44  '44'
               30  FOR_ITER             70  'to 70'
               32  STORE_FAST               'element'

 L.  67        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'element'
               38  LOAD_ATTR                base_element
               40  LOAD_GLOBAL              BrainAtlas
               42  CALL_FUNCTION_2       2  '2 positional arguments'
               44  POP_JUMP_IF_FALSE    30  'to 30'

 L.  68        46  LOAD_STR                 'list'
               48  LOAD_FAST                'element'
               50  LOAD_ATTR                base_element
               52  STORE_ATTR               collection_mode

 L.  69        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _find_rois
               58  LOAD_FAST                'element'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'roi_list'
               66  STORE_FAST               'atlas_obj'
               68  JUMP_BACK            30  'to 30'
               70  POP_BLOCK        
               72  JUMP_FORWARD        108  'to 108'
             74_0  COME_FROM            20  '20'

 L.  71        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'neuro_element'
               78  LOAD_ATTR                base_element
               80  LOAD_GLOBAL              BrainAtlas
               82  CALL_FUNCTION_2       2  '2 positional arguments'
               84  POP_JUMP_IF_FALSE   108  'to 108'

 L.  72        86  LOAD_STR                 'list'
               88  LOAD_FAST                'neuro_element'
               90  LOAD_ATTR                base_element
               92  STORE_ATTR               collection_mode

 L.  73        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _find_rois
               98  LOAD_FAST                'neuro_element'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'roi_list'
              106  STORE_FAST               'atlas_obj'
            108_0  COME_FROM            84  '84'
            108_1  COME_FROM            72  '72'
            108_2  COME_FROM_LOOP       22  '22'

 L.  74       108  LOAD_FAST                'roi_list'
              110  LOAD_FAST                'atlas_obj'
              112  BUILD_TUPLE_2         2 
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 108_2

    @staticmethod
    def _find_rois(element):
        roi_list = element.base_element.rois
        atlas_obj = AtlasLibrary().get_atlas(element.base_element.atlas_name)
        roi_objects = BrainAtlas._get_rois(atlas_obj, roi_list)
        return ([roi.label for roi in roi_objects], atlas_obj)

    def fit(self, X, y=None, **kwargs):
        if len(self.hyperpipes_to_fit) == 0:
            raise Exception("No hyperpipes to fit. Did you call 'generate_mappings'?")
        self.neuro_element.fit(X)
        X_extracted, _, _ = self.neuro_element.transform(X)
        X_extracted = self._reshape_roi_data(X_extracted)
        joblib.dump((self.neuro_element), (os.path.join(self.folder, 'neuro_element.pkl')), compress=1)
        hyperpipe_infos = dict()
        hyperpipe_results = dict()
        for roi_name, hyperpipe in self.hyperpipes_to_fit.items():
            hyperpipe.verbosity = self.verbosity
            (hyperpipe.fit)((X_extracted[self.roi_indices[roi_name]]), y, **kwargs)
            hyperpipe_infos[roi_name] = {'hyperpipe_name':hyperpipe.name,  'model_filename':os.path.join(hyperpipe.output_settings.results_folder, 'photon_best_model.photon'), 
             'roi_index':self.roi_indices[roi_name]}
            hyperpipe_results[roi_name] = ResultsHandler(hyperpipe.results).get_performance_outer_folds()

        self.hyperpipe_infos = hyperpipe_infos
        with open(os.path.join(self.folder, self.original_hyperpipe_name + '_atlas_mapper_meta.json'), 'w') as (fp):
            json.dump(self.hyperpipe_infos, fp)
        df = pd.DataFrame(hyperpipe_results)
        df.to_csv(os.path.join(self.folder, self.original_hyperpipe_name + '_atlas_mapper_results.csv'))
        performances = list()
        for roi_name, roi_res in hyperpipe_results.items():
            n_voxels = len(X_extracted[self.roi_indices[roi_name]][0])
            performances.append(np.repeat(roi_res[self.best_config_metric], n_voxels))

        backmapped_img, _, _ = self.neuro_element.inverse_transform(performances)
        backmapped_img.to_filename(os.path.join(self.folder, 'atlas_mapper_performances.nii.gz'))
        if self.create_surface_plots:
            self.surface_plots(backmapped_img)

    def surface_plots(self, perf_img):
        print('Creating surface plots')
        figure, axes = plt.subplots(2, 2, subplot_kw={'projection': '3d'}, figsize=(12,
                                                                                    12))
        axes = axes.ravel()
        big_fsaverage = datasets.fetch_surf_fsaverage('fsaverage')
        cnt = 0
        for hemi, infl, sulc, pial in [('left', big_fsaverage.infl_left, big_fsaverage.sulc_left, big_fsaverage.pial_left),
         (
          'right', big_fsaverage.infl_right, big_fsaverage.sulc_right, big_fsaverage.pial_right)]:
            print('Hemi {}'.format(hemi))
            big_texture = surface.vol_to_surf(perf_img, pial, interpolation='nearest')
            for view in ('lateral', 'medial'):
                print('   View {}'.format(view))
                if cnt == 3:
                    output_file = os.path.join(self.folder, 'importance_scores_surface.png')
                else:
                    output_file = None
                plotting.plot_surf_stat_map(infl, big_texture, hemi=hemi, colorbar=True, title=('{} hemisphere {} view'.format(hemi, view)),
                  threshold=0.0001,
                  bg_map=sulc,
                  view=view,
                  output_file=output_file,
                  axes=(axes[cnt]))
                cnt += 1

    def _reshape_roi_data(self, X):
        roi_data = [list() for n in range(len(X[0]))]
        for roi_i in range(len(X[0])):
            for sub_i in range(len(X)):
                roi_data[roi_i].append(X[sub_i][roi_i])

        return roi_data

    def predict(self, X, **kwargs):
        if len(self.hyperpipes_to_fit) == 0:
            raise Exception('No hyperpipes to predict. Did you remember to fit or load the Atlas Mapper?')
        X_extracted, _, _ = self.neuro_element.transform(X)
        X_extracted = self._reshape_roi_data(X_extracted)
        predictions = dict()
        for roi, infos in self.hyperpipe_infos.items():
            roi_index = infos['roi_index']
            predictions[roi] = (self.hyperpipes_to_fit[roi].predict)((X_extracted[roi_index]), **kwargs)

        return predictions

    def load_from_file(self, file: str):
        if not os.path.exists(file):
            raise FileNotFoundError("Couldn't find atlas mapper meta file")
        self._load(file)

    def load_from_folder(self, folder: str, analysis_name: str=None):
        if not os.path.exists(folder):
            raise NotADirectoryError('{} is not a directory'.format(folder))
        else:
            if analysis_name:
                meta_file = glob(os.path.join(folder, analysis_name + '_atlas_mapper_meta.json'))
            else:
                meta_file = glob(os.path.join(folder, '*_atlas_mapper_meta.json'))
            if len(meta_file) == 0:
                raise FileNotFoundError("Couldn't find atlas_mapper_meta.json file in {}. Did you specify the correct analysis name?".format(folder))
            else:
                if len(meta_file) > 1:
                    raise ValueError('Found multiple atlas_mapper_meta.json files in {}'.format(folder))
        self._load(meta_file[0])

    def _load(self, file):
        self.folder = os.path.split(file)[0]
        self.neuro_element = joblib.load(os.path.join(self.folder, 'neuro_element.pkl'))
        with open(file, 'r') as (read_file):
            self.hyperpipe_infos = json.load(read_file)
        roi_models = dict()
        for roi_name, infos in self.hyperpipe_infos.items():
            roi_models[roi_name] = Hyperpipe.load_optimum_pipe(infos['model_filename'])
            self.hyperpipes_to_fit = roi_models