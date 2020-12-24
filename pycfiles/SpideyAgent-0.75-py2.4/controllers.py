# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider/controllers.py
# Compiled at: 2006-05-14 04:27:28
import turbogears
from model import *
from docutils.core import publish_parts
import cherrypy, re
from sqlobject import SQLObjectNotFound
from turbogears import validators
import spider
from thread import *
import os
from cPickle import *
from time import *
from string import *
s = None
spiders = []

class Root:
    __module__ = __name__

    def __init__(self):
        self.master_dict = {}
        connect(1)

    @turbogears.expose(html='spider.templates.welcome')
    def index(self):
        return dict(data='')

    @turbogears.expose(html='spider.templates.results')
    def search(self, data=None, username='', page=1, submit=None):
        print username
        page = int(page)
        conpool.getConnection()
        words = data.split()
        resultsperpage = 20
        number = len(words)
        sites = []
        Union = set()
        a = set()
        descriptions = {}
        for x in words:
            selected = Entry.select(Entry.q.word == x)
            selected_as_list = list(selected)
            a = set()
            if len(selected_as_list) > 0:
                if len(Union) == 0:
                    for y in selected_as_list:
                        if y.user.name == username or username == '':
                            Union.add(str(y.uri.address))

                else:
                    for y in selected_as_list:
                        if y.user.name == username or username == '':
                            a.add(y.uri.address + '')

                    Union = a.intersection(Union)
            else:
                Union = set()
                break

        sites = list(Union)
        numberofpages = 1 + len(sites) / resultsperpage
        sites = sites[page * resultsperpage:(1 + page) * resultsperpage]
        for each in sites:
            u = URI.select(URI.q.address == each)
            l = list(u)
            for site in l:
                for word in words:
                    lines = 0
                    if descriptions.has_key(site.address):
                        pass
                    else:

                        def getworddata(data):
                            showing = re.sub('<[^>]*>', '', data)
                            words = re.findall('\\w+', showing)
                            return words

                        wds = getworddata(site.data)
                        wds_ = (' ').join(wds)
                        ln = len(wds_)
                        start = find(wds_, word)
                        if ln >= start + 100:
                            descriptions[site.address] = wds_[start:start + 100]
                        else:
                            descriptions[site.address] = wds_[start:-1]

        return dict(username=username, data=data, descriptions=descriptions, words=words, sites=sites, numberofpages=numberofpages, page=page)

    @turbogears.expose(html='spider.templates.authenticateAdmin')
    def admin(self):
        return dict()

    @turbogears.expose(html='spider.templates.admin')
    def adminAuth(self, password, submit=''):
        conpool.getConnection()
        selected = Admin.select()
        selL = list(selected)
        if len(selL) > 0:
            a = selL[0]
            if a.password == password:
                selected = User.select()
                selected_as_list = list(selected)
                users = [ x.name for x in selected_as_list ]
                return dict(users=users)
            else:
                return 'Password does not match'
        else:
            b = Admin(password='admin', email='admin@business.com')
            return 'No administrator has logged in yet so the default admin user has been created with a login password "admin"'

    @turbogears.expose(html='spider.templates.login')
    def login(self):
        return dict()

    @turbogears.expose(html='spider.templates.newuser')
    def newuser(self):
        return dict()

    @turbogears.expose(html='spider.templates.userpage')
    def validateuser(self, username, password='', submit=''):
        print username
        conpool.getConnection()

        def wrds(u):
            sel = User.select(User.q.name == u)
            selL = list(sel)
            if len(selL) > 0:
                print Entry.q
                l = Entry.select(Entry.q.userID == selL[0].id)
                l = list(l)
                return len(l)
            return 0

        def sites(u):
            ss = set()
            sel = User.select(User.q.name == u)
            selL = list(sel)
            if len(selL) > 0:
                print Entry.q
                l = Entry.select(Entry.q.userID == selL[0].id)
                ll = list(l)
                for x in ll:
                    ss.add(x.uriID)

                return len(ss)
            return 0

        def nq(u):
            sel = User.select(User.q.name == u)
            selL = list(sel)
            if len(selL) > 0:
                q = Que.select(Que.q.userID == selL[0].id)
                ql = list(q)
                return len(ql)
            return 0

        root_sites = []
        time = ''
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            print 'User exists validated'
            time = selL[0].wait
        else:
            return 'User does not exist'
        root_sites = [ x.address for x in selL[0].rootSites ]
        numberofwords = 0
        numberofsites = 0
        numberinque = 0
        return dict(username=username, password=password, time=time, root_sites=root_sites, numberofwords=numberofwords, numberofsites=numberofsites, numberinque=numberinque)

    @turbogears.expose(html='spider.templates.login')
    def createuser(self, username, password, email, interval, submit):
        conpool.getConnection()
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            return 'User already exists'
        else:
            interval = str(interval)
            wait = interval
            u = User(name=username, password=password, email=email, wait=wait)
        root_sites = [ x.adress for x in u.rootSites ]
        return dict()

    @turbogears.expose(html='spider.templates.userpage')
    def start(self, username, submit):
        global s
        global spiders
        conpool.getConnection()
        for x in spiders:
            if x.user == username:
                return 'already running'

        hub.begin()
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            print selL[0].name
        else:
            hub.end()
            return 'No such user'
        hub.end()
        try:
            s = spider.spider(username)
            spiders.append(s)
            start_new(s.run, ())
            print 'thread started'
        except:
            print 'error while trying to start spider thread'

        def wrds(u):
            sel = User.select(User.q.name == u)
            selL = list(sel)
            if len(selL) > 0:
                print Entry.q
                l = Entry.select(Entry.q.userID == selL[0].id)
                l = list(l)
                return len(l)
            return 0

        def sites(u):
            ss = set()
            sel = User.select(User.q.name == u)
            selL = list(sel)
            if len(selL) > 0:
                print Entry.q
                l = Entry.select(Entry.q.userID == selL[0].id)
                ll = list(l)
                for x in ll:
                    ss.add(x.uriID)

                return len(ss)
            return 0

        def nq(u):
            sel = User.select(User.q.name == u)
            selL = list(sel)
            if len(selL) > 0:
                q = Que.select(Que.q.userID == selL[0].id)
                ql = list(q)
                return len(ql)
            return 0

        root_sites = []
        time = ''
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            print 'User exists validated'
            time = selL[0].wait
        else:
            return 'User does not exist'
        root_sites = [ x.address for x in selL[0].rootSites ]
        numberofwords = 0
        numberofsites = 0
        numberinque = 0
        return dict(username=username, password='', time=time, root_sites=root_sites, numberofwords=numberofwords, numberofsites=numberofsites, numberinque=numberinque)

    @turbogears.expose(html='spider.templates.stop')
    def stop(self, username, submit):
        for x in spiders:
            if x.user == username:
                x.stop = True
                sleep(0.1)
                spiders.remove(x)

        return dict()

    @turbogears.expose(html='spider.templates.add')
    def add(self, username, submit):
        return dict(username=username)

    @turbogears.expose(html='spider.templates.remove')
    def remove(self, username, submit):
        return dict()

    @turbogears.expose(html='spider.templates.userpage')
    def insertNewSite(self, address, username, submit):
        print 'inserting new site'
        conpool.getConnection()
        hub.begin()
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            user = selL[0]
            password = user.password + ''
            ns = RootSite(address=address, user=user)
        else:
            hub.end()
            return 'no such user %s, cannot insert ' % username
        hub.commit()
        root_sites = []
        time = ''
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            print 'User exists validated'
            time = selL[0].wait
        else:
            return 'User does not exist'
        root_sites = [ x.address for x in selL[0].rootSites ]
        numberofwords = 0
        numberofsites = 0
        numberinque = 0
        hub.end()
        return dict(username=username, password=password, time=time, root_sites=root_sites, numberofwords=numberofwords, numberofsites=numberofsites, numberinque=numberinque)

    @turbogears.expose(html='spider.templates.userpage')
    def deleteSite(self, user, address, submit):
        username = user
        conpool.getConnection()
        hub.begin()
        sel = User.select(User.q.name == user)
        selL = list(sel)
        sites = selL[0].rootSites
        for x in sites:
            if x.address == address:
                RootSite.delete(x.id)

        hub.commit()
        root_sites = []
        time = ''
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            print 'User exists validated'
            time = selL[0].wait
            usr = selL[0]
            password = usr.password + ''
        else:
            return 'User does not exist'
        root_sites = [ x.address for x in selL[0].rootSites ]
        numberofwords = 0
        numberofsites = 0
        numberinque = 0
        hub.end()
        return dict(username=username, password=password, time=time, root_sites=root_sites, numberofwords=numberofwords, numberofsites=numberofsites, numberinque=numberinque)

    @turbogears.expose(html='spider.templates.setInterval')
    def setInterval(self, username, submit, time):
        conpool.getConnection()
        hub.begin()
        sel = User.select(User.q.name == username)
        selectedList = list(sel)
        time = int(time)
        if len(selectedList) == 1:
            selectedList[0].wait = time
        hub.commit()
        hub.end()
        return 'Update interval has been set to %d' % time

    @turbogears.expose()
    def clearQ(self, username, submit):
        conpool.getConnection()
        hub.begin()
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            usr = selL[0]
            for x in usr.que:
                Que.delete(x.id)

        ps = usr.que + ['']
        print usr.que
        hub.commit()
        hub.end()
        return str(ps)

    @turbogears.expose()
    def setMedia(self, mpg='off', avi='off', wmv='off', submit=None):
        return mpg + avi + wmv

    @turbogears.expose(html='spider.templates.edit_user')
    def edit_user(self, username, submit=None):
        conpool.getConnection()
        hub.begin()
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            usr = selL[0]
        else:
            hub.end()
            return 'error with getting the users data'
        name = usr.name + ''
        password = usr.password + ''
        email = usr.email + ''
        interval = str(usr.wait) + ''
        rootSites = usr.rootSites + []
        que = usr.que + []
        hub.end()
        return dict(name=name, password=password, email=email, interval=interval, rootSites=rootSites, que=que)

    @turbogears.expose(html='spider.templates.admin')
    def save_changes(self, username, password, email, interval, submit=None):
        conpool.getConnection()
        hub.begin()
        sel = User.select(User.q.name == username)
        selL = list(sel)
        if len(selL) > 0:
            usr = selL[0]
        else:
            hub.end()
            return 'error with getting the users data'
        usr.name = username
        usr.password = password
        usr.email = email
        hub.commit()
        hub.end()
        return self.admin()