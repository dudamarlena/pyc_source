# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/castarco/Proyectos/Pytingo/pytingo/pytingo_json_file_loader.py
# Compiled at: 2014-06-15 14:10:35
from __future__ import absolute_import, division, print_function, unicode_literals
import os, six, json, time, errno
from .pytingo_loader import PytingoLoader as _PytingoLoader

class PytingoJSONFileLoader(_PytingoLoader):
    """Settings JSON files loader."""

    def __init__(self, path, env_var=b'', env_var_default=b'', n_retries=3, millis_before_retry=200):
        """
        Args:
            :param path: The path where we can found the settings JSON files.
            :type path: str

            :param env_var: Name of the ENVIRONMENT VARIABLE used to modify the settings files names.
            :type env_var: str

            :param env_var_default: Default value used if the environment variable specified by `env_var` is not defined.
            :type env_var_default: str

            :param n_retries: The maximum number of retries the loader will do in order to load the settings file.
            :type n_retries: int
        
            :param millis_before_retry: The number of milliseconds the loader will wait before retrying to load the settings file.
            :type millis_before_retry: int

        Raises:
            ValueError: Type checking error.
        """
        if not isinstance(path, six.string_types):
            raise ValueError(b'path must be a string')
        if not isinstance(env_var, six.string_types):
            raise ValueError(b'env_var must be a string')
        if not isinstance(env_var_default, six.string_types):
            raise ValueError(b'env_var_default must be a string')
        if not isinstance(n_retries, int):
            raise ValueError(b'n_retries must be an integer')
        if not isinstance(millis_before_retry, int):
            raise ValueError(b'millis_before_retry must be an integer')
        if path[(-1)] != os.sep:
            path += os.sep
        self._path = path
        self._env_var = env_var
        self._env_var_default = env_var_default
        self._n_retries = n_retries
        self._millis_before_retry = [ millis_before_retry * i for i in range(1, n_retries + 1) ]

    def get(self, section):
        """Returns a dictionary with the section settings.

        Args:
            :param section: The name of the 'settings section' we want to load.
            :type section: str

        Returns:
            A dict with the settings data.

        Raises:
            IOError: The section settings file couldn't be loaded.
        """
        if self._env_var == b'':
            section_path = os.path.join(self._path, section, section + b'.json')
        else:
            section_path = os.path.join(self._path, section, section + b'_' + os.environ.get(self._env_var, self._env_var_default) + b'.json')
        for n_try in range(self._n_retries):
            try:
                with open(section_path, b'r') as (f):
                    result = json.load(f)
                return result
            except IOError as ioe:
                if ioe.errno not in [errno.EAGAIN, errno.EMFILE, errno.EIO, errno.EINTR]:
                    raise ioe
                else:
                    time.sleep(0.001 * self._millis_before_retry[n_try])