# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimir/monitor/presence.py
# Compiled at: 2012-05-10 08:39:36
from wokkel.xmppim import PresenceClientProtocol

class Storage(object):

    def __init__(self, dbpool):
        self._dbpool = dbpool
        d = self._dbpool.runOperation("UPDATE presences\n                                         SET type='unavailable', show='',\n                                             status='', priority=0\n                                         WHERE type='available'")

        def eb(failure):
            print failure

        d.addErrback(eb)

    def set_presence(self, entity, available, show, status, priority):
        return self._dbpool.runInteraction(self._set_presence, entity, available, show, status, priority)

    def _set_presence(self, cursor, entity, available, show, status, priority):
        if available:
            type = 'available'
        else:
            type = 'unavailable'
        show = show or ''
        status = status or ''
        changed = False
        cursor.execute('SELECT presence_id, type, show FROM presences\n                          WHERE jid=%s AND resource=%s', (
         entity.userhost(), entity.resource))
        result = cursor.fetchone()
        print 'result: %r' % result
        if result:
            id, old_type, old_show = result
            if old_type == 'unavailable':
                cursor.execute('DELETE FROM presences WHERE presence_id=%s', id)
        if result and old_type == 'available':
            if show != old_show:
                print '  show != old_show'
                changed = True
            cursor.execute('UPDATE presences SET\n                              type=%s, show=%s, status=%s, priority=%s,\n                              last_updated=now()\n                              WHERE presence_id=%s', (
             type, show, status, priority, id))
        else:
            print '  new presence record'
            changed = True
            cursor.execute('INSERT INTO presences\n                              (type, show, status, priority, jid, resource)\n                              VALUES (%s, %s, %s, %s, %s, %s)', (
             type, show, status, priority,
             entity.userhost(), entity.resource))
        return changed

    def update_roster(self, changed, entity):
        return self._dbpool.runInteraction(self._update_roster, changed, entity)

    def _update_roster(self, cursor, changed, entity):
        print 'Updating roster for %r' % entity.full()
        cursor.execute("SELECT presence_id, resource FROM presences\n                          WHERE jid=%s ORDER by type, priority desc,\n                          (CASE WHEN type='available'\n                                THEN presence_id\n                                ELSE 0\n                           END), last_updated desc", entity.userhost())
        result = cursor.fetchone()
        top_id, top_resource = result
        cursor.execute('SELECT presence_id FROM roster WHERE jid=%s', entity.userhost())
        result = cursor.fetchone()
        print 'result 2: %r' % result
        if result:
            old_top_id = result[0]
            print '  old_top_id %d' % old_top_id
            if old_top_id != top_id:
                print '  old_top_id != top_id'
                changed = True
            elif entity.resource != top_resource:
                print '  we are not the top resource'
                changed = False
            cursor.execute('UPDATE roster SET presence_id=%s WHERE jid=%s', (
             top_id, entity.userhost()))
        else:
            changed = True
            cursor.execute('INSERT INTO roster\n                              (presence_id, jid) VALUES\n                              (%s, %s)', (
             top_id, entity.userhost()))
        return changed

    def remove_presences(self, entity):
        return self._dbpool.runInteraction(self._remove_presences, entity)

    def _remove_presences(self, cursor, entity):
        cursor.execute('DELETE FROM roster WHERE jid=%s', entity.userhost())
        cursor.execute('DELETE FROM presences WHERE jid=%s', entity.userhost())


class Monitor(PresenceClientProtocol):

    def __init__(self, storage):
        self.storage = storage
        self.callbacks = []

    def connectionInitialized(self):
        PresenceClientProtocol.connectionInitialized(self)
        self.available()

    def register_callback(self, f):
        self.callbacks.append(f)

    def store_presence(self, entity, available, show, status, priority):
        d = self.storage.set_presence(entity, available, show, status, priority)
        d.addCallback(self.storage.update_roster, entity)

        def cb(changed, entity):
            print 'Changed %r: %s' % (entity.full(), changed)
            if changed:
                for f in self.callbacks:
                    f(entity, available, show)

        d.addCallback(cb, entity)
        d.addErrback(self.error)

    def availableReceived(self, entity, show, statuses, priority):
        print 'available: %r' % entity.full()
        if statuses:
            status = statuses.popitem()[1]
        else:
            status = None
        print '  status: %r' % status
        self.store_presence(entity, True, show, status, priority)
        return

    def unavailableReceived(self, entity, statuses):
        if statuses:
            status = statuses.popitem()[1]
        else:
            status = None
        print '  status: %r' % status
        self.store_presence(entity, False, None, status, 0)
        return

    def error(self, failure):
        print failure


class RosterMonitor(Monitor):

    def connectionInitialized(self):
        self.send("<iq type='get'><query xmlns='jabber:iq:roster'/></iq>")
        Monitor.connectionInitialized(self)

    def subscribeReceived(self, entity):
        self.subscribed(entity)
        self.subscribe(entity)

    def unsubscribeReceived(self, entity):
        self.unsubscribed(entity)
        self.unsubscribe(entity)

    def unsubscribedReceived(self, entity):
        d = self.storage.remove_presences(entity)
        d.addErrback(self.error)