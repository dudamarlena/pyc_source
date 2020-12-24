# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximsmirnov/.virtualenvs/django-antivirus-field/lib/python2.7/site-packages/django_antivirus_field/utils.py
# Compiled at: 2014-10-10 08:01:32
from __future__ import unicode_literals
import warnings
from django.conf import settings
ANTIVIRUS_ON = getattr(settings, b'CLAMAV_ACTIVE', False)
if ANTIVIRUS_ON:
    try:
        import pyclamd
        clam = pyclamd.ClamdUnixSocket()
        clam.ping()
    except Exception as err:
        warnings.warn((b'Problem with ClamAV: {}').format(str(err)))
        clam = None

def is_infected(stream):
    """
    Create tmp file and scan it with ClamAV
    Returns
        True, 'Virus name' - if virus detected
        False, '' - if not virus detected
        None, '' - status unknown (pyclamd not installed)
    """
    if not ANTIVIRUS_ON or clam is None:
        return (None, '')
    result = clam.scan_stream(stream)
    if result:
        return (True, result[b'stream'])
    else:
        return (
         False, b'')