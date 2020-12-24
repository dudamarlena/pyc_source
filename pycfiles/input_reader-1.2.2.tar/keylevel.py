# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Seth/Programming/input_reader/input_reader/keylevel.py
# Compiled at: 2014-03-01 14:21:20
from __future__ import division, print_function, unicode_literals
from .helpers import ReaderError, SUPPRESS
from .py23compat import py23_str, py23_basestring

class _KeyLevel(object):
    """An abstract base class that provides functionality essential
    for a key"""

    def __init__(self, case=False):
        """Init the KeyLevel class"""
        self._case = case
        if not isinstance(case, bool):
            raise ValueError(b'case must be bool, given ' + repr(self._case))

    def _validate_string(self, string):
        """Make sure a string has no spaces"""
        if string is None:
            return
        else:
            if hasattr(string, b'pattern'):
                for s in ('\\s', '.'):
                    if s in string.pattern:
                        msg = b': Regex should not allow the possibility of spaces'
                        msg += b', given "' + string.pattern + b'"'
                        raise ValueError(self.name + msg)

            elif len(string.split()) == 0:
                msg = b': String cannot be of zero length'
                raise ValueError(self.name + msg)
            elif len(string.split()) > 1:
                msg = b': String cannot contain spaces, given "' + string + b'"'
                raise ValueError(self.name + msg)
            return

    def _return_val(self, i, val, namespace):
        """Returns the result properly, depending on the key type
        and how the user wants it."""
        name = self._dest if self._dest is not None else self.name
        if self._repeat:
            if name in namespace:
                return (i, name, getattr(namespace, name) + (val,))
            else:
                return (
                 i, name, (val,))

        elif name in namespace:
            raise ReaderError(self.name + b': The key "' + name + b'" appears twice')
        else:
            return (
             i, name, val)
        return

    def _add_kwargs(self, **kwargs):
        """Generic keyword arguments common to many methods"""
        self._default = getattr(self, b'default', None)
        if self._default is None:
            self._default = kwargs.pop(b'default', None)
        self._repeat = kwargs.pop(b'repeat', False)
        if not isinstance(self._repeat, bool):
            raise ValueError(b'repeat value must be a bool, given ' + repr(self._repeat))
        self._required = kwargs.pop(b'required', False)
        if not isinstance(self._required, bool):
            raise ValueError(b'required value must be a bool, given ' + repr(self._required))
        self._dest = getattr(self, b'dest', None)
        if self._dest is None:
            self._dest = kwargs.pop(b'dest', None)
        if self._dest is not None and not isinstance(self._dest, py23_basestring):
            raise ValueError(b'dest value ' + repr(self._dest) + b' must be a str')
        self._depends = kwargs.pop(b'depends', None)
        if kwargs:
            msg = b': Unknown arguments given: ' + (b',').join(kwargs)
            raise TypeError(self.name + msg)
        return


class BooleanKey(_KeyLevel):
    """A class to store data in a boolean key"""

    def __init__(self, keyname, action, **kwargs):
        """Defines a boolean key."""
        super(BooleanKey, self).__init__()
        self.name = keyname
        self._action = action
        self._add_kwargs(**kwargs)
        self._validate_string(self.name)
        self._validate_string(self._dest)

    def _parse(self, f, i, namespace):
        """Parses the current line for the key.  Returns the line that
        we read from and the value"""
        n = len(f[i].split())
        if n == 1:
            return self._return_val(i, self._action, namespace)
        raise ReaderError(b'The boolean "' + self.name + b'" was given arguments, this is illegal')


class Regex(_KeyLevel):
    """A class to store data from a regex"""

    def __init__(self, handle, regex, **kwargs):
        """Defines a regex searcher."""
        super(Regex, self).__init__()
        self.name = handle
        self._regex = regex
        self._add_kwargs(**kwargs)
        self._validate_string(self.name)
        self._validate_string(self._dest)

    def _parse(self, f, i, namespace):
        """Parses the current line for the regex.  Returns the match objext
        for the line."""
        val = self._regex.match(f[i])
        return self._return_val(i, val, namespace)


