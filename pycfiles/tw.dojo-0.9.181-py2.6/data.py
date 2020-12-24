# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tw/dojo/data.py
# Compiled at: 2013-01-02 11:28:41
from tw.dojo.core import DojoBase, JSONHash
from tw.api import Resource, Link, JSLink, JSSource, CSSLink, CSSSource, Widget, js_function, locations
from tw.api import RequestLocalDescriptor
from tw.core.resources import JSDynamicFunctionCalls
buildService = JSSource(src="\n    function buildService(url){\n        var service = function(query, queryOptions) {\n        if (queryOptions.isRender==undefined) queryOptions.isRender=true;\n        return dojo.xhrGet({url:url, content:{query:query, queryOptions:dojo.toJson(queryOptions)},handleAs:'json',handle:function(data){return data;}});\n        }\n        service.put = function(id, value) {\n        return dojo.xhrPut({url:url+'/'+id, handleAs:'json', content:{value:value}});\n        }\n        service.post = function(id, value) {\n        return dojo.xhrPost({url:url+'/'+id, content:{id:id, value:value}});\n        }\n        service.delete = function(id) {\n          var d = new dojo.Deferred();\n          d.callback(); //delete is a noop for pagers\n          return d;\n        }\n        return service\n\t\t};\n    ")

class DojoDataStore(DojoBase):
    url = ''
    params = {'url': 'url of remote data'}


class DojoItemFileReadStore(DojoDataStore):
    """DojoItemFileReadStore builds a dojo.data.ItemFileReadStore from a json source
    """
    require = [
     'dojo.data.ItemFileReadStore']
    dojoType = 'dojo.data.ItemFileReadStore'
    params = ['dojoType', 'id', 'url']
    template = '<div dojoType="${dojoType}" jsId="${id}"  id="${id}" url="${url}"/>'


class DojoItemFileWriteStore(DojoDataStore):
    require = [
     'dojo.data.ItemFileWriteStore']
    dojoType = 'dojo.data.ItemFileWriteStore'
    params = ['dojoType', 'id', 'url']
    template = '<div dojoType="${dojoType}" jsId="${id}" id="${id}" url="${url}"/>'


class DojoQueryReadStore(DojoDataStore):
    require = [
     'dojox.data.QueryReadStore']
    dojoType = 'dojox.data.QueryReadStore'
    params = ['dojoType', 'id', 'url']
    template = '<div dojoType="${dojoType}" jsId="${id}" id="${id}" url="${url}" />'


class DojoJsonRestStore(DojoBase):
    javascript = [
     buildService]
    require = ['twdojo.data.TWDojoRestStore']
    dojoType = 'twdojo.data.TWDojoRestStore'
    params = ['target', 'id', 'url', 'idAttribute', 'autoSave']
    idAttribute = 'id'
    autoSave = True
    template = '\n            <script type=\'text/javascript\'>\n                var ${id}=new twdojo.data.TWDojoRestStore({target:"${target}",autoSave:"${autoSave and \'true\' or \'false\'}", service:buildService("${url}"),idAttribute:"${idAttribute}"})\n            </script>'