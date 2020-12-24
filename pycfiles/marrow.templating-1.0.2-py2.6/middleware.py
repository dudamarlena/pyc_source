# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/cti/middleware.py
# Compiled at: 2012-05-16 12:10:40
import warnings
warnings.warn('The Common Template Interface middleware has been deprecated and moved into WebCore.\nUpdate your imports to reference "web.extras.templating" instead.', DeprecationWarning)
import web.extras.templating
from web.extras.templating import *
__all__ = web.extras.templating.__all__