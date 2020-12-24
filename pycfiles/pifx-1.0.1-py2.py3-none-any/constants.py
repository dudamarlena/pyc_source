# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pifx/constants.py
# Compiled at: 2018-01-23 16:12:23
A_OK_HTTP_CODES = [
 200,
 207]
A_ERROR_HTTP_CODES = {400: 'Request was invalid', 
   401: 'Invalid API key', 
   403: 'Bad OAuth scope', 
   404: 'Selector did not match any lights', 
   422: 'Missing or malformed parameters', 
   426: 'HTTP is required to perform transaction', 
   429: 'Rate limit exceeded', 
   500: 'API currently unavailable', 
   502: 'API currently unavailable', 
   503: 'API currently unavailable', 
   523: 'API currently unavailable'}