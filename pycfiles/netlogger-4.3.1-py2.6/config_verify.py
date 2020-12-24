# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/config_verify.py
# Compiled at: 2009-12-08 17:43:30
"""
Verify a configuration file against a 'specification'
which is itself a configuration file.

To handle cases where one form or another of a config file
is allowed, multiple specifications can be evaluated and
failure reported only if none match.
"""
__rcsid__ = '$Id: config_verify.py 23923 2009-09-18 22:42:26Z ksb $'
import logging, os, re
from netlogger import configobj
from netlogger.nllog import DoesLogging
from netlogger import nlapi
from netlogger import util

class ValidationError(Exception):
    """Base class for all errors raised when validating an
    input file against a (valid) specification.
    """

    def __init__(self, msg, key, path):
        self.msg, self.key, self.path = msg, key, path
        if path == '':
            Exception.__init__(self, msg + " '%s' at top level" % key)
        else:
            Exception.__init__(self, msg + " '%s' in %s" % (key, path))


class UnknownKeyError(ValidationError):

    def __init__(self, key, path):
        ValidationError.__init__(self, 'Unrecognized keyword', key, path)


class UnknownSectionError(ValidationError):

    def __init__(self, key, path):
        ValidationError.__init__(self, 'Unrecognized section', key, path)


class MissingKeyError(ValidationError):

    def __init__(self, key, path):
        ValidationError.__init__(self, 'Missing required keyword', key, path)


class MissingSectionError(ValidationError):

    def __init__(self, key, path):
        ValidationError.__init__(self, 'Missing required section', key, path)


class BadValueError(ValidationError):

    def __init__(self, key, path, type, value):
        ValidationError.__init__(self, "Value '%s' does not match type '%s' for key" % (
         value, type), key, path)


class SpecificationFileError(Exception):
    """Base class of exceptions raised when parsing a specification.
    """

    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, 'Invalid specification: %s' % msg)


class SpecificationSyntaxError(SpecificationFileError):
    pass


class InvalidSpecificationCommand(SpecificationFileError):
    pass


class InvalidSpecification(SpecificationFileError):
    pass


class UnknownRuleError(SpecificationFileError):

    def __init__(self, name):
        msg = "Cannot apply rule '%s': Rule not found" % name
        SpecificationFileError.__init__(self, msg)
        self.rule_name = name


def _check_path(value):
    """Check that input value is a valid file path.
    Raise ValueError if it's not.
    """
    return value


def _check_uri(value):
    """Check that input value is a valid URI.
    Raise ValueError if it's not.
    """
    m = re.match('(?P<scheme>[\\w-]+):///?(?P<netloc>[^/]+)', value)
    if m is None:
        raise ValueError('Invalid URI')
    return value


def _check_enum(value, domain):
    """Check that input value is a valid enumeration.
    Raise ValueError if it's not.
    """
    if value not in domain:
        raise ValueError("Enumeration value '%s' not in %s" % (
         value, domain))
    return value


def _check_interval(value):
    """Check that input value is a valid time interval like "10 seconds".
    Raise ValueError if it's not.
    """
    try:
        sec = util.timeToSec(value)
    except ValueError, E:
        raise ValueError("Value '%s' is not a valid time interval" % value)

    return value


