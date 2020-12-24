# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-tutelary/tutelary/engine.py
# Compiled at: 2017-12-04 06:48:57
# Size of source mod 2**32: 11559 bytes
import re
from json import loads, dumps, JSONDecodeError
from string import Template
import hashlib
from collections import Sequence
from .wildtree import WildTree
from .exceptions import EffectException, PatternOverlapException, PolicyBodyException, VariableSubstitutionException

class SimpleSeparated(Sequence):
    __doc__ = 'Simple sequences of strings delimited by a separator, with\n    wildcarding.\n\n    A wildcard component is represented by a ``*`` string and matches\n    any single string component.  Equality comparison between\n    sequences is exact comparison of components; matching between\n    wildcarded components can be tested using the ``match`` method.\n\n    '

    def __init__(self, s):
        if s is None:
            self.components = []
        else:
            if isinstance(s, str):
                self.components = self._split_components(s)
            else:
                if isinstance(s, Sequence):
                    self.components = s
                else:
                    raise ValueError('invalid initialiser for separated sequence')

    def _split_components(self, s):
        return s.split(self.separator)

    def __len__(self):
        return len(self.components)

    def __getitem__(self, idx):
        return self.components[idx]

    def __str__(self):
        return self.separator.join(self.components)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, str(self))

    def __eq__(self, other):
        return self.components == other.components

    def __hash__(self):
        return hash(str(self))

    def match(self, other):
        if len(self) != len(other):
            return False
        for cself, cother in zip(self.components, other.components):
            if not (cself == cother or cself == '*' or cother == '*'):
                return False

        return True


class EscapeSeparated(SimpleSeparated):
    __doc__ = 'Sequences of strings delimited by a separator that can be\n    backslash-escaped.  Backslashes can also be backslash-escaped; no\n    other escaping mechanism is supported.\n\n    '

    def _split_components(self, s):
        if not hasattr(self, 'regex'):
            type(self).regex = make_regex(self.separator)
        components = self.regex.split(s)[1::2]
        components = [unescape(s, self.separator) for s in components]
        return components

    def __str__(self):
        return self.separator.join([escape(s, self.separator) for s in self.components])


class Action(SimpleSeparated):
    __doc__ = 'Actions are represented by period-separated sequences of elements\n    (e.g. ``parcel.edit``, ``admin.assign-role``) with wildcard\n    elements indicated by ``*`` (e.g. ``party.*``).  A list of\n    *registered* actions is maintained to support permissions set\n    queries to find the set of actions that are permitted on a\n    specified object pattern.\n\n    '
    separator = '.'
    registered = set()

    def register(action):
        """Action registration is used to support generating lists of
        permitted actions from a permission set and an object pattern.
        Only registered actions will be returned by such queries.

        """
        if isinstance(action, str):
            Action.register(Action(action))
        else:
            if isinstance(action, Action):
                Action.registered.add(action)
            else:
                for a in action:
                    Action.register(a)


class Object(EscapeSeparated):
    __doc__ = 'Objects are represented by slash-separated sequences of elements\n    (e.g. ``Cadasta/Batangas/parcel/123``, ``H4H/PaP/party/118``) with\n    wildcard elements indicated by ``*``\n    (e.g. ``Cadasta/*/parcel/*``).  Slashes can be backslash-escaped,\n    as can backslashes (e.g. ``Cadasta/Village-X\\/Y/parcel/943``).\n\n    '
    separator = '/'


class Clause:
    __doc__ = 'A clause is a simple container for an effect ("allow" or "deny")\n    and a list of non-overlapping action patterns and non-overlapping\n    object patterns to which the effect applies.  (The patterns must\n    be non-overlapping because there is no ordering imposed between\n    the different action/object combinations within a clause.\n    Overlapping patterns are thus potentially ambiguous.)\n\n    '

    def __init__(self, effect=None, act=None, obj=None, dict=None):
        """A clause can be created either by giving explicit lists of
        ``Action`` and ``Object`` objects or by giving a dictionary
        with ``effect``, ``action`` and ``object`` keys pulled out of
        the JSON representation of a policy.

        """
        if dict is not None:
            effect = dict['effect']
            if isinstance(dict['action'], str):
                act = [
                 Action(dict['action'])]
            else:
                act = [Action(a) for a in dict['action']]
            obj = [Object(o) for o in dict['object']] if 'object' in dict else []
        if effect not in ('allow', 'deny'):
            raise EffectException(effect)
        if any(a1.match(a2) for a1 in act for a2 in act):
            raise PatternOverlapException('action')
        if any(o1.match(o2) for o1 in obj for o2 in obj):
            raise PatternOverlapException('object')
        self.effect = effect
        self.action = act
        self.object = obj


