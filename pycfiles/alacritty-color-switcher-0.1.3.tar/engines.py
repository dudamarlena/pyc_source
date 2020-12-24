# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/cti/engines.py
# Compiled at: 2010-03-18 05:47:02
import warnings
warnings.warn('Access to the common template interface via the "cti" package has been deprecated.\nUpdate your imports to reference "alacarte" instead.', DeprecationWarning)
import alacarte.engines
from alacarte.engines import *
__all__ = alacarte.engines.__all__