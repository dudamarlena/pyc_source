# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./miniature/models/utils.py
# Compiled at: 2013-10-17 00:46:37
from django.db import models

def create_model(name, fields=None, app_label='', module='', options=None):
    """
    Create specified model
    """

    class Meta:
        pass

    if app_label:
        setattr(Meta, 'app_label', app_label)
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    attrs = {'__module__': module, 'Meta': Meta}
    if fields:
        attrs.update(fields)
    model = type(name, (models.Model,), attrs)
    return model