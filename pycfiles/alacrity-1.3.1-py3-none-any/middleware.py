# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/cti/middleware.py
# Compiled at: 2010-03-18 15:03:39
import warnings
warnings.warn('The Common Template Interface middleware has been deprecated and moved into WebCore.\nUpdate your imports to reference "web.extras.templating" instead.', DeprecationWarning)
import web.extras.templating
from web.extras.templating import *
__all__ = web.extras.templating.__all__