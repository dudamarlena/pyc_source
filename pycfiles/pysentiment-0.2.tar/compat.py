# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/compat.py
# Compiled at: 2019-09-21 23:36:31
import os, sys
try:
    import pkg_resources
    get_module_res = lambda *res: pkg_resources.resource_stream(__name__, os.path.join(*res))
except ImportError:
    get_module_res = lambda *res: open(os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__), *res)), 'rb')

PY2 = sys.version_info[0] == 2
default_encoding = sys.getfilesystemencoding()
if PY2:
    text_type = unicode
    string_types = (str, unicode)
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
else:
    text_type = str
    string_types = (str,)
    xrange = range
    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

def strdecode(sentence):
    if not isinstance(sentence, text_type):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk', 'ignore')

    return sentence


def resolve_filename(f):
    try:
        return f.name
    except AttributeError:
        return repr(f)