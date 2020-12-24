# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/business_tools/bank_account.py
# Compiled at: 2011-07-05 05:12:41
"""Bank account support."""

class AccountNumber(object):
    """
    Generic base for bank account numbers.
    """
    _value = None

    def __init__(self, value):
        """
        @param value: A valid finnish bank account number.

        Should not be instantiated. Subclass instead.

        """
        self._value = value

    def bank_name(self):
        """
        Extract bank name from the account number.
        """
        return get_bank_name(self._value)

    def machine_format(self):
        """
        Return machine parseable account number.

        """
        return self._value


class BBAN(AccountNumber):
    """
    Finnish bank account number.
    """

    def __init__(self, value):
        """
        @param value: A valid finnish bank account number.

        """
        super(BBAN, self).__init__(value)
        if not BBAN.validate_account_number(value):
            raise ValueError('Invalid finnish BBAN')
        self._value = self.to_machine(value)

    def to_machine(self, value):
        """Convert value to machine parseable account number.
        @param value: A valid account number.

        """
        return self.expand_account_number(value)

    def human_format(self):
        """
        Return human readable account number.

        """
        return self.humanize_account_number(self._value)

    def __str__(self):
        """
        Return human formatted account number as string.

        """
        return self.human_format()

    @staticmethod
    def humanize_account_number(value):
        """Convert value to human formatted account number."""
        retval = value[0:6] + '-' + str(int(value[6:]))
        return retval

    @staticmethod
    def expand_account_number(number):
        """
        Transform account number to machine readable form
        """
        number = str(number).replace(' ', '')
        number = number.replace('-', '')
        if len(number) < 8 or len(number) > 14:
            return False
        if number[0] in ('4', '5'):
            number = number[0:7] + '0' * (14 - len(number)) + number[7:]
        else:
            number = number[0:6] + '0' * (14 - len(number)) + number[6:]
        return number

    @staticmethod
    def calculate_account_number_checksum(number):
        print 'Deprecated method calculate_account_number_checksum.'
        return BBAN.calculate_checksum(number)

    @staticmethod
    def calculate_checksum(number):
        """
        Return calculated checksum.
        """
        checksum_str = ''
        try:
            for i in range(13):
                value = int(number[i])
                checksum_str += str(value * (2 - i % 2))

        except ValueError:
            return

        checksum = 0
        for value in checksum_str:
            checksum += int(value)

        checksum = 10 - checksum % 10
        if checksum == 10:
            checksum = 0
        return str(checksum)

    @staticmethod
    def validate_account_number(number):
        """
        Validates a Finnish bank account number.
        """
        number = BBAN.expand_account_number(number)
        if not number:
            return False
        else:
            checksum = BBAN.calculate_account_number_checksum(number)
            if checksum is None:
                return False
            return number[(-1)] == checksum

    @staticmethod
    def is_valid(number):
        """Validate account number."""
        return BBAN.validate_account_number(number)


class IBAN(AccountNumber):
    """
    International bank account number.
    """

    def __init__(self, value):
        super(IBAN, self).__init__(value)
        if not IBAN.validate_account_number(str(value)):
            raise ValueError('Invalid IBAN')
        self._value = str(value)

    @staticmethod
    def validate_account_number(value):
        """
        Validate IBAN account number.
        """
        for i in range(2):
            if not value[i].isalpha():
                return False

        for i in range(2, len(value)):
            if not value[i].isdigit():
                return False

        if value[2:4] != IBAN.calculate_checksum(value[4:], value[0:2]):
            return False
        return True

    @staticmethod
    def calculate_checksum(bban, country_code='FI'):
        """
        Return calculated checksum.
        """
        if country_code != 'FI':
            raise ValueError('Only finnish account numbers are supported.')

        def letters_to_digits(data):
            new_data = ''
            for value in data:
                if value.isalpha():
                    new_data += str(ord(value) - 55)
                else:
                    new_data += value

            return new_data

        value = 98 - int(letters_to_digits(str(bban) + 'FI00')) % 97
        return '%.2d' % (value,)

    def bank_name(self):
        """
        Extract bank name from the account number.
        """
        return get_bank_name(iban_to_bban(self))

    def __str__(self):
        return self._value


def iban_to_bban(value):
    """
    Convert IBAN to BBAN. Return bban string in human format.
    """
    if not isinstance(value, IBAN):
        raise TypeError()
    return BBAN(value.machine_format()[4:]).human_format()


def bban_to_iban(value, country_code='FI'):
    """
    Convert BBAN to IBAN.
    """
    if not isinstance(value, BBAN):
        raise TypeError()
    account = value.machine_format()
    checksum = IBAN.calculate_checksum(account, 'FI')
    return country_code + checksum + account


def get_bank_name(account_number):
    """
    Returns the bank name based on the account number
    @param account_number: a Finnish bank account number (BBAN).
    @return: Bank name or 'Tuntematon'.
    """
    banks = {'1': 'Nordea', 
       '2': 'Nordea', 
       '31': 'Handelsbanken', 
       '33': 'SEB', 
       '34': 'Danske Bank', 
       '36': 'Tapiola', 
       '37': 'DnB NOR', 
       '38': 'Swedbank', 
       '39': 'S-Pankki', 
       '4': 'Säästöpankki', 
       '47': 'Pop', 
       '5': 'Osuuspankki', 
       '6': 'Ålandsbanken', 
       '8': 'Sampo'}
    if account_number == '500001':
        return 'OKO pankki'
    else:
        if account_number[0:4] in ('4055', '4050', '4970'):
            return 'Aktia'
        if account_number[0:2] in banks:
            return banks[account_number[0:2]]
        if account_number[0] in banks:
            return banks[account_number[0]]
        return 'Tuntematon'


def get_swift_code(bank_name):
    """
    Return a SWIFT (BIC) code for a known finnish bank.
    @param bank_name: A finnish bank name in lower case.
    @return: SWIFT-code (str) or None
    """
    data = {'nordea': 'NDEAFIHH', 'nandelsbanken': 'HANDFIHH', 
       'seb': 'ESSEFIHX', 
       'danske bank': 'DABAFIHX', 
       'tapiola': 'TAPIFI22', 
       'dnb nor': 'DNBAFIHX', 
       'swedbank': 'SWEDFIHH', 
       's-pankki': 'SBANFIHH', 
       'säästöpankki': 'HELSFIHH', 
       'pop': 'HELSFIHH', 
       'osuuspankki': 'OKOYFIHH', 
       'ålandsbanken': 'AABAFI22', 
       'sampo': 'DABAFIHH', 
       'aktia': 'HELSFIHH'}
    bank_name = bank_name.lower()
    if bank_name in data:
        return data[bank_name]
    else:
        return