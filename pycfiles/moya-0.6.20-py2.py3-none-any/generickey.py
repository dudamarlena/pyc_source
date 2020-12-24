# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/generickey.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
from .errors import ElementNotFoundError
from .compat import text_type
import logging
log = logging.getLogger(b'moya.db')

class GenericKey(object):
    """A generic foreign key"""

    def __init__(self, app, model, pk):
        self.app = app
        self.model = model
        self.pk = pk

    def __repr__(self):
        if self.app is None:
            return b'<generic-key (null)>'
        else:
            return (b'<generic-key {}#{} {}>').format(self.app.name, self.model.libname, self.pk)

    @classmethod
    def from_object(cls, obj):
        if obj is None:
            return cls(None, None, None)
        else:
            return cls(obj._app, obj._model, obj.id)

    @classmethod
    def decode(cls, value):
        if not value:
            return cls(None, None, None)
        else:
            try:
                app, model, pk = [ v or None for v in value.split(b',') ]
                pk = int(pk)
            except ValueError:
                return cls(None, None, None)

            from moya import pilot
            archive = pilot.context[b'.app'].archive
            app = archive.get_app(app)
            if app is None:
                return cls(None, None, None)
            try:
                app, model = archive.get_element((b'{}#{}').format(app.name, model))
            except:
                return cls(None, None, None)

            any_key = cls(app, model, pk)
            return any_key

    def __moyacontext__(self, context):
        return self.lookup(context)

    def __moyadbobject__(self):
        return self.encode()

    def encode(self):
        if not self.app:
            return None
        else:
            return (b',').join((self.app.name, self.model.libname, text_type(self.pk)))

    def lookup(self, context):
        if self.app is None:
            return
        else:
            element_ref = (b'{}#{}').format(self.app.name, self.model.libname)
            try:
                model_app, model = self.app.archive.get_element(element_ref)
            except ElementNotFoundError:
                log.warning(b'no model found for generic key {!r}', self)
                return

            db = model.get_db()
            dbsession = context[b'._dbsessions'][db.name]
            table_class = model.get_table_class(model_app)
            qs = dbsession.query(table_class).filter(table_class.id == self.pk)
            return qs.first()