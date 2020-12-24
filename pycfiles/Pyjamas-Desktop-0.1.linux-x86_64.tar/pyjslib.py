# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/pyjslib.py
# Compiled at: 2008-09-03 09:02:13
from pyjamas.__pyjamas__ import JS
if None:
    JS('\nStopIteration = function () {};\nStopIteration.prototype = new Error();\nStopIteration.name = \'StopIteration\';\nStopIteration.message = \'StopIteration\';\n\nKeyError = function () {};\nKeyError.prototype = new Error();\nKeyError.name = \'KeyError\';\nKeyError.message = \'KeyError\';\n\nfunction pyjslib_String_find(sub, start, end) {\n    var pos=this.indexOf(sub, start);\n    if (pyjslib_isUndefined(end)) return pos;\n\n    if (pos + sub.length>end) return -1;\n    return pos;\n}\n    \nfunction pyjslib_String_join(data) {\n    var text="";\n    \n    if (pyjslib_isArray(data)) {\n        return data.join(this);\n    }\n    else if (pyjslib_isIteratable(data)) {\n        var iter=data.__iter__();\n        try {\n            text+=iter.next();\n            while (true) {\n                var item=iter.next();\n                text+=this + item;\n            }\n        }\n        catch (e) {\n            if (e != StopIteration) throw e;\n        }\n    }\n\n    return text;\n}\n\nfunction pyjslib_String_replace(old, replace, count) {\n    var do_max=false;\n    var start=0;\n    var new_str="";\n    var pos=0;\n    \n    if (!pyjslib_isString(old)) return this.__replace(old, replace);\n    if (!pyjslib_isUndefined(count)) do_max=true;\n    \n    while (start<this.length) {\n        if (do_max && !count--) break;\n        \n        pos=this.indexOf(old, start);\n        if (pos<0) break;\n        \n        new_str+=this.substring(start, pos) + replace;\n        start=pos+old.length;\n    }\n    if (start<this.length) new_str+=this.substring(start);\n\n    return new_str;\n}\n\nfunction pyjslib_String_split(sep, maxsplit) {\n    var items=new pyjslib_List();\n    var do_max=false;\n    var subject=this;\n    var start=0;\n    var pos=0;\n    \n    if (pyjslib_isUndefined(sep) || pyjslib_isNull(sep)) {\n        sep=" ";\n        subject=subject.strip();\n        subject=subject.replace(/\\s+/g, sep);\n    }\n    else if (!pyjslib_isUndefined(maxsplit)) do_max=true;\n\n    while (start<subject.length) {\n        if (do_max && !maxsplit--) break;\n    \n        pos=subject.indexOf(sep, start);\n        if (pos<0) break;\n        \n        items.append(subject.substring(start, pos));\n        start=pos+sep.length;\n    }\n    if (start<subject.length) items.append(subject.substring(start));\n    \n    return items;\n}\n\nfunction pyjslib_String_strip(chars) {\n    return this.lstrip(chars).rstrip(chars);\n}\n\nfunction pyjslib_String_lstrip(chars) {\n    if (pyjslib_isUndefined(chars)) return this.replace(/^\\s+/, "");\n\n    return this.replace(new RegExp("^[" + chars + "]+"), "");\n}\n\nfunction pyjslib_String_rstrip(chars) {\n    if (pyjslib_isUndefined(chars)) return this.replace(/\\s+$/, "");\n\n    return this.replace(new RegExp("[" + chars + "]+$"), "");\n}\n\nfunction pyjslib_String_startswith(prefix, start) {\n    if (pyjslib_isUndefined(start)) start = 0;\n\n    if (this.substring(start, prefix.length) == prefix) return true;\n    return false;\n}\n\nString.prototype.__getitem__ = String.prototype.charAt;\nString.prototype.upper = String.prototype.toUpperCase;\nString.prototype.lower = String.prototype.toLowerCase;\nString.prototype.find=pyjslib_String_find;\nString.prototype.join=pyjslib_String_join;\n\nString.prototype.__replace=String.prototype.replace;\nString.prototype.replace=pyjslib_String_replace;\n\nString.prototype.split=pyjslib_String_split;\nString.prototype.strip=pyjslib_String_strip;\nString.prototype.lstrip=pyjslib_String_lstrip;\nString.prototype.rstrip=pyjslib_String_rstrip;\nString.prototype.startswith=pyjslib_String_startswith;\n\nvar str = String;\n\nvar pyjslib_abs = Math.abs;\n\nfunction pyjs_extend(klass, base) {\n    function klass_object_inherit() {}\n    klass_object_inherit.prototype = base.prototype;\n    klass_object = new klass_object_inherit();\n    for (var i in base.prototype.__class__) {\n        v = base.prototype.__class__[i];\n        if (typeof v == "function" && (v.class_method || v.static_method || v.unbound_method))\n        {\n            klass_object[i] = v;\n        }\n    }\n    \n    function klass_inherit() {}\n    klass_inherit.prototype = klass_object;\n    klass.prototype = new klass_inherit();\n    klass_object.constructor = klass;\n    klass.prototype.__class__ = klass_object;\n    \n    for (var i in base.prototype) {\n        v = base.prototype[i];\n        if (typeof v == "function" && v.instance_method)\n        {\n            klass.prototype[i] = v;\n        }\n    }\n}\n\nfunction pyjs_kwargs_function_call(func, args)\n{\n    return func.apply(null, func.parse_kwargs.apply(null, args));\n}\n\nfunction pyjs_kwargs_method_call(obj, method_name, args)\n{\n    var method = obj[method_name];\n    return method.apply(obj, method.parse_kwargs.apply(null, args));\n}\n\n')

