# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\Ity\Utilities\CorpusText.py
# Compiled at: 2013-12-05 14:11:49
__author__ = 'kohlmannj'
import codecs, os, Ity
from Ity.Utilities.FilePaths import get_valid_path

class CorpusText(object):

    def __init__(self, path, name=None, corpus=None, output_path=None):
        if type(path) is not str:
            raise ValueError('Invalid path argument provided.')
        if not os.path.isabs(path):
            if corpus is None and hasattr(corpus, 'texts_path') and type(corpus.texts_path) is str:
                path = os.path.join(corpus.texts_path, path)
            else:
                raise ValueError('Given a relative path to a text without a corpus argument.')
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            raise ValueError("Text file at path '%s' does not exist." % self.path)
        if name is None or type(name) is not str:
            name = os.path.splitext(os.path.basename(self.path))[0]
        self.name = name
        self.corpus = corpus
        self.output_path = get_valid_path(path=output_path, fallback_path=os.path.join(Ity.output_root, self.name))
        self.metadata = None
        self._text_str = None
        self.tokens = []
        self.tag_data = {}
        self.format_data = {}
        return

    @property
    def text_str(self):
        if self._text_str is None:
            with codecs.open(self.path, 'r', encoding='utf-8') as (text_file):
                self._text_str = text_file.read()
        return self._text_str