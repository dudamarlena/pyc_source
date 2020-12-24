# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimir/monitor/news.py
# Compiled at: 2012-05-10 09:32:59
import re, time, feedparser, simplejson
from zope.interface import Interface, implements
from twisted.application import service
from twisted.internet import reactor
from twisted.python import components, failure
from twisted.words.xish import domish
from wokkel import pubsub
from wokkel.iwokkel import IXMPPHandler
SGMLTAG = re.compile('<.+?>', re.DOTALL)
NS_ATOM = 'http://www.w3.org/2005/Atom'

class FeedParserEncoder(simplejson.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, time.struct_time):
            return tuple(obj)
        else:
            if isinstance(obj, Exception):
                return failure.Failure(obj).getTraceback()
            return simplejson.JSONEncoder.default(self, obj)


class NoNotify(Exception):
    pass


class INewsService(Interface):

    def process(channel, items):
        """
        Process new items for channel

        @param items: atom entries
        @type items: L{domish.Element}
        """
        pass


class NewsService(service.Service):
    implements(INewsService)

    def __init__(self, presenceMonitor, dbpool):
        self._dbpool = dbpool
        presenceMonitor.register_callback(self.onPresenceChange)

    def error(self, failure):
        print failure

    def onPresenceChange(self, entity, available, show):
        if available:
            if show not in ('away', 'xa', 'dnd', 'chat'):
                show = 'online'
        else:
            show = 'offline'
        print '  presence change to %s for %r', (show, entity.full())
        reactor.callLater(5, self.pageNotify, entity, show)

    def pageNotify(self, entity, show):
        d = self._dbpool.runInteraction(self._checkNotify, entity, show)
        d.addCallback(self._doNotify, entity)
        d.addCallback(self._setNotified)
        d.addErrback(lambda failure: failure.trap(NoNotify))
        d.addErrback(self.error)

    def _checkNotify(self, cursor, entity, show):
        cursor.execute('SELECT user_id, message_type, ssl,\n                                 count(news_id) as count\n                          FROM auth_user\n                          NATURAL JOIN news_prefs\n                          NATURAL JOIN news_notify_presences\n                          NATURAL JOIN news_page\n                          NATURAL JOIN news_flags\n                          NATURAL JOIN news\n                          WHERE jid=%s AND\n                                NOT suspended AND\n                                presence=%s AND\n                                NOT notified AND\n                                date>last_visit\n                          GROUP BY user_id, message_type, ssl', (
         entity.userhost(),
         show))
        result = cursor.fetchone()
        if not result:
            return failure.Failure(NoNotify())
        return result

    def _doNotify(self, result, entity):
        userId, messageType, ssl, count = result
        title = 'New news on Mimír!'
        link = '%s://mimir.ik.nu/news' % (ssl and 'https' or 'http')
        description = 'There '
        if count == 1:
            description += 'is 1 new item'
        else:
            description += 'are %s new items' % count
        description += ' on your news page'
        self.notifier.sendNotification(entity.full(), True, messageType, title, link, description)
        return userId

    def _setNotified(self, userId):
        return self._dbpool.runOperation('UPDATE news_page SET notified=true\n                                            WHERE user_id=%s', userId)

    def process(self, channel, items):
        print 'Got entries: %r' % items
        d = self._dbpool.runInteraction(self._processItems, channel, items)
        d.addCallback(self.notify)
        d.addErrback(self.error)

    def _processItems(self, cursor, channel, items):
        cursor.execute('SELECT title from channels WHERE channel=%s', channel)
        title = cursor.fetchone()[0]
        print 'Channel title: %r' % title
        feedDocument = domish.Element((NS_ATOM, 'feed'))
        for item in items:
            feedDocument.addChild(item)

        feed = feedparser.parse(feedDocument.toXml().encode('utf-8'))
        entries = feed.entries
        cursor.execute('SELECT user_id, jid, notify,\n                                 description_in_notify, message_type,\n                                 store_offline, notify_items\n                          FROM news_prefs\n                            NATURAL JOIN news_subscriptions\n                            NATURAL JOIN news_notify\n                          WHERE NOT suspended AND channel=%s', channel)
        notifyList = cursor.fetchall()
        notifications = []
        markUnread = []
        for userId, jid, notify, descriptionInNotify, messageType, storeOffline, notifyItems in notifyList:
            if notify and notifyItems:
                notifications.append((jid,
                 descriptionInNotify,
                 messageType))
            elif storeOffline:
                markUnread.append(userId)

        notifyItems = []
        for entry in entries:
            newsId = self._storeItem(cursor, channel, entry)
            if newsId:
                for userId in markUnread:
                    cursor.execute('INSERT INTO news_flags\n                                      (user_id, news_id, unread) VALUES\n                                      (%s, %s, true)', (
                     userId, newsId))
                    cursor.execute('UPDATE news_page SET notified=false\n                                      WHERE user_id=%s', userId)

                notifyItems.append(entry)

        return (
         title, notifications, notifyItems)

    def _extractBasics(self, entry):
        if 'title' in entry:
            title = entry.title
            if 'source' in entry and 'title' in entry.source:
                content = '%s: %s' % (entry.source.title, title)
            if entry.title_detail == 'text/plain':
                title = feedparser._xmlescape(title)
        else:
            title = ''
        if 'link' in entry:
            link = entry.get('feedburner_origlink', entry.link)
        else:
            link = ''
        content = None
        if 'content' in entry and entry.content[0].value:
            content = entry.content[0]
        else:
            if 'summary' in entry:
                content = entry.summary_detail
            if content:
                value = content.value
                if content.type == 'text/plain':
                    value = feedparser._xmlescape(value)
                description = value
            else:
                description = ''
            date = None
            for attribute in ('updated', 'published', 'created'):
                if attribute in entry:
                    date = getattr(entry, '%s_parsed' % attribute)

        date = time.strftime('%Y-%m-%d %H:%M:%Sz', date or time.gmtime())
        return (
         title, link, description, date)

    def _storeItem(self, cursor, channel, entry):
        title, link, description, date = self._extractBasics(entry)
        json = simplejson.dumps(entry, cls=FeedParserEncoder)
        print 'Storing item: %r' % entry.id
        cursor.execute('UPDATE news\n                          SET title=%s, description=%s, date=%s, parsed=%s\n                          WHERE channel=%s AND link=%s', (
         title, description, date, json, channel, link))
        if cursor.rowcount == 1:
            print 'UPDATE'
            return None
        else:
            cursor.execute('INSERT INTO news\n                          (channel, title, link, description, date, parsed)\n                          VALUES\n                          (%s, %s, %s, %s, %s, %s)', (
             channel, title, link, description, date, json))
            print 'INSERT',
            cursor.execute('SELECT news_id FROM news\n                          WHERE channel=%s and link=%s', (
             channel, link))
            newsId = cursor.fetchone()[0]
            print newsId
            return newsId

    def notify(self, result):
        channelTitle, notifications, entries = result
        for entry in entries:
            title = '%s: %s' % (channelTitle,
             entry.get('title', '-- no title --'))
            link = entry.get('link', '')
            description = entry.get('summary')
            if description:
                description = SGMLTAG.sub('', description)
                description = domish.unescapeFromXml(description)
                description = description.rstrip() or None
            for jid, descriptionInNotify, messageType in notifications:
                self.notifier.sendNotification(jid, descriptionInNotify, messageType, title, link, description)

        return


class XMPPHandlerFromService(pubsub.PubSubClient):

    def __init__(self, service):
        self.service = service

    def sendNotification(self, jid, descriptionInNotify, messageType, title, link, description):
        message = domish.Element((None, 'message'))
        message['to'] = jid
        message['type'] = messageType
        if messageType == 'chat':
            body = '%s\n%s' % (title, link)
            if description and descriptionInNotify:
                body += '\n\n%s\n\n' % description
            message.addElement('body', None, body)
        elif messageType == 'headline':
            message.addElement('subject', None, title)
            if description:
                message.addElement('body', None, description)
            oob = message.addElement(('jabber:x:oob', 'x'))
            oob.addElement('url', None, link)
            oob.addElement('desc', None, title)
        print 'Sending: %r' % message.toXml()
        self.send(message)
        return

    def itemsReceived(self, event):
        m = re.match('^mimir/news/(.+)$', event.nodeIdentifier)
        if not m:
            return
        channel = m.group(1)
        entries = (item.entry for item in event.items if item.entry and item.entry.uri == NS_ATOM)
        self.service.process(channel, entries)


components.registerAdapter(XMPPHandlerFromService, INewsService, IXMPPHandler)