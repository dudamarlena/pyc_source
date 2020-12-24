# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/email/templates.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = b'\n.. py:module:: bridgedb.email.templates\n    :synopsis: Templates for formatting emails sent out by the email\n               distributor.\n\nbridgedb.email.templates\n========================\n\nTemplates for formatting emails sent out by the email distributor.\n'
from __future__ import print_function
from __future__ import unicode_literals
import logging, os
from datetime import datetime
from bridgedb import strings
from bridgedb.email.distributor import MAX_EMAIL_RATE

def addCommands(template):
    """Add some text telling a client about supported email command, as well as
    which Pluggable Transports are currently available.
    """
    cmdlist = []
    cmdlist.append(template.gettext(strings.EMAIL_MISC_TEXT.get(3)))
    for cmd, desc in strings.EMAIL_COMMANDS.items():
        command = b'  '
        command += cmd
        while not len(command) >= 25:
            command += b' '

        command += template.gettext(desc)
        cmdlist.append(command)

    commands = (b'\n').join(cmdlist) + b'\n\n'
    commands += template.gettext(strings.EMAIL_MISC_TEXT.get(5))
    commands += b'\n'
    for pt in strings._getSupportedTransports():
        commands += b'  ' + pt + b'\n'

    return commands


def addGreeting(template, clientName=None, welcome=False):
    greeting = b''
    if not clientName:
        greeting = template.gettext(strings.EMAIL_MISC_TEXT[7])
    else:
        greeting = template.gettext(strings.EMAIL_MISC_TEXT[6]) % clientName
    if greeting:
        if welcome:
            greeting += b' '
            greeting += template.gettext(strings.EMAIL_MISC_TEXT[4])
        greeting += b'\n\n'
    return greeting


def addKeyfile(template):
    return b'%s\n\n' % strings.BRIDGEDB_OPENPGP_KEY


def addBridgeAnswer(template, answer):
    bridgeLines = template.gettext(strings.EMAIL_MISC_TEXT[0])
    bridgeLines += b'\n\n'
    bridgeLines += template.gettext(strings.EMAIL_MISC_TEXT[1])
    bridgeLines += b'\n\n'
    bridgeLines += b'%s\n\n' % answer
    return bridgeLines


def addHowto(template):
    """Add help text on how to add bridges to Tor Browser.

    :type template: ``gettext.NullTranslation`` or ``gettext.GNUTranslation``
    :param template: A gettext translations instance, optionally with fallback
        languages set.
    """
    howToTBB = template.gettext(strings.HOWTO_TBB[1]) % strings.EMAIL_SPRINTF[b'HOWTO_TBB1']
    howToTBB += b'\n\n'
    howToTBB += template.gettext(strings.HOWTO_TBB[2])
    howToTBB += b'\n\n'
    howToTBB += (b'\n').join([ (b'> {0}').format(ln) for ln in template.gettext(strings.HOWTO_TBB[3]).split(b'\n')
                             ])
    howToTBB += b'\n\n'
    howToTBB += template.gettext(strings.HOWTO_TBB[4])
    howToTBB += b'\n\n'
    howToTBB += strings.EMAIL_REFERENCE_LINKS.get(b'HOWTO_TBB1')
    howToTBB += b'\n\n'
    return howToTBB


def addFooter(template, clientAddress=None):
    """Add a footer::

        --
        <3 BridgeDB
       ________________________________________________________________________
       Public Keys: https://bridges.torproject.org/keys

       This email was generated with rainbows, unicorns, and sparkles
       for alice@example.com on Friday, 09 May, 2014 at 18:59:39.

    :type template: ``gettext.NullTranslation`` or ``gettext.GNUTranslation``
    :param template: A gettext translations instance, optionally with fallback
        languages set.
    :type clientAddress: :api:`twisted.mail.smtp.Address`
    :param clientAddress: The client's email address which should be in the
        ``To:`` header of the response email.
    """
    now = datetime.utcnow()
    clientAddr = clientAddress.addrstr
    footer = b' --\n'
    footer += b' <3 BridgeDB\n'
    footer += b'_' * 70
    footer += b'\n'
    footer += template.gettext(strings.EMAIL_MISC_TEXT[8])
    footer += b': https://bridges.torproject.org/keys\n'
    footer += template.gettext(strings.EMAIL_MISC_TEXT[9]) % (
     clientAddr,
     now.strftime(b'%A, %d %B, %Y'),
     now.strftime(b'%H:%M:%S'))
    footer += b'\n\n'
    return footer


def buildKeyMessage(template, clientAddress=None):
    message = addKeyfile(template)
    message += addFooter(template, clientAddress)
    return message


def buildWelcomeText(template, clientAddress=None):
    sections = []
    sections.append(addGreeting(template, clientAddress.local, welcome=True))
    commands = addCommands(template)
    sections.append(commands)
    welcome = template.gettext(strings.WELCOME[0]) % strings.EMAIL_SPRINTF[b'WELCOME0']
    welcome += template.gettext(strings.WELCOME[1])
    welcome += template.gettext(strings.WELCOME[2]) % strings.EMAIL_SPRINTF[b'WELCOME2']
    sections.append(welcome)
    message = (b'\n\n').join(sections)
    message += strings.EMAIL_REFERENCE_LINKS.get(b'WELCOME0')
    message += b'\n\n'
    message += addFooter(template, clientAddress)
    return message


def buildAnswerMessage(template, clientAddress=None, answer=None):
    try:
        message = addGreeting(template, clientAddress.local)
        message += addBridgeAnswer(template, answer)
        message += addHowto(template)
        message += b'\n\n'
        message += addCommands(template)
        message += b'\n\n'
        message += addFooter(template, clientAddress)
    except Exception as error:
        logging.error(b'Error while formatting email message template:')
        logging.exception(error)

    return message


def buildSpamWarning(template, clientAddress=None):
    message = addGreeting(template, clientAddress.local)
    try:
        message += template.gettext(strings.EMAIL_MISC_TEXT[0])
        message += b'\n\n'
        message += template.gettext(strings.EMAIL_MISC_TEXT[2]) % str(MAX_EMAIL_RATE / 3600)
        message += b'\n\n'
        message += addFooter(template, clientAddress)
    except Exception as error:
        logging.error(b'Error while formatting email spam template:')
        logging.exception(error)

    return message