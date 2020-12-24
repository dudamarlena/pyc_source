# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\action_mimic.py
# Compiled at: 2009-04-06 11:18:29
"""
Mimic action
============================================================================

"""
from .action_base import ActionBase, ActionError
from ..engines.engine import get_engine

class Mimic(ActionBase):
    r"""
        Mimic recognition action.

        The constructor arguments are the words which will be mimicked. 
        These should be passed as a variable argument list.  For example::

            action = Mimic("hello", "world", r"!\exclamation-mark")
            action.execute()

        If an error occurs during mimicking the given recognition, then an 
        *ActionError* is raised.  A common error is that the engine does 
        not know the given words and can therefore not recognize them. 
        For example, the following attempts to mimic recognition of *one 
        single word* including a space and an exclamation-mark; this will 
        almost certainly fail::

            Mimic("hello world!").execute()   # Will raise ActionError.

        The constructor accepts the optional *extra* keyword argument, and 
        uses this to retrieve dynamic data from the extras associated with 
        the recognition.  For example, this can be used as follows to 
        implement dynamic mimicking::

            class ExampleRule(MappingRule):
                mapping  = {
                            "mimic recognition <text> [<n> times]":
                                Mimic(extra="text") * Repeat(extra="n"),
                           }
                extras   = [
                            IntegerRef("n", 1, 10),
                            Dictation("text"),
                           ]
                defaults = {
                            "n": 1,
                           }

        The example above will allow the user to speak **"mimic 
        recognition hello world! 3 times"**, which would result in the 
        exact same output as if the user had spoken **"hello world!"** 
        three times in a row.

    """

    def __init__(self, *words, **kwargs):
        ActionBase.__init__(self)
        self._words = tuple(words)
        if 'extra' in kwargs:
            self._extra = kwargs.pop('extra')
        else:
            self._extra = None
        if kwargs:
            raise ActionError('Invalid arguments: %r' % (', ').join(kwargs.keys()))
        return

    def _execute(self, data=None):
        engine = get_engine()
        words = self._words
        if self._extra:
            try:
                extra = data[self._extra]
            except KeyError:
                raise ActionError('No extra data available for extra %r' % self._extra)
            else:
                if isinstance(extra, engine.DictationContainer):
                    words += extra.words
                elif isinstance(extra, (tuple, list)):
                    words += tuple(extra)
                elif isinstance(extra, basestr):
                    words += (extra,)
                else:
                    raise ActionError('Invalid extra data type: %r' % extra)
        self._log.debug('Mimicking recognition: %r' % (words,))
        try:
            engine.disable_recognition_observers()
            engine.mimic(words)
            engine.enable_recognition_observers()
        except Exception, e:
            raise ActionError('Mimicking failed: %s' % e)