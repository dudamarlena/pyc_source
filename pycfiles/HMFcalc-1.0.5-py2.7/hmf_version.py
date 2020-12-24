# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/HMFcalc/templatetags/hmf_version.py
# Compiled at: 2013-05-14 01:22:59
"""
Created on Apr 10, 2013

@author: Steven
"""
from django import template
register = template.Library()

def current_version():
    from hmf.Perturbations import version
    return version


register.simple_tag(current_version)