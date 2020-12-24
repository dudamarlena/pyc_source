# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bytecodehacks/fleshy.py
# Compiled at: 2000-03-15 15:55:42
import new
fleshable_dict_name = intern('$ forgot to call __init__ did we? $')
old_self_key = intern('$ weird obfuscated name $')

class Flesher:
    MagicSelfValue = []

    def __init__(self):
        setattr(self, fleshable_dict_name, {})

    def make_fleshed(self, attr_name, **data):
        attr = self.__dict__[attr_name]
        delattr(self, attr_name)
        getattr(self, fleshable_dict_name)[attr_name] = (attr, data)

    def __getattr__(self, attr_name):
        dict = self.__dict__[fleshable_dict_name]
        attr, data = dict.get(attr_name, (None, None))
        if attr is not None:
            return attr.flesh(data, owner=self)
        else:
            raise AttributeError, attr_name
            return


class Fleshable:

    def unflesh(self):
        return self.__dict__.get(old_self_key, self)

    def flesh(self, data=None, owner=None, **kw):
        if data is None:
            data = kw
        newdict = self.__dict__.copy()
        for k, v in data.items():
            if v is Flesher.MagicSelfValue:
                newdict[k] = owner
            else:
                newdict[k] = v

        if not newdict.has_key(old_self_key):
            newdict[old_self_key] = self
        return new.instance(self.__class__, newdict)

    def __setattr__(self, attr, value):
        selfd = self.__dict__
        if selfd.has_key(old_self_key):
            selfd[old_self_key].__dict__[attr] = value
        selfd[attr] = value

    def __getattr__(self, attr, u=[], error=AttributeError(), old_self_key=old_self_key):
        if self.__dict__.has_key(old_self_key):
            dict = self.__dict__[old_self_key].__dict__
            if dict.has_key(attr):
                ret = dict[attr]
                self.__dict__[attr] = ret
                return ret
        error.args = (
         attr,)
        raise error

    def __cmp__(self, other):
        lid = id(getattr(self, old_self_key, self))
        rid = id(getattr(other, old_self_key, other))
        return lid - rid


class TF(Fleshable, Flesher):

    def __init__(self):
        self.s = self
        self.make_fleshed('s', s=self)