# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/auth.py
# Compiled at: 2015-09-23 07:09:31
import cherrypy, urlparse, config, time, util, data, uuid, sqlalchemy, string, random

def is_sequence(arg):
    return not hasattr(arg, 'strip') and hasattr(arg, '__getitem__') or hasattr(arg, '__iter__')


def https_filter():
    request = cherrypy.request
    headers = request.headers
    forwarded_ssl = headers.get('X-Forwarded-Ssl', 'off')
    if forwarded_ssl == 'on':
        base = headers.get('X-Forwarded-Host', 'localhost')
        request.base = 'https://' + base


cherrypy.tools.https_filter = cherrypy.Tool('on_start_resource', https_filter)

def make_secure():
    if not util.get_WeBIAS().no_SSL:
        url = urlparse.urlparse(cherrypy.url(qs=cherrypy.request.query_string))
        if not url[0] == 'https':
            secure_url = urlparse.urlunparse(('https', url[1], url[2], url[3], url[4], url[5]))
            cherrypy.request.preserve = True
            raise cherrypy.HTTPRedirect(secure_url)


cherrypy.tools.secure = cherrypy.Tool('before_handler', make_secure, priority=20)

def safe_get_acl(feature):
    if hasattr(feature.__class__, '_acl'):
        return feature._acl
    else:
        return [
         'any']


def protect(allowed):
    noauth = False
    try:
        handler = cherrypy.request.handler.callable
    except AttributeError:
        return
    else:
        if hasattr(handler, '_get_acl'):
            try:
                handler._get_acl = True
            except AttributeError:
                handler.im_func._get_acl = True
            else:
                allowed = cherrypy.request.handler()
                noauth = getattr(handler, '_noauth', False)
        elif hasattr(handler, '_acl'):
            allowed = handler._acl
            noauth = getattr(handler, '_noauth', False)
        elif hasattr(handler, 'im_self') and hasattr(handler.im_self, '_acl'):
            allowed = handler.im_self._acl
            noauth = getattr(handler.im_self, '_noauth', False)
        if cherrypy.request.method == 'POST':
            handler = cherrypy.request.handler
            args = handler.args
            kwargs = handler.kwargs

            def action():
                return handler.callable(*args, **kwargs)

            fl = ForceLogin(acl=allowed, action=action, noauth=noauth)
        else:
            fl = ForceLogin(acl=allowed, goto=cherrypy.url(qs=cherrypy.request.query_string), noauth=noauth)
        if not fl.match(get_login()):
            fl.do()
        else:
            return


cherrypy.tools.protect = cherrypy.Tool('before_handler', protect)

class CleanupUsers(cherrypy.process.plugins.Monitor):

    def __init__(self, bus, frequency=300):
        self.engine = sqlalchemy.create_engine(config.db_url, echo=False, pool_recycle=1800)
        self.engine.connect()
        self.Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        cherrypy.process.plugins.Monitor.__init__(self, bus, self.run, frequency)

    def run(self):
        session = self.Session()
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 86400))
        session.query(data.User).filter(data.User.date < date, data.User.status == 'NEW', ~data.User.requests.any()).delete(synchronize_session=False)
        session.query(data.User).filter(data.User.date < date, data.User.status == 'NEW', data.User.requests.any()).update({'login': None, 'password': None, 'date': None, 'status': '', 'uuid': None, 'last_login': None}, synchronize_session=False)
        session.commit()
        return


def set_admin_pw():
    engine = sqlalchemy.create_engine(config.db_url, echo=False)
    engine.connect()
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    import getpass
    e_mail = raw_input('Enter administrator e-mail: ')
    passwd = getpass.getpass('Enter password: ')
    passwd1 = getpass.getpass('Re-enter password: ')
    if passwd != passwd1:
        print 'Passwords do not match.'
        return
    else:
        u = session.query(data.User).get(0)
        if u == None:
            u = data.User(e_mail, 'admin', passwd, 'OK')
            session.add(u)
            session.commit()
            u.id = 0
            session.commit()
        else:
            if u.login != 'admin':
                print 'User table corrupted. Repair it manually.'
                return
            u.update_passwd(passwd)
            u.e_mail = e_mail
            session.commit()
        return


