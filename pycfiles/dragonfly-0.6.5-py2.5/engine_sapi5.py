# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\engine_sapi5.py
# Compiled at: 2009-04-08 02:25:46
"""
SAPI 5 engine class
============================================================================

"""
from win32com.client import Dispatch, getevents, constants
from win32com.client.gencache import EnsureDispatch
from pywintypes import com_error
from .engine_base import EngineBase
from .compiler_sapi5 import Sapi5Compiler
from .dictation_sapi5 import Sapi5DictationContainer
from ..grammar.state import State
from ..windows.window import Window

class Sapi5Engine(EngineBase):
    """ Speech recognition engine back-end for SAPI 5. """
    _name = 'sapi5'
    DictationContainer = Sapi5DictationContainer

    @classmethod
    def is_available(cls):
        """ Check whether this engine is available. """
        try:
            Dispatch('SAPI.SpSharedRecognizer')
        except com_error:
            return False

        return True

    def __init__(self):
        EnsureDispatch('SAPI.SpSharedRecognizer')
        EnsureDispatch('SAPI.SpVoice')
        self._recognizer = Dispatch('SAPI.SpSharedRecognizer')
        self._speaker = Dispatch('SAPI.SpVoice')
        self._compiler = Sapi5Compiler()
        self._recognition_observer_manager = None
        return

    def load_grammar(self, grammar):
        """ Load the given *grammar*. """
        self._log.debug('Loading grammar %s.' % grammar.name)
        grammar.engine = self
        context = self._recognizer.CreateRecoContext()
        handle = self._compiler.compile_grammar(grammar, context)
        wrapper = GrammarWrapper(grammar, handle, context, self)
        self._set_grammar_wrapper(grammar, wrapper)
        self.activate_grammar(grammar)
        for l in grammar.lists:
            l._update()

    def activate_grammar(self, grammar):
        """ Activate the given *grammar*. """
        self._log.debug('Activating grammar %s.' % grammar.name)
        grammar_handle = self._get_grammar_wrapper(grammar).handle
        grammar_handle.State = constants.SGSEnabled

    def deactivate_grammar(self, grammar):
        """ Deactivate the given *grammar*. """
        self._log.debug('Deactivating grammar %s.' % grammar.name)
        grammar_handle = self._get_grammar_wrapper(grammar).handle
        grammar_handle.State = constants.SGSDisabled

    def activate_rule(self, rule, grammar):
        """ Activate the given *rule*. """
        self._log.debug('Activating rule %s in grammar %s.' % (
         rule.name, grammar.name))
        grammar_handle = self._get_grammar_wrapper(grammar).handle
        grammar_handle.CmdSetRuleState(rule.name, constants.SGDSActive)
        rule_handle = grammar_handle.Rules.FindRule(rule.name)
        self._log.debug('Activating rule %r (id %r).' % (rule_handle.Name, rule_handle.Id))
        self._log.debug('Activating rule %r -> %r.' % (rule_handle.Id, constants.SGDSActive))

    def deactivate_rule(self, rule, grammar):
        """ Deactivate the given *rule*. """
        self._log.debug('Deactivating rule %s in grammar %s.' % (
         rule.name, grammar.name))
        grammar_handle = self._get_grammar_wrapper(grammar).handle
        grammar_handle.CmdSetRuleState(rule.name, constants.SGDSInactive)
        rule_handle = grammar_handle.Rules.FindRule(rule.name)
        self._log.debug('Deactivating rule %r (id %r).' % (rule_handle.Name, rule_handle.Id))
        self._log.debug('Deactivating rule %r -> %r.' % (rule_handle.Id, constants.SGDSInactive))

    def update_list(self, lst, grammar):
        grammar_handle = self._get_grammar_wrapper(grammar).handle
        list_rule_name = '__list_%s' % lst.name
        rule_handle = grammar_handle.Rules.FindRule(list_rule_name)
        rule_handle.Clear()
        src_state = rule_handle.InitialState
        dst_state = None
        for item in lst.get_list_items():
            src_state.AddWordTransition(dst_state, item)

        grammar_handle.Rules.Commit()
        return

    def _set_grammar_wrapper(self, grammar, grammar_wrapper):
        grammar._grammar_wrapper = grammar_wrapper

    def _get_grammar_wrapper(self, grammar):
        return grammar._grammar_wrapper

    def mimic(self, words):
        """ Mimic a recognition of the given *words*. """
        if isinstance(words, basestring):
            phrase = words
        else:
            phrase = (' ').join(words)
        result = self._recognizer.EmulateRecognition(phrase)
        self._log.error('Emulate results: %r' % result)

    def speak(self, text):
        """ Speak the given *text* using text-to-speech. """
        self._speaker.Speak(text)

    def _get_language(self):
        return 'en'


def collection_iter(collection):
    if not collection:
        return
    for index in xrange(0, collection.Count):
        yield collection.Item(index)


class GrammarWrapper(object):

    def __init__(self, grammar, handle, context, engine):
        self.grammar = grammar
        self.handle = handle
        self.engine = engine
        base = getevents('SAPI.SpSharedRecoContext')

        class ContextEvents(base):
            pass

        c = ContextEvents(context)
        c.OnRecognition = self.recognition_callback
        c.OnPhraseStart = self.phrase_start_callback

    def phrase_start_callback(self, stream_number, stream_position):
        window = Window.get_foreground()
        self.grammar.process_begin(window.executable, window.title, window.handle)

    def recognition_callback(self, StreamNumber, StreamPosition, RecognitionType, Result):
        try:
            newResult = Dispatch(Result)
            phrase_info = newResult.PhraseInfo
            rule_name = phrase_info.Rule.Name
            element = phrase_info.Rule
            name = element.Name
            start = element.FirstElement
            count = element.NumberOfElements
            rule_names = [name] * count
            stack = [
             collection_iter(phrase_info.Rule.Children)]
            while stack:
                try:
                    element = stack[(-1)].next()
                except StopIteration:
                    stack.pop()
                    continue

                name = element.Name
                start = element.FirstElement
                count = element.NumberOfElements
                rule_names[start:(start + count)] = [name] * count
                if element.Children:
                    stack.append(collection_iter(element.Children))

            replacements = [
             False] * len(rule_names)
            if phrase_info.Replacements:
                for replacement in collection_iter(phrase_info.Replacements):
                    begin = replacement.FirstElement
                    end = begin + replacement.NumberOfElements
                    replacements[begin] = replacement.Text
                    for index in range(begin + 1, end):
                        replacements[index] = True

            results = []
            rule_set = list(set(rule_names))
            elements = phrase_info.Elements
            for index in range(len(rule_names)):
                element = elements.Item(index)
                rule_id = rule_set.index(rule_names[index])
                replacement = replacements[index]
                info = [element.LexicalForm, rule_id,
                 element.DisplayText, element.DisplayAttributes,
                 replacement]
                results.append(info)

            s = State(results, rule_set, self.engine)
            for r in self.grammar._rules:
                if r.name != rule_name:
                    continue
                s.initialize_decoding()
                for result in r.decode(s):
                    if s.finished():
                        root = s.build_parse_tree()
                        r.process_recognition(root)
                        return

        except Exception, e:
            Sapi5Engine._log.error('Grammar %s: exception: %s' % (
             self.grammar._name, e), exc_info=True)

        self.engine._log.error('Grammar %s: failed to decode recognition %r.' % (
         self.grammar._name, [ r[0] for r in results ]))