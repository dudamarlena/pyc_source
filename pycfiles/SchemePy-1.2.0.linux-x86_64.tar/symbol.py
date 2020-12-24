# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/symbol.py
# Compiled at: 2015-09-07 19:23:32
from scheme import debug
from scheme.Globals import Globals
import re

class Symbol(unicode):
    line = 0

    def setLine(self, line):
        self.line = line
        return self

    def toObject(self, env):
        if hasattr(self, 'cache'):
            ret = self.cache
            del self.cache
            return ret
        else:
            if len(self) > 0:
                if self[0] == self[(-1)] == '"':
                    return self[1:-1]
            if '.' in self and not self.replace('-', '').replace('.', '').replace('e', '').isdigit() and 'lambda:' not in self and '.' != self:
                lst = self.split('.')
                val = Symbol(lst[0]).toObject(env)
                for i in lst[1:]:
                    val = Symbol('getattr').toObject(env)(val, i)

                return val
            if '[' in self:
                m = re.match('^(.+?)\\[(.+?)\\]$', self)
                if m is not None:
                    obj, key = m.groups()
                    val = Symbol('getitem').toObject(env)(Symbol(obj).toObject(env), Symbol(key).toObject(env))
                    return val
            while env is not None:
                if unicode(self) in env:
                    return env[self]
                if hasattr(env, 'parent'):
                    env = env.parent
                else:
                    env = None

            if self.lstrip('-').isdigit():
                return int(self)
            if self.replace('-', '').replace('.', '').replace('e', '').isdigit() and not self.startswith('e'):
                return float(self)
            if self == '#t':
                return True
            if self == '#f':
                return False
            try:
                return complex(self.replace('i', 'j', 1))
            except:
                raise NameError("Symbol '%s' undefined" % self)

            return

    def isBound(self, env, cache=True):
        try:
            if self.lstrip('-').isdigit():
                return True
            else:
                if self.replace('-', '').replace('.', '').replace('e', '').isdigit() and not self.startswith('e'):
                    return True
                if self == '#t':
                    return True
                if self == '#f':
                    return True
                try:
                    complex(self.replace('i', 'j', 1))
                    return True
                except ValueError:
                    pass

                if cache:
                    self.cache = self.toObject(env)
                return True

        except NameError:
            return False
        except AttributeError:
            return False

    def getEnv(self, env):
        while env is not None:
            if unicode(self) in env:
                return env
            env = env.parent

        if self.lstrip('-').isdigit() or self.lstrip('-').replace('.', '').isdigit() or self[0] == self[(-1)] == '"' or self == '#t' or self == '#f':
            return Globals
        raise NameError("Symbol '%s' undefined in enclosing environments" % self)
        return

    def __repr__(self):
        if debug.getDebug('symbols'):
            return '<Symbol %s (line %i)>' % (self, self.line)
        return str(self)

    def __bool__(self):
        if self.isBound(None):
            return bool(self.toObject(Globals))
        else:
            return True

    def __eq__(self, other):
        if not isinstance(other, (unicode, str)) and self.isBound(Globals, True):
            return self.toObject(Globals) == other
        return unicode.__eq__(self, other)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return self.toObject(Globals) + other.toObject(Globals)
        else:
            if self.isBound(None):
                return self.toObject(None) + other
            return str(self) + other