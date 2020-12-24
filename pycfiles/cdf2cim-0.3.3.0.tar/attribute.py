# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/cdf/attribute.py
# Compiled at: 2010-11-11 15:27:36
import weakref, internal, framework, entry

class attribute(framework.hashablyUniqueObject):

    def __init__(self, parent=None, num=None):
        self._parent = None
        self._num = None
        self._cache = None
        if parent is not None:
            self.adopt(parent)
            if num is not None:
                self._num = num
                self._meta()
                self._fill()
        return

    def adopt(self, parent):
        if parent is not None:
            self._parent = weakref.ref(parent)
        else:
            self._parent = None
        return

    def _canon(self, value):
        if isinstance(value, list):
            if len(value) == 1:
                value = value[0]
            else:
                value = tuple(value)
        return value

    def _meta(self):
        pass

    def _fill(self):
        pass

    def _write(self):
        pass


class gAttribute(attribute, list):
    _tokens = {'NAME': internal.ATTR_NAME_, 
       'SELECT_ATTR': internal.ATTR_, 
       'SELECT_ENTRY': internal.gENTRY_, 
       'GET_ENTRY': internal.gENTRY_DATA_, 
       'GET_ENTRY_DATATYPE': internal.gENTRY_DATATYPE_, 
       'GET_ENTRY_NUMELEMS': internal.gENTRY_NUMELEMS_, 
       'GET_ATTR_NUMENTRIES': internal.ATTR_NUMgENTRIES_}

    def __init__(self, value=None, archive=None, num=None):
        list.__init__(self)
        attribute.__init__(self, archive, num)
        if value is not None:
            value = self._canon(value)
            if instance(value, list):
                self.extend(value)
            else:
                self.append(value)
        return

    def _fill(self):
        (count,) = internal.CDFlib(internal.GET_, self._tokens['GET_ATTR_NUMENTRIES'])
        for num in xrange(0, count):
            (value,) = internal.CDFlib(internal.SELECT_, self._tokens['SELECT_ATTR'], self._num, self._tokens['SELECT_ENTRY'], num, internal.GET_, self._tokens['GET_ENTRY'])
            self.append(self._canon(value))


class vAttribute(attribute):

    def __init__(self, value=None, variable=None, num=None):
        self._value = None
        attribute.__init__(self, variable, num)
        if value is not None:
            self._value = self._canon(value)
        return

    def _fill(self):
        try:
            if self._parent is not None:
                parent = self._parent()
                if parent is not None:
                    internal.CDFlib(internal.SELECT_, parent._tokens['SELECT_ATTR'], self._num, parent._tokens['SELECT_ENTRY'], parent._num)
                    (cdfType,) = internal.CDFlib(internal.GET_, parent._tokens['GET_ENTRY_DATATYPE'])
                    (value,) = internal.CDFlib(internal.GET_, parent._tokens['GET_ENTRY'])
                    self._value = self._canon(value)
        except:
            self._value = None

        return

    def __repr__(self):
        return repr(self._value)

    def __coerce__(self, other):
        return type(other)(self._value)


class variableTable(framework.coerciveDictionary, framework.hashablyUniqueObject):

    def __init__(self, variable):
        self._variable = variable
        self._invalid = {}
        framework.coerciveDictionary.__init__(self)

    def __setitem__(self, key, value):
        if key in self:
            dict.__setitem__(self, key, value)
        else:
            archive = self._variable._archive()
            if archive is not None:
                if archive.attributes._reserve(key, self):
                    dict.__setitem__(self, key, value)
                else:
                    self._invalid[key] = value
            else:
                dict.__setitem__(self, key, value)
        return

    def __delitem__(self, key):
        if key in self:
            dict.__delitem__(self, key)
            archive = self._variable._archive()
            if archive:
                archive.attributes._relinquish(key, self)
        else:
            del self._invalid[key]

    def _invalidate(self, key):
        self._invalid[key] = self[key]
        del self[key]

    def _available(self, key):
        if key in self._invalid:
            self[key] = self._invalid[key]
            del self._invalid[key]

    def notifyDisassociation(self):
        archive = self._variable._archive()
        if archive:
            for key in self.keys():
                archive.attributes._relinquish(key, self)

            for key in self._invalid.keys():
                archive.attributes._relinquish(key, self)

    def notifyAssociation(self):
        archive = self._variable._archive()
        if archive:
            migrate = {}
            for key in self._invalid.keys():
                if archive.attributes._reserve(key, self):
                    migrate[key] = self._invalid[key]
                    del self._invalid[key]

            for key in self.keys():
                if not archive.attributes._reserve(key, self):
                    self._invalid[key] = self[key]
                    del self[key]

            self.update(migrate)

    def read(self):
        archive = self._variable._archive()
        if archive is not None:
            for name in archive.attributes._keys():
                num = archive.attributes._number(name)
                value = vAttribute(variable=self._variable, num=num)._value
                if value is not None:
                    self[name] = value

        return

    def write(self):
        archive = self._variable._archive()
        if archive is not None:
            for key in self.keys():
                value = self[key]
                if isinstance(value, vAttribute):
                    value = value._value
                value = entry.entry(value, simple=True)
                num = archive.attributes._number(key)
                if num is not None:
                    value.write(self._variable._tokens['SELECT_ENTRY'], self._variable._tokens['GET_ENTRY'], num, self._variable._num)

        return


