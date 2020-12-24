# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/coding/Lantern/lantern-flask/.virtualenv/lib/python3.6/site-packages/lantern_flask/flask/api.py
# Compiled at: 2018-11-30 11:45:11
# Size of source mod 2**32: 657 bytes
import logging
from flask_restplus import Api
from lantern_flask import settings
log = logging.getLogger(__name__)
api = Api(version=(settings.get('API_VERSION', '1.0')),
  title=(settings.get('API_TITLE', 'Lantern Engine API')),
  description=(settings.get('API_DESC', 'Lantern Tech')))

@api.errorhandler
def default_error_handler(e):
    """Default Error Handles
    
    Args:
        e (Exception): Any exeption generated
    
    Returns:
        json: A proper json message
    """
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not settings.get('DEBUG', False):
        return (
         {'message': message}, 500)