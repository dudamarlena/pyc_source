# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/auth/backends/ldap_auth.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11629 bytes
from future.utils import native
import flask_login
from flask_login import login_required, current_user, logout_user
from flask import flash
from wtforms import Form, PasswordField, StringField
from wtforms.validators import InputRequired
from ldap3 import Server, Connection, Tls, set_config_parameter, LEVEL, SUBTREE
import ssl
from flask import url_for, redirect
from airflow import models
from airflow import configuration
from airflow.configuration import AirflowConfigException
from airflow.utils.db import provide_session
import traceback, re
from airflow.utils.log.logging_mixin import LoggingMixin
LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.login_view = 'airflow.login'
LOGIN_MANAGER.login_message = None
log = LoggingMixin().log

class AuthenticationError(Exception):
    pass


class LdapException(Exception):
    pass


def get_ldap_connection(dn=None, password=None):
    try:
        cacert = configuration.conf.get('ldap', 'cacert')
    except AirflowConfigException:
        pass

    try:
        ignore_malformed_schema = configuration.conf.get('ldap', 'ignore_malformed_schema')
    except AirflowConfigException:
        pass

    if ignore_malformed_schema:
        set_config_parameter('IGNORE_MALFORMED_SCHEMA', ignore_malformed_schema)
    tls_configuration = Tls(validate=(ssl.CERT_REQUIRED), ca_certs_file=cacert)
    server = Server((configuration.conf.get('ldap', 'uri')), use_ssl=True,
      tls=tls_configuration)
    conn = Connection(server, native(dn), native(password))
    if not conn.bind():
        log.error('Cannot bind to ldap server: %s ', conn.last_error)
        raise AuthenticationError('Cannot bind to ldap server')
    return conn


def group_contains_user(conn, search_base, group_filter, user_name_attr, username):
    search_filter = '(&({0}))'.format(group_filter)
    if not conn.search((native(search_base)), (native(search_filter)), attributes=[
     native(user_name_attr)]):
        log.warning('Unable to find group for %s %s', search_base, search_filter)
    else:
        for entry in conn.entries:
            if username.lower() in map(lambda attr: attr.lower(), getattr(entry, user_name_attr).values):
                return True

    return False


def groups_user(conn, search_base, user_filter, user_name_att, username):
    search_filter = '(&({0})({1}={2}))'.format(user_filter, user_name_att, username)
    try:
        memberof_attr = configuration.conf.get('ldap', 'group_member_attr')
    except Exception:
        memberof_attr = 'memberOf'

    res = conn.search((native(search_base)), (native(search_filter)), attributes=[
     native(memberof_attr)])
    if not res:
        log.info('Cannot find user %s', username)
        raise AuthenticationError('Invalid username or password')
    if conn.response and memberof_attr not in conn.response[0]['attributes']:
        log.warning('Missing attribute "%s" when looked-up in Ldap database.\n        The user does not seem to be a member of a group and therefore won\'t see any dag\n        if the option filter_by_owner=True and owner_mode=ldapgroup are set', memberof_attr)
        return []
    else:
        user_groups = conn.response[0]['attributes'][memberof_attr]
        regex = re.compile('cn=([^,]*).*', re.IGNORECASE)
        groups_list = []
        try:
            groups_list = [regex.search(i).group(1) for i in user_groups]
        except IndexError:
            log.warning("Parsing error when retrieving the user's group(s). Check if the user belongs to at least one group or if the user's groups name do not contain special characters")

        return groups_list


