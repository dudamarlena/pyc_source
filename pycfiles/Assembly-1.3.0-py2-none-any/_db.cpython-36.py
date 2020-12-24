# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Assembly/assembly/_db.py
# Compiled at: 2019-12-24 09:58:14
# Size of source mod 2**32: 4899 bytes
"""
Assembly: _db

Active Alchemy with some custom types
Just like sqlalchemy_utils, this module contains some custom types to
save in the db
"""
import flask_cloudy, active_alchemy, sqlalchemy_utils as sa_utils
from sqlalchemy.engine.url import make_url as sa_make_url

class ActiveAlchemyProxy(active_alchemy.ActiveAlchemy):
    __doc__ = '\n    A custom ActiveAlchemyProxy which defers the connection\n    '

    def __init__(self):
        self.Model = active_alchemy.declarative_base(cls=(active_alchemy.Model), name='Model')
        self.BaseModel = active_alchemy.declarative_base(cls=(active_alchemy.BaseModel), name='BaseModel')
        self._initialized = False
        self._IS_OK_ = False
        active_alchemy._include_sqlalchemy(self)
        self.StorageObjectType = StorageObjectType

    def connect__(self, uri, app):
        self.uri = uri
        self.info = sa_make_url(uri)
        self.options = self._cleanup_options(echo=False,
          pool_size=None,
          pool_timeout=None,
          pool_recycle=None,
          convert_unicode=True)
        self._initialized = True
        self._IS_OK_ = True
        self.connector = None
        self._engine_lock = active_alchemy.threading.Lock()
        self.session = active_alchemy._create_scoped_session(self, query_cls=(active_alchemy.BaseQuery))
        self.Model.db, self.BaseModel.db = self, self
        self.Model._query, self.BaseModel._query = self.session.query, self.session.query
        self.init_app(app)


class StorageObjectType(sa_utils.JSONType):
    __doc__ = '\n    A type to store flask_cloudy Storage Object Type:\n    -> https://github.com/mardix/flask-cloudy\n\n    It provides a convenient way to store object and retrieve it as you would\n    in the Assembly\'s storage.\n\n    By default it will hold basic info such as name and url, size, extension\n    Querying object.url, will not query the storage but use the default data\n    this way it prevents certain overhead when dealing with multiple items\n\n    Once an object is not found, it will try to connect to the storage and pull\n    the file data\n\n    If object is not found, it will return None.\n\n    Example:\n        from assembly import db\n\n        class Image(db.Model):\n            name = db.Column(db.String(255))\n            image = db.Column(db.StorageObjectType)\n            ...\n\n        # Setting the object\n        file = request.files.get("file")\n        if file:\n            upload = storage.upload(file)\n            if upload is not None:\n                new_img = Image.create(name="New Upload", image=upload)\n\n        # Getting the object. By default, most keys are cached,\n        # if not found it will load from the storage\n\n        img = Image.get(1234)\n        if img.image:\n            url = img.image.url\n            size = img.image.size\n            full_url = img.image.full_url\n            download_url = img.image.download_url\n\n        # Force loading of the storage\n        img.image.from_storage(my_other_storage)\n\n        img.image.url (will get it from my_other_storage)\n\n\n    '
    DEFAULT_KEYS = [
     'name', 'size', 'hash', 'url', 'full_url',
     'extension', 'type', 'path', 'provider_name']

    def process_bind_param(self, obj, dialect):
        value = obj or {}
        if isinstance(obj, flask_cloudy.Object):
            value = {}
            for k in self.DEFAULT_KEYS:
                value[k] = getattr(obj, k)

        return super(self.__class__, self).process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        value = super(self.__class__, self).process_result_value(value, dialect)
        if value:
            return StorageObject(value)


class StorageObject(dict):
    __doc__ = '\n    This object will be loaded when querying the table\n    It also app_context dict so it can json serialized when being copied\n    '

    def __init__(self, data):
        self._storage_obj = None
        self._storage_loaded = False
        self._data = data
        super(self.__class__, self).__init__(data)

    def __getattr__(self, item):
        if item in self._data:
            if not self._storage_loaded:
                return self._data.get(item)
        if not self._storage_loaded:
            from Assembly.ext import storage
            self.from_storage(storage)
        return getattr(self._storage_obj, item)

    def from_storage(self, storage):
        """
        To use a different storage
        :param storage: flask_cloudy.Storage instance
        """
        self._storage_obj = storage.get(self._data['name'])
        self._storage_loaded = True