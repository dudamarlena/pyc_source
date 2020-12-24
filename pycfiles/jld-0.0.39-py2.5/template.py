# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\tools\template.py
# Compiled at: 2008-12-04 08:40:48
""" Specialized String Template
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: template.py 708 2008-12-04 13:40:35Z JeanLou.Dupont $'
from string import Template

class ExTemplate(Template):
    """String Template to ease integration with other string processing modules e.g. OptionParser
    """
    delimiter = '^^'

    def __init__(self, init):
        Template.__init__(self, init)