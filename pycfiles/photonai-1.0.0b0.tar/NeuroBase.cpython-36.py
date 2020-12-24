# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/neuro/NeuroBase.py
# Compiled at: 2019-09-03 12:40:08
# Size of source mod 2**32: 8491 bytes
from ..base.PhotonBase import Branch, CallbackElement
from ..configuration.Register import PhotonRegister
from ..base.Helper import PHOTONDataHelper
from ..neuro.BrainAtlas import BrainAtlas
from ..photonlogger.Logger import Logger
from nibabel.nifti1 import Nifti1Image
from multiprocessing import Process, Queue
from fasteners import ReaderWriterLock
import queue, os, uuid

class NeuroModuleBranch(Branch):
    __doc__ = '\n    A substream of neuro elements that are encapsulated into a single block of PipelineElements that all perform\n    transformations on MRI data. A NeuroModuleBranch takes niftis or nifti paths as input and should pass a numpy array\n    to the subsequent PipelineElements.\n\n    Parameters\n    ----------\n    * `name` [str]:\n        Name of the NeuroModule pipeline branch\n\n    '
    NEURO_ELEMENTS = PhotonRegister().get_package_info(['PhotonNeuro'])

    def __init__(self, name, nr_of_processes=1, output_img: bool=False, apply_groupwise: bool=False):
        Branch.__init__(self, name)
        self.nr_of_processes = nr_of_processes
        self.output_img = output_img
        self.has_hyperparameters = True
        self.needs_y = False
        self.needs_covariates = True
        self.current_config = None
        if self.nr_of_processes > 1:
            Logger().warn('Groupwise processing of NeuroElements not supported when working on multiple CPUs. Falling back to single subject processing.')

    def fit(self, X, y=None, **kwargs):
        return self

    def __iadd__(self, pipe_element):
        """
        Add an element to the neuro branch. Only neuro pipeline elements are allowed.
        Returns self

        Parameters
        ----------
        * `pipe_element` [PipelineElement]:
            The transformer object to add. Should be registered in the Neuro module.
        """
        if pipe_element.name in NeuroModuleBranch.NEURO_ELEMENTS:
            pipe_element.base_element.output_img = True
            self.elements.append(pipe_element)
            self._prepare_pipeline()
        else:
            if isinstance(pipe_element, CallbackElement):
                self.elements.append(pipe_element)
                self._prepare_pipeline()
            else:
                Logger().error('PipelineElement {} is not part of the Neuro module:'.format(pipe_element.name))
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
                raise isinstance(new_pic, Nifti1Image) or ValueError('last element of branch does not return a nifti image')
            new_filename = os.path.join(save_to_folder, filename + str(nr_of_tested) + '_transformed.nii')
            new_pic.to_filename(new_filename)
            nr_of_tested += 1

    def transform(self, X, y=None, **kwargs):
        if self.base_element.cache_folder is not None:
            self.base_element.single_subject_caching = True
            self.base_element.caching = True
        if self.nr_of_processes > 1:
            if self.base_element.cache_folder is not None:
                self.apply_transform_parallelized(X)
            else:
                Logger().error('Cannot use parallelization without a cache folder specified in the hyperpipe.Using single core instead')
        X_new, _, _ = self.base_element.transform(X)
        return (
         X_new, y, kwargs)

    def set_params(self, **kwargs):
        self.current_config = kwargs
        (super(NeuroModuleBranch, self).set_params)(**kwargs)

    def copy_me(self):
        new_copy = super().copy_me()
        new_copy.base_element.current_config = self.base_element.current_config
        new_copy.base_element.single_subject_caching = True
        new_copy.base_element.cache_folder = self.base_element.cache_folder
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

    class ImageJob:

        def __init__(self, data, delegate, lock_setter=None, job_key=0, sort_index=0):
            self.data = data
            self.delegate = delegate
            self.sort_index = sort_index
            self.job_index = job_key
            self.lock_setter = lock_setter

    @staticmethod
    def parallel_application(folds_to_do, lock):
        while True:
            try:
                task = folds_to_do.get_nowait()
            except queue.Empty:
                break
            else:
                task.lock_setter(lock)
                task.delegate(task.data)

        return True

    def apply_transform_parallelized(self, X):
        """

        :param X: the data to which the delegate should be applied paralelly
        """
        if self.nr_of_processes > 1:
            jobs_to_do = Queue()
            lock = ReaderWriterLock()
            num_of_jobs_todo = 0
            for start, stop in PHOTONDataHelper.chunker(PHOTONDataHelper.find_n(X), self.nr_of_processes):
                X_batched, _, _ = PHOTONDataHelper.split_data(X, None, {}, start, stop)
                unique_key = uuid.uuid4()
                new_pipe_mr = self.copy_me()
                new_pipe_copy = new_pipe_mr.base_element
                new_pipe_copy.cache_folder = self.base_element.cache_folder
                new_pipe_copy.skip_loading = True
                job_delegate = new_pipe_copy.transform
                new_job = NeuroModuleBranch.ImageJob(data=X_batched, delegate=job_delegate, job_key=unique_key,
                  lock_setter=(new_pipe_copy.set_lock),
                  sort_index=start)
                jobs_to_do.put(new_job)
                num_of_jobs_todo += 1

            process_list = list()
            for w in range(self.nr_of_processes):
                p = Process(target=(NeuroModuleBranch.parallel_application), args=(jobs_to_do, lock))
                process_list.append(p)
                p.start()

            for p in process_list:
                p.join()


class NeuroTransformerMixin:

    def __init__(self):
        self.output_img = False