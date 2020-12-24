# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/./src/SBI/error/SeqAliError.py
# Compiled at: 2020-04-28 10:16:58


class SeqAliError(Exception):
    """
    Complementary Error Class: SeqAliError
    """

    def __init__(self, code=None, value=None):
        self.value = value
        self.code = code
        if self.get_code() is not None:
            self._determine_message()
        return

    def get_value(self):
        return self.value

    def get_code(self):
        return self.code

    def _determine_message(self):
        if self.get_code() == 1:
            self.value = 'Something has gone wrong with the sequence fragment detection\n'
        elif self.get_code() == 2:
            self.value = ("A multiple sequence alignment of {0} sequences cannot be evaluated with Rost's Twilight Zone\n").format(self.value)

    def __str__(self):
        error_str = '\n\n ###################\n[SeqAliError Type: %d]\n ###################\n%s\n' % (self.get_code(), self.get_value())
        return error_str