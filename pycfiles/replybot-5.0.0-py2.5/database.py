# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/database.py
# Compiled at: 2008-08-09 12:39:34
"""Manage the database."""
from __future__ import with_statement
__metaclass__ = type
__all__ = [
 'Corruption',
 'Database',
 'Entry',
 'Notice',
 'Version',
 'Whitelist']
import re, os, sys, time, errno, logging, datetime, pkg_resources
from email.utils import parseaddr
from storm.locals import *
from botlib import version
from botlib.configuration import config
from botlib.i18n import _
from botlib.reply import do_reply
SCHEMA_KEY = 'DatabaseSchema'
PROGRAM_KEY = 'Replybot'
COUNT_KEY = 'Invocation'
log = logging.getLogger('replybot')

class Corruption(Exception):
    """Database is corrupted"""
    pass


class Entry(Storm):
    __storm_table__ = 'entry'
    id = Int(primary=True)
    address = Unicode()
    last_sent = DateTime()
    context = Unicode()

    def __init__(self, address, last_sent, context):
        self.address = unicode(address)
        self.last_sent = last_sent
        self.context = unicode(context)


class Whitelist(Storm):
    __storm_table__ = 'whitelist'
    id = Int(primary=True)
    matcher = Unicode()
    is_pattern = Bool()

    def __init__(self, matcher):
        matcher = unicode(matcher)
        if matcher.startswith('^'):
            self.is_pattern = True
            self.matcher = matcher[1:]
        else:
            self.is_pattern = False
            self.matcher = matcher


class Notice(Storm):
    __storm_table__ = 'notice'
    id = Int(primary=True)
    filename = Unicode()
    uri = Unicode()
    retrieved = DateTime()

    def __init__(self, filename, uri, retrieved):
        self.filename = unicode(filename)
        self.uri = unicode(uri)
        self.retrieved = retrieved


class Version(Storm):
    __storm_table__ = 'version'
    id = Int(primary=True)
    component = Unicode()
    version = Int()

    def __init__(self, component, version):
        self.component = unicode(component)
        self.version = version


