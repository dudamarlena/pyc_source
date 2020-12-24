# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nmadnani/work/python-zpar/zpar/Tagger.py
# Compiled at: 2014-11-10 18:52:06
"""
:author: Nitin Madnani (nmadnani@ets.org)
:organization: ETS
"""
import ctypes as c, os

class Tagger(object):
    """The ZPar English POS Tagger"""

    def __init__(self, modelpath, libptr, zpar_session_obj):
        super(Tagger, self).__init__()
        self._zpar_session_obj = zpar_session_obj
        self._load_tagger = libptr.load_tagger
        self._load_tagger.restype = c.c_int
        self._load_tagger.argtypes = [c.c_void_p, c.c_char_p]
        self._tag_sentence = libptr.tag_sentence
        self._tag_sentence.restype = c.c_char_p
        self._tag_sentence.argtypes = [c.c_void_p, c.c_char_p, c.c_bool]
        self._tag_file = libptr.tag_file
        self._tag_file.restype = None
        self._tag_file.argtypes = [c.c_void_p, c.c_char_p, c.c_char_p, c.c_bool]
        if self._load_tagger(self._zpar_session_obj, modelpath.encode('utf-8')):
            raise OSError(('Cannot find tagger model at {}\n').format(modelpath))
        return

    def tag_sentence(self, sentence, tokenize=True):
        if not sentence.strip():
            ans = ''
        else:
            zpar_compatible_sentence = sentence.strip() + '\n '
            zpar_compatible_sentence = zpar_compatible_sentence.encode('utf-8')
            tagged_sent = self._tag_sentence(self._zpar_session_obj, zpar_compatible_sentence, tokenize)
            ans = tagged_sent.decode('utf-8')
        return ans

    def tag_file(self, inputfile, outputfile, tokenize=True):
        if os.path.exists(inputfile):
            self._tag_file(self._zpar_session_obj, inputfile.encode('utf-8'), outputfile.encode('utf-8'), tokenize)
        else:
            raise OSError(('File {} does not exist.').format(inputfile))

    def cleanup(self):
        self._load_tagger = None
        self._tag_sentence = None
        self._tag_file = None
        self._zpar_session_obj = None
        return