class Object:
    pass


class Class:

    def __init__(self, name):
        self.name = name

    def __str___(self):
        return self.name


def cmp(a, b):
    if hasattr(a, '__cmp__'):
        return a.__cmp__(b)
    elif hasattr(a, '__cmp__'):
        return -b.__cmp__(a)
    if a > b:
        return 1
    elif b > a:
        return -1
    else:
        return 0


class List:

    def __init__(self, data=None):
        JS('\n        this.l = [];\n        \n        if (pyjslib_isArray(data)) {\n            for (var i=0; i < data.length; i++) {\n                this.l[i]=data[i];\n                }\n            }\n        else if (pyjslib_isIteratable(data)) {\n            var iter=data.__iter__();\n            var i=0;\n            try {\n                while (true) {\n                    var item=iter.next();\n                    this.l[i++]=item;\n                    }\n                }\n            catch (e) {\n                if (e != StopIteration) throw e;\n                }\n            }\n        ')

    def append(self, item):
        JS('    this.l[this.l.length] = item;')

    def remove(self, value):
        JS('\n        var index=this.index(value);\n        if (index<0) return false;\n        this.l.splice(index, 1);\n        return true;\n        ')

    def index(self, value, start=0):
        JS('\n        var length=this.l.length;\n        for (var i=start; i<length; i++) {\n            if (this.l[i]==value) {\n                return i;\n                }\n            }\n        return -1;\n        ')

    def insert(self, index, value):
        JS('    var a = this.l; this.l=a.slice(0, index).concat(value, a.slice(index));')

    def pop(self, index=-1):
        JS('\n        if (index<0) index = this.l.length + index;\n        var a = this.l[index];\n        this.l.splice(index, 1);\n        return a;\n        ')

    def slice(self, lower, upper):
        JS('\n        if (upper==null) return pyjslib_List(this.l.slice(lower));\n        return pyjslib_List(this.l.slice(lower, upper));\n        ')

    def __getitem__(self, index):
        JS('\n        if (index<0) index = this.l.length + index;\n        return this.l[index];\n        ')

    def __setitem__(self, index, value):
        JS('    this.l[index]=value;')

    def __delitem__(self, index):
        JS('    this.l.splice(index, 1);')

    def __len__(self):
        JS('    return this.l.length;')

    def __contains__(self, value):
        return self.index(value) >= 0

    def __iter__(self):
        JS("\n        var i = 0;\n        var l = this.l;\n        \n        return {\n            'next': function() {\n                if (i >= l.length) {\n                    throw StopIteration;\n                }\n                return l[i++];\n            },\n            '__iter__': function() {\n                return this;\n            }\n        };\n        ")

    def sort(self, compareFunc=None, keyFunc=None, reverse=False):
        global cmp
        if not compareFunc:
            compareFunc = cmp
        if keyFunc and reverse:

            def thisSort1(a, b):
                return -compareFunc(keyFunc(a), keyFunc(b))

            self.l.sort(thisSort1)
        elif keyFunc:

            def thisSort2(a, b):
                return compareFunc(keyFunc(a), keyFunc(b))

            self.l.sort(thisSort2)
        elif reverse:

            def thisSort3(a, b):
                return -compareFunc(a, b)

            self.l.sort(thisSort3)
        else:
            self.l.sort(compareFunc)

    def getArray(self):
        """
        Access the javascript Array that is used internally by this list
        """
        return self.l


