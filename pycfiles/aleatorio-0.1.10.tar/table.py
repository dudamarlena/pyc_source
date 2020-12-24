# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-ppc/egg/alea/table.py
# Compiled at: 2007-08-03 02:53:18
__doc__ = ' Implement tables for random results\n'

class TableResultSetError(AssertionError):
    """ Raised when result set does not match between dice and entries """
    __module__ = __name__

    def __init__(self, dice_results, entry_results):
        """ Set up a new instance """
        self.dice_results = dice_results
        self.entry_results = entry_results

    def __str__(self):
        return 'Table result set mismatch: dice range == %s, entry results == %s' % (self.dice_results, self.entry_results)


class TableEntry(object):
    """ Single entry on a table """
    __module__ = __name__

    def __init__(self, results, data):
        """ Set up a new instance """
        self.results = results
        self.data = data

    def __repr__(self):
        params = []
        params.append('results=%s' % self.results)
        params.append('data=%s' % self.data)
        repr_str = 'TableEntry(%s)' % (', ').join(params)
        return repr_str


class Table(object):
    """ Table for determining results randomly """
    __module__ = __name__

    def __init__(self, entries, roller):
        """ Set up a new instance """
        self.entries = entries
        self.roller = roller
        entry_results = self._get_entry_result_list()
        dice_results = self.roller.total_range
        if not dice_results == entry_results:
            raise TableResultSetError(dice_results, entry_results)

    def __repr__(self):
        params = []
        params.append('entries=%s' % self.entries)
        params.append('roller=%s' % self.roller)
        repr_str = 'Table(%s)' % (', ').join(params)
        return repr_str

    def _get_entry_result_list(self):
        results = []
        for entry in self.entries:
            results.extend(entry.results)

        results.sort()
        return results

    def get_entry(self, number):
        """ Get an entry by the result number """
        candidate_entries = (entry for entry in self.entries if number in entry.results)
        try:
            entry = candidate_entries.next()
        except StopIteration:
            entry = None

        return entry

    def get_random_entry(self, roller=None):
        """ Get an entry by random result of the dice """
        if not roller:
            roller = self.roller
        result = roller.get_result()
        entry = self.get_entry(result.total())
        return (
         result, entry)