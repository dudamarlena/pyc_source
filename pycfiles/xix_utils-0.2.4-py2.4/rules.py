# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/rules.py
# Compiled at: 2006-03-02 13:59:00
"""
rules rules!

TODO create a badass rules engine

$Id: rules.py 159 2005-12-02 20:35:19Z drew $
"""
from xix.utils.interfaces import IRule, IRuleChain
from xix.utils.python import allexcept
from xix.utils.config import configFactory
from xix.utils.comp.interface import implements
__author__ = 'Drew Smathers <drew.smathers@gmail.com>'
__version__ = '$Revision: 159 $'[11:-2]
__copyright__ = 'Copyright (C) 2005, Drew Smathers'
_rulescfg = configFactory.getConfig()
engineRegistry = _rulescfg.engineRegistry

class RulesException(Exception):
    """Generic RulesException.
    """
    __module__ = __name__


class RulesEngineAlreadyRegisteredException(RulesException):
    """Raised when when trying to register a rules engine with registered name.
    """
    __module__ = __name__


class Rule:
    """Validation rule functor.
    """
    __module__ = __name__
    implements(IRule)

    def __call__(self, *pargs, **kwargs):
        """Example:

        >>> rule  = Rule()
        >>> rule("the world")
        True
        """
        return True


class RuleChain:
    """Functor for series of short-circuiting rules.
    """
    __module__ = __name__
    implements(IRuleChain)

    def __init__(self, rules=None):
        self.rules = rules or []

    def __call__(self, *pargs, **kwargs):
        """Example:

        >>> class MyRule(Rule):
        ...     def __call__(self, *pargs, **kwargs):
        ...         return False
        ...
        >>> rule1, rule2 = Rule(), MyRule()
        >>> chain = RuleChain([rule1, rule2])
        >>> chain("me up an beat me with a shoe")
        False
        """
        result = True
        for rule in self.rules:
            result &= rule(*pargs, **kwargs)
            if not result:
                break

        return result


def registerEngine(engineName, rulesEngine):
    """Register a rules enging with name engineName.
    """
    if engineName in engineRegistry:
        raise RulesEngineAlreadyRegisteredException, 'Engine with name %s already registered' % engineName
    engineRegistry[engineName] = rulesEngine


__all__ = allexcept('IRule', 'IRuleChain', 'allexcept', 'configFactory', 'implements')