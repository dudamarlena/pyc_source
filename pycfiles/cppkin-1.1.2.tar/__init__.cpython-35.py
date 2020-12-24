# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bung/.virtualenvs/whatlangid/lib/python3.5/site-packages/cppjieba_py/__init__.py
# Compiled at: 2018-08-18 07:16:17
# Size of source mod 2**32: 1166 bytes
import libcppjieba
from libcppjieba import Tokenizer, add_word, tokenize, load_userdict, find, lookup_tag
from libcppjieba import lcut, lcut_for_search, initialize
from libcppjieba import cut_all as _cut_all, lcut_all

def _iter_wraps_doc(origin):
    return origin.__doc__.replace(origin.__name__, 'Iterator wraps %s' % origin.__name__, 1)


def cut(*args, **kvargs):
    it = libcppjieba.cut(*args, **kvargs)
    return iter(it)


def cut_all(*args, **kvargs):
    it = _cut_all(*args, **kvargs)
    return iter(it)


cut.__doc__ = _iter_wraps_doc(libcppjieba.cut)

def cut_for_search(*args, **kvargs):
    it = libcppjieba.cut_for_search(*args, **kvargs)
    return iter(it)


cut_for_search.__doc__ = _iter_wraps_doc(libcppjieba.cut_for_search)

def _cut(ins, *args, **kvargs):
    it = ins.cut_internal(*args, **kvargs)
    return iter(it)


def _cut_for_search(ins, *args, **kvargs):
    it = ins.cut_for_search_internal(*args, **kvargs)
    return iter(it)


_cut.__doc__ = _iter_wraps_doc(Tokenizer.cut_internal)
_cut_for_search.__doc__ = _iter_wraps_doc(Tokenizer.cut_for_search_internal)
setattr(Tokenizer, 'cut', _cut)
setattr(Tokenizer, 'cut_for_search', _cut_for_search)