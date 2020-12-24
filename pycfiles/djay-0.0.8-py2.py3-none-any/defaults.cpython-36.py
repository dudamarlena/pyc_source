# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/jinja2/jinja2/defaults.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 1400 bytes
"""
    jinja2.defaults
    ~~~~~~~~~~~~~~~

    Jinja default filters and tags.

    :copyright: (c) 2017 by the Jinja Team.
    :license: BSD, see LICENSE for more details.
"""
from jinja2._compat import range_type
from jinja2.utils import generate_lorem_ipsum, Cycler, Joiner, Namespace
BLOCK_START_STRING = '{%'
BLOCK_END_STRING = '%}'
VARIABLE_START_STRING = '{{'
VARIABLE_END_STRING = '}}'
COMMENT_START_STRING = '{#'
COMMENT_END_STRING = '#}'
LINE_STATEMENT_PREFIX = None
LINE_COMMENT_PREFIX = None
TRIM_BLOCKS = False
LSTRIP_BLOCKS = False
NEWLINE_SEQUENCE = '\n'
KEEP_TRAILING_NEWLINE = False
from jinja2.filters import FILTERS as DEFAULT_FILTERS
from jinja2.tests import TESTS as DEFAULT_TESTS
DEFAULT_NAMESPACE = {'range':range_type, 
 'dict':dict, 
 'lipsum':generate_lorem_ipsum, 
 'cycler':Cycler, 
 'joiner':Joiner, 
 'namespace':Namespace}
DEFAULT_POLICIES = {'compiler.ascii_str':True, 
 'urlize.rel':'noopener', 
 'urlize.target':None, 
 'truncate.leeway':5, 
 'json.dumps_function':None, 
 'json.dumps_kwargs':{'sort_keys': True}, 
 'ext.i18n.trimmed':False}
__all__ = tuple(x for x in locals().keys() if x.isupper())