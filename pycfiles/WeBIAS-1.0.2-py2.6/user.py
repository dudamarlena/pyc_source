# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/user.py
# Compiled at: 2015-04-13 16:10:51
import cherrypy, config, auth, query, data, sqlalchemy
from util import *

class Requests:
    title = 'Requests'
    caption = 'View submitted requests'

    @cherrypy.expose
    @persistent
    def index(self, p=1, all=None, **kwargs):
        session = cherrypy.request.db
        login = auth.get_login()
        user = data.User.get_by_login(session, login)
        q = session.query(data.Request).with_parent(user)
        fb = config.root + '/user/requests/'
        all = all != None
        if not all:
            q = q.filter(data.Request.starred == True)
            if q.count() == 0:
                raise cherrypy.HTTPRedirect(fb + '?all')
        else:
            fb = fb + '?all'
        return render_query_paged('system/user/requests.genshi', q, int(p), 'requests', fb, kwargs, all=all)

    def get_req(self, req_uuid):
        session = cherrypy.request.db
        req = data.Request.get_request(session, req_uuid)
        login = auth.get_login()
        user = data.User.get_by_login(session, login)
        return req

    def change_req(self, req_uuid, **kwargs):
        save_referer()
        req = self.get_req(req_uuid)
        for k in kwargs:
            setattr(req, k, kwargs[k])

        go_back()

    def req_acl(self, req_uuid, *args, **kwargs):
        req = self.get_req(req_uuid)
        return [
         [
          req.user.login], 'admin']

    @cherrypy.expose
    @auth.with_acl(req_acl)
    def tag(self, req_uuid, tag):
        if tag == '':
            tag = None
        self.change_req(req_uuid, tag=tag)
        return

    @cherrypy.expose
    @auth.with_acl(req_acl)
    def star(self, req_uuid):
        self.change_req(req_uuid, starred=True)

    @cherrypy.expose
    @auth.with_acl(req_acl)
    def unstar(self, req_uuid):
        self.change_req(req_uuid, starred=False)

    @cherrypy.expose
    @auth.with_acl(req_acl)
    def rerun(self, req_uuid):
        self.change_req(req_uuid, status='READY', sched_id=None)
        return

    @cherrypy.expose
    @auth.with_acl(req_acl)
    def asnew(self, req_uuid):
        req = self.get_req(req_uuid)
        q = query.Query(req.query)
        q.req = req
        return cherrypy.tree.apps[config.root].root.apps[req.app.id].render_form(q)


class User(FeatureList):
    _cp_config = {'tools.secure.on': True, 
       'tools.protect.allowed': [
                               'user']}
    _title = 'User panel'

    def __init__(self):
        self.requests = Requests()