# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/core.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import warnings
from djblets.deprecation import RemovedInDjblets20Warning
from djblets.webapi.decorators import SPECIAL_PARAMS
from djblets.webapi.encoders import BasicAPIEncoder, JSONEncoderAdapter, WebAPIEncoder, XMLEncoderAdapter, get_registered_encoders
from djblets.webapi.responses import WebAPIResponse, WebAPIResponseError, WebAPIResponseFormError, WebAPIResponsePaginated
warnings.warn(b'djblets.webapi.core is deprecated', RemovedInDjblets20Warning)
__all__ = [
 b'BasicAPIEncoder',
 b'JSONEncoderAdapter',
 b'SPECIAL_PARAMS',
 b'WebAPIEncoder',
 b'WebAPIResponse',
 b'WebAPIResponseError',
 b'WebAPIResponseFormError',
 b'WebAPIResponsePaginated',
 b'XMLEncoderAdapter',
 b'get_registered_encoders']