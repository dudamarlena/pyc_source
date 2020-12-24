# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/accessanalyzer.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 2686 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.accessanalyzer
from troposphere.accessanalyzer import ArchiveRule as _ArchiveRule, Filter as _Filter, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Filter(troposphere.accessanalyzer.Filter, Mixin):

    def __init__(self, title=None, Property=REQUIRED, Contains=NOTHING, Eq=NOTHING, Exists=NOTHING, Neq=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Property=Property, 
         Contains=Contains, 
         Eq=Eq, 
         Exists=Exists, 
         Neq=Neq, **kwargs)
        (super(Filter, self).__init__)(**processed_kwargs)


class ArchiveRule(troposphere.accessanalyzer.ArchiveRule, Mixin):

    def __init__(self, title=None, Filter=REQUIRED, RuleName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Filter=Filter, 
         RuleName=RuleName, **kwargs)
        (super(ArchiveRule, self).__init__)(**processed_kwargs)


class Analyzer(troposphere.accessanalyzer.Analyzer, Mixin):

    def __init__(self, title, template=None, validation=True, Type=REQUIRED, AnalyzerName=NOTHING, ArchiveRules=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Type=Type, 
         AnalyzerName=AnalyzerName, 
         ArchiveRules=ArchiveRules, 
         Tags=Tags, **kwargs)
        (super(Analyzer, self).__init__)(**processed_kwargs)