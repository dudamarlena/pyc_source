# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\Ity\Utilities\Corpus.py
# Compiled at: 2013-12-05 14:11:49
__author__ = 'kohlmannj'
import os, Ity
from Ity.Utilities.FilePaths import get_files_in_path, get_valid_path

class Corpus(object):

    def __init__(self, path, name=None, extensions=('.txt', ), texts_path=None, metadata_path=None, output_path=None):
        if type(path) is not str:
            raise ValueError('Invalid path argument provided.')
        if not os.path.isabs(path):
            path = os.path.join(Ity.corpus_root, path)
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            raise IOError("Corpus at path '%s' does not exist." % self.path)
        self.texts_path = get_valid_path(path=texts_path, relative_path_base=self.path, fallback_path=self.path)
        if type(self.texts_path) is not str or not os.path.exists(self.texts_path):
            raise ValueError("Path to texts ('%s') doesn't exist." % self.texts_path)
        if name is None or type(name) is not str:
            name = os.path.basename(self.path)
        self.name = name
        self.metadata_path = get_valid_path(path=metadata_path, relative_path_base=self.path, fallback_path=os.path.join(Ity.metadata_root, self.name))
        self.output_path = get_valid_path(path=output_path, relative_path_base=self.path, fallback_path=os.path.join(Ity.output_root, self.name))
        if extensions is None or type(extensions) is str or len(extensions) == 0:
            raise ValueError('Invalid extensions argument provided.')
        self.extensions = extensions
        self._texts = None
        self.metadata = {}
        self.batch_format_data = {}
        return

    @property
    def texts(self):
        if self._texts is None:
            self._texts = get_files_in_path(self.texts_path, self.extensions)
        return self._texts