class PolicyBody(Sequence):
    __doc__ = 'A policy body is just a sequence of clauses, possibly with a name.\n    Conversion to and from JSON representations (with\n    canonicalisation), and hash generation from the canonical\n    representation.\n\n    Can be composed into permission sets, so for convenience allow for\n    iteration over individual (action, object) pairs (note that each\n    clause can have multiple actions and objects).\n\n    '

    def __init__(self, json, variables=None):
        try:
            d = loads(strip_comments(Template(json).substitute(variables)))
        except JSONDecodeError as e:
            raise PolicyBodyException(lineno=e.lineno, colno=e.colno)
        except (KeyError, TypeError, ValueError):
            raise VariableSubstitutionException()

        self.version = 'version' in d and d['version'] or '2015-12-10'
        if 'clause' not in d:
            raise PolicyBodyException(msg='no policy clauses')
        self.clauses = d['clause']
        self.clauses = [Clause(dict=c) for c in self.clauses]
        self.nitems = sum([len(c.action) * len(c.object) for c in self.clauses])
        self.nclauses = len(self.clauses)
        if self.version not in ('2015-12-10', ):
            raise PolicyBodyException(msg='version not recognised')

    def __len__(self):
        return self.nitems

    def __getitem__(self, idx):
        return self.clauses[idx]

    def __str__(self):

        def one_clause(c):
            return {'effect': c.effect, 
             'action': [str(a) for a in c.action], 
             'object': [str(o) for o in c.object]}

        cs = [one_clause(c) for c in self.clauses]
        return dumps({'version': self.version, 'clause': cs})

    def __iter__(self):
        for c in self.clauses:
            e = c.effect
            for a in c.action:
                if len(c.object) == 0:
                    yield (
                     e, a, None)
                else:
                    for o in c.object:
                        yield (
                         e, a, o)

    def hash(self):
        return hashlib.md5(str(self).encode()).hexdigest()


class PermissionTree:
    __doc__ = 'A permission tree records, in a compact way, the permissions\n    associated with a sequence of policy clauses.  The construction of\n    permission trees handles the overriding of earlier clauses by later\n    clauses and the treatment of wildcards in the action and object\n    patterns for individual policy clauses.\n\n    Can:\n     - Create empty permissions trees.\n     - Compose statements and policies into a permission tree.\n     - Test an (action, object) pair against a permission tree.\n     - Determine the list of allowed actions for an object pattern from\n       a permission tree.\n\n    Most of the functionality needed here is implemented in the\n    ``WildTree`` class.\n\n    '

    def __init__(self, policies=None, json=None):
        """Permission trees are all by default empty, with an optional list of
        policies added.  They can also be deserialised from JSON.

        """
        self.tree = WildTree(json)
        if policies is not None:
            self.add(policies=policies)

    def __repr__(self):
        return '{}(\n{}\n)'.format(self.__class__.__name__, '  ' + str(self.tree).replace('\n', '\n  '))

    def add(self, effect=None, act=None, obj=None, policy=None, policies=None):
        """Insert an individual (effect, action, object) triple or all
        triples for a policy or list of policies.

        """
        if policies is not None:
            for p in policies:
                self.add(policy=p)

        else:
            if policy is not None:
                for e, a, o in policy:
                    self.add(e, a, o)

            else:
                objc = obj.components if obj is not None else []
                self.tree[act.components + objc] = effect

    def allow(self, act, obj=None):
        """Determine where a given action on a given object is allowed.

        """
        objc = obj.components if obj is not None else []
        try:
            return self.tree[(act.components + objc)] == 'allow'
        except KeyError:
            return False

    def permitted_actions(self, obj=None):
        """Determine permitted actions for a given object pattern.

        """
        return [a for a in Action.registered if self.allow(a, obj(str(a)) if obj is not None else None)]


def make_regex(separator):
    """Utility function to create regexp for matching escaped separators
    in strings.

    """
    return re.compile('(?:' + re.escape(separator) + ')?((?:[^' + re.escape(separator) + '\\\\]|\\\\.)+)')


def unescape(s, sep):
    """Unescape escaped separators and backslashes in strings.

    """
    return s.replace('\\' + sep, sep).replace('\\\\', '\\')


def escape(s, sep):
    """Escape unescapes separators and backslashes in strings.

    """
    return s.replace('\\', '\\\\').replace(sep, '\\' + sep)


def strip_comments(text):
    """Comment stripper for JSON.

    """
    regex = '\\s*(#|\\/{2}).*$'
    regex_inline = '(:?(?:\\s)*([A-Za-z\\d\\.{}]*)|((?<=\\").*\\"),?)(?:\\s)*(((#|(\\/{2})).*)|)$'
    lines = text.split('\n')
    for index, line in enumerate(lines):
        if re.search(regex, line):
            if re.search('^' + regex, line, re.IGNORECASE):
                lines[index] = ''
            elif re.search(regex_inline, line):
                lines[index] = re.sub(regex_inline, '\\1', line)

    return '\n'.join(lines)