# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/fetch.py
# Compiled at: 2018-06-03 05:32:46
# Size of source mod 2**32: 7909 bytes
"""Functions returning an IMAP account state

Usage: imap-cli-read [options] [<mail_uid>...]

Options:
    -c, --config-file=<FILE>    Configuration file (`~/.config/imap-cli` by
                                default)
    -d, --directory=<DIR>       Directory in wich the search occur
    -s, --save=<DIR>            Save attachment in specified directory
    -v, --verbose               Generate verbose messages
    -h, --help                  Show help options.
    --version                   Print program version.

----
imap-cli-read 0.7
Copyright (C) 2014 Romain Soufflet
License MIT
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
"""
import collections, email
from email import header
import logging, os, sys, docopt, imap_cli
from imap_cli import config
from imap_cli import const
app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

def display(fetched_mail, browser=False):
    displayable_parts = list()
    other_parts = list()
    for part in fetched_mail['parts']:
        if part['content_type'] == 'text/plain':
            displayable_parts.append(part.get('as_string'))
        else:
            if not part['content_type'].startswith('text'):
                other_parts.append(part)

    if len(displayable_parts) == 0:
        for part in fetched_mail['parts']:
            if part['content_type'].startswith('text'):
                displayable_parts.append(part.get('as_string'))

    if browser:
        return '<br><br>'.join(displayable_parts).strip()
    else:
        output = [
         'From       : {}'.format(fetched_mail['headers']['From']),
         'Subject    : {}'.format(fetched_mail['headers']['Subject']),
         'Date       : {}'.format(fetched_mail['headers'].get('Date')),
         '',
         '\n\n'.join(displayable_parts).strip()]
        if len(other_parts) > 0:
            output.append('\nAttachment:')
            for part in other_parts:
                if part['filename']:
                    output.append('    {}'.format(part['filename']))

        return '{}\n'.format('\n'.join(output))


def fetch(imap_account, message_set=None, message_parts=None):
    """Return mails corresponding to mails_id.

    Keyword arguments:
    message_set     -- Iterable containing mails ID (integers)
    message_parts   -- Iterable of message part names or IMAP protocoles
                       ENVELOP string

    Available message_parts are listed in const.MESSAGE_PARTS, for more
    information checkout RFC3501
    """
    if message_set is None or not isinstance(message_set, collections.Iterable):
        if isinstance(message_set, int):
            message_set = [
             str(message_set)]
        else:
            log.error("Can't fetch email {}".format(message_set))
            return
        if len(message_set) == 0:
            log.error('No uid given')
            return
        if message_parts is None:
            message_parts = [
             'RFC822']
    else:
        request_message_set = ','.join(str(mail_id) for mail_id in message_set)
        request_message_parts = '({})'.format(' '.join(message_parts) if isinstance(message_parts, collections.Iterable) else message_parts)
        if imap_account.state != 'SELECTED':
            log.warning('No directory specified, selecting {}'.format(const.DEFAULT_DIRECTORY))
            imap_cli.change_dir(imap_account, const.DEFAULT_DIRECTORY)
        typ, data_bytes = imap_account.uid('FETCH', request_message_set, request_message_parts)
        data = []
        for mail in data_bytes:
            if len(mail) == 1:
                pass
            else:
                mail_parts = []
                for mail_part in mail:
                    mail_parts.append(mail_part.decode('utf-8'))

                data.append(mail_parts)

        if typ == const.STATUS_OK:
            return data


def get_charset(message, default='ascii'):
    """Get the message charset."""
    if message.get_content_charset():
        return message.get_content_charset()
    else:
        if message.get_charset():
            return message.get_charset()
        return default


def read(imap_account, mail_uid, directory=None, save_directory=None):
    """Return mail information within a dict."""
    if not isinstance(mail_uid, list):
        mail_uid = [
         mail_uid]
    raw_mails = fetch(imap_account, mail_uid)
    if raw_mails is None:
        log.error("Server didn't sent this email")
        yield
    for raw_mail in raw_mails or []:
        if not raw_mail is None:
            if len(raw_mail) == 1:
                pass
            else:
                mail = email.message_from_string(raw_mail[1])
                mail_headers = {}
                for header_name, header_value in mail.items():
                    value, encoding = header.decode_header(header_value)[0]
                    if encoding is not None:
                        value = value.decode(encoding)
                    mail_headers[header_name] = value

                message_parts = []
                for part in mail.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get_content_type().startswith('text'):
                        charset = get_charset(part, get_charset(mail))
                        message_parts.append({'content_type':part.get_content_type(), 
                         'data':part.as_string(), 
                         'as_string':part.get_payload(decode=True).decode(charset, 'replace')})
                    else:
                        if part.get_filename():
                            message_parts.append({'content_type':part.get_content_type(), 
                             'filename':part.get_filename(), 
                             'data':part.get_payload(decode=True)})
                            if save_directory is not None:
                                if os.path.isdir(save_directory):
                                    attachment_full_filename = os.path.join(save_directory, part.get_filename())
                                    with open(attachment_full_filename, 'wb') as (attachment):
                                        attachment.write(part.get_payload(decode=True))
                            if save_directory is not None:
                                log.error(' '.join([
                                 "Can't save attachment, directory {}",
                                 'does not exist']).format(save_directory))

                yield {'headers':mail_headers, 
                 'parts':message_parts}


def main():
    args = docopt.docopt(('\n'.join(__doc__.split('\n')[2:])), version=(const.VERSION))
    logging.basicConfig(level=(logging.DEBUG if args['--verbose'] else logging.INFO),
      stream=(sys.stdout))
    if len(args['<mail_uid>']) == 0:
        args['<mail_uid>'] = sys.stdin.read().strip().split()
    if len(args['<mail_uid>']) == 0:
        sys.stderr.write('\n'.join(__doc__.split('\n')[2:]))
        return 1
    conf = config.new_context_from_file((args['--config-file']), section='imap')
    if conf is None:
        return 1
    else:
        try:
            imap_account = (imap_cli.connect)(**conf)
            imap_cli.change_dir(imap_account, args['--directory'] or const.DEFAULT_DIRECTORY)
            fetched_mails = read(imap_account, (args['<mail_uid>']),
              save_directory=(args['--save']))
            if fetched_mails is None:
                log.error('Mail was not fetched, an error occured')
                return 1
            for fetched_mail in fetched_mails:
                sys.stdout.write(display(fetched_mail))

            imap_cli.disconnect(imap_account)
        except KeyboardInterrupt:
            log.info('Interrupt by user, exiting')

        return 0


if __name__ == '__main__':
    sys.exit(main())