# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/cmsplugin_phlog/forms/fields.py
# Compiled at: 2013-06-26 16:38:22
from django.forms import Field
try:
    from cmsplugin_phlog.forms.widgets import PluginsWidget
except Exception as e:
    print str(e)
    raise e

class ChildPluginsField(Field):
    widget = PluginsWidget

    def __init__(self, **kwargs):
        kwargs['required'] = False
        super(ChildPluginsField, self).__init__(**kwargs)