class Database:
    """Basic interface to the database."""

    def __init__(self, uri):
        """Initialize the database connection.

        :param url: The database url
        :type url: string
        :raise Corruption: when the schema version in the database does not
            match the expected schema version.
        """
        log.debug('Using database url: %s', uri)
        database = create_database(uri)
        self.store = store = Store(database)
        table_names = [ item[0] for item in store.execute('select tbl_name from sqlite_master;')
                      ]
        if 'version' not in table_names:
            schema = pkg_resources.resource_string('botlib', 'replybot.sql')
            for statement in schema.split(';'):
                store.execute(statement + ';')

        v = store.find(Version, component=SCHEMA_KEY).one()
        if v is None:
            v = Version(SCHEMA_KEY, version.__schema__)
            store.add(v)
            v = Version(PROGRAM_KEY, version.HEX_VERSION)
            store.add(v)
        elif v.version != version.__schema__:
            raise Corruption('Unexpected schema version: %d' % v.version)
        v = store.find(Version, component=COUNT_KEY).one()
        if v is None:
            v = Version(COUNT_KEY, 0)
            store.add(v)
        else:
            v.version += 1
        log.debug('Invocation: %s', v.version)
        store.commit()
        return

    def get_version(self, component):
        """Return the version of the given component.

        :param component: the component key to look up
        :type component: string
        :return: the component's version
        :rtype: Version
        """
        return self.store.find(Version, Version.component == unicode(component)).one()

    def get_entry(self, address, context):
        """Get a matching entry.

        :param address: the email address to find
        :type address: string
        :param context: the reply context
        :type context: string
        :return: the matching entry or None
        :rtype: Entry
        """
        return self.store.find(Entry, Entry.address == unicode(address), Entry.context == unicode(context)).one()

    @property
    def entries(self):
        """All the entries, in no particular order."""
        for entry in self.store.find(Entry):
            yield entry

    def get_notice(self, uri):
        """Get the notice matching a uri.

        :param uri: the uri of the notice
        :type uri: string
        :return: the notice text or None
        :rtype: string
        """
        return self.store.find(Notice, Notice.uri == unicode(uri)).one()

    def is_whitelisted(self, address):
        """Return whether the address is whitelisted or not.

        :param address: the address to check
        :type address: string
        :return: True if the address is whitelisted
        :rtype: bool
        """
        match = self.store.find(Whitelist, Whitelist.matcher == unicode(address)).one()
        if match is not None:
            return True
        matchers = self.store.find(Whitelist, Whitelist.is_pattern == True)
        for matcher in matchers:
            if re.match(matcher.matcher, address, re.IGNORECASE):
                return True

        return False

    def put_whitelist(self, pattern):
        """Add a pattern or address to the whitelist.

        :param pattern: the pattern or address.  If the pattern starts with
            the caret (^) character, it is interpreted as a regular
            expression.  Otherwise it is interpreted as a literal address.
        :type pattern: string
        """
        if pattern.startswith('^'):
            is_pattern = True
            matcher = pattern[1:]
        else:
            is_pattern = False
            matcher = pattern
        matcher = self.store.find(Whitelist, Whitelist.matcher == unicode(matcher), Whitelist.is_pattern == is_pattern).one()
        if matcher is None:
            whitelist = Whitelist(pattern)
            self.store.add(whitelist)
            self.store.commit()
        return

    def purge_whitelisted(self):
        """Purge the whitelist of all entries."""
        self.store.find(Whitelist).remove()
        log.debug('Whitelist purged')
        self.store.commit()

    def put_notice(self, filename, uri, retrieved):
        """Add a notice to the database.

        :param filename: the filename to store the notice in the cache as
        :type filename: string
        :param uri: the uri of the notice (i.e. where it was downloaded from)
        :type uri: string
        :param retrieved: the date the notice was downloaded from the uri
        :type retrieved: datetime
        :return: the Notice object
        :rtype: Notice
        """
        notice = Notice(filename=filename, uri=uri, retrieved=retrieved)
        self.store.add(notice)
        self.store.commit()
        return notice

    def purge_notices(self, cache_directory):
        """Purge all notices from the database and cache.

        :param cache_directory: the directory containing the cached notices
        :type cache_directory: string
        """
        self.store.find(Notice).remove()
        log.debug('Notices purged')
        for filename in os.listdir(cache_directory):
            try:
                purgefile = os.path.join(cache_directory, filename)
                log.debug('Purging cache file: %s', purgefile)
                os.remove(purgefile)
            except OSError, error:
                if e.errno != errno.ENOENT:
                    raise

        self.store.commit()

    def put_entry(self, address, last_sent, context):
        """Put an entry representing a sent reply.

        :param address: the email address we're recording a response to
        :type address: string
        :param last_sent: the date the last response was sent
        :type last_sent: datetime
        :param context: the reply context
        :type context: string
        :return: the recorded entry
        :rtype: Entry
        """
        entry = Entry(address=address, last_sent=last_sent, context=context)
        self.store.add(entry)
        self.store.commit()
        return entry

    def purge_entries(self, context=None):
        """Purge all entries for the given key.

        :param context: the reply context to purge.  If None (the default),
            purge all entries for all contexts.
        :type context: string or None
        """
        if context is None:
            self.store.find(Entry).remove()
            log.debug('Purged all addresses in all contexts')
        else:
            self.store.find(Entry, Entry.context == context).remove()
            log.debug('Purged all addresses for context: %s', context)
        self.store.commit()
        return

    def do_purges(self, which):
        """Purge some or all of the database.

        :param which: what to purge; can be one of 'notices', 'replies', or
            'whitelist', or 'all'.
        :type which: sequence of strings
        """
        purge_set = set(which)
        if 'all' in purge_set:
            purge_set.update(('notices', 'replies', 'whitelist'))
        if 'notices' in purge_set:
            self.purge_notices(config.cache_directory)
            log.info(_('Notices cache has been purged'))
        if 'replies' in purge_set:
            self.purge_entries()
            log.info(_('Reply times have been purged'))
        if 'whitelist' in purge_set:
            self.purge_whitelisted()
            log.info(_('Whitelist has been purged'))

    def do_whitelist(self, additions, whitelist_file=None):
        """Add to the whitelist.

        :param additions: the set of whitelist additions, as accepted by
            `put_whitelist()`
        :type additions: sequence
        :param whitelist_file: the name of a text file containing whitelist
            patterns as accepted by `put_whitelist()`
        :type whitelist_file: string
        """
        for pattern in additions:
            self.put_whitelist(pattern)

        if not whitelist_file:
            return
        with open(whitelist_file) as (fp):
            for line in fp:
                line = line[:-1]
                if line.startswith('^'):
                    self.put_whitelist(line)
                else:
                    (realname, address) = parseaddr(line)
                    self.put_whitelist(address)

    def process_message(self, msg):
        """Process a message.

        :param msg: the message object
        :type msg: email.message.Message
        :return: True if a reply was sent
        :rtype: bool
        """
        message_id = msg.get('message-id', '(no message id available)')
        precedence = msg.get('precedence', '').lower()
        if precedence in ('bulk', 'junk', 'list'):
            log.info('%s No reply sent to Precedence %s', message_id, precedence)
            return False
        if 'list-id' in msg:
            log.info('%s No reply sent to List-ID: %s', message_id, msg.get('list-id', '(empty)'))
            return False
        sender_from = msg.get('from')
        if sender_from is None:
            log.info('%s No reply sent to missing sender', message_id)
            return False
        (realname, sender) = parseaddr(sender_from)
        if not sender:
            log.info('%s No reply sent to empty sender', message_id)
            return False
        sender = sender.lower()
        if msg.get('return-path') == '<>':
            log.info('%s Not replying to bounce', message_id)
            return False
        ack = msg.get('x-ack', '').lower()
        if ack == 'no':
            log.info('%s Not replying to X-Ack: no', message_id)
            return False
        elif config.options.testing and ack == 'yes':
            self.do_reply(msg, sender)
            return True
        if self.is_whitelisted(sender):
            log.info('%s Not replying to whitelisted address: %s', message_id, sender)
            return False
        entry = self.get_entry(sender, config.reply_context)
        if entry is None:
            do_reply(msg, sender)
            return True
        now = datetime.datetime.now()
        if entry.last_sent and now < entry.last_sent + config.grace_period:
            log.info('Not replying to graced address %s:%s %s', config.reply_context, sender, message_id)
            return
        do_reply(msg, sender)
        return