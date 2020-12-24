# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/url.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 1189 bytes
import re
from unidecode import unidecode
import six
_punct_re = re.compile('[\\t !"#:$%&\\\'()*\\-/<=>?@\\[\\\\\\]^_`{|},.]+')

def slugify(text, delim='-'):
    """
    Generates an ASCII-only slug. Taken from http://flask.pocoo.org/snippets/5/
    """
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())

    return six.text_type(delim.join(result))