class ForceLogin:

    def __init__(self, message='You have to be logged in to access this page.', acl=None, login=None, goto=None, action=None, noauth=False):
        self.message = message
        if acl == None:
            if login != None:
                if is_sequence(login):
                    acl = [
                     login]
                else:
                    acl = [
                     [
                      login]]
            else:
                acl = [
                 'any']
        self.acl = acl
        self.login = login
        self.goto = goto
        self.action = action
        self.noauth = noauth
        return

    @staticmethod
    def match_acl(acl, login):
        if acl == None:
            return True
        else:
            if login == 'admin':
                return True
            for i in acl:
                if i == 'any':
                    return True
                if i == 'anonymous' and login == None:
                    return True
                if i == 'user' and login != None:
                    return True
                if i == 'admin' and login == 'admin':
                    return True
                if not is_sequence(i) and i.startswith('role:') and login != None:
                    session = cherrypy.request.db
                    user = data.User.get_by_login(session, login)
                    if i[5:] == user.role_name:
                        return True
                elif is_sequence(i) and login in i:
                    return True

            return False

    def match(self, login):
        return ForceLogin.match_acl(self.acl, login)

    def do(self):
        login = get_login()
        ok = False
        if self.match(login):
            ok = True
        elif self.match(None):
            set_login(None)
            ok = True
        if ok:
            return self.success()
        else:
            if login != None or self.noauth:
                raise cherrypy.HTTPError(403, 'You are not authorized to access this page.')
            cherrypy.session['force_login'] = self
            self.keep = True
            raise cherrypy.HTTPRedirect(config.root + '/login/')
            return

    def success(self):
        if self.action != None:
            return self.action()
        else:
            if self.goto != None:
                raise cherrypy.HTTPRedirect(self.goto)
            else:
                util.go_back()
            return


def login_form(tmpl):
    fl = cherrypy.session.get('force_login')
    if fl != None:
        message = fl.message
        fl.keep = True
    else:
        message = cherrypy.session.get('message')
        try:
            cherrypy.session.pop('message')
        except KeyError:
            pass

        return util.render(tmpl, message=message)


def get_login():
    try:
        return cherrypy.session.get('login')
    except:
        None

    return


def set_login(login=None):
    if login == None:
        cherrypy.session.pop('login')
    else:
        cherrypy.session['login'] = login
    return


def random_password():
    f = lambda x, y: ('').join([ x[random.randint(0, len(x) - 1)] for i in xrange(y) ])
    return f(list(string.ascii_letters + string.digits), 8)


class Passwd:
    _cp_config = {'tools.protect.allowed': [
                               'user', 'admin']}

    @cherrypy.expose
    def index(self):
        return login_form('system/auth/passwd.genshi')

    @cherrypy.expose
    def submit(self, login, oldpass, newpass, verpass):
        session = cherrypy.request.db
        user = data.User.get_by_login(session, login)
        if login != get_login() or user == None:
            clear_session()
            cherrypy.session['message'] = 'Error. Please log again.'
            raise cherrypy.InternalRedirect('/login/')
        if newpass != verpass:
            cherrypy.session['message'] = 'Passwords do not match.'
            raise cherrypy.InternalRedirect('/login/passwd/')
        if not user.authenticate(oldpass):
            cherrypy.session['message'] = 'Wrong password.'
            raise cherrypy.InternalRedirect('/login/passwd/')
        user.update_passwd(newpass)
        util.go_back()
        return


class NewUser:

    @cherrypy.expose
    def index(self):
        return login_form('system/auth/newuser.genshi')

    @cherrypy.expose
    def submit(self, login, newpass, verpass, email):
        session = cherrypy.request.db
        if data.User.get_by_login(session, login) != None:
            cherrypy.session['message'] = 'User with this login already exists.'
            raise cherrypy.InternalRedirect('/login/newuser/')
        old_user = data.User.get_by_email(session, email)
        if old_user != None and old_user.status != '' and old_user.status is not None:
            cherrypy.session['message'] = 'User with this e-mail already exists.'
            raise cherrypy.InternalRedirect('/login/newuser/')
        if newpass != verpass:
            cherrypy.session['message'] = 'Passwords do not match.'
            raise cherrypy.InternalRedirect('/login/newuser/')
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        uid = uuid.uuid1().hex
        if old_user != None:
            user = old_user
            user.login = login
            user.status = 'NEW'
            user.uuid = uid
            user.date = date
            user.update_passwd(newpass)
        else:
            user = data.User(email, login, newpass, 'NEW', uid, date)
            session.add(user)
        util.email(email, 'system/email/newuser.genshi', newlogin=login, uuid=uid)
        return util.render('system/msg/newuser.genshi', newlogin=login)

    @cherrypy.expose
    def confirm(self, login, uuid):
        session = cherrypy.request.db
        user = data.User.get_by_login(session, login)
        if user != None:
            if user.uuid == uuid:
                if user.status == 'NEW':
                    user.status = 'OK'
                    session.commit()
                    return util.render('system/msg/userconfirm.genshi', login=login)
                if user.status == 'OK':
                    raise cherrypy.HTTPError(400, 'Account %s already activated.' % login)
        raise cherrypy.HTTPError(400)
        return