class LineKey(_KeyLevel):
    """A class to store data on a line key"""

    def __init__(self, keyname, type, glob, keywords, case, **kwargs):
        """Defines a line key."""
        super(LineKey, self).__init__(case=case)
        self.name = keyname
        self._add_kwargs(**kwargs)
        self._validate_string(self.name)
        self._validate_string(self._dest)
        if glob and keywords:
            msg = b': Cannot define both glob and keywords'
            raise TypeError(self.name + msg)
        if isinstance(type, list):
            self._type = type
            self._nolist = False
        elif type is None:
            self._type = []
            self._nolist = False
        else:
            self._type = [
             type]
            self._nolist = True
        self._check_types_in_list(self._type)
        if glob:
            if not isinstance(glob, dict):
                raise ValueError(self.name + b': glob must be a dict')
            if b'len' not in glob:
                raise ValueError(self.name + b': "len" required for glob')
            elif glob[b'len'] not in ('*', '+', '?'):
                msg = b': "len" must be one of "*", "+", or "?" in glob'
                raise ValueError(self.name + msg)
            if b'type' not in glob:
                glob[b'type'] = str
            if isinstance(glob[b'type'], list):
                msg = b': list not allowed in type for glob or keywords'
                raise ValueError(self.name + msg)
            self._check_types_in_list([glob[b'type']])
            if b'join' not in glob:
                glob[b'join'] = False
            if glob[b'join'] and glob[b'len'] == b'?':
                msg = b': "join=True" makes no sense for "len=?"'
                raise ValueError(self.name + msg)
            if set(glob.keys()) != set([b'len', b'type', b'join']):
                if set(glob.keys()) != set([b'len', b'type', b'join', b'default']):
                    raise TypeError(self.name + b': Unknown key in glob')
            if not isinstance(glob[b'join'], bool):
                raise ValueError(self.name + b': "join" must be a bool in glob')
            if not self._type and (glob[b'join'] or glob[b'len'] == b'?'):
                self._nolist = True
            else:
                self._nolist = False
            self._glob = glob
        else:
            self._glob = {}
        if keywords:
            if not isinstance(keywords, dict):
                raise ValueError(self.name + b': keywords must be a dict')
            for key in keywords:
                if not isinstance(key, py23_basestring):
                    msg = b': keys in keywords must be of type str'
                    raise ValueError(self.name + msg)
                else:
                    self._validate_string(key)
                if keywords[key] is None:
                    keywords[key] = {}
                elif not isinstance(keywords[key], dict):
                    msg = b': Options for keyword "' + key + b'" must be a dict'
                    raise ValueError(self.name + msg)
                if b'default' not in keywords[key]:
                    keywords[key][b'default'] = SUPPRESS
                if b'type' not in keywords[key]:
                    keywords[key][b'type'] = str
                if set(keywords[key].keys()) != set([b'default', b'type']):
                    msg = b': Unknown key in keyword: "' + key + b'"'
                    raise TypeError(self.name + msg)
                if isinstance(keywords[key][b'type'], list):
                    msg = b': list not allowed in type for glob or keywords'
                    raise ValueError(self.name + msg)
                else:
                    self._check_types_in_list([keywords[key][b'type']])

            self._keywords = keywords
            if not self._type:
                self._nolist = True if 1 else False
            else:
                self._keywords = {}
            msg = self._type or self._glob or self._keywords or b': type, glob and keywords cannot all be empty'
            raise ValueError(self.name + msg)
        return

    def _parse(self, f, i, namespace):
        """Parses the current line for the key.  Returns the line that
        we read from and the value"""
        if self._case:
            args = f[i].split()[1:]
        else:
            args = f[i].lower().split()[1:]
        if len(args) == len(self._type):
            if not self._glob and not self._keywords:
                pass
            elif self._glob.get(b'len') == b'+':
                msg = b': expected at least ' + str(len(self._type) + 1)
                msg += b' arguments, got ' + str(len(args))
                raise ReaderError(self.name + msg)
        else:
            if len(args) < len(self._type):
                if self._glob.get(b'len') == b'+':
                    msg = b': expected at least ' + str(len(self._type) + 1)
                else:
                    msg = b': expected ' + str(len(self._type))
                msg += b' arguments, got ' + str(len(args))
                raise ReaderError(self.name + msg)
            else:
                if len(args) > len(self._type):
                    if self._keywords:
                        pass
                    elif self._glob and self._glob[b'len'] in ('*', '+'):
                        pass
                    else:
                        n = len(self._type)
                        if self._glob.get(b'len') == b'?':
                            n += 1
                            msg = b': expected at most ' + str(n)
                        else:
                            msg = b': expected ' + str(n)
                        if len(args) != n:
                            msg += b' arguments, got ' + str(len(args))
                            raise ReaderError(self.name + msg)
                val = []
                for a, t in zip(args[:len(self._type)], self._type):
                    val.append(self._check_type_of_value(a, t, self._case))

            try:
                args = args[len(self._type):]
            except IndexError:
                args = []

        glob = []
        kw = {}
        if self._glob:
            t = self._glob[b'type']
            for a in args:
                glob.append(self._check_type_of_value(a, t, self._case))

            if self._glob[b'join']:
                if not glob:
                    try:
                        glob = self._glob[b'default']
                    except KeyError:
                        pass

                else:
                    for j, v in enumerate(glob):
                        glob[j] = py23_str(v)

                    glob = (b' ').join(glob)
            elif not glob:
                try:
                    glob.append(self._glob[b'default'])
                except KeyError:
                    pass

            if not val:
                if self._nolist:
                    if isinstance(glob, py23_basestring):
                        val = glob
                    else:
                        try:
                            val = glob[0]
                        except IndexError:
                            val = b''

                else:
                    val = tuple(glob)
            elif not glob:
                if self._nolist:
                    val = val[0]
                else:
                    val = tuple(val)
            elif self._glob[b'join']:
                val.append(glob)
                val = tuple(val)
            else:
                val.extend(glob)
                val = tuple(val)
        elif self._keywords:
            for kvpair in args:
                try:
                    key, value = kvpair.split(b'=')
                except ValueError:
                    msg = b': Error reading keyword argument "' + kvpair + b'"'
                    raise ReaderError(self.name + msg)

                if not self._case:
                    key = key.lower()
                if key not in self._keywords:
                    raise ReaderError(self.name + b': Unknown keyword: "' + key + b'"')
                try:
                    t = self._keywords[key][b'type']
                except KeyError:
                    t = str

                kw[key] = self._check_type_of_value(value, t, self._case)

            for key in self._keywords:
                try:
                    default = self._keywords[key][b'default']
                except KeyError:
                    continue

                if key not in kw and default is not SUPPRESS:
                    kw[key] = default

            if not val:
                val = kw
            elif not kw:
                if self._nolist:
                    val = val[0]
                else:
                    val.append({})
                    val = tuple(val)
            else:
                val.append(kw)
                val = tuple(val)
        elif self._nolist:
            try:
                val = val[0]
            except IndexError:
                val = b''

        else:
            val = tuple(val)
        return self._return_val(i, val, namespace)

    def _check_types_in_list(self, typ):
        """Make sure each type in a list is legal.  The function is recursive"""
        for t in typ:
            if isinstance(t, list):
                msg = b': Embedded lists not allowed in type'
                raise ValueError(self.name + msg)
            elif isinstance(t, tuple):
                if len(t) == 0:
                    msg = b': Empty tuple in type'
                    raise ValueError(self.name + msg)
                else:
                    self._check_types_in_list(t)
            elif not (isinstance(t, py23_basestring) or isinstance(t, int) or isinstance(t, float) or t is None or hasattr(t, b'pattern') or t is str or t is int or t is float):
                msg = b': type must be one of None, str, float int, or an instance of str, float, int or regex'
                raise ValueError(self.name + msg)
            if isinstance(t, py23_basestring) or hasattr(t, b'pattern'):
                self._validate_string(t)

        return

    def _validate_given_value(self, val, typ, case):
        """Checks that the given value is valid by checking
        its type. Raises ValueError if unsuccessful.
        """
        if not case:
            try:
                typ = type.lower()
            except AttributeError:
                pass

        if typ is float or typ is int or typ is str:
            return typ(val)
        else:
            if typ is None:
                if val.lower() == b'none':
                    return
                raise ValueError
            elif isinstance(typ, py23_basestring) or isinstance(typ, int) or isinstance(typ, float):
                if type(typ)(val) == typ:
                    return type(typ)(val)
                raise ValueError
            else:
                if typ.match(val):
                    return val
                raise ValueError
            return

    def _check_type_of_value(self, val, typ, case):
        """Checks the type of a value, accounting for
        various forms of type"""
        if isinstance(typ, tuple):
            for tp in typ:
                try:
                    return self._validate_given_value(val, tp, case)
                except ValueError:
                    continue

            else:
                msg = self.name + b': expected one of {0}, got "{1}"'
                t = sorted([ self._make_value_readable(x) for x in typ ])
                t = (b', ').join(t[:-1]) + b' or ' + t[(-1)]
                raise ReaderError(msg.format(t, val))

        else:
            try:
                return self._validate_given_value(val, typ, case)
            except ValueError:
                msg = self.name + b': expected {0}, got "{1}"'
                raise ReaderError(msg.format(self._make_value_readable(typ), val))

    def _make_value_readable(self, val):
        """Returns a a string version of the input value."""
        if isinstance(val, int) or isinstance(val, float):
            return str(val)
        else:
            if isinstance(val, py23_basestring):
                return b'"' + str(val) + b'"'
            if val is None:
                return b'"None"'
            try:
                return (b'regex({0})').format(val.pattern)
            except AttributeError:
                return str(val).split()[1].strip(b"'><")

            return