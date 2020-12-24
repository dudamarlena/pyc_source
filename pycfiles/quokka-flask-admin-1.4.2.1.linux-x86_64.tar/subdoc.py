# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/flask_admin/contrib/mongoengine/subdoc.py
# Compiled at: 2016-06-26 14:14:34
from flask_admin._compat import iteritems
from flask_admin.model.form import InlineBaseFormAdmin

class EmbeddedForm(InlineBaseFormAdmin):

    def __init__(self, **kwargs):
        super(EmbeddedForm, self).__init__(**kwargs)
        self._form_subdocuments = convert_subdocuments(getattr(self, 'form_subdocuments', {}))


def convert_subdocuments(values):
    result = {}
    for name, p in iteritems(values):
        if isinstance(p, dict):
            result[name] = EmbeddedForm(**p)
        elif isinstance(p, EmbeddedForm):
            result[name] = p
        else:
            raise ValueError('Invalid subdocument type: expecting dict or instance of flask_admin.contrib.mongoengine.EmbeddedForm, got %s' % type(p))

    return result