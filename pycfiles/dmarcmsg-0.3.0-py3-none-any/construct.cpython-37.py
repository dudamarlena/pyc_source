# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/teward/VCS Repos/GitLab/dmarcmsg/dmarcmsg/construct.py
# Compiled at: 2019-11-06 16:11:13
# Size of source mod 2**32: 7516 bytes
import datetime, email, email.utils, time
from typing import Union
AnyStr = Union[(str, bytes)]

def _construct_dmarc_message(msg, list_name, list_address, moderated=False, allow_posts=True, quotes_in_from=True):
    msg_components = {'To':msg['To'], 
     'From':msg['From'],  'Subject':msg['Subject']}
    retain_headers = [
     'to', 'subject', 'from', 'date', 'content-type', 'mime-version',
     'content-language', 'accept-language', 'auto-submitted', 'precedence',
     'content-transfer-encoding']
    newmsg = email.message_from_bytes(msg.as_bytes())
    for key in newmsg.keys():
        if str(key).lower() not in retain_headers:
            del newmsg[key]

    newmsg['Sender'] = list_address
    newmsg.replace_header('To', msg_components['To'])
    from_ = email.utils.parseaddr(newmsg['From'])
    if quotes_in_from:
        newfromfmt = "'{}' via '{}'"
    else:
        newfromfmt = '{} via {}'
    if from_[0] and from_[0] != '':
        newfrom = email.utils.formataddr((newfromfmt.format(from_[0], list_name), list_address))
    else:
        newfrom = email.utils.formataddr((newfromfmt.format(from_[1], list_name), list_address))
    newmsg.replace_header('From', newfrom)
    newmsg['Reply-To'] = msg_components['From']
    newmsg['CC'] = '{}'.format(msg_components['From'])
    newmsg['Message-ID'] = email.utils.make_msgid()
    if 'date' not in [key.lower() for key in newmsg.keys()]:
        newmsg['Date'] = email.utils.formatdate(time.mktime(datetime.datetime.utcnow().timetuple()))
    if list_name and list_name != list_address:
        try:
            newmsg.replace_header('List-Id', '{} <{}>'.format(list_name, list_address))
        except KeyError:
            newmsg['List-Id'] = '{} <{}>'.format(list_name, list_address)

    else:
        try:
            newmsg.replace_header('List-Id', '<{}>'.format(list_address))
        except KeyError:
            newmsg['List-Id'] = '<{}>'.format(list_address)

        if allow_posts:
            if list_address:
                if list_address != '':
                    try:
                        newmsg.replace_header('List-Post', '<mailto:{}>'.format(list_address))
                    except KeyError:
                        newmsg['List-Post'] = '<mailto:{}>'.format(list_address)

            if moderated:
                newmsg.replace_header('List-Post', newmsg['List-Post'] + ' (Postings are Moderated)')
        else:
            try:
                newmsg.replace_header('List-Post', 'NO (posting not allowed on this list)')
            except KeyError:
                newmsg['List-Post'] = 'NO (posting not allowed on this list)'

        return newmsg


def from_string(msg_string, list_name, list_address, moderated=False, allow_posts=True, quotes_in_from=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a
    string-like object.
    :param msg_string: A string-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is
    "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is
    "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent
    out to a list.
    """
    return _construct_dmarc_message(email.message_from_string(msg_string), list_name, list_address, moderated, allow_posts, quotes_in_from)


def from_bytes(msg_bytes, list_name, list_address, moderated=False, allow_posts=True, quotes_in_from=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a
    bytes-like object.
    :param msg_bytes: A bytes-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is
    "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is
    "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent
    out to a list.
    """
    return _construct_dmarc_message(email.message_from_bytes(msg_bytes), list_name, list_address, moderated, allow_posts, quotes_in_from)


def from_message(msg_obj, list_name, list_address, moderated=False, allow_posts=True, quotes_in_from=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing email message
    object.
    :param msg_obj: An instance of email.message.Message containing the original email message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is
    "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is
    "True"
    :param quotes_in_from:
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent
    out to a list.
    """
    return _construct_dmarc_message(msg_obj, list_name, list_address, moderated, allow_posts, quotes_in_from)