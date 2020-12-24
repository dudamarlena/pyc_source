# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\utils\ciDict.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
try:
    from collections.abc import MutableMapping, Mapping
except ImportError:
    from collections import MutableMapping, Mapping

from .. import SEQUENCE_TYPES

class CaseInsensitiveDict(MutableMapping):

    def __init__(self, other=None, **kwargs):
        self._store = dict()
        self._case_insensitive_keymap = dict()
        if other or kwargs:
            if other is None:
                other = dict()
            self.update(other, **kwargs)
        return

    def __contains__(self, item):
        try:
            self.__getitem__(item)
            return True
        except KeyError:
            return False

    @staticmethod
    def _ci_key(key):
        if hasattr(key, 'lower'):
            return key.strip().lower()
        return key

    def __delitem__(self, key):
        ci_key = self._ci_key(key)
        del self._store[self._case_insensitive_keymap[ci_key]]
        del self._case_insensitive_keymap[ci_key]

    def __setitem__(self, key, item):
        ci_key = self._ci_key(key)
        if ci_key in self._case_insensitive_keymap:
            self._store[self._case_insensitive_keymap[ci_key]] = item
        else:
            self._store[key] = item
            self._case_insensitive_keymap[ci_key] = key

    def __getitem__(self, key):
        return self._store[self._case_insensitive_keymap[self._ci_key(key)]]

    def __iter__(self):
        return self._store.__iter__()

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return repr(self._store)

    def __str__(self):
        return str(self._store)

    def keys(self):
        return self._store.keys()

    def values(self):
        return self._store.values()

    def items(self):
        return self._store.items()

    def __eq__(self, other):
        if not isinstance(other, (Mapping, dict)):
            return NotImplemented
        if isinstance(other, CaseInsensitiveDict):
            if len(self.items()) != len(other.items()):
                return False
            else:
                for (key, value) in self.items():
                    if not (key in other and other[key] == value):
                        return False

                return True
        return self == CaseInsensitiveDict(other)

    def copy(self):
        return CaseInsensitiveDict(self._store)


class CaseInsensitiveWithAliasDict(CaseInsensitiveDict):

    def __init__(self, other=None, **kwargs):
        self._aliases = dict()
        self._alias_keymap = dict()
        CaseInsensitiveDict.__init__(self, other, **kwargs)

    def aliases(self):
        return self._aliases.keys()

    def __setitem__(self, key, value):
        if isinstance(key, SEQUENCE_TYPES):
            ci_key = self._ci_key(key[0])
            if ci_key not in self._aliases:
                CaseInsensitiveDict.__setitem__(self, key[0], value)
                self.set_alias(ci_key, key[1:])
            else:
                raise KeyError("'" + str(key[0] + ' already used as alias'))
        else:
            ci_key = self._ci_key(key)
            if ci_key not in self._aliases:
                CaseInsensitiveDict.__setitem__(self, key, value)
            else:
                self[self._aliases[ci_key]] = value

    def __delitem__(self, key):
        ci_key = self._ci_key(key)
        try:
            CaseInsensitiveDict.__delitem__(self, ci_key)
            if ci_key in self._alias_keymap:
                for alias in self._alias_keymap[ci_key][:]:
                    self.remove_alias(alias)

            return
        except KeyError:
            if ci_key in self._aliases:
                self.remove_alias(ci_key)

    def set_alias(self, key, alias, ignore_duplicates=False):
        if not isinstance(alias, SEQUENCE_TYPES):
            alias = [
             alias]
        for alias_to_add in alias:
            ci_key = self._ci_key(key)
            if ci_key in self._case_insensitive_keymap:
                ci_alias = self._ci_key(alias_to_add)
                if ci_alias not in self._case_insensitive_keymap:
                    if ci_alias not in self._aliases:
                        self._aliases[ci_alias] = ci_key
                        if ci_key in self._alias_keymap:
                            self._alias_keymap[ci_key].append(self._ci_key(ci_alias))
                        else:
                            self._alias_keymap[ci_key] = list()
                            self._alias_keymap[ci_key].append(self._ci_key(ci_alias))
                    elif ci_key in self._alias_keymap and ci_alias in self._alias_keymap[ci_key]:
                        pass
                    elif not ignore_duplicates:
                        raise KeyError("'" + str(alias_to_add) + "' already used as alias")
                elif ci_key == self._ci_key(self._case_insensitive_keymap[ci_alias]):
                    pass
                elif not ignore_duplicates:
                    raise KeyError("'" + str(alias_to_add) + "' already used as key")
            else:
                for keymap in self._alias_keymap:
                    if ci_key in self._alias_keymap[keymap]:
                        self.set_alias(keymap, alias + [ci_key], ignore_duplicates=ignore_duplicates)
                        break
                else:
                    raise KeyError("'" + str(ci_key) + "' is not an existing alias or key")

    def remove_alias(self, alias):
        if not isinstance(alias, SEQUENCE_TYPES):
            alias = [
             alias]
        for alias_to_remove in alias:
            ci_alias = self._ci_key(alias_to_remove)
            self._alias_keymap[self._aliases[ci_alias]].remove(ci_alias)
            if not self._alias_keymap[self._aliases[ci_alias]]:
                del self._alias_keymap[self._aliases[ci_alias]]
            del self._aliases[ci_alias]

    def __getitem__(self, key):
        try:
            return CaseInsensitiveDict.__getitem__(self, key)
        except KeyError:
            return CaseInsensitiveDict.__getitem__(self, self._aliases[self._ci_key(key)])

    def copy(self):
        new = CaseInsensitiveWithAliasDict(self._store)
        new._aliases = self._aliases.copy()
        new._alias_keymap = self._alias_keymap
        return new