class Specification(DoesLogging):
    """Validate input against a simple
    'specification', both of which are ConfigObj instances
    or simply nested dictionaries.

    The specification lists all valid sections and
    valid keywords of each section. The validate() method
    raises an exception if the input has a section or section/kewyord
    combination that's not in the specification.

    However, wildcard sections and keywords are allowed.
    """
    ANY_KW = '__ANY__'
    ANY_SEC = '*'
    REQ_PFX = 'required_'
    TYPE_CONVERT = {'str': lambda x: True, 
       'string': lambda x: True, 
       'int': int, 
       'float': float, 
       'bool': util.as_bool, 
       'path': _check_path, 
       'uri': _check_uri, 
       'enum': _check_enum, 
       'interval': _check_interval}

    def __init__(self, source):
        DoesLogging.__init__(self)
        self._cfg = configobj.ConfigObj(source)

    def validate(self, cfg):
        self._walk(cfg, self._cfg)

    def _is_section(self, val):
        return isinstance(val, dict)

    def _walk(self, input, spec, depth=0, path=''):
        any_kw, any_sec = False, False
        if spec.has_key(self.ANY_KW):
            any_kw = True
        elif spec.has_key(self.ANY_SEC):
            any_sec = True
        required = {}
        for key in spec.keys():
            if key.startswith(self.REQ_PFX):
                barekey = key[len(self.REQ_PFX):]
                required[barekey] = True
                spec[barekey] = spec[key]
                del spec[key]
            else:
                required[key] = False

        for (key, value) in spec.items():
            if required[key]:
                if not input.has_key(key):
                    if self._is_section(spec[key]):
                        raise MissingSectionError(key, path)
                    else:
                        raise MissingKeyError(key, path)

        for key in input.keys():
            self.log.debug('validate.key.start', key=key)
            is_section = self._is_section(input[key])
            if is_section and any_sec or not is_section and any_kw:
                self.log.debug('validate.key.end', key=key, status=0, msg='wildcard')
                continue
            if depth == 0:
                if not is_section:
                    self.log.debug('validate.key.end', key=key, status=0, msg='top-level variable')
                    continue
                if not spec.has_key(key):
                    self.log.debug('validate.key.end', key=key, status=1, msg='unknown')
                    if is_section:
                        raise UnknownSectionError(key, path)
                    else:
                        raise UnknownKeyError(key, path)
                section_mismatch = self._is_section(spec[key]) != is_section
                if section_mismatch:
                    if is_section:
                        self.log.debug('validate.key.end', key=key, status=2, msg='keyword found, section expected')
                        raise UnknownSectionError(key, path)
                    else:
                        self.log.debug('validate.key.end', key=key, status=3, msg='section found, keyword expected')
                        raise UnknownKeyError(key, path)
                if not is_section:
                    expected_type = spec[key] or 'str'
                else:
                    expected_type = spec[key].lower().split(None, 1)[0]
                if self.TYPE_CONVERT.has_key(expected_type):
                    value = input[key]
                    try:
                        if expected_type == 'enum':
                            domain = spec[key].split()[1:]
                            self.TYPE_CONVERT[expected_type](value, domain)
                        else:
                            self.TYPE_CONVERT[expected_type](value)
                    except ValueError, E:
                        self.log.debug('validate.key.end', key=key, status=4, msg=E, type=expected_type, value=value)
                        type_name = spec[key]
                        raise BadValueError(key, path, type_name, value)

                else:
                    self.log.warn('validate.key.unknownType', key=key, type=expected_type, msg='skipped')
            self.log.debug('validate.key.end', key=key, status=0, msg='OK')

        walked_any = False
        for (key, val) in input.items():
            if self._is_section(val):
                component = '[' * (depth + 1) + key + ']' * (depth + 1)
                if path == '':
                    ppath = component
                else:
                    ppath = path + ':' + component
                if not spec.has_key(key):
                    if walked_any:
                        continue
                    else:
                        section = spec[self.ANY_SEC]
                        walked_any = True
                else:
                    section = spec[key]
                self._walk(val, section, depth=depth + 1, path=ppath)

        return