list = List

class Tuple(List):

    def __init__(self, data):
        List.__init__(self, data)


tuple = Tuple

class Dict:

    def __init__(self, data=None):
        JS('\n        this.d = {};\n\n        if (pyjslib_isArray(data)) {\n            for (var i in data) {\n                var item=data[i];\n                this.d[item[0]]=item[1];\n                }\n            }\n        else if (pyjslib_isIteratable(data)) {\n            var iter=data.__iter__();\n            try {\n                while (true) {\n                    var item=iter.next();\n                    this.d[item.__getitem__(0)]=item.__getitem__(1);\n                    }\n                }\n            catch (e) {\n                if (e != StopIteration) throw e;\n                }\n            }\n        else if (pyjslib_isObject(data)) {\n            for (var key in data) {\n                this.d[key]=data[key];\n                }\n            }\n        ')

    def __setitem__(self, key, value):
        JS(' this.d[key]=value;')

    def __getitem__(self, key):
        JS('\n        var value=this.d[key];\n        // if (pyjslib_isUndefined(value)) throw KeyError;\n        return value;\n        ')

    def __len__(self):
        JS('\n        var size=0;\n        for (var i in this.d) size++;\n        return size;\n        ')

    def has_key(self, key):
        JS('\n        if (pyjslib_isUndefined(this.d[key])) return false;\n        return true;\n        ')

    def __delitem__(self, key):
        JS(' delete this.d[key];')

    def __contains__(self, key):
        JS('    return (pyjslib_isUndefined(this.d[key])) ? false : true;')

    def keys(self):
        JS('\n        var keys=new pyjslib_List();\n        for (var key in this.d) keys.append(key);\n        return keys;\n        ')

    def values(self):
        JS('\n        var keys=new pyjslib_List();\n        for (var key in this.d) keys.append(this.d[key]);\n        return keys;\n        ')

    def __iter__(self):
        JS('\n        return this.keys().__iter__();\n        ')

    def iterkeys(self):
        JS('\n        return this.keys().__iter__();\n        ')

    def itervalues(self):
        JS('\n        return this.values().__iter__();\n        ')

    def iteritems(self):
        JS("\n        var d = this.d;\n        var iter=this.keys().__iter__();\n        \n        return {\n            '__iter__': function() {\n                return this;\n            },\n\n            'next': function() {\n                var key;\n                while (key=iter.next()) {\n                    var item=new pyjslib_List();\n                    item.append(key);\n                    item.append(d[key]);\n                    return item;\n                }\n            }\n        };\n        ")

    def setdefault(self, key, default_value):
        if not self.has_key(key):
            self[key] = default_value

    def get(self, key, default_value=None):
        value = self[key]
        JS('if(pyjslib_isUndefined(value)) { value = default_value; }')
        return value

    def update(self, d):
        for (k, v) in d.iteritems():
            self[k] = v

    def getObject(self):
        """
        Return the javascript Object which this class uses to store dictionary keys and values
        """
        return self.d


dict = Dict

