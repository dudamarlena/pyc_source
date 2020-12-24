# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fosswallproxy0/base.py
# Compiled at: 2008-02-12 03:23:59
import string
from turbogears import controllers, expose, flash, redirect
LETTERS = string.ascii_uppercase
BASE_DIR = '/opt/falb/res'

class Base(controllers.RootController):
    pass