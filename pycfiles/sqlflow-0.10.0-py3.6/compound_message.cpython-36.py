# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlflow/compound_message.py
# Compiled at: 2020-04-10 03:26:06
# Size of source mod 2**32: 1727 bytes
from sqlflow.rows import Rows

class CompoundMessage:

    def __init__(self):
        """Message containing return result of several SQL statements
           CompoundMessage can not display in notebook since we need to
           output log messages for long running training sqls.
        """
        self._messages = []
        self.TypeRows = 1
        self.TypeMessage = 2
        self.TypeHTML = 3

    def add_rows(self, rows, eoe):
        assert isinstance(rows, Rows)
        rows.__str__()
        self._messages.append((rows, eoe, self.TypeRows))

    def add_message(self, message, eoe):
        assert isinstance(message, str)
        self._messages.append((message, eoe, self.TypeMessage))

    def add_html(self, message, eoe):
        assert isinstance(message, str)
        self._messages.append((message, eoe, self.TypeHTML))

    def length(self):
        return len(self._messages)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        all_string = ''
        for r in self._messages:
            if isinstance(r[0], Rows):
                all_string = '\n'.join([all_string, r[0].__repr__()])
            else:
                all_string = '\n'.join([all_string, r[0].__repr__()])

        return all_string

    def _repr_html_(self):
        all_html = ''
        for r in self._messages:
            if isinstance(r[0], Rows):
                all_html = ''.join([all_html, r[0]._repr_html_()])
            else:
                all_html = ''.join([all_html, '<p>%s</p>' % r[0].__str__().replace('\n', '<br>')])

        return all_html

    def get(self, idx):
        return self._messages[idx][0]