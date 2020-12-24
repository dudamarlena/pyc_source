# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dojo\store.py
# Compiled at: 2013-06-06 04:20:26
__doc__ = ' Dojo Store\n\n    Memory\n    JsonRest\n    Cache\n    Observable\n    \n    Not implemented:\n    \n    DataStore: compatibility with old API data/stores\n\n'
from pyojo.js import js_code, Object
from _base import Dojo

class Store(Dojo):
    require = [
     'dojo/store/Memory']

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.loc = '%s = new Memory({data: [%s],' % (name, data)
        self.loc += 'getChildren: function(object){return this.query({parent: object.id});}});'

    def get_json(self, url):
        self.require += ['dojo/json', 'dojo/text!' + url]
        self.loc = '%s = new Memory({data: [ json.parse(data) ],' % self.name
        self.loc += 'getChildren: function(object){return object.children || [];}});'


FUNC = {}
FUNC['Memory.getChildren.children'] = 'function(object){return object.children || [];}});'
FUNC['Memory.getChildren.parent'] = 'function(object){return this.query({parent: object.id});}'

class Memory(Object, Dojo):
    """
        
        x = new memory(options)
        
        :param data: string containing a Javascript array
        :param idProperty: identity property
        :param index:
        
        JS Methods:
        x.queryEngine
        
        x.add(object, options)
        x.get(id)
        x.getChildren(parent, options)
        x.getIdentity(object)
        x.getMetadata(object)
        x.put(object, options)
        x.query(query, options)
        x.remove(id)
        s.setData(data)
        x.transaction()
        
        @see http://dojotoolkit.org/api/1.9/dojo/store/Memory
    
    """
    require = [
     'dojo/store/Memory']

    def __init__(self, name, data=None, json=None, **member):
        if json is not None:
            self.require += ['dojo/json', 'dojo/text!' + json]
            self.data = 'json.parse(data)'
        else:
            self.data = data
        member['data'] = self.data
        Object.__init__(self, **member)
        return

    def add(self, data):
        self.loc_post += '%s.add(%s);' % (self.name, js_code(data))

    def remove(self, key):
        self.loc_post += "%s.remove('%s');" % key


class JsonRest(Object, Dojo):
    """ For larger data sets should use dojo.store.JsonRest etc. 
        instead of dojo.store.Memory
        
        x = new JsonRest(options)
        
        @param accepts: HTTP request accept header
        @param ascendingPrefix:
        @param descendingPrefix:
        @param headers:
        @param idProperty: identity property
        @param queryEngine:
        @param target:
        
        JS Methods:
        x.add(object, options)
        x.get(id)
        x.getChildren(parent, options)
        x.getIdentity(object)
        x.getMetadata(object)
        x.put(object, options)
        x.query(query, options)
        x.remove(id)
        x.transaction()
        
        @see http://dojotoolkit.org/api/1.9/dojo/store/Memory
    
    """
    require = [
     'dojo/store/JsonRest']

    def X__init__(self, name=None, **options):
        self.name = name
        self.options = options
        self.new()