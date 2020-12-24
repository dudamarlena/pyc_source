# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\action_text.py
# Compiled at: 2009-02-02 02:43:30
"""
Text action -- type a given text
============================================================================

This section describes the :class:`Text` action object. This type of 
action is used for typing text into the foreground application.

It differs from the :class:`Key` action in that :class:`Text` is used for 
typing literal text, while :class:`dragonfly.actions.action_key.Key` 
emulates pressing keys on the keyboard.  An example of this is that the 
arrow-keys are not part of a text and so cannot be typed using the 
:class:`Text` action, but can be sent by the 
:class:`dragonfly.actions.action_key.Key` action.

"""
from dragonfly.actions.action_base import DynStrActionBase, ActionError
from dragonfly.actions.typeables import typeables
from dragonfly.actions.keyboard import Keyboard
from dragonfly.actions.action_key import Key
from dragonfly.windows.clipboard import Clipboard
from dragonfly.engines.engine import get_engine

class Text(DynStrActionBase):
    """
        Action that sends keyboard events to type text.

        Arguments:
         - *spec* (*str*) -- the text to type
         - *static* (boolean) --
           if *True*, do not dynamically interpret *spec*
           when executing this action
         - *pause* (*float*) --
           the time to pause between each keystroke, given
           in seconds
         - *autofmt* (boolean) --
           if *True*, attempt to format the text with correct
           spacing and capitalization.  This is done by first mimicking
           a word recognition and then analyzing its spacing and
           capitalization and applying the same formatting to the text.

    """
    _pause_default = 0.02
    _keyboard = Keyboard()
    _specials = {'\n': typeables['enter'], 
       '\t': typeables['tab']}

    def __init__(self, spec=None, static=False, pause=_pause_default, autofmt=False):
        self._pause = pause
        self._autofmt = autofmt
        DynStrActionBase.__init__(self, spec=spec, static=static)

    def _parse_spec(self, spec):
        """ Convert the given *spec* to keyboard events. """
        events = []
        for character in spec:
            if character in self._specials:
                typeable = self._specials[character]
            else:
                typeable = Keyboard.get_typeable(character)
            events.extend(typeable.events(self._pause))

        return events

    def _execute_events(self, events):
        """
            Send keyboard events.

            If instance was initialized with *autofmt* True,
            then this method will mimic a word recognition
            and analyze its formatting so as to autoformat
            the text's spacing and capitalization before
            sending it as keyboard events.

        """
        if self._autofmt:
            get_engine().mimic('test')
            Key('cs-left, c-c/5').execute()
            word = Clipboard.get_text()
            index = word.find('test')
            if index == -1:
                index = word.find('Test')
                capitalize = True
                if index == -1:
                    self._log.error('Failed to autoformat.')
                    return False
            else:
                capitalize = False
            text = self._spec
            if capitalize:
                text = text[0].capitalize() + text[1:]
            prefix = word[:index]
            suffix = word[index + 4:]
            events = self._parse_spec(prefix + text + suffix)
        self._keyboard.send_keyboard_events(events)
        return True