class SpecificationFile(DoesLogging):
    """List of specifications and rules to combine them.
    Syntax is:
    %spec NAME1
    ..specification (config file)..
    %spec NAME2
    ..another specification (config file)..
    %rule RULE1 %NAME1 or %NAME2 # expression
    # order to apply rules
    %apply RULE1
    """
    (BETWEEN, IN_SPEC) = (0, 1)
    SPEC_RE = re.compile('%spec\\s+(\\w+)')
    RULE_RE = re.compile('%rule\\s+(\\w+)\\s+(\\S+)')
    APPLY_RE = re.compile('%apply\\s+(any|all)(.*)')

    def __init__(self, path):
        DoesLogging.__init__(self)
        self._specs = {}
        f = file(path)
        (rules, rule_groups) = self._parseFile(f)
        rule_exprs = self._buildRuleExprs(rules)
        self._apply = self._buildApply(rules, rule_exprs, rule_groups)

    def _parseFile(self, fileobj):
        """Parse specification file into a dictionary of named
        rules and a list of ruleGroups that execute one or
        more rules.
        Returns (rules, rule_groups).
        """
        self.log.debug('parsefile.start')
        rule_groups = []
        rules = {}
        state = self.BETWEEN
        cur_spec = None
        cur_spec_contents = []
        for line in fileobj:
            lstrip = line.strip()
            if lstrip.startswith('%'):
                if state == self.IN_SPEC:
                    try:
                        spec = Specification(cur_spec_contents)
                    except configobj.ConfigObjError, E:
                        raise SpecificationSyntaxError(E)
                    else:
                        self._specs[cur_spec] = spec
                        state = self.BETWEEN
                if len(lstrip) == 1:
                    raise InvalidSpecificationCommand('Empty command')
                if self.SPEC_RE.match(lstrip):
                    state = self.IN_SPEC
                    cur_spec = self.SPEC_RE.match(lstrip).group(1)
                    cur_spec_contents = []
                elif self.RULE_RE.match(lstrip):
                    m = self.RULE_RE.match(lstrip)
                    rules[m.group(1)] = m.group(2)
                elif self.APPLY_RE.match(lstrip):
                    m = self.APPLY_RE.match(lstrip)
                    is_any = m.group(1) == 'any'
                    rule_list = m.group(2)
                    rule_groups.append((rule_list, is_any))
                else:
                    raise InvalidSpecificationCommand('Unknown command: %s' % lstrip)
            elif state == self.IN_SPEC:
                cur_spec_contents.append(line)

        self.log.debug('parsefile.end', status=0, nrules=len(rules), nrulegroups=len(rule_groups))
        return (rules, rule_groups)

    def _buildRuleExprs(self, rules):
        """Build an expression for each rule.

        Returns a dictionary of expressions with the same keys
        as the input dictionary of rules.
        """
        rule_expr = {}
        for rk in rules.keys():
            rule = rules[rk]
            for sk in self._specs.keys():
                ref = "self._specs['%s'].validate(obj)" % sk
                rule = re.sub('%%%s' % sk, ref, rule)

            rule_expr[rk] = rule

        return rule_expr

    def _buildApply(self, rules, rule_expr, rule_groups):
        """Match rule names in the rule_groups to rule expressions
        in rule_expr, and concatenate them to make a list
        of rule expressions to apply.
        """
        result = []
        pos = 1
        for (rule_list, is_any) in rule_groups:
            self.log.debug('expr.build.start', rules=rule_list, pos=pos)
            rules = rule_list.split()
            exprs = []
            for rk in rules:
                if not rule_expr.has_key(rk):
                    raise UnknownRuleError(rk)
                exprs.append(rule_expr[rk])

            result.append((rules, exprs, is_any))
            self.log.debug('expr.build.end', pos=pos, value=exprs, status=0)
            pos += 1

        return result

    def validate(self, source):
        """Validate the source (whatever the ConfigObj constructor
        considers a valid source type) against this specification.

        Return a pair. On failure:
          (False, [(name-of-rule-that-failed, why-it-failed), ..])
       and on success:
          (True, [])
        """
        self.log.info('validate.start')
        obj = util.IncConfigObj(source)
        failures, is_valid = [], True
        for (rule_names, rule_list, is_any) in self._apply:
            pass_, why = False, None
            for (name, rule) in zip(rule_names, rule_list):
                try:
                    eval(rule, {'self': self}, {'obj': obj})
                    result = True
                except ValidationError, E:
                    result = False
                    why = str(E)

                if result:
                    pass_ = True
                    break
                failures.append((name, why))
                if not is_any:
                    break

            if not pass_:
                is_valid = False
                break

        self.log.info('validate.end', status=0, valid=is_valid)
        return (is_valid, failures)