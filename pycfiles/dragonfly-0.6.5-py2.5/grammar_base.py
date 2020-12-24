# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\grammar_base.py
# Compiled at: 2009-03-30 02:12:06
"""
    This file implements the Grammar class.

"""
from ..log import get_log
from ..engines.engine import get_engine
from .rule_base import Rule
from .list import ListBase
from .context import Context

class GrammarError(Exception):
    pass


class Grammar(object):
    """
        Grammar class for managing a set of rules.

        This base grammar class takes care of the communication 
        between Dragonfly's object model and the backend speech 
        recognition engine.  This includes compiling rules and 
        elements, loading them, activating and deactivating 
        them, and unloading them.  It may, depending on the 
        engine, also include receiving recognition results and 
        dispatching them to the appropriate rule.

         - *name* -- name of this grammar
         - *description* (str, default: None) --
           description for this grammar
         - *context* (Context, default: None) --
           context within which to be active.  If *None*, the grammar will
           always be active.

    """
    _log_load = get_log('grammar.load')
    _log_begin = get_log('grammar.begin')
    _log_results = get_log('grammar.results')
    _log = get_log('grammar')

    def __init__(self, name, description=None, context=None):
        self._name = name
        self._description = description
        assert isinstance(context, Context) or context is None
        self._context = context
        self._rules = []
        self._lists = []
        self._rule_names = None
        self._loaded = False
        self._enabled = True
        self._in_context = False
        self._engine = get_engine()
        return

    def __del__(self):
        try:
            self.unload()
        except Exception, e:
            pass

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self._name)

    name = property(lambda self: self._name, doc="A grammar's name.")
    rules = property(lambda self: tuple(self._rules), doc="List of a grammar's rules.")
    lists = property(lambda self: tuple(self._lists), doc="List of a grammar's lists.")
    loaded = property(lambda self: self._loaded, doc='Whether a grammar is loaded into its SR engine or not.')

    def enable(self):
        """
            Enable this grammar so that it is active to receive 
            recognitions.

        """
        self._enabled = True

    def disable(self):
        """
            Disable this grammar so that it is not active to 
            receive recognitions.

        """
        self._enabled = False

    enabled = property(lambda self: self._enabled, doc='Whether a grammar is active to receive recognitions or not.')

    def _set_engine(self, engine):
        if self._loaded:
            raise GrammarError(' Grammar %s: Cannot set engine while loaded.' % self)
        self._engine = engine

    engine = property(lambda self: self._engine, _set_engine, doc="A grammar's SR engine.")

    def add_rule(self, rule):
        """ Add a rule to this grammar. """
        self._log_load.debug('Grammar %s: adding rule %s.' % (
         self._name, rule.name))
        if self._loaded:
            raise GrammarError('Cannot add rule while loaded.')
        elif not isinstance(rule, Rule):
            raise GrammarError('Invalid rule object: %s' % rule)
        elif rule in self._rules:
            return
        elif rule.imported:
            return
        elif [ True for r in self._rules if r.name == rule.name ]:
            raise GrammarError("Two rules with the same name '%s' notallowed." % rule.name)
        self._rules.append(rule)
        rule.grammar = self

    def remove_rule(self, rule):
        """ Remove a rule from this grammar. """
        self._log_load.debug('Grammar %s: removing rule %s.' % (
         self._name, rule.name))
        if self._loaded:
            raise GrammarError('Cannot remove rule while loaded.')
        elif not isinstance(rule, Rule):
            raise GrammarError('Invalid rule object: %s' % rule)
        elif rule not in self._rules:
            return
        self._rules.remove(rule)
        rule.grammar = None
        return

    def add_list(self, lst):
        """ Add a list to this grammar. """
        self._log_load.debug('Grammar %s: adding list %s.' % (
         self._name, lst.name))
        if self._loaded:
            raise GrammarError('Cannot add list while loaded.')
        elif not isinstance(lst, ListBase):
            raise GrammarError('Invalid list object: %s' % lst)
        elif lst in self._lists:
            return
        elif [ True for l in self._lists if l.name == lst.name ]:
            raise GrammarError("Two lists with the same name '%s' notallowed." % lst.name)
        self._lists.append(lst)
        lst.grammar = self

    def add_dependency(self, dep):
        """
            Add a rule or list dependency to this grammar.

            **Internal:** this method is normally *not* called 
            by the user, but instead automatically during 
            grammar compilation.

        """
        if isinstance(dep, Rule):
            self.add_rule(dep)
        elif isinstance(dep, ListBase):
            self.add_list(dep)
        else:
            raise GrammarError('Unknown dependency type %s.' % dep)

    def activate_rule(self, rule):
        """
            Activate a rule loaded in this grammar.

            **Internal:** this method is normally *not* called 
            directly by the user, but instead automatically when 
            the rule itself is activated by the user.

        """
        self._log_load.debug('Grammar %s: activating rule %s.' % (
         self._name, rule.name))
        assert self._loaded
        assert isinstance(rule, Rule), 'Dragonfly rule objects must be of the type dragonfly.rule.Rule'
        if rule not in self._rules:
            raise GrammarError("Rule '%s' not loaded in this grammar." % rule.name)
        if not rule.exported:
            return
        self._engine.activate_rule(rule, self)

    def deactivate_rule(self, rule):
        """
            Deactivate a rule loaded in this grammar.

            **Internal:** this method is normally *not* called 
            directly by the user, but instead automatically when 
            the rule itself is deactivated by the user.

        """
        self._log_load.debug('Grammar %s: deactivating rule %s.' % (
         self._name, rule.name))
        assert self._loaded
        assert isinstance(rule, Rule), 'Dragonfly rule objects must be of the type dragonfly.rule.Rule'
        if rule not in self._rules:
            raise GrammarError("Rule '%s' not loaded in this grammar." % rule.name)
        if not rule.exported:
            return
        self._engine.deactivate_rule(rule, self)

    def update_list(self, lst):
        """
            Update a list's content loaded in this grammar.

            **Internal:** this method is normally *not* called 
            directly by the user, but instead automatically when 
            the list itself is modified by the user.

        """
        self._log_load.debug('Grammar %s: updating list %s.' % (
         self._name, lst.name))
        if lst not in self._lists:
            raise GrammarError("List '%s' not loaded in this grammar." % lst.name)
        elif [ True for w in lst.get_list_items() if not isinstance(w, (str, unicode)) ]:
            raise GrammarError("List '%s' contains objects other thanstrings." % lst.name)
        self._engine.update_list(lst, self)

    def load(self):
        """ Load this grammar into its SR engine. """
        if self._loaded:
            return
        self._log_load.debug('Grammar %s: loading.' % self._name)
        self._engine.load_grammar(self)
        self._loaded = True
        self._in_context = False
        for rule in self._rules:
            if rule.active != False:
                rule.activate()

        for lst in self._lists:
            lst._update()

    def unload(self):
        """ Unload this grammar from its SR engine. """
        if not self._loaded:
            return
        self._log_load.debug('Grammar %s: unloading.' % self._name)
        self._engine.unload_grammar(self)
        self._loaded = False
        self._in_context = False

    def process_begin(self, executable, title, handle):
        """
            Start of phrase callback.

            This method is called when the speech recognition 
            engine detects that the user has begun to speak a 
            phrase.

            Arguments:
             - *executable* -- the full path to the module whose 
               window is currently in the foreground.
             - *title* -- window title of the foreground window.
             - *handle* -- window handle to the foreground window.

        """
        self._log_begin.debug('Grammar %s: detected beginning of utterance.' % self._name)
        self._log_begin.debug("Grammar %s:     executable '%s', title '%s'." % (
         self._name, executable, title))
        if not self._enabled:
            [ r.deactivate() for r in self._rules if r.active ]
        elif not self._context or self._context.matches(executable, title, handle):
            if not self._in_context:
                self._in_context = True
                self.enter_context()
            self._process_begin(executable, title, handle)
            for r in self._rules:
                if r.exported and hasattr(r, 'process_begin'):
                    r.process_begin(executable, title, handle)

        else:
            if self._in_context:
                self._in_context = False
                self.exit_context()
            [ r.deactivate() for r in self._rules if r.active ]
        self._log_begin.debug('Grammar %s:     active rules: %s.' % (
         self._name, [ r.name for r in self._rules if r.active ]))

    def enter_context(self):
        """
            Enter context callback.

            This method is called when a phrase-start has been 
            detected.  It is only called if this grammar's 
            context previously did not match but now does
            match positively.

        """
        pass

    def exit_context(self):
        """
            Exit context callback.

            This method is called when a phrase-start has been 
            detected.  It is only called if this grammar's 
            context previously did match but now doesn't 
            match positively anymore.

        """
        pass

    def _process_begin(self, executable, title, handle):
        """
            Start of phrase callback.

            *This usually the method which should be overridden 
            to give derived grammar classes custom behavior.*

            This method is called when the speech recognition 
            engine detects that the user has begun to speak a 
            phrase.  This method is only called when this 
            grammar's context does match positively.  It is 
            called by the ``Grammar.process_begin`` method.

            Arguments:
             - *executable* -- the full path to the module whose 
               window is currently in the foreground.
             - *title* -- window title of the foreground window.
             - *handle* -- window handle to the foreground window.

        """
        pass