def range():
    JS("\n    var start = 0;\n    var stop = 0;\n    var step = 1;\n\n    if (arguments.length == 2) {\n        start = arguments[0];\n        stop = arguments[1];\n        }\n    else if (arguments.length == 3) {\n        start = arguments[0];\n        stop = arguments[1];\n        step = arguments[2];\n        }\n    else if (arguments.length>0) stop = arguments[0];\n\n    return {\n        'next': function() {\n            if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) throw StopIteration;\n            var rval = start;\n            start += step;\n            return rval;\n            },\n        '__iter__': function() {\n            return this;\n            }\n        }\n    ")


def slice(object, lower, upper):
    JS('\n    if (pyjslib_isString(object)) {\n        if (pyjslib_isNull(upper)) upper=object.length;\n        return object.substring(lower, upper);\n        }\n    if (pyjslib_isObject(object) && object.slice) return object.slice(lower, upper);\n    \n    return null;\n    ')


def len(object):
    JS('\n    if (object==null) return 0;\n    if (pyjslib_isObject(object) && object.__len__) return object.__len__();\n    return object.length;\n    ')


def getattr(obj, method):
    JS('\n    if (!pyjslib_isObject(obj)) return null;\n    if (!pyjslib_isFunction(obj[method])) return obj[method];\n\n    return function() {\n        obj[method].call(obj);\n        }\n    ')


def hasattr(obj, method):
    JS('\n    if (!pyjslib_isObject(obj)) return false;\n    if (pyjslib_isUndefined(obj[method])) return false;\n\n    return true;\n    ')


def dir(obj):
    JS('\n    var properties=new pyjslib_List();\n    for (property in obj) properties.append(property);\n    return properties;\n    ')


def filter(obj, method, sequence=None):
    items = []
    if sequence == None:
        sequence = method
        method = obj
        for item in sequence:
            if method(item):
                items.append(item)

    for item in sequence:
        if method.call(obj, item):
            items.append(item)

    return items


def map(obj, method, sequence=None):
    items = []
    if sequence == None:
        sequence = method
        method = obj
        for item in sequence:
            items.append(method(item))

    for item in sequence:
        items.append(method.call(obj, item))

    return items


next_hash_id = 0

def hash(obj):
    JS('\n    if (obj == null) return null;\n    \n    if (obj.$H) return obj.$H;\n    if (obj.__hash__) return obj.__hash__();\n    if (obj.constructor == String || obj.constructor == Number || obj.constructor == Date) return obj;\n    \n    obj.$H = ++pyjslib_next_hash_id;\n    return obj.$H;\n    ')


def isObject(a):
    JS("\n    return (a && typeof a == 'object') || pyjslib_isFunction(a);\n    ")


def isFunction(a):
    JS("\n    return typeof a == 'function';\n    ")


def isString(a):
    return isinstance(a, str) or isinstance(a, type(''))


def isNull(a):
    JS("\n    return typeof a == 'object' && !a;\n    ")


def isArray(a):
    JS('\n    return pyjslib_isObject(a) && a.constructor == Array;\n    ')


def isUndefined(a):
    JS("\n    return typeof a == 'undefined';\n    ")


def isIteratable(a):
    JS('\n    return pyjslib_isObject(a) && a.__iter__;\n    ')


def isNumber(a):
    return type(a) is int or type(a) is long


def toJSObjects(x):
    """
       Convert the pyjs pythonic List and Dict objects into javascript Object and Array
       objects, recursively.
    """
    result = x
    if isObject(x) and x.__class__:
        if x.__class__ == 'pyjslib_Dict':
            return toJSObjects(x.d)
        elif x.__class__ == 'pyjslib_List':
            return toJSObjects(x.l)
    if isObject(x):
        JS('\n        result = {};\n        for(var k in x) {\n           var v = x[k];\n           var tv = pyjslib_toJSObjects(v)\n           result[k] = tv;\n        }\n        ')
    if isArray(x):
        JS('\n        result = [];\n        for(var k=0; k < x.length; k++) {\n           var v = x[k];\n           var tv = pyjslib_toJSObjects(v);\n           result.push(tv);\n        }\n        ')
    return result


def printFunc(objs):
    JS('\n    var s = "";\n    for(var i=0; i < objs.length; i++) {\n        if(s != "") s += " ";\n        s += objs[i];\n    }\n    console.debug(s)\n    ')