# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevogears/visit.py
# Compiled at: 2008-01-19 12:10:14
"""schevogears visit support.

For copyright, license, and warranty, see bottom of file.
"""
from datetime import datetime, timedelta
import cherrypy
from turbogears.util import DictObj
import turbogears.visit.api as visitapi
from schevogears.database import package_database
import logging
log = logging.getLogger('turbogears.visit')
db = None

def schevo_to_dict(obj):
    d = obj.sys.fields().value_map()
    d['_oid'] = obj.sys.oid
    d['_rev'] = obj.sys.rev
    return d


def start_extension():
    """Overridden extension started for visitor tracking."""
    if not cherrypy.config.get('visit.on', False):
        return
    log.info('Visit tracking starting.')
    from schevogears import visit as sgvisit
    sgvisit.db = package_database()
    visitapi._manager = sgvisit.SchevoVisitManager(timedelta(0, 3600))
    filter = sgvisit.VisitFilter()
    if not hasattr(cherrypy.root, '_cp_filters'):
        cherrypy.root._cp_filters = []
    cherrypy.root._cp_filters.append(filter)


def shutdown_extension():
    if not cherrypy.config.get('visit.on', False):
        return
    log.info('Visit tracking shutting down.')
    if visitapi._manager:
        visitapi._manager.shutdown()


class VisitFilter(visitapi.VisitFilter):

    def new_visit(self):
        log.info('Creating new visit')
        now = datetime.now()
        visit_key = self._generate_key()
        tx = db.IdentityVisit.t.create(key=visit_key, expires=now + self.timeout)
        visit = db.execute(tx)
        visit = DictObj(schevo_to_dict(visit))
        visit['id'] = visit['_oid']
        visit['is_new'] = True
        self.send_cookie(visit_key)
        for plugin in visitapi._plugins:
            plugin.new_visit(visit.id)

        return visit

    def get_visit(self):
        cookies = cherrypy.request.simpleCookie
        if self.cookie_name not in cookies:
            return self.new_visit()
        now = datetime.now()
        visit_key = cookies[self.cookie_name].value
        lock = db.read_lock()
        try:
            visit = db.IdentityVisit.findone(key=visit_key)
            if visit and now < visit.expires:
                visitapi._manager.update_visit(visit, now + self.timeout)
                visit = DictObj(schevo_to_dict(visit))
                visit['id'] = visit['_oid']
                visit['is_new'] = False
                return visit
            log.debug('Visit (%s) has expired', visit_key)
            return self.new_visit()
        finally:
            lock.release()


class SchevoVisitManager(visitapi.BaseVisitManager):

    def clean_queue(self):
        try:
            self.lock.acquire()
            queue = self.queue
            self.queue = dict()
            self.lock.release()
        except:
            self.lock.release()
            raise

        for (visit, expires) in queue.iteritems():
            if visit in db.IdentityVisit:
                tx = visit.t.update(expires=expires)
                db.execute(tx)

    def new_visit_with_key(self, visit_key):
        lock = db.write_lock()
        try:
            tx = db.IdentityVisit.t.create(key=visit_key, expires=datetime.now() + self.timeout)
            db.execute(tx)
        finally:
            lock.release()

        return visitapi.Visit(visit_key, True)

    def visit_for_key(self, visit_key):
        lock = db.read_lock()
        try:
            visit = db.IdentityVisit.findone(key=visit_key)
            now = datetime.now()
            if visit is None or visit.expires < now:
                return
            self.update_visit(visit_key, now + self.timeout)
        finally:
            lock.release()

        return visitapi.Visit(visit_key, False)

    def update_queued_visits(self, queue):
        if db is None:
            return
        lock = db.write_lock()
        try:
            db.execute(db.IdentityVisit.t.update_queued_visits(queue.items()))
        finally:
            lock.release()

        return