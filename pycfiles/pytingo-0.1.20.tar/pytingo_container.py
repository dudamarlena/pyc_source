# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/castarco/Proyectos/Pytingo/pytingo/pytingo_container.py
# Compiled at: 2014-06-15 15:34:28
from __future__ import absolute_import, division, print_function, unicode_literals
from .pytingo_data import PytingoData as _PytingoData
from .pytingo_loader import PytingoLoader as _PytingoLoader
from .pytingo_loading_exception import PytingoLoadingException as _PytingoLoadingException

class PytingoContainer:
    """In-memory settings container."""

    def __init__(self, loader, process_meta=True):
        """Initializes the container.

        Args:
            :param loader: PytingoLoader instance, or a list of PytingoLoader instances.

        Raises:
            ValueError: Type check error.
        """
        if isinstance(loader, _PytingoLoader):
            self._loader = [
             loader]
        elif isinstance(loader, list):
            for l in loader:
                if not isinstance(l, _PytingoLoader):
                    raise ValueError(b'loader must be a PytingoLoader object or a list of PytingoLoader objects.')

            self._loader = loader
        else:
            raise ValueError(b'loader must be a PytingoLoader object or a list of PytingoLoader objects.')
        self._process_meta = process_meta
        self._loaded_settings = {}

    def get(self, section):
        if section in self._loaded_settings:
            return self._loaded_settings[section]
        else:
            section_settings_dict, excs = None, []
            for loader in self._loader:
                try:
                    section_settings_dict = loader.get(section)
                    break
                except IOError as e:
                    excs.append(e)

            if section_settings_dict is None:
                raise _PytingoLoadingException(b"It was impossible to load the section '" + section + b"'", excs)
            self._loaded_settings[section] = _PytingoData(data_dict=section_settings_dict, process_meta=self._process_meta)
            return self._loaded_settings[section]

    def __getattr__(self, item):
        """
        Convenient accessor to 'get'.
        """
        return self.get(item)