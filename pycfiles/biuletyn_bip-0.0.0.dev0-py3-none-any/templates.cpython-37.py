# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/templates.py
# Compiled at: 2019-09-28 15:06:24
# Size of source mod 2**32: 515 bytes
from wtforms.fields import HiddenField
from .._version import get_version
from utils.pagination import url_for_other_page
from utils.text import yesno

def extra_context(**kwargs):
    extra = {'version':get_version(), 
     'is_hidden_field':lambda x: isinstance(x, HiddenField), 
     'url_for_other_page':url_for_other_page}
    extra.update(kwargs)
    return extra


def extra_filters(**kwargs):
    extra = {'yesno': yesno}
    extra.update(kwargs)
    return extra