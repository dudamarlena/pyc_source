# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/lib/db/db.py
# Compiled at: 2018-12-07 08:05:33
from pprint import pprint
import time, xio
from .handlers import python
from .handlers import json
__DATABASES__ = {}
__HANDLERS__ = {'python': python.Database, 
   'json': json.Database}
try:
    from .handlers import mongo
    __HANDLERS__['mongo'] = mongo.Database
except:
    pass

try:
    from .handlers import redis
    __HANDLERS__['redis'] = redis.Database
except:
    pass

def db(name=None, type='python', params=None):
    cls = __HANDLERS__.get(type)
    assert cls, 'no handler for dbtype %s ' % type
    params = params or {}
    return Db(name, cls, params)


class Db:

    def __init__(self, name, cls, params, containers=None, **kwargs):
        self.name = name
        self.handler = cls(name, params)

    def list(self):
        return self.handler.list()

    def head(self, name):
        return bool(self.get(name))

    def get(self, name):
        chandler = self.handler.get(name)
        if chandler:
            return Container(self, chandler)
        else:
            return

    def container(self, name, factory=None):
        container = self.get(name)
        if not container:
            container = self.put(name)
        container._factory = factory
        return container

    def put(self, name):
        exist = self.head(name)
        assert not exist, Exception(409)
        chandler = self.handler.put(name)
        return Container(self, chandler)

    def delete(self, name):
        count = self.get(name).count()
        assert count == 0, Exception(409)
        log.info('DELETE CONTAINER %s' % name)
        self.handler.delete(name)


class Container:

    def __init__(self, db, handler):
        self.db = db
        self.handler = handler
        self.name = handler.name
        self._factory = None
        return

    def new(self, id=None, **data):
        obj = self._factory(container=self)
        obj.id = id
        if data:
            obj.update(data)
        return obj

    def head(self, id):
        return self.handler.exist(id)

    def get(self, id, fields=None):
        if not id:
            raise AssertionError
            data = self.handler.get(id)
            if data and '_ttl' in data:
                created = data.get('_created')
                ttl = data.get('_ttl')
                now = int(time.time())
                if ttl and now > created + ttl:
                    self.handler.delete(id)
                    return None
            return self._factory or xio.data(data, fields=fields)
        else:
            return self._factory(data, container=self)

    def select(self, filter=None, fields=None, limit=None, start=0, sort=None, **kwargs):
        data = self.handler.select(filter=filter, fields=fields, limit=limit, start=start, sort=sort)
        return xio.data(data, filter=filter, fields=fields)

    def put(self, index, data, ttl=None):
        data['_id'] = index
        data['_created'] = int(time.time())
        if ttl:
            data['_ttl'] = ttl
        self.handler.put(index, data)
        return True

    def update(self, index, data, ttl=None):
        data['_updated'] = int(time.time())
        if ttl:
            data['_ttl'] = ttl
        self.handler.update(index, data)
        return True

    def delete(self, index=None, filter=None):
        deleted_item = self.get(index)
        assert deleted_item, 404
        self.handler.delete(index=index, filter=filter)
        return True

    def truncate(self):
        return self.handler.truncate()

    def count(self, **kwargs):
        return self.handler.count(**kwargs)


class Item(dict):
    """
    helper class for basic Class inherance

    todo: merge with xio.data with resource-based container handling

        class Item(db.Item):

            def incr(self):
                self.counter += 1
                self.save()

            def check(self):
                print '====>', self.title, self.counter, self.walou

        db = xio.db()

        container = db.container('items',factory=Item)

        item = Item(container=container)
        item.description = 'test ok'
        item.save()

        # other method
        item = container.new()
        item.description = 'test ok'
        item.save()

    """

    def __init__(self, *args, **kwargs):
        self._container = kwargs.get('container')
        if args and not isinstance(args[0], dict):
            id = args[0]
            self._data = self._container.get(id) or {'_id': id}
        elif args and isinstance(args[0], dict):
            self._data = args[0]
        else:
            self._data = dict()
        dict.__init__(self, **self._data)
        self.id = self._data.get('_id')

    def __getattr__(self, name):
        return self.get(name, None)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def save(self):
        if not self.id:
            import uuid
            self.id = str(uuid.uuid4())
        reqcall = False
        for k, v in self.items():
            if k[0] != '_' and k != 'id':
                oldvalue = self._data.get(k)
                newvalue = v
                reqcall = reqcall or newvalue != oldvalue
                self._data[k] = newvalue

        if reqcall:
            self._container.put(self.id, self._data)