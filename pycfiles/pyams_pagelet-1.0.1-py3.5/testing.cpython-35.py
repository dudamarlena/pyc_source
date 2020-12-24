# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_pagelet/testing.py
# Compiled at: 2020-02-20 08:01:50
# Size of source mod 2**32: 898 bytes
"""PyAMS_pagelet.testing module

This module is used to add additional testing features.
"""
import sys
from pyams_pagelet.pagelet import pagelet_config
from pyams_template.template import template_config
__docformat__ = 'restructuredtext'
if sys.argv[(-1)].endswith('/bin/test'):

    @pagelet_config(name='testing.html')
    class PageletTestView:
        __doc__ = 'Pagelet test view'