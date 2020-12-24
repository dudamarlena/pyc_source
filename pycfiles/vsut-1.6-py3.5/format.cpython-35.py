# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vsut/format.py
# Compiled at: 2016-05-12 02:33:33
# Size of source mod 2**32: 3332 bytes
from vsut.unit import Unit

class Formatter:
    __doc__ = 'A Formatter formats the results of a unit for viewing.\n    '

    def format(self, unit):
        """Formats the result of a unit.
        """
        pass


class TableFormatter(Formatter):
    __doc__ = "A TableFormatter formats the results of a unit as a table.\n\n    The table looks as follows:\n    Id | Name | Status | Time | Assert | Message\n\n    NOTE: The TableFormatter currently only supports up to 999 test ids, as its id column width is fixed to 3.\n            Please refrain from ever running more than 999 tests. That's crazy.\n    "

    def format(self, unit):
        nameLength = max([len(name) for name in unit.tests.values()])
        if len([result for result in unit.results.values() if result is not None]) != 0:
            assertLength = max([len(result.assertion) for result in unit.results.values() if result is not None])
        else:
            assertLength = 6
        ret = '[{0}]\n'.format(type(unit).__name__)
        ret += '{0:^3} | {1:^{nameLength}} | {2:^6} | {3:^8} | {4:^{assertLength}} | {5}\n'.format('Id', 'Name', 'Status', 'Time', 'Assert', 'Message', nameLength=nameLength, assertLength=assertLength)
        for id, name in unit.tests.items():
            result = unit.results[id]
            if result == None:
                ret += '{0:<3} | {1:<{nameLength}} | {2:^6} | {3:<8} | {4:<{assertLength}} |\n'.format(id, name, 'OK', unit.times[id], '', nameLength=nameLength, assertLength=assertLength)
            else:
                ret += '{0:<3} | {1:<{nameLength}} | {2:^6} | {3:<8} | {4:<{assertLength}} | {5}\n'.format(id, name, 'FAIL', unit.times[id], result.assertion, result.message, nameLength=nameLength, assertLength=assertLength)

        return ret


class CSVFormatter(Formatter):
    __doc__ = "A CSVFormatter formats the result of a unit as a comma-separated-values list.\n\n        Its separator can be specified when formatting, the default value is ','.\n    "

    def __init__(self, separator=';'):
        self.separator = separator

    def format(self, unit):
        """Formats the results of a unit.
        """
        ret = '{0}\n'.format(type(unit).__name__)
        for id, name in unit.tests.items():
            result = unit.results[id]
            if result is None:
                ret += '{1}{0}{2}{0}OK{0}{3}\n'.format(self.separator, id, name, unit.times[id])
            else:
                ret += '{1}{0}{2}{0}FAIL{0}{3}{0}{4}{0}{5}\n'.format(self.separator, id, name, unit.times[id], result.assertion, result.message)

        return ret