# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/__init__.py
# Compiled at: 2018-06-03 05:36:57
# Size of source mod 2**32: 4591 bytes
"""IMAP basic helpers"""
import imaplib, logging, re
from imap_cli import const
from imap_cli import string
log = logging.getLogger('imap-cli')
LIST_DIR_RE = re.compile('\\((?P<flags>[^\\)]*)\\) "(?P<delimiter>[^"]*)" "(?P<directory>[^"]*)"')
STATUS_RE = re.compile('{directory} \\({messages_count} {recent} {unseen}\\)'.format(directory='"(?P<directory>.*)"',
  messages_count='MESSAGES (?P<mail_count>\\d{1,5})',
  recent='RECENT (?P<mail_recent>\\d{1,5})',
  unseen='UNSEEN (?P<mail_unseen>\\d{1,5})'))

def change_dir(imap_account, directory, read_only=True):
    if imap_account.state == 'SELECTED':
        imap_account.close()
    status, mail_count = imap_account.select(directory, read_only)
    if status == const.STATUS_OK:
        return mail_count[0]
    else:
        log.error("Can't select directory {}".format(directory))
        return -1


def connect(hostname, username, password=None, port=None, ssl=True, sasl_auth=None, sasl_ir=None):
    """Return an IMAP account object (see imaplib documentation for details)

    .. versionadded:: 0.1

    Example:

    >>> import imap_cli
    >>> from imap_cli import config
    >>> conf = config.new_context_from_file(section='imap')
    >>> imap_cli.connect(**conf)
    <imaplib.IMAP4_SSL instance at 0x7fccd57579e0>
    """
    if port is None:
        port = const.DEFAULT_PORT if ssl is False else const.DEFAULT_SSL_PORT
    else:
        if ssl is True:
            log.debug('Connecting with SSL on {}'.format(hostname))
            imap_account = imaplib.IMAP4_SSL(hostname, port)
        else:
            log.debug('Connecting on {}'.format(hostname))
            imap_account = imaplib.IMAP4(hostname, port)
        if sasl_auth:
            imap_account.authenticate(sasl_auth, lambda x: sasl_ir)
        else:
            imap_account.login(username, password)
    return imap_account


def disconnect(imap_account):
    """Disconnect IMAP account object

    .. versionadded:: 0.1

    Example:

    >>> import imap_cli
    >>> from imap_cli import config
    >>> conf = config.new_context_from_file(section='imap')
    >>> imap_account = imap_cli.connect(**conf)
    >>> imap_account
    <imaplib.IMAP4_SSL instance at 0x7fccd57579e0>
    >>> imap_cli.change_dir(imap_account, 'INBOX')
    >>> imap_cli.disconnect(imap_account)
    """
    log.debug('Disconnecting from {}'.format(imap_account.host))
    if imap_account.state == 'SELECTED':
        imap_account.close()
    if imap_account.state != 'LOGOUT':
        imap_account.logout()


def list_dir(imap_account):
    status, data_bytes = imap_account.list()
    data = [data_byte.decode('utf-8') for data_byte in data_bytes]
    if status == const.STATUS_OK:
        for datum in data:
            datum_match = LIST_DIR_RE.match(datum)
            if datum_match is None:
                log.warning('Ignoring "LIST" response part : {}'.format(datum))
            else:
                datum_dict = datum_match.groupdict()
                yield {'flags':datum_dict['flags'], 
                 'delimiter':datum_dict['delimiter'], 
                 'directory':datum_dict['directory']}


def status(imap_account):
    """Return an interator of directory status.

    Each directory status provide the following keys::

        u'count'    # Number of mail in directory
        u'directory # Name of directory
        u'recent    # Number of recent mail
        u'unseen    # Number of unseen mail

    .. versionadded:: 0.1

    Example:

    >>> import imap_cli
    >>> from imap_cli import config
    >>> conf = config.new_context_from_file(section='imap')
    >>> imap_account = imap_cli.connect(**conf)
    >>> for directory_status in imap_cli.status(imap_account):
    >>>     print directory_status
    """
    for directory_info in list_dir(imap_account):
        status, data = imap_account.status(directory_info['directory'], '(MESSAGES RECENT UNSEEN)')
        if status != const.STATUS_OK:
            log.warning('Wrong status : {}'.format(repr(data)))
        else:
            status_match = STATUS_RE.match(data[0])
            if status_match is None:
                log.warning('Ignoring directory : {}'.format(repr(data)))
            else:
                group_dict = status_match.groupdict()
                yield {'directory':string.decode(group_dict['directory']), 
                 'unseen':group_dict['mail_unseen'], 
                 'count':group_dict['mail_count'], 
                 'recent':group_dict['mail_recent']}