# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/athena.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 1335 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.athena
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class NamedQuery(troposphere.athena.NamedQuery, Mixin):

    def __init__(self, title, template=None, validation=True, Database=REQUIRED, QueryString=REQUIRED, Description=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Database=Database, 
         QueryString=QueryString, 
         Description=Description, 
         Name=Name, **kwargs)
        (super(NamedQuery, self).__init__)(**processed_kwargs)