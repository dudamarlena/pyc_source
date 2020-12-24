# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/utf8validator.py
# Compiled at: 2015-11-13 17:02:49
from six.moves import range
try:
    from wsaccel.utf8validator import Utf8Validator
except:

    class Utf8Validator:
        """
        Incremental UTF-8 validator with constant memory consumption (minimal
        state).

        Implements the algorithm "Flexible and Economical UTF-8 Decoder" by
        Bjoern Hoehrmann (http://bjoern.hoehrmann.de/utf-8/decoder/dfa/).
        """
        UTF8VALIDATOR_DFA = [
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
         7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
         8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
         10, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3, 3,
         11, 6, 6, 6, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
         0, 1, 2, 3, 5, 8, 7, 1, 1, 1, 4, 6, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,
         1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1,
         1, 3, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        UTF8_ACCEPT = 0
        UTF8_REJECT = 1

        def __init__(self):
            self.reset()

        def decode(self, b):
            """
            Eat one UTF-8 octet, and validate on the fly.

            Returns UTF8_ACCEPT when enough octets have been consumed, in which case
            self.codepoint contains the decoded Unicode code point.

            Returns UTF8_REJECT when invalid UTF-8 was encountered.

            Returns some other positive integer when more octets need to be eaten.
            """
            type = Utf8Validator.UTF8VALIDATOR_DFA[b]
            if self.state != Utf8Validator.UTF8_ACCEPT:
                self.codepoint = b & 63 | self.codepoint << 6
            else:
                self.codepoint = 255 >> type & b
            self.state = Utf8Validator.UTF8VALIDATOR_DFA[(256 + self.state * 16 + type)]
            return self.state

        def reset(self):
            """
            Reset validator to start new incremental UTF-8 decode/validation.
            """
            self.state = Utf8Validator.UTF8_ACCEPT
            self.codepoint = 0
            self.i = 0

        def validate(self, ba):
            """
            Incrementally validate a chunk of bytes provided as string.

            Will return a quad (valid?, endsOnCodePoint?, currentIndex, totalIndex).

            As soon as an octet is encountered which renders the octet sequence
            invalid, a quad with valid? == False is returned. currentIndex returns
            the index within the currently consumed chunk, and totalIndex the
            index within the total consumed sequence that was the point of bail out.
            When valid? == True, currentIndex will be len(ba) and totalIndex the
            total amount of consumed bytes.
            """
            l = len(ba)
            ba = bytearray(ba)
            for i in range(l):
                self.state = Utf8Validator.UTF8VALIDATOR_DFA[(256 + (self.state << 4) + Utf8Validator.UTF8VALIDATOR_DFA[ba[i]])]
                if self.state == Utf8Validator.UTF8_REJECT:
                    self.i += i
                    return (
                     False, False, i, self.i)

            self.i += l
            return (
             True, self.state == Utf8Validator.UTF8_ACCEPT, l, self.i)