class LdapUser(models.User):

    def __init__(self, user):
        self.user = user
        self.ldap_groups = []
        conn = get_ldap_connection(configuration.conf.get('ldap', 'bind_user'), configuration.conf.get('ldap', 'bind_password'))
        superuser_filter = None
        data_profiler_filter = None
        try:
            superuser_filter = configuration.conf.get('ldap', 'superuser_filter')
        except AirflowConfigException:
            pass

        if not superuser_filter:
            self.superuser = True
            log.debug('Missing configuration for superuser settings or empty. Skipping.')
        else:
            self.superuser = group_contains_user(conn, configuration.conf.get('ldap', 'basedn'), superuser_filter, configuration.conf.get('ldap', 'user_name_attr'), user.username)
        try:
            data_profiler_filter = configuration.conf.get('ldap', 'data_profiler_filter')
        except AirflowConfigException:
            pass

        if not data_profiler_filter:
            self.data_profiler = True
            log.debug('Missing configuration for data profiler settings or empty. Skipping.')
        else:
            self.data_profiler = group_contains_user(conn, configuration.conf.get('ldap', 'basedn'), data_profiler_filter, configuration.conf.get('ldap', 'user_name_attr'), user.username)
        try:
            self.ldap_groups = groups_user(conn, configuration.conf.get('ldap', 'basedn'), configuration.conf.get('ldap', 'user_filter'), configuration.conf.get('ldap', 'user_name_attr'), user.username)
        except AirflowConfigException:
            log.debug('Missing configuration for ldap settings. Skipping')

    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection(configuration.conf.get('ldap', 'bind_user'), configuration.conf.get('ldap', 'bind_password'))
        search_filter = '(&({0})({1}={2}))'.format(configuration.conf.get('ldap', 'user_filter'), configuration.conf.get('ldap', 'user_name_attr'), username)
        search_scope = LEVEL
        if configuration.conf.has_option('ldap', 'search_scope'):
            if configuration.conf.get('ldap', 'search_scope') == 'SUBTREE':
                search_scope = SUBTREE
            else:
                search_scope = LEVEL
        res = conn.search((native(configuration.conf.get('ldap', 'basedn'))), (native(search_filter)),
          search_scope=(native(search_scope)))
        if not res:
            log.info('Cannot find user %s', username)
            raise AuthenticationError('Invalid username or password')
        entry = conn.response[0]
        conn.unbind()
        if 'dn' not in entry:
            raise AuthenticationError('Invalid username or password')
        try:
            conn = get_ldap_connection(entry['dn'], password)
        except KeyError:
            log.error("\n            Unable to parse LDAP structure. If you're using Active Directory\n            and not specifying an OU, you must set search_scope=SUBTREE in airflow.cfg.\n            %s\n            ", traceback.format_exc())
            raise LdapException('Could not parse LDAP structure. Try setting search_scope in airflow.cfg, or check logs')

        if not conn:
            log.info('Password incorrect for user %s', username)
            raise AuthenticationError('Invalid username or password')

    @property
    def is_active(self):
        """Required by flask_login"""
        return True

    @property
    def is_authenticated(self):
        """Required by flask_login"""
        return True

    @property
    def is_anonymous(self):
        """Required by flask_login"""
        return False

    def get_id(self):
        """Returns the current user id as required by flask_login"""
        return self.user.get_id()

    def data_profiling(self):
        """Provides access to data profiling tools"""
        return self.data_profiler

    def is_superuser(self):
        """Access all the things"""
        return self.superuser


@LOGIN_MANAGER.user_loader
@provide_session
def load_user(userid, session=None):
    log.debug('Loading user %s', userid)
    if not userid or userid == 'None':
        return
    else:
        user = session.query(models.User).filter(models.User.id == int(userid)).first()
        return LdapUser(user)


@provide_session
def login(self, request, session=None):
    if current_user.is_authenticated:
        flash('You are already logged in')
        return redirect(url_for('admin.index'))
    else:
        username = None
        password = None
        form = LoginForm(request.form)
        if request.method == 'POST':
            if form.validate():
                username = request.form.get('username')
                password = request.form.get('password')
        if not username or not password:
            return self.render('airflow/login.html', title='Airflow - Login',
              form=form)
        try:
            LdapUser.try_login(username, password)
            log.info('User %s successfully authenticated', username)
            user = session.query(models.User).filter(models.User.username == username).first()
            if not user:
                user = models.User(username=username,
                  is_superuser=False)
                session.add(user)
            session.commit()
            session.merge(user)
            flask_login.login_user(LdapUser(user))
            session.commit()
            return redirect(request.args.get('next') or url_for('admin.index'))
        except (LdapException, AuthenticationError) as e:
            if type(e) == LdapException:
                flash(e, 'error')
            else:
                flash('Incorrect login details')
            return self.render('airflow/login.html', title='Airflow - Login',
              form=form)


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])