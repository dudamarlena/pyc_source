# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\wordinfo.py
# Compiled at: 2009-03-12 05:59:33
"""
    This file implements a dication formatter for capitalization
    and spacing of dictated text fragments.
"""
try:
    import natlink
except ImportError:
    natlink = None

from ..log import get_log

class Word(object):
    _flag_names = ('custom', 'undefined', 'undefined', 'undeletable', 'cap next', 'force cap next',
                   'upper next', 'lower next', 'no space after', 'double space after',
                   'no space between', 'cap mode', 'upper mode', 'lower mode', 'no space mode',
                   'normal space mode', 'None', 'not after period', 'no formatting',
                   'keep space', 'keep cap', 'no space before', 'normal cap mode',
                   'newline after', 'double newline after', 'no cap in title', 'None',
                   'space after', 'None', 'None', 'vocab builder', 'None')
    _flag_bits = dict(zip(_flag_names, [ 1 << index for index in xrange(32) ]))
    _replacements = {'one': ('1', 1024), 
       'two': ('2', 1024), 
       'three': ('3', 1024), 
       'four': ('4', 1024), 
       'five': ('5', 1024), 
       'six': ('6', 1024), 
       'seven': ('7', 1024), 
       'eight': ('8', 1024), 
       'nine': ('9', 1024)}

    def __init__(self, word):
        if word in self._replacements:
            (word, self._info) = self._replacements[word]
        else:
            self._info = natlink.getWordInfo(word)
        self._word = word
        index = word.rfind('\\')
        if index == -1:
            self.written = word
            self.spoken = word
        else:
            self.written = word[:index]
            self.spoken = word[index + 1:]
        for (name, bit) in Word._flag_bits.items():
            self.__dict__[name.replace(' ', '_')] = self._info & bit != 0

    def __str__(self):
        flags = [ flag for flag in self._flag_names if self._info & self._flag_bits[flag]
                ]
        flags.insert(0, '')
        return '%s(%r%s)' % (self.__class__.__name__, self._word,
         (', ').join(flags))


class FormatState(object):
    _log = get_log('dictation.formatter')
    (normal, capitalize, upper, lower, force) = range(5)
    (normal, no, double) = range(3)

    def __init__(self):
        self.capitalization = self.normal
        self.capitalization_mode = self.normal
        self.spacing = self.no
        self.spacing_mode = self.normal
        self.between = False

    def apply_formatting(self, word):
        c = self.capitalization
        if c == self.normal or word.no_formatting:
            written = word.written
        elif c == self.force:
            written = word.written.capitalize()
        elif c == self.capitalize:
            written = word.written.capitalize()
        elif c == self.upper:
            written = word.written.upper()
        elif c == self.lower:
            written = word.written.lower()
        else:
            raise ValueError('Unexpected internal state')
        if word.no_space_before or word.no_formatting:
            prefix = ''
        elif self.between and word.no_space_between:
            prefix = ''
        elif self.spacing == self.normal:
            prefix = ' '
        elif self.spacing == self.no:
            prefix = ''
        elif self.spacing == self.double:
            prefix = '  '
        else:
            raise ValueError('Unexpected internal state')
        if word.newline_after:
            suffix = '\n'
        elif word.double_newline_after:
            suffix = '\n\n'
        elif word.space_after:
            suffix = ' '
        else:
            suffix = ''
        return ('').join((prefix, written, suffix))

    def update_state(self, word):
        if word.normal_cap_mode:
            self.capitalization_mode = self.normal
        elif word.cap_mode:
            self.capitalization_mode = self.capitalize
        elif word.upper_mode:
            self.capitalization_mode = self.upper
        elif word.lower_mode:
            self.capitalization_mode = self.lower
        if word.force_cap_next:
            self.capitalization = self.force
        elif word.cap_next:
            self.capitalization = self.capitalize
        elif word.upper_next:
            self.capitalization = self.upper
        elif word.lower_next:
            self.capitalization = self.lower
        elif not word.keep_cap:
            self.capitalization = self.capitalization_mode
        if word.no_space_mode:
            self.spacing_mode = self.no
        elif word.normal_space_mode:
            self.spacing_mode = self.normal
        if word.no_space_after:
            self.spacing = self.no
        elif word.double_space_after:
            self.spacing = self.double
        elif not word.keep_space:
            self.spacing = self.spacing_mode
        self.between = word.no_space_between

    def format_words(self, words):
        output = []
        for word in words:
            if not isinstance(word, Word):
                word = Word(word)
            if self._log:
                self._log.debug("Formatting word: '%s'" % word)
            output.append(self.apply_formatting(word))
            self.update_state(word)

        output = ('').join(output)
        if self._log:
            self._log.debug("Formatted output: '%s'" % output)
        return output