class archiveTable(framework.coerciveDictionary):

    def __init__(self, archive):
        self._archive = weakref.ref(archive)
        self._globalScopeNamesToNumbers = {}
        self._variableScopeNamesToNumbers = {}
        self._variableScopeUsers = {}
        self._variableScopeBlockers = {}
        self._deletionNumbers = set()
        self._creationKeys = set()
        self._variableKeys = set()
        framework.coerciveDictionary.__init__(self)

    def __setitem__(self, key, value, fromDisk=False):
        if key in self._variableScopeUsers:
            for user in self._variableScopeUsers[key]:
                user = user()
                if user is not None:
                    user._invalidate(key)

            del self._variableScopeUsers[key]
        if not fromDisk:
            if key in self and key in self._globalScopeNamesToNumbers:
                self._deletionNumbers.add(self._globalScopeNamesToNumbers[key])
                del self._globalScopeNamesToNumbers[key]
            self._creationKeys.add(key)
        dict.__setitem__(self, key, value)
        return

    def __delitem__(self, key):
        if key in self._creationKeys:
            self._creationKeys.remove(key)
        if key in self._globalScopeNamesToNumbers:
            self._deletionNumbers.add(self._globalScopeNamesToNumbers[key])
            self._globalScopeNamesToNumbers.remove(key)
        dict.__delitem__(self, key)
        if key in self._variableScopeBlockers:
            for user in self._variableScopeBlockers[key]:
                user = user()
                if user is not None:
                    user._available(key)

            self._variableScopeBlockers.remove(key)
        return

    def _keys(self):
        return self._variableScopeNamesToNumbers.keys()

    def _number(self, key):
        if key in self._globalScopeNamesToNumbers:
            return
        elif key not in self._variableScopeNamesToNumbers:
            (num,) = internal.CDFlib(internal.CREATE_, internal.ATTR_, key, internal.VARIABLE_SCOPE)
            self._variableScopeNamesToNumbers[key] = num
        return self._variableScopeNamesToNumbers[key]

    def _reserve(self, key, user):
        if key in self:
            self._variableScopeBlockers.get(key, set()).add(weakref.ref(user))
            return False
        else:
            users = self._variableScopeUsers.get(key, [])
            found = False
            for ref in users[:]:
                deref = ref()
                if deref is None:
                    users.remove(ref)
                elif deref is user:
                    found = True

            if not found:
                users.append(weakref.ref(user))
                self._variableScopeUsers[key] = users
            return True
        return

    def _relinquish(self, key, user):
        users = self._variableScopeUsers.get(key, [])
        for ref in users[:]:
            deref = ref()
            if deref is None:
                users.remove(ref)
            elif deref is user:
                users.remove(user)

        if len(users) == 0:
            self._variableScopeUsers.remove(key)
            if key in self._variableScopeNamesToNumbers:
                self._deletionNumbers.add(self._variableScopeNamesToNumbers[key])
                self._variableScopeNamesToNumbers.remove(key)
        else:
            self._variableScopeUsers[key] = users
        return

    def write(self):
        ordering = list(self._deletionNumbers)
        ordering.sort()
        ordering.reverse()
        for num in ordering:
            internal.CDFlib(internal.SELECT_, internal.ATTR_, num, internal.DELETE_, internal.ATTR_)

        self._deletionNumbers = []
        for key in self._creationKeys:
            value = entry.entry(self[key])
            (attrNum,) = internal.CDFlib(internal.CREATE_, internal.ATTR_, key, internal.GLOBAL_SCOPE)
            if attrNum is not None:
                value.write(internal.gENTRY_, internal.gENTRY_DATA_, attrNum)
                self._globalScopeNamesToNumbers[key] = attrNum

        self._creationKeys = set()
        return

    def read(self):
        (numAttrs,) = internal.CDFlib(internal.GET_, internal.CDF_NUMATTRS_)
        for num in xrange(0, numAttrs):
            internal.CDFlib(internal.SELECT_, internal.ATTR_, num)
            (name, scope) = internal.CDFlib(internal.GET_, internal.ATTR_NAME_, internal.ATTR_SCOPE_)
            if scope == internal.GLOBAL_SCOPE:
                self._globalScopeNamesToNumbers[name] = num
                self.__setitem__(name, gAttribute(archive=self, num=num), True)
            else:
                self._variableScopeNamesToNumbers[name] = num
                self._variableKeys.add(name)