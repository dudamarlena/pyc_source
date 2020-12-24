# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/speech.py
# Compiled at: 2009-02-27 09:30:00
"""
speech recognition and voice synthesis module.

Please let me know if you like or use this module -- it would make my day!

speech.py: Copyright 2008 Michael Gundlach  (gundlach at gmail)
License: Apache 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

For this module to work, you'll need pywin32 (http://tinyurl.com/5ezco9
for Python 2.5 or http://tinyurl.com/5uzpox for Python 2.4) and
the Microsoft Speech kit (http://tinyurl.com/zflb).

Classes:
    Listener: represents a command to execute when phrases are heard.

Functions:
    say(phrase): Say the given phrase out loud.
    input(prompt, phraselist): Block until input heard, then return text.
    stoplistening(): Like calling stoplistening() on all Listeners.
    islistening(): True if any Listener is listening.
    listenforanything(callback): Run a callback when any text is heard.
    listenfor(phraselist, callback): Run a callback when certain text is heard.

Very simple usage example:

import speech

speech.say("Say something.")

print "You said " + speech.input()

def L1callback(phrase, listener):
    print phrase

def L2callback(phrase, listener):
    if phrase == "wow":
        listener.stoplistening()
    speech.say(phrase)

# callbacks are executed on a separate events thread.
L1 = speech.listenfor(["hello", "good bye"], L1callback)
L2 = speech.listenforanything(L2callback)

assert speech.islistening()
assert L2.islistening()

L1.stoplistening()
assert not L1.islistening()

speech.stoplistening()
"""
from win32com.client import constants as _constants
import win32com.client, pythoncom, time, thread
from win32com.client import gencache
gencache.EnsureModule('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 0, 5, 0)
_voice = win32com.client.Dispatch('SAPI.SpVoice')
_recognizer = win32com.client.Dispatch('SAPI.SpSharedRecognizer')
_listeners = []
_handlerqueue = []
_eventthread = None

class Listener(object):
    """Listens for speech and calls a callback on a separate thread."""
    __module__ = __name__
    _all = set()

    def __init__(self, context, grammar, callback):
        """
        This should never be called directly; use speech.listenfor()
        and speech.listenforanything() to create Listener objects.
        """
        self._grammar = grammar
        Listener._all.add(self)
        _handlerqueue.append((context, self, callback))
        _ensure_event_thread()

    def islistening(self):
        """True if this Listener is listening for speech."""
        return self in Listener._all

    def stoplistening(self):
        """Stop listening for speech.  Returns True if we were listening."""
        global _eventthread
        try:
            Listener._all.remove(self)
        except KeyError:
            return False

        self._grammar = None
        if not Listener._all:
            _eventthread = None
        return True


_ListenerBase = win32com.client.getevents('SAPI.SpSharedRecoContext')

class _ListenerCallback(_ListenerBase):
    """Created to fire events upon speech recognition.  Instances of this
    class automatically die when their listener loses a reference to
    its grammar.  TODO: we may need to call self.close() to release the
    COM object, and we should probably make goaway() a method of self
    instead of letting people do it for us.
    """
    __module__ = __name__

    def __init__(self, oobj, listener, callback):
        _ListenerBase.__init__(self, oobj)
        self._listener = listener
        self._callback = callback

    def OnRecognition(self, _1, _2, _3, Result):
        if self._listener and not self._listener.islistening():
            self.close()
            self._listener = None
        if self._callback and self._listener:
            newResult = win32com.client.Dispatch(Result)
            phrase = newResult.PhraseInfo.GetText()
            self._callback(phrase, self._listener)
        return


def say(phrase):
    """Say the given phrase out loud."""
    _voice.Speak(phrase)


def input(prompt=None, phraselist=None):
    """
    Print the prompt if it is not None, then listen for a string in phraselist
    (or anything, if phraselist is None.)  Returns the string response that is
    heard.  Note that this will block the thread until a response is heard or
    Ctrl-C is pressed.
    """

    def response(phrase, listener):
        if not hasattr(listener, '_phrase'):
            listener._phrase = phrase
        listener.stoplistening()

    if prompt:
        print prompt
    if phraselist:
        listener = listenfor(phraselist, response)
    else:
        listener = listenforanything(response)
    while listener.islistening():
        time.sleep(0.1)

    return listener._phrase


def stoplistening():
    """
    Cause all Listeners to stop listening.  Returns True if at least one
    Listener was listening.
    """
    listeners = set(Listener._all)
    returns = [ l.stoplistening() for l in listeners ]
    return any(returns)


def islistening():
    """True if any Listeners are listening."""
    return not not Listener._all


def listenforanything(callback):
    """
    When anything resembling English is heard, callback(spoken_text, listener)
    is executed.  Returns a Listener object.

    The first argument to callback will be the string of text heard.
    The second argument will be the same listener object returned by
    listenforanything().

    Execution takes place on a single thread shared by all listener callbacks.
    """
    return _startlistening(None, callback)


def listenfor(phraselist, callback):
    """
    If any of the phrases in the given list are heard,
    callback(spoken_text, listener) is executed.  Returns a Listener object.

    The first argument to callback will be the string of text heard.
    The second argument will be the same listener object returned by
    listenfor().

    Execution takes place on a single thread shared by all listener callbacks.
    """
    return _startlistening(phraselist, callback)


def _startlistening(phraselist, callback):
    """
    Starts listening in Command-and-Control mode if phraselist is
    not None, or dictation mode if phraselist is None.  When a phrase is
    heard, callback(phrase_text, listener) is executed.  Returns a
    Listener object.

    The first argument to callback will be the string of text heard.
    The second argument will be the same listener object returned by
    listenfor().

    Execution takes place on a single thread shared by all listener callbacks.
    """
    context = _recognizer.CreateRecoContext()
    grammar = context.CreateGrammar()
    if phraselist:
        grammar.DictationSetState(0)
        rule = grammar.Rules.Add('rule', _constants.SRATopLevel + _constants.SRADynamic, 0)
        rule.Clear()
        for phrase in phraselist:
            rule.InitialState.AddWordTransition(None, phrase)

        grammar.Rules.Commit()
        grammar.CmdSetRuleState('rule', 1)
        grammar.Rules.Commit()
    else:
        grammar.DictationSetState(1)
    return Listener(context, grammar, callback)


def _ensure_event_thread():
    """
    Make sure the eventthread is running, which checks the handlerqueue
    for new eventhandlers to create, and runs the message pump.
    """
    global _eventthread
    if not _eventthread:

        def loop():
            while _eventthread:
                pythoncom.PumpWaitingMessages()
                if _handlerqueue:
                    (context, listener, callback) = _handlerqueue.pop()
                    _ListenerCallback(context, listener, callback)
                time.sleep(0.5)

        _eventthread = 1
        _eventthread = thread.start_new_thread(loop, ())