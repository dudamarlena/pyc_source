# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/suelta/exceptions.py
# Compiled at: 2017-01-31 22:58:59
# Size of source mod 2**32: 883 bytes


class SASLError(Exception):

    def __init__(self, sasl, text, mech=None):
        """
        :param sasl: The main `suelta.SASL` object.
        :param text: Descpription of the error.
        :param mech: Optional reference to the mechanism object.

        :type sasl: `suelta.SASL`
        """
        self.sasl = sasl
        self.text = text
        self.mech = mech

    def __str__(self):
        if self.mech is None:
            return 'SASL Error: %s' % self.text
        else:
            return 'SASL Error (%s): %s' % (self.mech, self.text)


class SASLCancelled(SASLError):

    def __init__(self, sasl, mech=None):
        """
        :param sasl: The main `suelta.SASL` object.
        :param mech: Optional reference to the mechanism object.

        :type sasl: `suelta.SASL`
        """
        super(SASLCancelled, self).__init__(sasl, 'User cancelled', mech)