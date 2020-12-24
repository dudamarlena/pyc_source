# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/base/cache_manager.py
# Compiled at: 2019-09-11 12:57:17
# Size of source mod 2**32: 8464 bytes
import os, shutil, pickle, uuid, numpy as np, fcntl
from contextlib import contextmanager
from photonai.photonlogger import Logger

class CacheManager:
    M_READ, M_WRITE, M_READWRITE = range(3)
    MODES = (
     (
      os.O_RDONLY, fcntl.LOCK_SH, 'rb'),
     (
      os.O_WRONLY | os.O_CREAT | os.O_TRUNC, fcntl.LOCK_EX, 'wb'),
     (
      os.O_RDWR | os.O_CREAT, fcntl.LOCK_EX, 'r+b'))
    BLOCKING_FLAGS = (
     fcntl.LOCK_NB, 0)

    def __init__(self, _hash=None, cache_folder=None):
        self._hash = _hash
        self.cache_folder = cache_folder
        self.pipe_order = None
        self.cache_index = None
        self.state = None
        self.cache_file_name = None
        self.lock = None

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        if not isinstance(value, str):
            self._hash = str(value)
        else:
            self._hash = value

    def set_lock(self, lock):
        self.lock = lock

    class State:

        def __init__(self, config=None, nr_items=None, first_data_hash=None, first_data_str: str=''):
            self.config = config
            self.nr_items = nr_items
            self.first_data_hash = first_data_hash
            self.first_data_str = first_data_str

    def update_single_subject_state_info(self, X):
        self.state.first_data_hash = hash(str(X[0]))
        if isinstance(X[0], str):
            self.state.first_data_str = X[0]
        else:
            self.state.first_data_str = str(self.state.first_data_hash)

    def prepare(self, pipe_elements, config, X=None, single_subject_caching=False):
        cache_name = 'photon_cache_index.p'
        self.cache_file_name = os.path.join(self.cache_folder, cache_name)
        self._read_cache_index()
        self.pipe_order = pipe_elements
        self.state = CacheManager.State(config=config)
        if X is not None:
            self.state.first_data_hash = hash(str(X[0]))
            if isinstance(X, np.ndarray):
                self.state.nr_items = X.shape[0]
            else:
                self.state.nr_items = len(X)
            self.state.first_data_str = str(self.state.first_data_hash)
        if single_subject_caching:
            self.state.nr_items = 1

    def _read_cache_index(self):
        if os.path.isfile(self.cache_file_name):
            try:
                with CacheManager.locked_open(self.cache_file_name, CacheManager.M_READ) as (f):
                    self.cache_index = pickle.load(f)
            except EOFError as e:
                print(e)
                print('EOF Error... retrying!')
                print('Cache index loaded: ' + str(self.cache_index))
                self._read_cache_index()

        else:
            self.cache_index = {}

    def _find_config_for_element(self, pipe_element_name):
        relevant_keys = list()
        for item in self.pipe_order:
            if item != pipe_element_name:
                relevant_keys.append(item)
            elif item == pipe_element_name:
                relevant_keys.append(item)
                break

        relevant_dict = dict()
        if self.state.config is not None:
            if len(self.state.config) > 0:
                for key_name, key_value in self.state.config.items():
                    key_name_list = key_name.split('__')
                    if len(key_name_list) > 0:
                        item_name = key_name_list[0]
                    else:
                        item_name = key_name
                    if item_name in relevant_keys:
                        if isinstance(key_value, list):
                            key_value = frozenset(key_value)
                        relevant_dict[key_name] = key_value

        return hash(frozenset(relevant_dict.items()))

    def load_cached_data(self, pipe_element_name):
        config_hash = self._find_config_for_element(pipe_element_name)
        cache_query = (pipe_element_name, self.hash, config_hash, self.state.nr_items, self.state.first_data_hash)
        if cache_query in self.cache_index:
            Logger().debug('Loading data from cache for ' + pipe_element_name + ': ' + str(self.state.nr_items) + ' items ' + self.state.first_data_str + ' - ' + str(self.state.config))
            with open(self.cache_index[cache_query], 'rb') as (f):
                X, y, kwargs = pickle.load(f)
            return (X, y, kwargs)

    def check_cache(self, pipe_element_name):
        config_hash = self._find_config_for_element(pipe_element_name)
        cache_query = (pipe_element_name, self.hash, config_hash, self.state.nr_items, self.state.first_data_hash)
        if cache_query in self.cache_index:
            return True
        else:
            return False

    def save_data_to_cache(self, pipe_element_name, data):
        config_hash = self._find_config_for_element(pipe_element_name)
        filename = os.path.join(self.cache_folder, str(uuid.uuid4()) + '.p')
        self.cache_index[(pipe_element_name, self.hash, config_hash, self.state.nr_items, self.state.first_data_hash)] = filename
        Logger().debug('Saving data to cache for ' + pipe_element_name + ': ' + str(self.state.nr_items) + ' items ' + self.state.first_data_str + ' - ' + str(self.state.config))
        with open(filename, 'wb') as (f):
            pickle.dump(data, f)

    def save_cache_index(self):
        self._write_cache_index()

    def _write_cache_index(self):
        with CacheManager.locked_open(self.cache_file_name, CacheManager.M_WRITE) as (f):
            pickle.dump(self.cache_index, f)

    def _read_cache_index(self):
        if os.path.isfile(self.cache_file_name):
            with CacheManager.locked_open(self.cache_file_name, CacheManager.M_READ) as (f):
                try:
                    self.cache_index = pickle.load(f)
                except EOFError as e:
                    print('EOF Error... retrying!')
                    print('Cache index loaded: ' + str(self.cache_index))
                    f.close()

        else:
            self.cache_index = {}

    @contextmanager
    def locked_open(filename, mode=M_READ, blocking=True):
        open_mode, flock_flags, mode_str = CacheManager.MODES[mode]
        flock_flags = flock_flags | CacheManager.BLOCKING_FLAGS[blocking]
        fd = os.open(filename, open_mode)
        try:
            fcntl.flock(fd, flock_flags)
            fileobj = os.fdopen(fd, mode_str)
            try:
                yield fileobj
            finally:
                fileobj.flush()
                os.fdatasync(fd)

        finally:
            os.close(fd)

    def clear_cache(self):
        CacheManager.clear_cache_files(self.cache_folder)

    @staticmethod
    def clear_cache_files(cache_folder, force_all=False):
        if cache_folder is not None:
            if os.path.isdir(cache_folder):
                for the_file in os.listdir(cache_folder):
                    file_path = os.path.join(cache_folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        else:
                            if os.path.isdir(file_path):
                                if not file_path.endswith('DND') or force_all:
                                    shutil.rmtree(file_path)
                    except Exception as e:
                        print(e)