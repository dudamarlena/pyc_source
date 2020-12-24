# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/neuro/neuro_branch.py
# Compiled at: 2019-10-31 13:38:46
# Size of source mod 2**32: 8065 bytes
import os, dask, numpy as np
from dask.distributed import Client
from nibabel.nifti1 import Nifti1Image
from photonai.base import Branch, CallbackElement
from photonai.base.registry.element_dictionary import ElementDictionary
from photonai.helper.helper import PhotonDataHelper
from photonai.neuro.brain_atlas import BrainAtlas
import photonai.photonlogger.logger as logger

class NeuroBranch(Branch):
    __doc__ = '\n    A substream of neuro elements that are encapsulated into a single block of PipelineElements that all perform\n    transformations on MRI data. A NeuroBranch takes niftis or nifti paths as input and should pass a numpy array\n    to the subsequent PipelineElements.\n\n    Parameters\n    ----------\n    * `name` [str]:\n        Name of the NeuroModule pipeline branch\n\n    '
    NEURO_ELEMENTS = ElementDictionary.get_package_info(['PhotonNeuro'])

    def __init__(self, name, nr_of_processes=1, output_img: bool=False):
        Branch.__init__(self, name)
        self._nr_of_processes = 1
        self.local_cluster = None
        self.client = None
        self.nr_of_processes = nr_of_processes
        self.output_img = output_img
        self.has_hyperparameters = True
        self.needs_y = False
        self.needs_covariates = True
        self.current_config = None

    def __del__(self):
        if self.local_cluster is not None:
            self.local_cluster.close()

    def fit(self, X, y=None, **kwargs):
        return self

    @property
    def nr_of_processes(self):
        return self._nr_of_processes

    @nr_of_processes.setter
    def nr_of_processes(self, value):
        self._nr_of_processes = value
        if self._nr_of_processes > 1:
            if self.local_cluster is None:
                self.local_cluster = Client(threads_per_worker=1, n_workers=(self.nr_of_processes),
                  processes=False)
            else:
                self.local_cluster.n_workers = self.nr_of_processes
        else:
            self.local_cluster = None

    def __iadd__(self, pipe_element):
        """
        Add an element to the neuro branch. Only neuro pipeline elements are allowed.
        Returns self

        Parameters
        ----------
        * `pipe_element` [PipelineElement]:
            The transformer object to add. Should be registered in the Neuro module.
        """
        if pipe_element.name in NeuroBranch.NEURO_ELEMENTS:
            pipe_element.base_element.output_img = True
            self.elements.append(pipe_element)
            self._prepare_pipeline()
        else:
            if isinstance(pipe_element, CallbackElement):
                self.elements.append(pipe_element)
                self._prepare_pipeline()
            else:
                logger.error('PipelineElement {} is not part of the Neuro module:'.format(pipe_element.name))
        return self

    def test_transform(self, X, nr_of_tests=1, save_to_folder='.', **kwargs):
        nr_of_tested = 0
        if kwargs:
            if len(kwargs) > 0:
                (self.set_params)(**kwargs)
        copy_of_me = self.copy_me()
        copy_of_me.nr_of_processes = 1
        copy_of_me.output_img = True
        for p_element in copy_of_me.pipeline_elements:
            if isinstance(p_element.base_element, BrainAtlas):
                p_element.base_element.extract_mode = 'img'

        filename = self.name + '_testcase_'
        for x_el in X:
            if nr_of_tested > nr_of_tests:
                break
            else:
                new_pic, _, _ = copy_of_me.transform(x_el)
                if isinstance(new_pic, list):
                    new_pic = new_pic[0]
                assert isinstance(new_pic, Nifti1Image), 'last element of branch does not return a nifti image'
            new_filename = os.path.join(save_to_folder, filename + str(nr_of_tested) + '_transformed.nii')
            new_pic.to_filename(new_filename)
            nr_of_tested += 1

    def transform(self, X, y=None, **kwargs):
        if self.base_element.cache_folder is not None:
            self.base_element.single_subject_caching = True
            self.base_element.caching = True
        else:
            if self.nr_of_processes > 1:
                if self.base_element.cache_folder is not None:
                    self.apply_transform_parallelized(X)
                else:
                    logger.error('Cannot use parallelization without a cache folder specified in the hyperpipe.Using single core instead')
            logger.debug('NeuroBranch' + self.name + ' is collecting data from the different cores...')
            X_new, _, _ = self.base_element.transform(X)
            if self.output_img or isinstance(X_new, list) and len(X_new) > 0 or isinstance(X_new, np.ndarray):
                if len(X_new.shape) == 1:
                    if isinstance(X_new[0], Nifti1Image):
                        X_new = np.asarray([i.dataobj for i in X_new])
        return (
         X_new, y, kwargs)

    def set_params(self, **kwargs):
        self.current_config = kwargs
        (super(NeuroBranch, self).set_params)(**kwargs)

    def copy_me(self):
        new_copy = super().copy_me()
        new_copy.base_element.current_config = self.base_element.current_config
        new_copy.base_element.single_subject_caching = True
        new_copy.base_element.cache_folder = self.base_element.cache_folder
        new_copy.local_cluster = self.local_cluster
        new_copy.nr_of_processes = self.nr_of_processes
        new_copy.do_not_delete_cache_folder = True
        return new_copy

    def inverse_transform(self, X, y=None, **kwargs):
        for transform in self.elements[::-1]:
            if hasattr(transform, 'inverse_transform'):
                X, y, kwargs = (transform.inverse_transform)(X, y, **kwargs)
            else:
                return (
                 X, y, kwargs)

        return (
         X, y, kwargs)

    @staticmethod
    def parallel_application(pipe_copy, data):
        pipe_copy.transform(data)

    def apply_transform_parallelized(self, X):
        """

        :param X: the data to which the delegate should be applied in parallel
        """
        if self.nr_of_processes > 1:
            jobs_to_do = list()
            number_of_items_to_process = PhotonDataHelper.find_n(X)
            number_of_items_for_each_core = int(np.ceil(number_of_items_to_process / self.nr_of_processes))
            logger.info('NeuroBranch ' + self.name + ': Using ' + str(self.nr_of_processes) + ' cores calculating ' + str(number_of_items_for_each_core) + ' items each')
            for start, stop in PhotonDataHelper.chunker(number_of_items_to_process, number_of_items_for_each_core):
                X_batched, _, _ = PhotonDataHelper.split_data(X, None, {}, start, stop)
                new_pipe_mr = self.copy_me()
                new_pipe_copy = new_pipe_mr.base_element
                new_pipe_copy.cache_folder = self.base_element.cache_folder
                new_pipe_copy.skip_loading = True
                new_pipe_copy._parallel_use = True
                del_job = dask.delayed(NeuroBranch.parallel_application)(new_pipe_copy, X_batched)
                jobs_to_do.append(del_job)

            (dask.compute)(*jobs_to_do)