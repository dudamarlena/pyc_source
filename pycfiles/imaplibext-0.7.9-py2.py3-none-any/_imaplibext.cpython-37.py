# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/teward/PyCharm Projects/imaplibext/imaplibext/_imaplibext.py
# Compiled at: 2019-07-26 13:00:25
# Size of source mod 2**32: 11451 bytes
import imaplib, socket, sys
from typing import Any, List, Optional, Tuple, Union
AnyStr = Union[(str, bytes)]

class IMAP4(imaplib.IMAP4):

    def __init__(self, host='', port=imaplib.IMAP4_PORT, timeout=None, maxbytes=50000):
        if timeout:
            socket.setdefaulttimeout(timeout)
        if maxbytes:
            imaplib._MAXLINE = maxbytes
        imaplib.IMAP4.__init__(self, host, port)

    def copy(self, message_set, new_mailbox):
        """Copy 'message_set' messages onto end of 'new_mailbox'.

        (typ, [data]) = <instance>.copy(message_set, new_mailbox)
        """
        return self.uid('COPY', message_set, new_mailbox)

    def fetch(self, message_set, message_parts='(RFC822)'):
        """Fetch (parts of) messages, using UID values.

        (typ, [data, ...]) = <instance>.fetch(message_set, message_parts)

        'message_parts' should be a string of selected parts
        enclosed in parentheses, eg: "(UID BODY[TEXT])".

        'data' are tuples of message part envelope and data.
        """
        if isinstance(message_set, bytes):
            message_set = message_set.decode('utf-8')
        return self.uid('FETCH', str(message_set), message_parts)

    def search(self, charset, *criteria):
        """Search mailbox for matching messages.

        (typ, [data]) = <instance>.search(charset, criterion, ...)

        'data' is space separated list of matching message UID numbers.
        If UTF8 is enabled, charset MUST be None.
        """
        return self.uid('SEARCH', charset, ' '.join(criteria))

    def sort(self, sort_criteria, charset, *search_criteria):
        """IMAP4rev1 extension SORT command.

        (typ, [data]) = <instance>.sort(sort_criteria, charset, search_criteria, ...)
        """
        _search_criterion = []
        for criterion in search_criteria:
            criterion = str(criterion)
            _search_criterion.extend(criterion.split())

        search_criteria = tuple(_search_criterion)
        if sort_criteria[0] != '(':
            sort_criteria = '(' + sort_criteria
        if sort_criteria[(len(sort_criteria) - 1)] != ')':
            sort_criteria += ')'
        if not charset:
            charset = 'UTF-8'
        return self.uid('SORT', sort_criteria, charset, ' '.join(search_criteria))

    def store(self, message_set, command, flags):
        """Alters flag dispositions for messages in mailbox, using UID values.

        (typ, [data]) = <instance>.store(message_set, command, flags)
        """
        return self.uid('STORE', message_set, command, flags)

    def thread(self, threading_algorithm, charset, *search_criteria):
        """IMAPrev1 extension THREAD command.

        (type, [data]) = <instance>.thread(threading_algorithm, charset, search_criteria, ...)
        """
        _search_criterion = []
        for criterion in search_criteria:
            criterion = str(criterion)
            if ' ' in criterion:
                for subcriterion in criterion.split():
                    _search_criterion.append(subcriterion)

            else:
                _search_criterion.append(criterion)

        search_criteria = tuple(list(_search_criterion))
        if not charset:
            charset = 'UTF-8'
        return self.uid('THREAD', threading_algorithm, charset, search_criteria)


class IMAP4_SSL(imaplib.IMAP4_SSL):

    def __init__(self, host='', port=imaplib.IMAP4_PORT, timeout=None, maxbytes=50000, keyfile=None, certfile=None, ssl_context=None):
        self.timeout = timeout
        if timeout:
            socket.setdefaulttimeout(timeout)
        else:
            if maxbytes:
                imaplib._MAXLINE = maxbytes
            if sys.version_info.major < 3:
                if ssl_context:
                    print("Warning: Defining `ssl_context` is not supported in Python 2's IMAP4_SSL implementation.")
                imaplib.IMAP4_SSL.__init__(self, host, port, keyfile, certfile)
            else:
                imaplib.IMAP4_SSL.__init__(self, host, port, keyfile, certfile, ssl_context)
        imaplib._MAXLINE = 200000

    def copy(self, message_set, new_mailbox):
        """Copy 'message_set' messages onto end of 'new_mailbox'.

        (typ, [data]) = <instance>.copy(message_set, new_mailbox)
        """
        return self.uid('COPY', message_set, new_mailbox)

    def fetch(self, message_set, message_parts='(RFC822)'):
        """Fetch (parts of) messages, using UID values.

        (typ, [data, ...]) = <instance>.fetch(message_set, message_parts)

        'message_parts' should be a string of selected parts
        enclosed in parentheses, eg: "(UID BODY[TEXT])".

        'data' are tuples of message part envelope and data.
        """
        if isinstance(message_set, bytes):
            message_set = message_set.decode('utf-8')
        return self.uid('FETCH', message_set, message_parts)

    def search(self, charset, *criteria):
        """Search mailbox for matching messages.

        (typ, [data]) = <instance>.search(charset, criterion, ...)

        'data' is space separated list of matching message UID numbers.
        If UTF8 is enabled, charset MUST be None.
        """
        return self.uid('SEARCH', charset, ' '.join(criteria))

    def sort(self, sort_criteria, charset, *search_criteria):
        """IMAP4rev1 extension SORT command.

        (typ, [data]) = <instance>.sort(sort_criteria, charset, search_criteria, ...)
        """
        _search_criterion = []
        for criterion in search_criteria:
            criterion = str(criterion)
            if ' ' in criterion:
                for subcriterion in criterion.split():
                    _search_criterion.append(subcriterion)

            else:
                _search_criterion.append(criterion)

        search_criteria = tuple(list(_search_criterion))
        while True:
            if sort_criteria[0] != '(':
                sort_criteria = '(' + sort_criteria
                continue
            if sort_criteria[(len(sort_criteria) - 1)] != ')':
                sort_criteria += ')'
                continue
            break

        if not charset:
            charset = 'UTF-8'
        return self.uid('SORT', sort_criteria, charset, ' '.join(search_criteria))

    def store(self, message_set, command, flags):
        """Alters flag dispositions for messages in mailbox, using UID values.

        (typ, [data]) = <instance>.store(message_set, command, flags)
        """
        return self.uid('STORE', message_set, command, flags)

    def thread(self, threading_algorithm, charset, *search_criteria):
        """IMAPrev1 extension THREAD command.

        (type, [data]) = <instance>.thread(threading_algorithm, charset, search_criteria, ...)
        """
        _search_criterion = []
        for criterion in search_criteria:
            criterion = str(criterion)
            if ' ' in criterion:
                for subcriterion in criterion.split():
                    _search_criterion.append(subcriterion)

            else:
                _search_criterion.append(criterion)

        search_criteria = tuple(list(_search_criterion))
        if not charset:
            charset = 'UTF-8'
        return self.uid('THREAD', threading_algorithm, charset, search_criteria)