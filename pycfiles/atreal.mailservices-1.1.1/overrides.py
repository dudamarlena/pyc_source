# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.mailservices/atreal/mailservices/browser/overrides.py
# Compiled at: 2011-11-25 03:57:49
"""
"""
from zope.publisher.browser import isCGI_NAME
from zope.i18n.interfaces import IUserPreferredCharsets
from Products.Five.browser.decode import _decode

def processInputs(request, charsets=None):
    """ Override Products.Five.browser.decode.processInputs
    """
    if charsets is None:
        envadapter = IUserPreferredCharsets(request)
        charsets = envadapter.getPreferredCharsets() or ['utf-8']
    for (name, value) in request.form.items():
        if not (isCGI_NAME(name) or name.startswith('HTTP_')):
            if name == 'groups' or name == 'users':
                request.form[name] = value
            elif isinstance(value, str):
                request.form[name] = _decode(value, charsets)
            elif isinstance(value, list):
                request.form[name] = [ _decode(val, charsets) for val in value if isinstance(val, str)
                                     ]
            elif isinstance(value, tuple):
                request.form[name] = tuple([ _decode(val, charsets) for val in value if isinstance(val, str)
                                           ])

    return