# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/context_processors.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import warnings
from djblets.cache.context_processors import ajax_serial as ajaxSerial, media_serial as mediaSerial
from djblets.deprecation import RemovedInDjblets20Warning
from djblets.siteconfig.context_processors import settings_vars as settingsVars
from djblets.urls.context_processors import site_root as siteRoot
warnings.warn(b'djblets.util.context_processors is deprecated', RemovedInDjblets20Warning)
__all__ = [
 b'ajaxSerial',
 b'mediaSerial',
 b'settingsVars',
 b'siteRoot']