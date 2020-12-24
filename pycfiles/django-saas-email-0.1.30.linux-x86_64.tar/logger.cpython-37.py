# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/logger.py
# Compiled at: 2018-10-24 06:32:38
# Size of source mod 2**32: 197 bytes
import logging
logger = logging.getLogger('root')
FORMAT = '%(filename)s:%(lineno)s %(funcName)s() - %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)