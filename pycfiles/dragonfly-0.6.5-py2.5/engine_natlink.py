# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\engine_natlink.py
# Compiled at: 2009-04-08 02:25:23
"""
Natlink and DNS engine class
============================================================================

"""
natlink = None
import win32com.client
from .engine_base import EngineBase
from .dictation_natlink import NatlinkDictationContainer
from .recobs_natlink import NatlinkRecObsManager

class NatlinkEngine(EngineBase):
    """ Speech recognition engine back-end for Natlink and DNS. """
    _name = 'natlink'
    DictationContainer = NatlinkDictationContainer

    @classmethod
    def is_available(cls):
        """ Check whether Natlink is available. """
        try:
            import natlink
        except ImportError:
            return False

        if natlink.isNatSpeakRunning():
            return True
        else:
            return False

    def __init__(self):
        global natlink
        EngineBase.__init__(self)
        self._natlink = None
        if natlink:
            self._natlink = natlink
        else:
            try:
                import natlink as natlink_
            except ImportError:
                self._log.error('%s: failed to import natlink module.' % self)
                raise EngineError('Failed to import the Natlink module.')

            natlink = natlink_
            self._natlink = natlink_
        self._recognition_observer_manager = NatlinkRecObsManager(self)
        return

    def load_grammar(self, grammar):
        """ Load the given *grammar* into natlink. """
        self.load_natlink_grammar(grammar)

    def load_natlink_grammar(self, grammar, all_results=False, hypothesis=False):
        """ Load the given *grammar* into natlink. """
        self._log.debug('Engine %s: loading grammar %s.' % (
         self, grammar.name))
        grammar.engine = self
        grammar_object = self._natlink.GramObj()
        wrapper = GrammarWrapper(grammar, grammar_object, self)
        grammar_object.setBeginCallback(wrapper.begin_callback)
        grammar_object.setResultsCallback(wrapper.results_callback)
        grammar_object.setHypothesisCallback(None)
        for r in grammar._rules:
            for d in r.dependencies():
                grammar.add_dependency(d)

        c = NatlinkCompiler()
        (compiled_grammar, rule_names) = c.compile_grammar(grammar)
        grammar._rule_names = rule_names
        try:
            grammar_object.load(compiled_grammar, all_results, hypothesis)
        except self._natlink.NatError, e:
            self._log.warning('%s: failed to load grammar %r: %s.' % (
             self, grammar.name, e))
            self._set_grammar_wrapper(grammar, None)
            return

        self._set_grammar_wrapper(grammar, wrapper)
        return

    def unload_grammar(self, grammar):
        """ Unload the given *grammar* from natlink. """
        try:
            grammar_object = self._get_grammar_wrapper(grammar).grammar_object
            grammar_object.setBeginCallback(None)
            grammar_object.setResultsCallback(None)
            grammar_object.setHypothesisCallback(None)
            grammar_object.unload()
        except self._natlink.NatError, e:
            self._log.warning('Engine %s: failed to unload: %s.' % (
             self, e))

        return

    def activate_grammar(self, grammar):
        self._log.debug('Activating grammar %s.' % grammar.name)

    def deactivate_grammar(self, grammar):
        self._log.debug('Deactivating grammar %s.' % grammar.name)

    def activate_rule(self, rule, grammar):
        self._log.debug('Activating rule %s in grammar %s.' % (rule.name, grammar.name))
        wrapper = self._get_grammar_wrapper(grammar)
        if not wrapper:
            return
        grammar_object = wrapper.grammar_object
        grammar_object.activate(rule.name, 0)

    def deactivate_rule(self, rule, grammar):
        self._log.debug('Deactivating rule %s in grammar %s.' % (rule.name, grammar.name))
        wrapper = self._get_grammar_wrapper(grammar)
        if not wrapper:
            return
        grammar_object = wrapper.grammar_object
        grammar_object.deactivate(rule.name)

    def update_list(self, lst, grammar):
        wrapper = self._get_grammar_wrapper(grammar)
        if not wrapper:
            return
        grammar_object = wrapper.grammar_object
        n = lst.name
        f = grammar_object.appendList
        grammar_object.emptyList(n)
        [ f(n, word) for word in lst.get_list_items() ]

    def _set_grammar_wrapper(self, grammar, grammar_wrapper):
        grammar._grammar_wrapper = grammar_wrapper

    def _get_grammar_wrapper(self, grammar):
        return grammar._grammar_wrapper

    def mimic(self, words):
        """ Mimic a recognition of the given *words*. """
        self._natlink.recognitionMimic(list(words))

    def speak(self, text):
        """ Speak the given *text* using text-to-speech. """
        self._natlink.execScript('TTSPlayString "%s"' % text)

    def _get_language(self):
        app = win32com.client.Dispatch('Dragon.DgnEngineControl')
        language = app.SpeakerLanguage('')
        try:
            tag = self._language_tags[language]
            tag = tag[0]
        except KeyError:
            self._log.error('Unknown speaker language: 0x%04x' % language)
            raise GrammarError('Unknown speaker language: 0x%04x' % language)

        return tag

    _language_tags = {3081: ('en', 'AustralianEnglish'), 
       61450: ('es', 'CastilianSpanish'), 
       1043: ('nl', 'Dutch'), 
       9: ('en', 'English'), 
       1036: ('fr', 'French'), 
       1031: ('de', 'German'), 
       61449: ('en', 'IndianEnglish'), 
       1040: ('it', 'Italian'), 
       1041: ('jp', 'Japanese'), 
       62474: ('es', 'LatinAmericanSpanish'), 
       1046: ('pt', 'Portuguese'), 
       62473: ('en', 'SingaporeanEnglish'), 
       1034: ('es', 'Spanish'), 
       2057: ('en', 'UKEnglish'), 
       1033: ('en', 'USEnglish')}


class GrammarWrapper(object):

    def __init__(self, grammar, grammar_object, engine):
        self.grammar = grammar
        self.grammar_object = grammar_object
        self.engine = engine

    def begin_callback(self, module_info):
        (executable, title, handle) = module_info
        self.grammar.process_begin(executable, title, handle)

    def results_callback(self, words, results):
        if words == 'other':
            words_rules = results.getResults(0)
        elif words == 'reject':
            words_rules = []
        else:
            words_rules = words
        NatlinkEngine._log.debug('Grammar %s: received recognition %r.' % (
         self.grammar._name, words))
        if hasattr(self.grammar, 'process_results'):
            if not self.grammar.process_results(words, results):
                return
        s = state_.State(words_rules, self.grammar._rule_names, self.engine)
        for r in self.grammar._rules:
            if not r.active:
                continue
            s.initialize_decoding()
            for result in r.decode(s):
                if s.finished():
                    root = s.build_parse_tree()
                    r.process_recognition(root)
                    return

        NatlinkEngine._log.warning('Grammar %s: failed to decode recognition %r.' % (
         self.grammar._name, words))


from dragonfly.engines.compiler_natlink import NatlinkCompiler
import dragonfly.grammar.state as state_, dragonfly.grammar.wordinfo as wordinfo