class Forgotten:

    @cherrypy.expose
    def index(self):
        return login_form('system/auth/forgotten.genshi')

    @cherrypy.expose
    def submit(self, login, email):
        session = cherrypy.request.db
        user = data.User.get_by_login(session, login)
        if not (user != None and user.e_mail == email and (user.status == 'OK' or user.status == 'FORGOTTEN')):
            cherrypy.session['message'] = 'User with these credentials does not exist.'
            raise cherrypy.InternalRedirect('/login/forgotten/')
        user.status = 'FORGOTTEN'
        user.uuid = uuid.uuid1().hex
        util.email(email, 'system/email/forgotten.genshi', newlogin=login, uuid=user.uuid)
        return util.render('system/msg/forgotten.genshi', newlogin=login)

    @cherrypy.expose
    def confirm(self, login, uuid):
        session = cherrypy.request.db
        user = data.User.get_by_login(session, login)
        if user != None:
            if user.uuid == uuid:
                if user.status == 'FORGOTTEN':
                    user.status = 'OK'
                    passwd = random_password()
                    user.update_passwd(passwd)
                    return util.render('system/msg/forgottenconfirm.genshi', newlogin=login, password=passwd)
                if user.status == 'OK':
                    raise cherrypy.HTTPError(400, 'Expired link.')
        raise cherrypy.HTTPError(400)
        return


class Login:
    _cp_config = {'tools.secure.on': True, 
       'tools.protect.allowed': [
                               'anonymous']}

    @cherrypy.expose
    def index(self):
        fl = cherrypy.session.get('force_login')
        if fl != None:
            fl.keep = True
        return login_form('system/auth/login.genshi')

    @cherrypy.expose
    def submit(self, login, passwd):
        fl = cherrypy.session.get('force_login', ForceLogin(message='', acl=[[login]]))
        session = cherrypy.request.db
        if not self.authenticate(session, login, passwd):
            fl.message = 'Invalid login or password.'
        return fl.do()

    @cherrypy.expose
    def signout(self):
        set_login(None)
        raise cherrypy.HTTPRedirect(config.server_url)
        return

    def authenticate(self, session, login, passwd):
        user = data.User.get_by_login(session, login)
        if user != None:
            if user.authenticate(passwd):
                set_login(login)
                user.last_login = time.strftime('%Y-%m-%d %H:%M:%S')
                session.commit()
                return True
        return False

    passwd = Passwd()
    newuser = NewUser()
    forgotten = Forgotten()


def with_acl(acl, noauth=False):

    def with_acl_decorator(handler):

        def wrap_handler(self, *args, **kwargs):
            if wrap_handler._get_acl:
                wrap_handler._get_acl = False
                if hasattr(acl, '__len__'):
                    return acl
                return acl(self, *args, **kwargs)
            else:
                return handler(self, *args, **kwargs)

        wrap_handler._get_acl = False
        wrap_handler._noauth = noauth
        return wrap_handler

    return with_acl_decorator


def get_acl_for_id(mode, cls, message='Bad item id.'):

    def acl(self, id, *args, **kwargs):
        session = cherrypy.request.db
        dbid = data.get_by_id(session, cls, id, message)
        return dbid.get_acl(mode)

    return acl


def app_acl(mode):
    return get_acl_for_id(mode, data.Application, 'Bad application id.')


def sched_acl(mode):
    return get_acl_for_id(mode, data.Scheduler, 'Bad scheduler id.')