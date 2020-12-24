# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/controllers/auth.py
# Compiled at: 2005-08-14 05:52:18
import logging
from pylons import Response
from authproxy.lib.base import *
from authkit.authorize.pylons_adaptors import authorize, authorized
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn
from authkit.permissions import HasAuthKitRole, HasAuthKitGroup, And
from authkit.authorize import authorize_request
from authkit.permissions import RemoteUser
log = logging.getLogger(__name__)

class AuthController(BaseController):

    def index(self):
        return 'Hello AuthController'

    def serverinfo(self, name=None, message=None):
        import cgi, pprint
        c.pretty_environ = cgi.escape(pprint.pformat(request.environ))
        c.name = 'The Black Knight'
        c.message = message
        return render('/servinfo.mako')

    def signin(self):
        c.base_url = 'http://127.0.0.1:5000/'
        c.openid_url = c.base + '/verify'
        c.form_url = c.base + 'private'
        return render('genshi', 'signin')

    def info(self):
        import cgi, pprint
        c.pretty_environ = cgi.escape(pprint.pformat(request.environ))
        c.title = 'The Page'
        c.env_wsgi = []
        for (k, v) in request.environ.items():
            c.env_wsgi.append([k, v])

        return render('genshi', 'pylons_style')

    def jones(self, name='Mr jones'):
        """  exploitation de sqlalchemyManager     """
        model = request.environ['sqlalchemy.model']
        session = request.environ['sqlalchemy.session']
        multiple_mr_jones = session.query(model.MyClass).filter(model.MyClass.name == name).all()
        lines = []
        for m in multiple_mr_jones:
            lines.append('id:%d,name:%s' % (m.id, m.name))

        return str(lines)

    def show(self):
        print truc
        lines = ''
        if authorized(RemoteUser()):
            lines += 'utilisateur autorise: environ[REMOTE_USER]:%s\n' % request.environ['REMOTE_USER']
        return lines

    def private_openid(self):
        request.environ['authkit.authhandler'] = 'openid'
        authorize_request(request.environ, RemoteUser())
        username = request.environ['REMOTE_USER']
        session = request.environ['sqlalchemy.session']
        self.users = request.environ['authkit.users']
        if not self.users.user_exists(username):
            log.info('user openid identified but not registred...')
            self.users.user_create(username, 'cocoon', group='guest')
            session.flush()
            session.commit()
            log.info('account created in group guest for openid user %s' % username)
        result = [
         'You Have Access To This Page.\n\nHere is the environment...\n\n']
        for (k, v) in request.environ.items():
            result.append('%s: %s\n' % (k, v))

        return result

    def private_form(self):
        authorize_request(request.environ, RemoteUser())
        result = ['You Have Access To This Page.\n\nHere is the environment...\n\n']
        for (k, v) in request.environ.items():
            result.append('%s: %s\n' % (k, v))

        return result

    def private_basic(self):
        request.environ['authkit.authhandler'] = 'basic'
        authorize_request(request.environ, RemoteUser())
        result = ['You Have Access To This Page.\n\nHere is the environment...\n\n']
        for (k, v) in request.environ.items():
            result.append('%s: %s\n' % (k, v))

        return result

    def private_digest(self):
        request.environ['authkit.authhandler'] = 'digest'
        authorize_request(request.environ, RemoteUser())
        result = ['You Have Access To This Page.\n\nHere is the environment...\n\n']
        for (k, v) in request.environ.items():
            result.append('%s: %s\n' % (k, v))

        return result

    @authorize(ValidAuthKitUser())
    def private(self):
        result = 'You Have Access To This Page.\n\nHere is the environment...\n\n'
        for (k, v) in request.environ.items():
            result += '%s: %s\n' % (k, v)

        return result

    @authorize(ValidAuthKitUser())
    def registred(self):
        c.my_value = 'ceci est ma valeur, you are registered'
        return render('genshi', 'welcome')

    @authorize(RemoteUser())
    def identified(self):
        message = 'You are just identified \n and Have Access To This Page.\n\nHere is the environment...\n\n'
        return self.serverinfo('identified', message)

    @authorize(And(HasAuthKitRole('admin'), HasAuthKitGroup(['super', 'pylons'])))
    def admin(self):
        return Response('You are in the admin page !')

    @authorize(RemoteUser())
    def access(self):
        model = request.environ['sqlalchemy.model']
        session = request.environ['sqlalchemy.session']
        username = request.environ['REMOTE_USER']
        user_q = session.query(model.User)
        users = user_q.all()
        lines = []
        for u in users:
            lines.append(u.username)

        found_user = user_q.filter(model.User.username == username).one()
        if found_user:
            lines.append('valid user:%s' % found_user.username)
        else:
            lines.append('user not found')
        return str(lines)

    def signout(self):
        if request.environ.get('REMOTE_USER', None) != None:
            return 'signed out'
        else:
            return 'not signed in'
        return

    def logout(self):
        if request.environ.get('REMOTE_USER', None) != None:
            return 'signed out'
        else:
            return 'not signed in'
        return