# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/juvawa/Dropbox/afstuderen/prototype/bibtexparser/bibdatabase.py
# Compiled at: 2015-05-06 14:26:37
from collections import OrderedDict

class BibDatabase(object):
    """
    A bibliographic database object following the data structure of a BibTeX file.
    """

    def __init__(self):
        self.entries = []
        self._entries_dict = {}
        self.comments = []
        self.strings = OrderedDict()
        self.preambles = []

    def get_entry_list(self):
        """Get a list of bibtex entries.

        :returns: BibTeX entries
        :rtype: list
        .. deprecated:: 0.5.6
           Use :attr:`entries` instead.
        """
        return self.entries

    @staticmethod
    def entry_sort_key(entry, fields):
        result = []
        for field in fields:
            result.append(str(entry.get(field, '')).lower())

        return tuple(result)

    def get_entry_dict(self):
        """Return a dictionary of BibTeX entries.
        The dict key is the BibTeX entry key
        """
        if not self._entries_dict:
            for entry in self.entries:
                self._entries_dict[entry['ID']] = entry

        return self._entries_dict

    entries_dict = property(get_entry_dict)