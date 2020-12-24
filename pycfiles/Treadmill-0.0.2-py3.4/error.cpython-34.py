# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/api/model/error.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 454 bytes
"""
Error API data models
"""
from flask_restplus import fields
ERROR_ID_WHY_FIELDS = {'_id': fields.String(description='Application ID'), 
 'why': fields.String(description='Why the error?')}

def models(api):
    """Get the error models"""
    erorr_id_why = api.model('ErrorIdWhy', ERROR_ID_WHY_FIELDS)
    error_model = api.model('ErrorResp', {'_error': fields.Nested(erorr_id_why)})
    return (
     erorr_id_why, error_model)