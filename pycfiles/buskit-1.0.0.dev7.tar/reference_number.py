# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/business_tools/reference_number.py
# Compiled at: 2011-07-05 05:12:41
__doc__ = '\nReference number feature.\n'

class ReferenceNumber(object):
    """
    Datatype for bank transaction reference number.
    """

    def __init__(self, value):
        """
        >>> r = ReferenceNumber('12344')
        >>>
        """
        if not ReferenceNumber.validate(value):
            raise ValueError
        self._value = value

    def human_format(self):
        """Return reference number in human readable format"""
        return ReferenceNumber.group(self._value)

    def machine_format(self):
        """Return reference number in machine readable format"""
        ref = self._value.replace(' ', '')
        return '0' * (20 - len(ref)) + ref

    def __repr__(self):
        return '<Reference number: %s>' % self.human_format()

    def __str__(self):
        """
        Return unformatted value as string.
        """
        return str(self._value)

    def __unicode__(self):
        """
        Return unformatted value as unicode.
        """
        return unicode(self._value)

    @staticmethod
    def group(reference):
        """
        Reference number should be in groups of five digits from the right.
        Zeros in the beginning of the reference should be removed.
        """
        reference = reference.replace(' ', '')
        reference = reference.lstrip('0')
        if len(reference) < 6:
            return reference
        pos = len(reference) % 5
        if pos == 0:
            pos = 5
        ret = reference[:pos]
        for i in range(pos, len(reference), 5):
            ret += ' ' + reference[i:i + 5]

        return ret

    @staticmethod
    def is_valid(reference):
        """
        Validate reference number.
        """
        return ReferenceNumber.validate(reference)

    @staticmethod
    def validate(reference):
        """
        Validates a Finnish invoice reference number.

        XXX: Will be renamed to is_valid in the future.
        """
        if not reference:
            return False
        else:
            if isinstance(reference, basestring) and len(reference) == 0:
                return True
            reference = reference.replace(' ', '')
            if len(reference) == 0 or len(reference) > 20:
                return False
            checksum_digit = reference[(-1)]
            checksum = ReferenceNumber.calculate_checksum(reference[:-1])
            if checksum is None:
                return False
            return checksum_digit == checksum

    @staticmethod
    def calculate_checksum(reference):
        """
        Calculates checksum for a Finnish invoice reference number.

        Returns the checksum or raises ValueError if the checksum can't
        be calculated because the given reference contains non-digit
        characters.
        """
        if not reference:
            raise ValueError
        weight = [7, 3, 1]
        reference = reference.replace(' ', '')[::-1]
        checksum = 0
        for i in range(len(reference)):
            value = int(reference[i])
            checksum += weight[(i % 3)] * value

        checksum = 10 - checksum % 10
        if checksum == 10:
            checksum = 0
        return str(checksum)