# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/handler.py
# Compiled at: 2020-05-05 08:50:12
# Size of source mod 2**32: 39471 bytes
"""web2ldap.app.handler: base handler

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import sys, inspect, socket, time, urllib.parse, logging
from collections import defaultdict
from ipaddress import ip_address, ip_network
import ldap0
from ldap0.ldapurl import is_ldapurl
from ldap0.dn import DNObj
from ldap0.err import PasswordPolicyException, PasswordPolicyExpirationWarning
import web2ldapcnf, web2ldapcnf.hosts
COMMAND_COUNT = defaultdict(lambda : 0)
import web2ldap.web.forms, web2ldap.web.helper, web2ldap.web.session
from web2ldap.web.helper import get_remote_ip
import web2ldap.__about__, web2ldap.ldaputil, web2ldap.ldaputil.dns, web2ldap.ldapsession
from web2ldap.ldaputil.extldapurl import ExtendedLDAPUrl
from web2ldap.ldapsession import LDAPSession
from web2ldap.log import LogHelper, logger, log_exception
import web2ldap.app.gui, web2ldap.app.cnf, web2ldap.app.passwd, web2ldap.app.dit, web2ldap.app.searchform, web2ldap.app.locate, web2ldap.app.search, web2ldap.app.addmodifyform, web2ldap.app.add, web2ldap.app.modify, web2ldap.app.dds, web2ldap.app.delete, web2ldap.app.params, web2ldap.app.read, web2ldap.app.conninfo, web2ldap.app.login, web2ldap.app.connect, web2ldap.app.referral, web2ldap.app.monitor, web2ldap.app.groupadm, web2ldap.app.rename, web2ldap.app.urlredirect, web2ldap.app.bulkmod, web2ldap.app.srvrr, web2ldap.app.schema.viewer, web2ldap.app.metrics
from web2ldap.app.gui import exception_message
from web2ldap.app.form import Web2LDAPForm
from web2ldap.app.session import session_store
from web2ldap.app.schema.syntaxes import syntax_registry
from web2ldap.ldaputil import AD_LDAP49_ERROR_CODES, AD_LDAP49_ERROR_PREFIX
from web2ldap.app.core import ErrorExit
SCOPE2COMMAND = {None: 'search', 
 ldap0.SCOPE_BASE: 'read', 
 ldap0.SCOPE_ONELEVEL: 'search', 
 ldap0.SCOPE_SUBTREE: 'search', 
 ldap0.SCOPE_SUBORDINATE: 'search'}
CONNTYPE2URLSCHEME = {0:'ldap', 
 1:'ldap', 
 2:'ldaps', 
 3:'ldapi'}
FORM_CLASS = {}
logger.debug('Registering Form classes')
for _, cls in inspect.getmembers(sys.modules['web2ldap.app.form'], inspect.isclass):
    if cls.__name__.startswith('Web2LDAPForm_') and cls.command is not None:
        logger.debug('Register class %s for command %r', cls.__name__, cls.command)
        FORM_CLASS[cls.command] = cls
else:
    SIMPLE_MSG_HTML = '\n<html>\n  <head>\n    <title>Note</title>\n  </head>\n  <body>\n    {message}\n  </body>\n</html>\n'
    COMMAND_FUNCTION = {'':web2ldap.app.connect.w2l_connect, 
     'disconnect':None, 
     'locate':web2ldap.app.locate.w2l_locate, 
     'monitor':web2ldap.app.monitor.w2l_monitor, 
     'urlredirect':web2ldap.app.urlredirect.w2l_urlredirect, 
     'searchform':web2ldap.app.searchform.w2l_searchform, 
     'search':web2ldap.app.search.w2l_search, 
     'add':web2ldap.app.add.w2l_add, 
     'modify':web2ldap.app.modify.w2l_modify, 
     'dds':web2ldap.app.dds.w2l_dds, 
     'bulkmod':web2ldap.app.bulkmod.w2l_bulkmod, 
     'delete':web2ldap.app.delete.w2l_delete, 
     'dit':web2ldap.app.dit.w2l_dit, 
     'rename':web2ldap.app.rename.w2l_rename, 
     'passwd':web2ldap.app.passwd.w2l_passwd, 
     'read':web2ldap.app.read.w2l_read, 
     'conninfo':web2ldap.app.conninfo.w2l_conninfo, 
     'params':web2ldap.app.params.w2l_params, 
     'login':web2ldap.app.login.w2l_login, 
     'groupadm':web2ldap.app.groupadm.w2l_groupadm, 
     'oid':web2ldap.app.schema.viewer.w2l_schema_viewer}
    if web2ldap.app.metrics.METRICS_AVAIL:
        COMMAND_FUNCTION['metrics'] = web2ldap.app.metrics.w2l_metrics
    syntax_registry.check()

    def check_access(env, command):
        """
    simple access control based on REMOTE_ADDR
    """
        remote_addr = ip_address(env['REMOTE_ADDR'])
        access_allowed = web2ldapcnf.access_allowed.get(command, web2ldapcnf.access_allowed['_'])
        for net in access_allowed:
            if remote_addr in ip_network(net, strict=False):
                return True
            return False


    class AppHandler(LogHelper):
        __doc__ = '\n    Class implements web application entry point\n    and dispatches requests to use-case functions w2l_*()\n    '

        def __init__(self, env, outf):
            self.current_access_time = time.time()
            self.inf = env['wsgi.input']
            self.outf = outf
            self.env = env
            self.script_name = self.env['SCRIPT_NAME']
            self.command, self.sid = self.path_info(env)
            self.form = None
            self.ls = None
            self.dn_obj = None
            self.query_string = env.get('QUERY_STRING', '')
            self.ldap_url = None
            self.schema = None
            self.cfg_key = None
            if is_ldapurl(self.query_string):
                self.ldap_url = ExtendedLDAPUrl(self.query_string)
                if not self.command:
                    self.command = SCOPE2COMMAND[self.ldap_url.scope]

        @property
        def dn(self):
            """
        get current DN
        """
            return str(self.dn_obj)

        @dn.setter
        def dn(self, dn):
            """
        set current DN and related class attributes
        """
            assert ldap0.dn.is_dn(dn), ValueError('Expected LDAP DN as dn, was %r' % dn)
            self.dn_obj = DNObj.from_str(dn)
            if self.ls:
                if self.ls.uri:
                    self.dn_obj.charset = self.ls.charset
                    self.schema = self.ls.get_sub_schema(self.dn, self.cfg_param('_schema', None), self.cfg_param('supplement_schema', None), self.cfg_param('schema_strictcheck', True))

        @property
        def naming_context(self):
            if self.ls and self.ls.uri:
                res = self.ls.get_search_root(self.dn)
            else:
                res = DNObj(())
            return res

        @property
        def audit_context(self):
            if self.ls and self.ls.uri:
                res = self.ls.get_audit_context(self.naming_context)
            else:
                res = None
            return res

        @property
        def parent_dn(self):
            """
        get parent DN of current DN
        """
            return str(self.dn_obj.parent())

        @property
        def ldap_dn(self):
            """
        get LDAP encoding (UTF-8) of current DN
        """
            return bytes(self.dn_obj)

        def cfg_param(self, param_key, default):
            if self.ls and self.ls.uri:
                cfg_url = self.ls.uri
            else:
                cfg_url = 'ldap://'
            return web2ldap.app.cnf.LDAP_DEF.get_param(cfg_url, self.naming_context or '', param_key, default)

        @property
        def binddn_mapping(self):
            """
        get parameter 'binddn_mapping' from cascaded configuration
        """
            return self.cfg_param('binddn_mapping', 'ldap:///_??sub?(uid={user})')

        def anchor(self, command, anchor_text, form_parameters, target=None, title=None, anchor_id=None):
            """
        Build the HTML text of a anchor with form parameters
        """
            if not isinstance(command, str):
                raise AssertionError(TypeError('command must be str, but was %r', command))
            else:
                if not isinstance(anchor_text, str):
                    raise AssertionError(TypeError('anchor_text must be str, but was %r', anchor_text))
                else:
                    if not anchor_id is None:
                        assert isinstance(anchor_id, str), TypeError('anchor_id must be None or str, but was %r', anchor_id)
                    if not target is None:
                        if not isinstance(target, str):
                            raise AssertionError(TypeError('target must be None or str, but was %r', target))
                if not title is None:
                    if not isinstance(title, str):
                        raise AssertionError(TypeError('title must be None or str, but was %r', title))
            target_attr = ''
            if target:
                target_attr = ' target="%s"' % target
            title_attr = ''
            if title:
                title_attr = ' title="%s"' % self.form.utf2display(title).replace(' ', '&nbsp;')
            if anchor_id:
                anchor_id = '#%s' % self.form.utf2display(anchor_id)
            res = '<a class="CL"%s%s href="%s?%s%s">%s</a>' % (
             target_attr,
             title_attr,
             self.form.action_url(command, self.sid),
             '&amp;'.join(['%s=%s' % (param_name, urllib.parse.quote(param_value)) for param_name, param_value in form_parameters]),
             anchor_id or '',
             anchor_text)
            assert isinstance(res, str), TypeError('res must be str, was %r', res)
            return res

        def begin_form(self, command, method, target=None, enctype='application/x-www-form-urlencoded'):
            """
        convenience wrapper for Web2LDAPForm.begin_form()
        which sets non-zero sid
        """
            return self.form.begin_form(command,
              (self.sid),
              method,
              target=target,
              enctype=enctype)

        def form_html(self, command, submitstr, method, form_parameters, extrastr='', target=None):
            """
        Build the HTML text of a submit form
        """
            form_str = [
             self.begin_form(command, method, target)]
            for param_name, param_value in form_parameters:
                form_str.append(self.form.hiddenFieldHTML(param_name, param_value, ''))
            else:
                form_str.append('<p>\n<input type="submit" value="%s">\n%s\n</p>\n</form>' % (
                 submitstr,
                 extrastr))
                return '\n'.join(form_str)

        def dispatch(self):
            """
        Execute function for self.command
        """
            assert isinstance(self.dn, str), TypeError('Class attribute %s.dn must be str, was %r' % (
             self.__class__.__name__,
             self.dn))
            assert isinstance(self.ldap_url, ExtendedLDAPUrl), TypeError('Class attribute %s.ldap_url must be LDAPUrl instance, was %r' % (
             self.__class__.__name__,
             self.ldap_url))
            self.log(logging.DEBUG, '%s.ldap_url is %s', self.__class__.__name__, self.ldap_url)
            self.log(logging.DEBUG, 'Dispatch command %r to function %s.%s()', self.command, COMMAND_FUNCTION[self.command].__module__, COMMAND_FUNCTION[self.command].__name__)
            COMMAND_FUNCTION[self.command](self)

        def path_info(self, env):
            """
        Extract the command and sid from PATH_INFO env var
        """
            path_info = env.get('PATH_INFO', '/')[1:]
            self.log(logging.DEBUG, 'splitting path_info %r', path_info)
            if not path_info:
                cmd, sid = ('', '')
            else:
                script_name = env['SCRIPT_NAME']
                if path_info.startswith(script_name):
                    path_info = path_info[len(script_name):]
                try:
                    cmd, sid = path_info.split('/', 1)
                except ValueError:
                    cmd, sid = path_info, ''
                else:
                    self.log(logging.DEBUG, 'split path_info to (%r, %r)', cmd, sid)
                    return (cmd, sid)

        def display_dn(self, dn, commandbutton=False):
            """Display a DN as LDAP URL with or without button"""
            assert isinstance(dn, str), TypeError("Argument 'dn' must be str, was %r" % (dn,))
            dn_str = self.form.utf2display(dn or '- World -')
            if commandbutton:
                command_buttons = [dn_str,
                 self.anchor('read', 'Read', [('dn', dn)])]
                return web2ldapcnf.command_link_separator.join(command_buttons)
            return dn_str

        def simple_message(self, title='', message='', main_div_id='Message', main_menu_list=None, context_menu_list=None):
            web2ldap.app.gui.top_section(self,
              title,
              main_menu_list,
              context_menu_list=context_menu_list,
              main_div_id=main_div_id)
            self.outf.write(message)
            web2ldap.app.gui.footer(self)

        def simple_msg(self, msg):
            """
        Output HTML text.
        """
            web2ldap.app.gui.Header(self, 'text/html', self.form.accept_charset)
            self.outf.write(SIMPLE_MSG_HTML.format(message=msg))

        def url_redirect(self, redirect_msg, link_text='Continue&gt;&gt;', refresh_time=3, target_url=None):
            """
        Outputs HTML text with redirecting <head> section.
        """
            if self.form is None:
                self.form = Web2LDAPForm(None, self.env)
            else:
                target_url = target_url or self.script_name
                url_redirect_template_str = web2ldap.app.gui.read_template(self,
                  None, 'redirect', tmpl_filename=(web2ldapcnf.redirect_template))
                if refresh_time:
                    message_class = 'ErrorMessage'
                else:
                    message_class = 'SuccessMessage'
            web2ldap.app.gui.Header(self, 'text/html', self.form.accept_charset)
            self.outf.write(url_redirect_template_str.format(refresh_time=refresh_time,
              target_url=target_url,
              message_class=message_class,
              redirect_msg=(self.form.utf2display(redirect_msg)),
              link_text=link_text))

        def _new_session(self):
            """
        create new session
        """
            self.sid = session_store.new(self.env)
            self.ls = LDAPSession(get_remote_ip(self.env), web2ldapcnf.ldap_trace_level, web2ldapcnf.ldap_cache_ttl)
            self.ls.cookie = self.form.set_cookie(str(id(self.ls)))
            session_store.save(self.sid, self.ls)

        def _get_session(self):
            """
        Restore old or initialize new web session object
        """
            if self.sid:
                try:
                    last_session_timestamp, _ = session_store.sessiondict[self.sid]
                except KeyError:
                    pass
                else:
                    self.ls = session_store.retrieveSession(self.sid, self.env)
                    if not isinstance(self.ls, LDAPSession):
                        raise web2ldap.app.session.InvalidSessionInstance()
                    if self.ls.cookie:
                        cookie_name = ''.join((self.form.cookie_name_prefix, str(id(self.ls))))
                        raise cookie_name in self.form.cookies and self.ls.cookie[cookie_name].value == self.form.cookies[cookie_name].value or web2ldap.app.session.WrongSessionCookie()
                    if web2ldapcnf.session_paranoid and self.current_access_time - last_session_timestamp > web2ldapcnf.session_paranoid:
                        self.sid = session_store.rename(self.sid, self.env)
            else:
                self.ls = None

        def _del_session(self):
            """
        delete the current session
        """
            session_store.delete(self.sid)
            del self.ls
            self.sid = self.ls = None

        def _handle_delsid(self):
            """
        if del_sid form parameter is present then delete the obsolete session
        """
            try:
                del_sid = self.form.field['delsid'].value[0]
            except IndexError:
                return
            else:
                try:
                    old_ls = session_store.retrieveSession(del_sid, self.env)
                except web2ldap.web.session.SessionException:
                    pass
                else:
                    self.form.unset_cookie(old_ls.cookie)
                session_store.delete(del_sid)

        def _get_ldapconn_params(self):
            """
        Extract parameters either from LDAP URL in query string or real form input
        """
            if is_ldapurl(self.form.query_string):
                try:
                    input_ldapurl = ExtendedLDAPUrl(self.form.query_string)
                except ValueError as err:
                    try:
                        raise ErrorExit('Error parsing LDAP URL: %s.' % self.form.utf2display(str(err)))
                    finally:
                        err = None
                        del err

                else:
                    self.command = self.command or SCOPE2COMMAND[input_ldapurl.scope]
                    if self.command in ('search', 'read'):
                        input_ldapurl.filterstr = input_ldapurl.filterstr or '(objectClass=*)'
                    self.form = FORM_CLASS.get(self.command, Web2LDAPForm)(self.inf, self.env)
            else:
                self._handle_delsid()
                if 'ldapurl' in self.form.input_field_names:
                    ldap_url_input = self.form.field['ldapurl'].value[0]
                    try:
                        input_ldapurl = ExtendedLDAPUrl(ldap_url_input)
                    except ValueError as err:
                        try:
                            raise ErrorExit('Error parsing LDAP URL: %s.' % (err,))
                        finally:
                            err = None
                            del err

                else:
                    input_ldapurl = ExtendedLDAPUrl()
                    conntype = int(self.form.getInputValue('conntype', [0])[0])
                    input_ldapurl.urlscheme = CONNTYPE2URLSCHEME[conntype]
                    input_ldapurl.hostport = self.form.getInputValue('host', [None])[0]
                    input_ldapurl.x_startTLS = str(web2ldap.ldapsession.START_TLS_REQUIRED * (conntype == 1))
            dn = self.form.getInputValue('dn', [input_ldapurl.dn])[0]
            who = self.form.getInputValue('who', [None])[0]
            if who is None:
                if input_ldapurl.who is not None:
                    who = input_ldapurl.who
                else:
                    input_ldapurl.who = who
                cred = self.form.getInputValue('cred', [None])[0]
                if cred is None:
                    if input_ldapurl.cred is not None:
                        cred = input_ldapurl.cred
            else:
                input_ldapurl.cred = cred
            assert isinstance(input_ldapurl.dn, str), TypeError("Type of 'input_ldapurl.dn' must be str, was %r" % input_ldapurl.dn)
            if not input_ldapurl.who is None:
                assert isinstance(input_ldapurl.who, str), TypeError("Type of 'input_ldapurl.who' must be str, was %r" % input_ldapurl.who)
            if not input_ldapurl.cred is None:
                assert isinstance(input_ldapurl.cred, str), TypeError("Type of 'input_ldapurl.cred' must be str, was %r" % input_ldapurl.cred)
            if not isinstance(dn, str):
                raise AssertionError(TypeError("Argument 'dn' must be str, was %r" % dn))
            elif not who is None:
                if not isinstance(who, str):
                    raise AssertionError(TypeError("Type of 'who' must be str, was %r" % who))
                else:
                    if not cred is None:
                        assert isinstance(cred, str), TypeError("Type of 'cred' must be str, was %r" % cred)
                    assert ldap0.dn.is_dn(dn, flags=1), 'Invalid DN.'
                scope_str = self.form.getInputValue('scope', [
                 {False:str(input_ldapurl.scope), 
                  True:''}[(input_ldapurl.scope is None)]])[0]
                if scope_str:
                    input_ldapurl.scope = int(scope_str)
            else:
                input_ldapurl.scope = None
            return (input_ldapurl, dn, who, cred)

        def ldap_error_msg(self, ldap_err, template='{error_msg}<br>{matched_dn}'):
            """
        Converts a LDAPError exception into HTML error message

        ldap_err
          LDAPError instance
        template
          Raw binary string to be used as template
          (must contain only a single placeholder)
        """
            matched_dn = None
            if not isinstance(ldap_err, ldap0.TIMEOUT):
                error_msg = ldap_err.args or ''
            else:
                pass
            if isinstance(ldap_err, ldap0.INVALID_CREDENTIALS) and AD_LDAP49_ERROR_PREFIX in ldap_err.args[0].get('info', ''):
                ad_error_code_pos = ldap_err.args[0]['info'].find(AD_LDAP49_ERROR_PREFIX) + len(AD_LDAP49_ERROR_PREFIX)
                ad_error_code = int(ldap_err.args[0]['info'][ad_error_code_pos:ad_error_code_pos + 3], 16)
                error_msg = '%s:\n%s (%s)' % (
                 ldap_err.args[0]['desc'].decode(self.ls.charset),
                 ldap_err.args[0].get('info', '').decode(self.ls.charset),
                 AD_LDAP49_ERROR_CODES.get(ad_error_code, 'unknown'))
            else:
                try:
                    error_desc = ldap_err.args[0]['desc'].decode(self.ls.charset)
                    error_info = ldap_err.args[0].get('info', '').decode(self.ls.charset)
                except UnicodeDecodeError:
                    error_msg = str(ldap_err)
                except (TypeError, IndexError):
                    error_msg = str(ldap_err)
                else:
                    error_msg = '{desc}: {info}'.format(desc=error_desc,
                      info=error_info)
                try:
                    matched_dn = ldap_err.args[0].get('matched', '').decode(self.ls.charset)
                except AttributeError:
                    matched_dn = None
                else:
                    error_msg = error_msg.replace('\r', '').replace('\t', '')
                    error_msg_html = self.form.utf2display(error_msg, lf_entity='<br>')
                    if matched_dn:
                        matched_dn_html = '<br>Matched DN: %s' % self.form.utf2display(matched_dn)
                    else:
                        matched_dn_html = ''
                    return template.format(error_msg=error_msg_html,
                      matched_dn=matched_dn_html)

        def run--- This code section failed: ---

 L. 690         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              log
                4  LOAD_GLOBAL              logging
                6  LOAD_ATTR                DEBUG
                8  LOAD_STR                 'Entering .run()'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L. 693        14  LOAD_DEREF               'self'
               16  LOAD_ATTR                command
               18  LOAD_GLOBAL              COMMAND_FUNCTION
               20  COMPARE_OP               not-in
               22  POP_JUMP_IF_FALSE    56  'to 56'

 L. 695        24  LOAD_DEREF               'self'
               26  LOAD_METHOD              log
               28  LOAD_GLOBAL              logging
               30  LOAD_ATTR                WARN
               32  LOAD_STR                 'Received invalid command %r'
               34  LOAD_DEREF               'self'
               36  LOAD_ATTR                command
               38  CALL_METHOD_3         3  ''
               40  POP_TOP          

 L. 696        42  LOAD_DEREF               'self'
               44  LOAD_METHOD              url_redirect
               46  LOAD_STR                 'Invalid web2ldap command'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 697        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            22  '22'

 L. 700        56  LOAD_GLOBAL              COMMAND_COUNT
               58  LOAD_DEREF               'self'
               60  LOAD_ATTR                command
               62  JUMP_IF_TRUE_OR_POP    66  'to 66'
               64  LOAD_STR                 'connect'
             66_0  COME_FROM            62  '62'
               66  DUP_TOP_TWO      
               68  BINARY_SUBSCR    
               70  LOAD_CONST               1
               72  INPLACE_ADD      
               74  ROT_THREE        
               76  STORE_SUBSCR     

 L. 703        78  LOAD_GLOBAL              FORM_CLASS
               80  LOAD_METHOD              get
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                command
               86  LOAD_GLOBAL              Web2LDAPForm
               88  CALL_METHOD_2         2  ''
               90  LOAD_DEREF               'self'
               92  LOAD_ATTR                inf
               94  LOAD_DEREF               'self'
               96  LOAD_ATTR                env
               98  CALL_FUNCTION_2       2  ''
              100  LOAD_DEREF               'self'
              102  STORE_ATTR               form

 L. 709   104_106  SETUP_FINALLY      1466  'to 1466'

 L. 711       108  LOAD_DEREF               'self'
              110  LOAD_ATTR                command
              112  LOAD_GLOBAL              FORM_CLASS
              114  COMPARE_OP               in
              116  POP_JUMP_IF_FALSE   140  'to 140'
              118  LOAD_GLOBAL              is_ldapurl
              120  LOAD_DEREF               'self'
              122  LOAD_ATTR                form
              124  LOAD_ATTR                query_string
              126  CALL_FUNCTION_1       1  ''
              128  POP_JUMP_IF_TRUE    140  'to 140'

 L. 713       130  LOAD_DEREF               'self'
              132  LOAD_ATTR                form
              134  LOAD_METHOD              getInputFields
              136  CALL_METHOD_0         0  ''
              138  POP_TOP          
            140_0  COME_FROM           128  '128'
            140_1  COME_FROM           116  '116'

 L. 716       140  LOAD_GLOBAL              check_access
              142  LOAD_DEREF               'self'
              144  LOAD_ATTR                env
              146  LOAD_DEREF               'self'
              148  LOAD_ATTR                command
              150  CALL_FUNCTION_2       2  ''
              152  POP_JUMP_IF_TRUE    188  'to 188'

 L. 717       154  LOAD_DEREF               'self'
              156  LOAD_METHOD              log

 L. 718       158  LOAD_GLOBAL              logging
              160  LOAD_ATTR                WARN

 L. 719       162  LOAD_STR                 'Access denied from %r to command %r'

 L. 720       164  LOAD_DEREF               'self'
              166  LOAD_ATTR                env
              168  LOAD_STR                 'REMOTE_ADDR'
              170  BINARY_SUBSCR    

 L. 721       172  LOAD_DEREF               'self'
              174  LOAD_ATTR                command

 L. 717       176  CALL_METHOD_4         4  ''
              178  POP_TOP          

 L. 723       180  LOAD_GLOBAL              ErrorExit
              182  LOAD_STR                 'Access denied.'
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           152  '152'

 L. 726       188  LOAD_DEREF               'self'
              190  LOAD_ATTR                command
              192  LOAD_CONST               {'', 'urlredirect', 'metrics', 'locate', 'monitor'}
              194  COMPARE_OP               in
              196  POP_JUMP_IF_FALSE   218  'to 218'

 L. 727       198  LOAD_GLOBAL              COMMAND_FUNCTION
              200  LOAD_DEREF               'self'
              202  LOAD_ATTR                command
              204  BINARY_SUBSCR    
              206  LOAD_DEREF               'self'
              208  CALL_FUNCTION_1       1  ''
              210  POP_TOP          

 L. 728       212  POP_BLOCK        
              214  LOAD_CONST               None
              216  RETURN_VALUE     
            218_0  COME_FROM           196  '196'

 L. 730       218  LOAD_DEREF               'self'
              220  LOAD_METHOD              _get_session
              222  CALL_METHOD_0         0  ''
              224  POP_TOP          

 L. 732       226  LOAD_DEREF               'self'
              228  LOAD_ATTR                command
              230  LOAD_STR                 'disconnect'
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   292  'to 292'

 L. 734       238  LOAD_DEREF               'self'
              240  LOAD_ATTR                form
              242  LOAD_METHOD              unset_cookie
              244  LOAD_DEREF               'self'
              246  LOAD_ATTR                ls
              248  LOAD_ATTR                cookie
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L. 736       254  LOAD_GLOBAL              session_store
              256  LOAD_METHOD              delete
              258  LOAD_DEREF               'self'
              260  LOAD_ATTR                sid
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L. 737       266  LOAD_CONST               None
              268  LOAD_DEREF               'self'
              270  STORE_ATTR               sid

 L. 739       272  LOAD_DEREF               'self'
              274  LOAD_ATTR                url_redirect
              276  LOAD_STR                 'Disconnecting...'
              278  LOAD_CONST               0
              280  LOAD_CONST               ('refresh_time',)
              282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              284  POP_TOP          

 L. 740       286  POP_BLOCK        
              288  LOAD_CONST               None
              290  RETURN_VALUE     
            292_0  COME_FROM           234  '234'

 L. 742       292  LOAD_DEREF               'self'
              294  LOAD_METHOD              _get_ldapconn_params
              296  CALL_METHOD_0         0  ''
              298  UNPACK_SEQUENCE_4     4 
              300  LOAD_DEREF               'self'
              302  STORE_ATTR               ldap_url
              304  LOAD_DEREF               'self'
              306  STORE_ATTR               dn
              308  STORE_FAST               'who'
              310  STORE_FAST               'cred'

 L. 744       312  LOAD_DEREF               'self'
              314  LOAD_ATTR                command
          316_318  JUMP_IF_TRUE_OR_POP   352  'to 352'

 L. 745       320  LOAD_CONST               None

 L. 745       322  LOAD_STR                 'searchform'

 L. 746       324  LOAD_GLOBAL              ldap0
              326  LOAD_ATTR                SCOPE_BASE

 L. 746       328  LOAD_STR                 'read'

 L. 747       330  LOAD_GLOBAL              ldap0
              332  LOAD_ATTR                SCOPE_ONELEVEL

 L. 747       334  LOAD_STR                 'search'

 L. 748       336  LOAD_GLOBAL              ldap0
              338  LOAD_ATTR                SCOPE_SUBTREE

 L. 748       340  LOAD_STR                 'search'

 L. 744       342  BUILD_MAP_4           4 

 L. 749       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                ldap_url
              348  LOAD_ATTR                scope

 L. 744       350  BINARY_SUBSCR    
            352_0  COME_FROM           316  '316'
              352  LOAD_DEREF               'self'
              354  STORE_ATTR               command

 L. 755       356  LOAD_DEREF               'self'
              358  LOAD_ATTR                ldap_url
              360  LOAD_ATTR                hostport
              362  LOAD_STR                 ''
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   542  'to 542'

 L. 756       370  LOAD_DEREF               'self'
              372  LOAD_ATTR                ldap_url
              374  LOAD_ATTR                urlscheme
              376  LOAD_STR                 'ldap'
              378  COMPARE_OP               ==

 L. 755   380_382  POP_JUMP_IF_FALSE   542  'to 542'

 L. 757       384  LOAD_DEREF               'self'
              386  LOAD_ATTR                ls
              388  LOAD_CONST               None
              390  COMPARE_OP               is

 L. 755   392_394  POP_JUMP_IF_TRUE    410  'to 410'

 L. 757       396  LOAD_DEREF               'self'
              398  LOAD_ATTR                ls
              400  LOAD_ATTR                uri
              402  LOAD_CONST               None
              404  COMPARE_OP               is

 L. 755   406_408  POP_JUMP_IF_FALSE   542  'to 542'
            410_0  COME_FROM           392  '392'

 L. 760       410  LOAD_GLOBAL              web2ldap
              412  LOAD_ATTR                ldaputil
              414  LOAD_ATTR                dns
              416  LOAD_METHOD              dc_dn_lookup
              418  LOAD_DEREF               'self'
              420  LOAD_ATTR                dn
              422  CALL_METHOD_1         1  ''
              424  STORE_FAST               'dns_srv_rrs'

 L. 761       426  LOAD_CLOSURE             'self'
              428  BUILD_TUPLE_1         1 
              430  LOAD_LISTCOMP            '<code_object <listcomp>>'
              432  LOAD_STR                 'AppHandler.run.<locals>.<listcomp>'
              434  MAKE_FUNCTION_8          'closure'

 L. 763       436  LOAD_FAST                'dns_srv_rrs'

 L. 761       438  GET_ITER         
              440  CALL_FUNCTION_1       1  ''
              442  STORE_FAST               'init_uri_list'

 L. 765       444  LOAD_FAST                'init_uri_list'
          446_448  POP_JUMP_IF_TRUE    494  'to 494'

 L. 767       450  LOAD_GLOBAL              session_store
              452  LOAD_METHOD              delete
              454  LOAD_DEREF               'self'
              456  LOAD_ATTR                sid
              458  CALL_METHOD_1         1  ''
              460  POP_TOP          

 L. 768       462  LOAD_CONST               None
              464  LOAD_DEREF               'self'
              466  STORE_ATTR               sid

 L. 769       468  LOAD_GLOBAL              web2ldap
              470  LOAD_ATTR                app
              472  LOAD_ATTR                connect
              474  LOAD_ATTR                w2l_connect

 L. 770       476  LOAD_DEREF               'self'

 L. 771       478  LOAD_STR                 'Connect failed'

 L. 772       480  LOAD_STR                 'No host specified.'

 L. 769       482  LOAD_CONST               ('h1_msg', 'error_msg')
              484  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              486  POP_TOP          

 L. 774       488  POP_BLOCK        
              490  LOAD_CONST               None
              492  RETURN_VALUE     
            494_0  COME_FROM           446  '446'

 L. 775       494  LOAD_GLOBAL              len
              496  LOAD_FAST                'init_uri_list'
              498  CALL_FUNCTION_1       1  ''
              500  LOAD_CONST               1
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   518  'to 518'

 L. 776       508  LOAD_FAST                'init_uri_list'
              510  LOAD_CONST               0
              512  BINARY_SUBSCR    
              514  STORE_FAST               'init_uri'
              516  JUMP_FORWARD        540  'to 540'
            518_0  COME_FROM           504  '504'

 L. 779       518  LOAD_GLOBAL              web2ldap
              520  LOAD_ATTR                app
              522  LOAD_ATTR                srvrr
              524  LOAD_METHOD              w2l_chasesrvrecord

 L. 780       526  LOAD_DEREF               'self'

 L. 781       528  LOAD_FAST                'init_uri_list'

 L. 779       530  CALL_METHOD_2         2  ''
              532  POP_TOP          

 L. 783       534  POP_BLOCK        
              536  LOAD_CONST               None
              538  RETURN_VALUE     
            540_0  COME_FROM           516  '516'
              540  JUMP_FORWARD        584  'to 584'
            542_0  COME_FROM           406  '406'
            542_1  COME_FROM           380  '380'
            542_2  COME_FROM           366  '366'

 L. 784       542  LOAD_DEREF               'self'
              544  LOAD_ATTR                ldap_url
              546  LOAD_ATTR                hostport
              548  LOAD_CONST               None
              550  COMPARE_OP               is-not
          552_554  POP_JUMP_IF_FALSE   580  'to 580'

 L. 785       556  LOAD_GLOBAL              str
              558  LOAD_DEREF               'self'
              560  LOAD_ATTR                ldap_url
              562  LOAD_METHOD              connect_uri
              564  CALL_METHOD_0         0  ''
              566  LOAD_CONST               None
              568  LOAD_CONST               None
              570  BUILD_SLICE_2         2 
              572  BINARY_SUBSCR    
              574  CALL_FUNCTION_1       1  ''
              576  STORE_FAST               'init_uri'
              578  JUMP_FORWARD        584  'to 584'
            580_0  COME_FROM           552  '552'

 L. 787       580  LOAD_CONST               None
              582  STORE_FAST               'init_uri'
            584_0  COME_FROM           578  '578'
            584_1  COME_FROM           540  '540'

 L. 789       584  LOAD_FAST                'init_uri'
          586_588  POP_JUMP_IF_FALSE   796  'to 796'

 L. 790       590  LOAD_DEREF               'self'
              592  LOAD_ATTR                ls
              594  LOAD_CONST               None
              596  COMPARE_OP               is

 L. 789   598_600  POP_JUMP_IF_TRUE    630  'to 630'

 L. 790       602  LOAD_DEREF               'self'
              604  LOAD_ATTR                ls
              606  LOAD_ATTR                uri
              608  LOAD_CONST               None
              610  COMPARE_OP               is

 L. 789   612_614  POP_JUMP_IF_TRUE    630  'to 630'

 L. 790       616  LOAD_FAST                'init_uri'
              618  LOAD_DEREF               'self'
              620  LOAD_ATTR                ls
              622  LOAD_ATTR                uri
              624  COMPARE_OP               !=

 L. 789   626_628  POP_JUMP_IF_FALSE   796  'to 796'
            630_0  COME_FROM           612  '612'
            630_1  COME_FROM           598  '598'

 L. 793       630  LOAD_DEREF               'self'
              632  LOAD_METHOD              _del_session
              634  CALL_METHOD_0         0  ''
              636  POP_TOP          

 L. 794       638  LOAD_DEREF               'self'
              640  LOAD_METHOD              _new_session
              642  CALL_METHOD_0         0  ''
              644  POP_TOP          

 L. 796       646  LOAD_GLOBAL              web2ldapcnf
              648  LOAD_ATTR                hosts
              650  LOAD_ATTR                restricted_ldap_uri_list
          652_654  POP_JUMP_IF_FALSE   680  'to 680'

 L. 797       656  LOAD_FAST                'init_uri'
              658  LOAD_GLOBAL              web2ldap
              660  LOAD_ATTR                app
              662  LOAD_ATTR                cnf
              664  LOAD_ATTR                LDAP_URI_LIST_CHECK_DICT
              666  COMPARE_OP               not-in

 L. 796   668_670  POP_JUMP_IF_FALSE   680  'to 680'

 L. 798       672  LOAD_GLOBAL              ErrorExit
              674  LOAD_STR                 'Only pre-configured LDAP servers allowed.'
              676  CALL_FUNCTION_1       1  ''
              678  RAISE_VARARGS_1       1  'exception instance'
            680_0  COME_FROM           668  '668'
            680_1  COME_FROM           652  '652'

 L. 800       680  LOAD_FAST                'init_uri'
              682  LOAD_DEREF               'self'
              684  LOAD_ATTR                ls
              686  STORE_ATTR               uri

 L. 802       688  LOAD_DEREF               'self'
              690  LOAD_ATTR                ls
              692  LOAD_ATTR                open

 L. 803       694  LOAD_FAST                'init_uri'

 L. 804       696  LOAD_DEREF               'self'
              698  LOAD_METHOD              cfg_param
              700  LOAD_STR                 'timeout'
              702  LOAD_GLOBAL              web2ldap
              704  LOAD_ATTR                ldapsession
              706  LOAD_ATTR                LDAP_DEFAULT_TIMEOUT
              708  CALL_METHOD_2         2  ''

 L. 805       710  LOAD_DEREF               'self'
              712  LOAD_ATTR                ldap_url
              714  LOAD_METHOD              get_starttls_extop

 L. 806       716  LOAD_DEREF               'self'
              718  LOAD_METHOD              cfg_param
              720  LOAD_STR                 'starttls'
              722  LOAD_GLOBAL              web2ldap
              724  LOAD_ATTR                ldapsession
              726  LOAD_ATTR                START_TLS_NO
              728  CALL_METHOD_2         2  ''

 L. 805       730  CALL_METHOD_1         1  ''

 L. 808       732  LOAD_DEREF               'self'
              734  LOAD_ATTR                env

 L. 809       736  LOAD_DEREF               'self'
              738  LOAD_METHOD              cfg_param
              740  LOAD_STR                 'session_track_control'
              742  LOAD_CONST               0
              744  CALL_METHOD_2         2  ''

 L. 810       746  LOAD_DEREF               'self'
              748  LOAD_METHOD              cfg_param
              750  LOAD_STR                 'tls_options'
              752  BUILD_MAP_0           0 
              754  CALL_METHOD_2         2  ''

 L. 802       756  LOAD_CONST               ('tls_options',)
              758  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              760  POP_TOP          

 L. 813       762  LOAD_DEREF               'self'
              764  LOAD_METHOD              cfg_param
              766  LOAD_STR                 'timeout'
              768  LOAD_CONST               60
              770  CALL_METHOD_2         2  ''
              772  LOAD_DEREF               'self'
              774  LOAD_ATTR                ls
              776  LOAD_ATTR                l
              778  STORE_ATTR               timeout

 L. 816       780  LOAD_GLOBAL              session_store
              782  LOAD_METHOD              save
              784  LOAD_DEREF               'self'
              786  LOAD_ATTR                sid
              788  LOAD_DEREF               'self'
              790  LOAD_ATTR                ls
              792  CALL_METHOD_2         2  ''
              794  POP_TOP          
            796_0  COME_FROM           626  '626'
            796_1  COME_FROM           586  '586'

 L. 819       796  LOAD_DEREF               'self'
              798  LOAD_ATTR                ls
              800  LOAD_CONST               None
              802  COMPARE_OP               is
          804_806  POP_JUMP_IF_FALSE   824  'to 824'

 L. 821       808  LOAD_DEREF               'self'
              810  LOAD_METHOD              url_redirect
              812  LOAD_STR                 'No valid session!'
              814  CALL_METHOD_1         1  ''
              816  POP_TOP          

 L. 822       818  POP_BLOCK        
              820  LOAD_CONST               None
              822  RETURN_VALUE     
            824_0  COME_FROM           804  '804'

 L. 824       824  LOAD_DEREF               'self'
              826  LOAD_ATTR                ls
              828  LOAD_ATTR                uri
              830  LOAD_CONST               None
              832  COMPARE_OP               is
          834_836  POP_JUMP_IF_FALSE   882  'to 882'

 L. 825       838  LOAD_GLOBAL              session_store
              840  LOAD_METHOD              delete
              842  LOAD_DEREF               'self'
              844  LOAD_ATTR                sid
              846  CALL_METHOD_1         1  ''
              848  POP_TOP          

 L. 826       850  LOAD_CONST               None
              852  LOAD_DEREF               'self'
              854  STORE_ATTR               sid

 L. 827       856  LOAD_GLOBAL              web2ldap
              858  LOAD_ATTR                app
              860  LOAD_ATTR                connect
              862  LOAD_ATTR                w2l_connect

 L. 828       864  LOAD_DEREF               'self'

 L. 829       866  LOAD_STR                 'Connect failed'

 L. 830       868  LOAD_STR                 'No valid LDAP connection.'

 L. 827       870  LOAD_CONST               ('h1_msg', 'error_msg')
              872  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              874  POP_TOP          

 L. 832       876  POP_BLOCK        
              878  LOAD_CONST               None
              880  RETURN_VALUE     
            882_0  COME_FROM           834  '834'

 L. 836       882  LOAD_GLOBAL              session_store
              884  LOAD_METHOD              save
              886  LOAD_DEREF               'self'
              888  LOAD_ATTR                sid
              890  LOAD_DEREF               'self'
              892  LOAD_ATTR                ls
              894  CALL_METHOD_2         2  ''
              896  POP_TOP          

 L. 837       898  LOAD_DEREF               'self'
              900  LOAD_ATTR                dn
              902  LOAD_DEREF               'self'
              904  STORE_ATTR               dn

 L. 839       906  LOAD_DEREF               'self'
              908  LOAD_ATTR                form
              910  LOAD_METHOD              getInputValue

 L. 840       912  LOAD_STR                 'login_mech'

 L. 841       914  LOAD_DEREF               'self'
              916  LOAD_ATTR                ldap_url
              918  LOAD_ATTR                saslMech
          920_922  JUMP_IF_TRUE_OR_POP   926  'to 926'
              924  LOAD_STR                 ''
            926_0  COME_FROM           920  '920'
              926  BUILD_LIST_1          1 

 L. 839       928  CALL_METHOD_2         2  ''

 L. 842       930  LOAD_CONST               0

 L. 839       932  BINARY_SUBSCR    
              934  LOAD_METHOD              upper
              936  CALL_METHOD_0         0  ''
          938_940  JUMP_IF_TRUE_OR_POP   944  'to 944'

 L. 842       942  LOAD_CONST               None
            944_0  COME_FROM           938  '938'

 L. 839       944  STORE_FAST               'login_mech'

 L. 845       946  LOAD_FAST                'who'
              948  LOAD_CONST               None
              950  COMPARE_OP               is-not

 L. 844   952_954  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 846       956  LOAD_FAST                'cred'
              958  LOAD_CONST               None
              960  COMPARE_OP               is

 L. 844   962_964  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 847       966  LOAD_FAST                'login_mech'
          968_970  JUMP_IF_TRUE_OR_POP   974  'to 974'
              972  LOAD_STR                 ''
            974_0  COME_FROM           968  '968'
              974  LOAD_METHOD              encode
              976  LOAD_STR                 'ascii'
              978  CALL_METHOD_1         1  ''
              980  LOAD_GLOBAL              ldap0
              982  LOAD_ATTR                sasl
              984  LOAD_ATTR                SASL_NONINTERACTIVE_MECHS
              986  COMPARE_OP               not-in

 L. 844   988_990  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 850       992  LOAD_GLOBAL              web2ldap
              994  LOAD_ATTR                app
              996  LOAD_ATTR                login
              998  LOAD_ATTR                w2l_login

 L. 851      1000  LOAD_DEREF               'self'

 L. 852      1002  LOAD_STR                 ''

 L. 853      1004  LOAD_FAST                'who'

 L. 853      1006  LOAD_CONST               0

 L. 853      1008  LOAD_CONST               1

 L. 854      1010  LOAD_DEREF               'self'
             1012  LOAD_ATTR                ldap_url
             1014  LOAD_ATTR                saslMech

 L. 850      1016  LOAD_CONST               ('login_msg', 'who', 'relogin', 'nomenu', 'login_default_mech')
             1018  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1020  POP_TOP          

 L. 856      1022  POP_BLOCK        
             1024  LOAD_CONST               None
             1026  RETURN_VALUE     
           1028_0  COME_FROM           988  '988'
           1028_1  COME_FROM           962  '962'
           1028_2  COME_FROM           952  '952'

 L. 859      1028  LOAD_FAST                'who'
             1030  LOAD_CONST               None
             1032  COMPARE_OP               is-not

 L. 858  1034_1036  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 859      1038  LOAD_FAST                'cred'
             1040  LOAD_CONST               None
             1042  COMPARE_OP               is-not

 L. 858  1044_1046  POP_JUMP_IF_TRUE   1078  'to 1078'
           1048_0  COME_FROM          1034  '1034'

 L. 860      1048  LOAD_FAST                'login_mech'
             1050  LOAD_CONST               None
             1052  COMPARE_OP               is-not

 L. 858  1054_1056  POP_JUMP_IF_FALSE  1302  'to 1302'

 L. 860      1058  LOAD_FAST                'login_mech'
             1060  LOAD_METHOD              encode
             1062  LOAD_STR                 'ascii'
             1064  CALL_METHOD_1         1  ''
             1066  LOAD_GLOBAL              ldap0
             1068  LOAD_ATTR                sasl
             1070  LOAD_ATTR                SASL_NONINTERACTIVE_MECHS
             1072  COMPARE_OP               in

 L. 858  1074_1076  POP_JUMP_IF_FALSE  1302  'to 1302'
           1078_0  COME_FROM          1044  '1044'

 L. 862      1078  LOAD_DEREF               'self'
             1080  LOAD_ATTR                dn
             1082  LOAD_DEREF               'self'
             1084  STORE_ATTR               dn

 L. 864      1086  LOAD_DEREF               'self'
             1088  LOAD_ATTR                form
             1090  LOAD_METHOD              getInputValue

 L. 865      1092  LOAD_STR                 'login_search_root'

 L. 866      1094  LOAD_DEREF               'self'
             1096  LOAD_ATTR                naming_context
             1098  BUILD_LIST_1          1 

 L. 864      1100  CALL_METHOD_2         2  ''

 L. 867      1102  LOAD_CONST               0

 L. 864      1104  BINARY_SUBSCR    
             1106  STORE_FAST               'login_search_root'

 L. 868      1108  SETUP_FINALLY      1226  'to 1226'

 L. 869      1110  LOAD_DEREF               'self'
             1112  LOAD_ATTR                ls
             1114  LOAD_ATTR                bind

 L. 870      1116  LOAD_FAST                'who'

 L. 871      1118  LOAD_FAST                'cred'
         1120_1122  JUMP_IF_TRUE_OR_POP  1126  'to 1126'
             1124  LOAD_STR                 ''
           1126_0  COME_FROM          1120  '1120'

 L. 872      1126  LOAD_FAST                'login_mech'

 L. 873      1128  LOAD_STR                 ''
             1130  LOAD_METHOD              join

 L. 874      1132  LOAD_DEREF               'self'
             1134  LOAD_ATTR                form
             1136  LOAD_METHOD              getInputValue
             1138  LOAD_STR                 'login_authzid_prefix'
             1140  LOAD_STR                 ''
             1142  BUILD_LIST_1          1 
             1144  CALL_METHOD_2         2  ''
             1146  LOAD_CONST               0
             1148  BINARY_SUBSCR    

 L. 875      1150  LOAD_DEREF               'self'
             1152  LOAD_ATTR                form
             1154  LOAD_METHOD              getInputValue

 L. 876      1156  LOAD_STR                 'login_authzid'

 L. 877      1158  LOAD_DEREF               'self'
             1160  LOAD_ATTR                ldap_url
             1162  LOAD_ATTR                saslAuthzId
         1164_1166  JUMP_IF_TRUE_OR_POP  1170  'to 1170'
             1168  LOAD_STR                 ''
           1170_0  COME_FROM          1164  '1164'
             1170  BUILD_LIST_1          1 

 L. 875      1172  CALL_METHOD_2         2  ''

 L. 878      1174  LOAD_CONST               0

 L. 875      1176  BINARY_SUBSCR    

 L. 873      1178  BUILD_TUPLE_2         2 
             1180  CALL_METHOD_1         1  ''
         1182_1184  JUMP_IF_TRUE_OR_POP  1188  'to 1188'

 L. 879      1186  LOAD_CONST               None
           1188_0  COME_FROM          1182  '1182'

 L. 880      1188  LOAD_DEREF               'self'
             1190  LOAD_ATTR                form
             1192  LOAD_METHOD              getInputValue
             1194  LOAD_STR                 'login_realm'
             1196  LOAD_DEREF               'self'
             1198  LOAD_ATTR                ldap_url
             1200  LOAD_ATTR                saslRealm
             1202  BUILD_LIST_1          1 
             1204  CALL_METHOD_2         2  ''
             1206  LOAD_CONST               0
             1208  BINARY_SUBSCR    

 L. 881      1210  LOAD_DEREF               'self'
             1212  LOAD_ATTR                binddn_mapping

 L. 882      1214  LOAD_FAST                'login_search_root'

 L. 869      1216  LOAD_CONST               ('loginSearchRoot',)
             1218  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1220  POP_TOP          
             1222  POP_BLOCK        
             1224  JUMP_FORWARD       1300  'to 1300'
           1226_0  COME_FROM_FINALLY  1108  '1108'

 L. 884      1226  DUP_TOP          
             1228  LOAD_GLOBAL              ldap0
             1230  LOAD_ATTR                NO_SUCH_OBJECT
             1232  COMPARE_OP               exception-match
         1234_1236  POP_JUMP_IF_FALSE  1298  'to 1298'
             1238  POP_TOP          
             1240  STORE_FAST               'err'
             1242  POP_TOP          
             1244  SETUP_FINALLY      1286  'to 1286'

 L. 885      1246  LOAD_GLOBAL              web2ldap
             1248  LOAD_ATTR                app
             1250  LOAD_ATTR                login
             1252  LOAD_ATTR                w2l_login

 L. 886      1254  LOAD_DEREF               'self'

 L. 887      1256  LOAD_DEREF               'self'
             1258  LOAD_METHOD              ldap_error_msg
             1260  LOAD_FAST                'err'
             1262  CALL_METHOD_1         1  ''

 L. 888      1264  LOAD_FAST                'who'

 L. 888      1266  LOAD_CONST               True

 L. 885      1268  LOAD_CONST               ('login_msg', 'who', 'relogin')
             1270  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1272  POP_TOP          

 L. 890      1274  POP_BLOCK        
             1276  POP_EXCEPT       
             1278  CALL_FINALLY       1286  'to 1286'
             1280  POP_BLOCK        
             1282  LOAD_CONST               None
             1284  RETURN_VALUE     
           1286_0  COME_FROM          1278  '1278'
           1286_1  COME_FROM_FINALLY  1244  '1244'
             1286  LOAD_CONST               None
             1288  STORE_FAST               'err'
             1290  DELETE_FAST              'err'
             1292  END_FINALLY      
             1294  POP_EXCEPT       
             1296  JUMP_FORWARD       1300  'to 1300'
           1298_0  COME_FROM          1234  '1234'
             1298  END_FINALLY      
           1300_0  COME_FROM          1296  '1296'
           1300_1  COME_FROM          1224  '1224'
             1300  JUMP_FORWARD       1312  'to 1312'
           1302_0  COME_FROM          1074  '1074'
           1302_1  COME_FROM          1054  '1054'

 L. 893      1302  LOAD_DEREF               'self'
             1304  LOAD_ATTR                ls
             1306  LOAD_METHOD              init_rootdse
             1308  CALL_METHOD_0         0  ''
             1310  POP_TOP          
           1312_0  COME_FROM          1300  '1300'

 L. 898      1312  LOAD_GLOBAL              isinstance
             1314  LOAD_DEREF               'self'
             1316  LOAD_ATTR                ls
             1318  LOAD_GLOBAL              LDAPSession
             1320  CALL_FUNCTION_2       2  ''
         1322_1324  POP_JUMP_IF_FALSE  1340  'to 1340'
             1326  LOAD_DEREF               'self'
             1328  LOAD_ATTR                ls
             1330  LOAD_ATTR                uri
             1332  LOAD_CONST               None
             1334  COMPARE_OP               is
         1336_1338  POP_JUMP_IF_FALSE  1356  'to 1356'
           1340_0  COME_FROM          1322  '1322'

 L. 899      1340  LOAD_DEREF               'self'
             1342  LOAD_METHOD              url_redirect
             1344  LOAD_STR                 'No valid LDAP connection!'
             1346  CALL_METHOD_1         1  ''
             1348  POP_TOP          

 L. 900      1350  POP_BLOCK        
             1352  LOAD_CONST               None
             1354  RETURN_VALUE     
           1356_0  COME_FROM          1336  '1336'

 L. 903      1356  LOAD_GLOBAL              session_store
             1358  LOAD_METHOD              save
             1360  LOAD_DEREF               'self'
             1362  LOAD_ATTR                sid
             1364  LOAD_DEREF               'self'
             1366  LOAD_ATTR                ls
             1368  CALL_METHOD_2         2  ''
             1370  POP_TOP          

 L. 906      1372  LOAD_DEREF               'self'
             1374  LOAD_ATTR                dn
             1376  LOAD_DEREF               'self'
             1378  STORE_ATTR               dn

 L. 909      1380  SETUP_FINALLY      1394  'to 1394'

 L. 910      1382  LOAD_DEREF               'self'
             1384  LOAD_METHOD              dispatch
             1386  CALL_METHOD_0         0  ''
             1388  POP_TOP          
             1390  POP_BLOCK        
             1392  JUMP_FORWARD       1444  'to 1444'
           1394_0  COME_FROM_FINALLY  1380  '1380'

 L. 911      1394  DUP_TOP          
             1396  LOAD_GLOBAL              ldap0
             1398  LOAD_ATTR                SERVER_DOWN
             1400  COMPARE_OP               exception-match
         1402_1404  POP_JUMP_IF_FALSE  1442  'to 1442'
             1406  POP_TOP          
             1408  POP_TOP          
             1410  POP_TOP          

 L. 913      1412  LOAD_DEREF               'self'
             1414  LOAD_ATTR                ls
             1416  LOAD_ATTR                l
             1418  LOAD_METHOD              reconnect
             1420  LOAD_DEREF               'self'
             1422  LOAD_ATTR                ls
             1424  LOAD_ATTR                uri
             1426  CALL_METHOD_1         1  ''
             1428  POP_TOP          

 L. 914      1430  LOAD_DEREF               'self'
             1432  LOAD_METHOD              dispatch
             1434  CALL_METHOD_0         0  ''
             1436  POP_TOP          
             1438  POP_EXCEPT       
             1440  JUMP_FORWARD       1460  'to 1460'
           1442_0  COME_FROM          1402  '1402'
             1442  END_FINALLY      
           1444_0  COME_FROM          1392  '1392'

 L. 917      1444  LOAD_GLOBAL              session_store
             1446  LOAD_METHOD              save
             1448  LOAD_DEREF               'self'
             1450  LOAD_ATTR                sid
             1452  LOAD_DEREF               'self'
             1454  LOAD_ATTR                ls
             1456  CALL_METHOD_2         2  ''
             1458  POP_TOP          
           1460_0  COME_FROM          1440  '1440'
             1460  POP_BLOCK        
         1462_1464  JUMP_FORWARD       2962  'to 2962'
           1466_0  COME_FROM_FINALLY   104  '104'

 L. 919      1466  DUP_TOP          
             1468  LOAD_GLOBAL              web2ldap
             1470  LOAD_ATTR                web
             1472  LOAD_ATTR                forms
             1474  LOAD_ATTR                FormException
             1476  COMPARE_OP               exception-match
         1478_1480  POP_JUMP_IF_FALSE  1560  'to 1560'
             1482  POP_TOP          
             1484  STORE_FAST               'form_error'
             1486  POP_TOP          
             1488  SETUP_FINALLY      1546  'to 1546'

 L. 920      1490  LOAD_GLOBAL              log_exception
             1492  LOAD_DEREF               'self'
             1494  LOAD_ATTR                env
             1496  LOAD_DEREF               'self'
             1498  LOAD_ATTR                ls
             1500  LOAD_DEREF               'self'
             1502  LOAD_ATTR                dn
             1504  LOAD_GLOBAL              web2ldapcnf
             1506  LOAD_ATTR                log_error_details
             1508  CALL_FUNCTION_4       4  ''
             1510  POP_TOP          

 L. 921      1512  LOAD_GLOBAL              exception_message

 L. 922      1514  LOAD_DEREF               'self'

 L. 923      1516  LOAD_STR                 'Error parsing form'

 L. 924      1518  LOAD_STR                 'Error parsing form:<br>%s'

 L. 925      1520  LOAD_DEREF               'self'
             1522  LOAD_ATTR                form
             1524  LOAD_METHOD              utf2display
             1526  LOAD_GLOBAL              str
             1528  LOAD_FAST                'form_error'
             1530  CALL_FUNCTION_1       1  ''
             1532  CALL_METHOD_1         1  ''

 L. 924      1534  BUILD_TUPLE_1         1 
             1536  BINARY_MODULO    

 L. 921      1538  CALL_FUNCTION_3       3  ''
             1540  POP_TOP          
             1542  POP_BLOCK        
             1544  BEGIN_FINALLY    
           1546_0  COME_FROM_FINALLY  1488  '1488'
             1546  LOAD_CONST               None
             1548  STORE_FAST               'form_error'
             1550  DELETE_FAST              'form_error'
             1552  END_FINALLY      
             1554  POP_EXCEPT       
         1556_1558  JUMP_FORWARD       2962  'to 2962'
           1560_0  COME_FROM          1478  '1478'

 L. 929      1560  DUP_TOP          
             1562  LOAD_GLOBAL              ldap0
             1564  LOAD_ATTR                SERVER_DOWN
             1566  COMPARE_OP               exception-match
         1568_1570  POP_JUMP_IF_FALSE  1664  'to 1664'
             1572  POP_TOP          
             1574  STORE_FAST               'err'
             1576  POP_TOP          
             1578  SETUP_FINALLY      1650  'to 1650'

 L. 931      1580  LOAD_GLOBAL              session_store
             1582  LOAD_METHOD              delete
             1584  LOAD_DEREF               'self'
             1586  LOAD_ATTR                sid
             1588  CALL_METHOD_1         1  ''
             1590  POP_TOP          

 L. 932      1592  LOAD_CONST               None
             1594  LOAD_DEREF               'self'
             1596  STORE_ATTR               sid

 L. 934      1598  LOAD_GLOBAL              web2ldap
             1600  LOAD_ATTR                app
             1602  LOAD_ATTR                connect
             1604  LOAD_ATTR                w2l_connect

 L. 935      1606  LOAD_DEREF               'self'

 L. 936      1608  LOAD_STR                 'Connect failed'

 L. 937      1610  LOAD_STR                 'Connecting to %s impossible!<br>%s'

 L. 938      1612  LOAD_DEREF               'self'
             1614  LOAD_ATTR                form
             1616  LOAD_METHOD              utf2display
             1618  LOAD_FAST                'init_uri'
         1620_1622  JUMP_IF_TRUE_OR_POP  1626  'to 1626'
             1624  LOAD_STR                 '-'
           1626_0  COME_FROM          1620  '1620'
             1626  CALL_METHOD_1         1  ''

 L. 939      1628  LOAD_DEREF               'self'
             1630  LOAD_METHOD              ldap_error_msg
             1632  LOAD_FAST                'err'
             1634  CALL_METHOD_1         1  ''

 L. 937      1636  BUILD_TUPLE_2         2 
             1638  BINARY_MODULO    

 L. 934      1640  LOAD_CONST               ('h1_msg', 'error_msg')
             1642  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1644  POP_TOP          
             1646  POP_BLOCK        
             1648  BEGIN_FINALLY    
           1650_0  COME_FROM_FINALLY  1578  '1578'
             1650  LOAD_CONST               None
             1652  STORE_FAST               'err'
             1654  DELETE_FAST              'err'
             1656  END_FINALLY      
             1658  POP_EXCEPT       
         1660_1662  JUMP_FORWARD       2962  'to 2962'
           1664_0  COME_FROM          1568  '1568'

 L. 943      1664  DUP_TOP          
             1666  LOAD_GLOBAL              ldap0
             1668  LOAD_ATTR                NO_SUCH_OBJECT
             1670  COMPARE_OP               exception-match
         1672_1674  POP_JUMP_IF_FALSE  1890  'to 1890'
             1676  POP_TOP          
             1678  STORE_FAST               'ldap_err'
             1680  POP_TOP          
             1682  SETUP_FINALLY      1876  'to 1876'

 L. 946      1684  LOAD_GLOBAL              web2ldap
             1686  LOAD_ATTR                ldaputil
             1688  LOAD_ATTR                dns
             1690  LOAD_METHOD              dc_dn_lookup
             1692  LOAD_DEREF               'self'
             1694  LOAD_ATTR                dn
             1696  CALL_METHOD_1         1  ''
             1698  STORE_FAST               'host_list'

 L. 947      1700  LOAD_DEREF               'self'
             1702  LOAD_METHOD              log
             1704  LOAD_GLOBAL              logging
             1706  LOAD_ATTR                DEBUG
             1708  LOAD_STR                 'host_list = %r'
             1710  LOAD_FAST                'host_list'
             1712  CALL_METHOD_3         3  ''
             1714  POP_TOP          

 L. 948      1716  LOAD_FAST                'host_list'
         1718_1720  POP_JUMP_IF_FALSE  1768  'to 1768'
             1722  LOAD_GLOBAL              ExtendedLDAPUrl
             1724  LOAD_DEREF               'self'
             1726  LOAD_ATTR                ls
             1728  LOAD_ATTR                uri
             1730  CALL_FUNCTION_1       1  ''
             1732  LOAD_ATTR                hostport
             1734  LOAD_FAST                'host_list'
             1736  COMPARE_OP               not-in
         1738_1740  POP_JUMP_IF_FALSE  1768  'to 1768'

 L. 950      1742  LOAD_GLOBAL              web2ldap
             1744  LOAD_ATTR                app
             1746  LOAD_ATTR                srvrr
             1748  LOAD_METHOD              w2l_chasesrvrecord
             1750  LOAD_DEREF               'self'
             1752  LOAD_FAST                'host_list'
             1754  CALL_METHOD_2         2  ''
             1756  POP_TOP          

 L. 951      1758  POP_BLOCK        
             1760  POP_EXCEPT       
             1762  CALL_FINALLY       1876  'to 1876'
             1764  LOAD_CONST               None
             1766  RETURN_VALUE     
           1768_0  COME_FROM          1738  '1738'
           1768_1  COME_FROM          1718  '1718'

 L. 954      1768  LOAD_GLOBAL              log_exception
             1770  LOAD_DEREF               'self'
             1772  LOAD_ATTR                env
             1774  LOAD_DEREF               'self'
             1776  LOAD_ATTR                ls
             1778  LOAD_DEREF               'self'
             1780  LOAD_ATTR                dn
             1782  LOAD_GLOBAL              web2ldapcnf
             1784  LOAD_ATTR                log_error_details
             1786  CALL_FUNCTION_4       4  ''
             1788  POP_TOP          

 L. 955      1790  LOAD_DEREF               'self'
             1792  LOAD_ATTR                dn
             1794  STORE_FAST               'failed_dn'

 L. 956      1796  LOAD_STR                 'matched'
             1798  LOAD_FAST                'ldap_err'
             1800  LOAD_ATTR                args
             1802  LOAD_CONST               0
             1804  BINARY_SUBSCR    
             1806  COMPARE_OP               in
         1808_1810  POP_JUMP_IF_FALSE  1838  'to 1838'

 L. 957      1812  LOAD_FAST                'ldap_err'
             1814  LOAD_ATTR                args
             1816  LOAD_CONST               0
             1818  BINARY_SUBSCR    
             1820  LOAD_STR                 'matched'
             1822  BINARY_SUBSCR    
             1824  LOAD_METHOD              decode
             1826  LOAD_DEREF               'self'
             1828  LOAD_ATTR                ls
             1830  LOAD_ATTR                charset
             1832  CALL_METHOD_1         1  ''
             1834  LOAD_DEREF               'self'
             1836  STORE_ATTR               dn
           1838_0  COME_FROM          1808  '1808'

 L. 958      1838  LOAD_GLOBAL              exception_message

 L. 959      1840  LOAD_DEREF               'self'

 L. 960      1842  LOAD_STR                 'No such object'

 L. 961      1844  LOAD_DEREF               'self'
             1846  LOAD_ATTR                ldap_error_msg

 L. 962      1848  LOAD_FAST                'ldap_err'

 L. 963      1850  LOAD_STR                 '{{error_msg}}<br>{0}{{matched_dn}}'
             1852  LOAD_METHOD              format

 L. 964      1854  LOAD_DEREF               'self'
             1856  LOAD_METHOD              display_dn
             1858  LOAD_FAST                'failed_dn'
             1860  CALL_METHOD_1         1  ''

 L. 963      1862  CALL_METHOD_1         1  ''

 L. 961      1864  LOAD_CONST               ('template',)
             1866  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 958      1868  CALL_FUNCTION_3       3  ''
             1870  POP_TOP          
             1872  POP_BLOCK        
             1874  BEGIN_FINALLY    
           1876_0  COME_FROM          1762  '1762'
           1876_1  COME_FROM_FINALLY  1682  '1682'
             1876  LOAD_CONST               None
             1878  STORE_FAST               'ldap_err'
             1880  DELETE_FAST              'ldap_err'
             1882  END_FINALLY      
             1884  POP_EXCEPT       
         1886_1888  JUMP_FORWARD       2962  'to 2962'
           1890_0  COME_FROM          1672  '1672'

 L. 969      1890  DUP_TOP          
             1892  LOAD_GLOBAL              ldap0
             1894  LOAD_ATTR                PARTIAL_RESULTS
             1896  LOAD_GLOBAL              ldap0
             1898  LOAD_ATTR                REFERRAL
             1900  BUILD_TUPLE_2         2 
             1902  COMPARE_OP               exception-match
         1904_1906  POP_JUMP_IF_FALSE  1950  'to 1950'
             1908  POP_TOP          
             1910  STORE_FAST               'err'
             1912  POP_TOP          
             1914  SETUP_FINALLY      1936  'to 1936'

 L. 970      1916  LOAD_GLOBAL              web2ldap
             1918  LOAD_ATTR                app
             1920  LOAD_ATTR                referral
             1922  LOAD_METHOD              w2l_chasereferral
             1924  LOAD_DEREF               'self'
             1926  LOAD_FAST                'err'
             1928  CALL_METHOD_2         2  ''
             1930  POP_TOP          
             1932  POP_BLOCK        
             1934  BEGIN_FINALLY    
           1936_0  COME_FROM_FINALLY  1914  '1914'
             1936  LOAD_CONST               None
             1938  STORE_FAST               'err'
             1940  DELETE_FAST              'err'
             1942  END_FINALLY      
             1944  POP_EXCEPT       
         1946_1948  JUMP_FORWARD       2962  'to 2962'
           1950_0  COME_FROM          1904  '1904'

 L. 972      1950  DUP_TOP          

 L. 973      1952  LOAD_GLOBAL              ldap0
             1954  LOAD_ATTR                INSUFFICIENT_ACCESS

 L. 974      1956  LOAD_GLOBAL              ldap0
             1958  LOAD_ATTR                STRONG_AUTH_REQUIRED

 L. 975      1960  LOAD_GLOBAL              ldap0
             1962  LOAD_ATTR                INAPPROPRIATE_AUTH

 L. 976      1964  LOAD_GLOBAL              web2ldap
             1966  LOAD_ATTR                ldapsession
             1968  LOAD_ATTR                UsernameNotFound

 L. 972      1970  BUILD_TUPLE_4         4 
             1972  COMPARE_OP               exception-match
         1974_1976  POP_JUMP_IF_FALSE  2032  'to 2032'
             1978  POP_TOP          
             1980  STORE_FAST               'err'
             1982  POP_TOP          
             1984  SETUP_FINALLY      2018  'to 2018'

 L. 978      1986  LOAD_GLOBAL              web2ldap
             1988  LOAD_ATTR                app
             1990  LOAD_ATTR                login
             1992  LOAD_ATTR                w2l_login

 L. 979      1994  LOAD_DEREF               'self'

 L. 980      1996  LOAD_STR                 ''

 L. 981      1998  LOAD_DEREF               'self'
             2000  LOAD_METHOD              ldap_error_msg
             2002  LOAD_FAST                'err'
             2004  CALL_METHOD_1         1  ''

 L. 982      2006  LOAD_CONST               True

 L. 978      2008  LOAD_CONST               ('who', 'login_msg', 'relogin')
             2010  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2012  POP_TOP          
             2014  POP_BLOCK        
             2016  BEGIN_FINALLY    
           2018_0  COME_FROM_FINALLY  1984  '1984'
             2018  LOAD_CONST               None
             2020  STORE_FAST               'err'
             2022  DELETE_FAST              'err'
             2024  END_FINALLY      
             2026  POP_EXCEPT       
         2028_2030  JUMP_FORWARD       2962  'to 2962'
           2032_0  COME_FROM          1974  '1974'

 L. 985      2032  DUP_TOP          

 L. 986      2034  LOAD_GLOBAL              ldap0
             2036  LOAD_ATTR                INVALID_CREDENTIALS

 L. 985      2038  BUILD_TUPLE_1         1 
             2040  COMPARE_OP               exception-match
         2042_2044  POP_JUMP_IF_FALSE  2100  'to 2100'
             2046  POP_TOP          
             2048  STORE_FAST               'err'
             2050  POP_TOP          
             2052  SETUP_FINALLY      2086  'to 2086'

 L. 988      2054  LOAD_GLOBAL              web2ldap
             2056  LOAD_ATTR                app
             2058  LOAD_ATTR                login
             2060  LOAD_ATTR                w2l_login

 L. 989      2062  LOAD_DEREF               'self'

 L. 990      2064  LOAD_DEREF               'self'
             2066  LOAD_METHOD              ldap_error_msg
             2068  LOAD_FAST                'err'
             2070  CALL_METHOD_1         1  ''

 L. 991      2072  LOAD_FAST                'who'

 L. 991      2074  LOAD_CONST               True

 L. 988      2076  LOAD_CONST               ('login_msg', 'who', 'relogin')
             2078  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2080  POP_TOP          
             2082  POP_BLOCK        
             2084  BEGIN_FINALLY    
           2086_0  COME_FROM_FINALLY  2052  '2052'
             2086  LOAD_CONST               None
             2088  STORE_FAST               'err'
             2090  DELETE_FAST              'err'
             2092  END_FINALLY      
             2094  POP_EXCEPT       
         2096_2098  JUMP_FORWARD       2962  'to 2962'
           2100_0  COME_FROM          2042  '2042'

 L. 994      2100  DUP_TOP          

 L. 995      2102  LOAD_GLOBAL              web2ldap
             2104  LOAD_ATTR                ldapsession
             2106  LOAD_ATTR                InvalidSimpleBindDN

 L. 996      2108  LOAD_GLOBAL              web2ldap
             2110  LOAD_ATTR                ldapsession
             2112  LOAD_ATTR                UsernameNotUnique

 L. 994      2114  BUILD_TUPLE_2         2 
             2116  COMPARE_OP               exception-match
         2118_2120  POP_JUMP_IF_FALSE  2182  'to 2182'
             2122  POP_TOP          
             2124  STORE_FAST               'err'
             2126  POP_TOP          
             2128  SETUP_FINALLY      2168  'to 2168'

 L. 998      2130  LOAD_GLOBAL              web2ldap
             2132  LOAD_ATTR                app
             2134  LOAD_ATTR                login
             2136  LOAD_ATTR                w2l_login

 L. 999      2138  LOAD_DEREF               'self'

 L.1000      2140  LOAD_DEREF               'self'
             2142  LOAD_ATTR                form
             2144  LOAD_METHOD              utf2display
             2146  LOAD_GLOBAL              str
             2148  LOAD_FAST                'err'
             2150  CALL_FUNCTION_1       1  ''
             2152  CALL_METHOD_1         1  ''

 L.1001      2154  LOAD_FAST                'who'

 L.1001      2156  LOAD_CONST               True

 L. 998      2158  LOAD_CONST               ('login_msg', 'who', 'relogin')
             2160  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2162  POP_TOP          
             2164  POP_BLOCK        
             2166  BEGIN_FINALLY    
           2168_0  COME_FROM_FINALLY  2128  '2128'
             2168  LOAD_CONST               None
             2170  STORE_FAST               'err'
             2172  DELETE_FAST              'err'
             2174  END_FINALLY      
             2176  POP_EXCEPT       
         2178_2180  JUMP_FORWARD       2962  'to 2962'
           2182_0  COME_FROM          2118  '2118'

 L.1004      2182  DUP_TOP          
             2184  LOAD_GLOBAL              PasswordPolicyExpirationWarning
             2186  COMPARE_OP               exception-match
         2188_2190  POP_JUMP_IF_FALSE  2312  'to 2312'
             2192  POP_TOP          
             2194  STORE_FAST               'err'
             2196  POP_TOP          
             2198  SETUP_FINALLY      2298  'to 2298'

 L.1006      2200  LOAD_DEREF               'self'
             2202  LOAD_ATTR                ls
             2204  LOAD_ATTR                l
             2206  LOAD_METHOD              whoami_s
             2208  CALL_METHOD_0         0  ''
             2210  LOAD_CONST               3
             2212  LOAD_CONST               None
             2214  BUILD_SLICE_2         2 
             2216  BINARY_SUBSCR    
         2218_2220  JUMP_IF_TRUE_OR_POP  2226  'to 2226'
             2222  LOAD_FAST                'err'
             2224  LOAD_ATTR                who
           2226_0  COME_FROM          2218  '2218'
             2226  LOAD_DEREF               'self'
             2228  STORE_ATTR               dn

 L.1008      2230  LOAD_GLOBAL              web2ldap
             2232  LOAD_ATTR                app
             2234  LOAD_ATTR                passwd
             2236  LOAD_METHOD              passwd_form

 L.1009      2238  LOAD_DEREF               'self'

 L.1010      2240  LOAD_STR                 ''

 L.1011      2242  LOAD_DEREF               'self'
             2244  LOAD_ATTR                dn

 L.1012      2246  LOAD_CONST               None

 L.1013      2248  LOAD_STR                 'Password change needed'

 L.1014      2250  LOAD_DEREF               'self'
             2252  LOAD_ATTR                form
             2254  LOAD_METHOD              utf2display

 L.1015      2256  LOAD_STR                 'Password will expire in %s!'

 L.1016      2258  LOAD_GLOBAL              web2ldap
             2260  LOAD_ATTR                app
             2262  LOAD_ATTR                gui
             2264  LOAD_METHOD              ts2repr

 L.1017      2266  LOAD_GLOBAL              web2ldap
             2268  LOAD_ATTR                app
             2270  LOAD_ATTR                schema
             2272  LOAD_ATTR                syntaxes
             2274  LOAD_ATTR                Timespan
             2276  LOAD_ATTR                time_divisors

 L.1018      2278  LOAD_STR                 ' '

 L.1019      2280  LOAD_FAST                'err'
             2282  LOAD_ATTR                timeBeforeExpiration

 L.1016      2284  CALL_METHOD_3         3  ''

 L.1015      2286  BINARY_MODULO    

 L.1014      2288  CALL_METHOD_1         1  ''

 L.1008      2290  CALL_METHOD_6         6  ''
             2292  POP_TOP          
             2294  POP_BLOCK        
             2296  BEGIN_FINALLY    
           2298_0  COME_FROM_FINALLY  2198  '2198'
             2298  LOAD_CONST               None
             2300  STORE_FAST               'err'
             2302  DELETE_FAST              'err'
             2304  END_FINALLY      
             2306  POP_EXCEPT       
         2308_2310  JUMP_FORWARD       2962  'to 2962'
           2312_0  COME_FROM          2188  '2188'

 L.1025      2312  DUP_TOP          
             2314  LOAD_GLOBAL              PasswordPolicyException
             2316  COMPARE_OP               exception-match
         2318_2320  POP_JUMP_IF_FALSE  2424  'to 2424'
             2322  POP_TOP          
             2324  STORE_FAST               'err'
             2326  POP_TOP          
             2328  SETUP_FINALLY      2410  'to 2410'

 L.1027      2330  LOAD_DEREF               'self'
             2332  LOAD_ATTR                ls
             2334  LOAD_ATTR                l
             2336  LOAD_METHOD              whoami_s
             2338  CALL_METHOD_0         0  ''
             2340  LOAD_CONST               3
             2342  LOAD_CONST               None
             2344  BUILD_SLICE_2         2 
             2346  BINARY_SUBSCR    
         2348_2350  JUMP_IF_TRUE_OR_POP  2356  'to 2356'
             2352  LOAD_FAST                'err'
             2354  LOAD_ATTR                who
           2356_0  COME_FROM          2348  '2348'
             2356  LOAD_METHOD              decode
             2358  LOAD_DEREF               'self'
             2360  LOAD_ATTR                ls
             2362  LOAD_ATTR                charset
             2364  CALL_METHOD_1         1  ''
             2366  LOAD_DEREF               'self'
             2368  STORE_ATTR               dn

 L.1029      2370  LOAD_GLOBAL              web2ldap
             2372  LOAD_ATTR                app
             2374  LOAD_ATTR                passwd
             2376  LOAD_METHOD              passwd_form

 L.1030      2378  LOAD_DEREF               'self'

 L.1031      2380  LOAD_STR                 ''

 L.1032      2382  LOAD_DEREF               'self'
             2384  LOAD_ATTR                dn

 L.1033      2386  LOAD_CONST               None

 L.1034      2388  LOAD_STR                 'Password change needed'

 L.1035      2390  LOAD_DEREF               'self'
             2392  LOAD_ATTR                form
             2394  LOAD_METHOD              utf2display
             2396  LOAD_FAST                'err'
             2398  LOAD_ATTR                desc
             2400  CALL_METHOD_1         1  ''

 L.1029      2402  CALL_METHOD_6         6  ''
             2404  POP_TOP          
             2406  POP_BLOCK        
             2408  BEGIN_FINALLY    
           2410_0  COME_FROM_FINALLY  2328  '2328'
             2410  LOAD_CONST               None
             2412  STORE_FAST               'err'
             2414  DELETE_FAST              'err'
             2416  END_FINALLY      
             2418  POP_EXCEPT       
         2420_2422  JUMP_FORWARD       2962  'to 2962'
           2424_0  COME_FROM          2318  '2318'

 L.1038      2424  DUP_TOP          

 L.1039      2426  LOAD_GLOBAL              socket
             2428  LOAD_ATTR                error

 L.1040      2430  LOAD_GLOBAL              socket
             2432  LOAD_ATTR                gaierror

 L.1041      2434  LOAD_GLOBAL              IOError

 L.1042      2436  LOAD_GLOBAL              UnicodeError

 L.1038      2438  BUILD_TUPLE_4         4 
             2440  COMPARE_OP               exception-match
         2442_2444  POP_JUMP_IF_FALSE  2526  'to 2526'
             2446  POP_TOP          
             2448  STORE_FAST               'err'
             2450  POP_TOP          
             2452  SETUP_FINALLY      2512  'to 2512'

 L.1044      2454  LOAD_GLOBAL              log_exception
             2456  LOAD_DEREF               'self'
             2458  LOAD_ATTR                env
             2460  LOAD_DEREF               'self'
             2462  LOAD_ATTR                ls
             2464  LOAD_DEREF               'self'
             2466  LOAD_ATTR                dn
             2468  LOAD_GLOBAL              web2ldapcnf
             2470  LOAD_ATTR                log_error_details
             2472  CALL_FUNCTION_4       4  ''
             2474  POP_TOP          

 L.1045      2476  LOAD_GLOBAL              exception_message

 L.1046      2478  LOAD_DEREF               'self'

 L.1047      2480  LOAD_STR                 'Unhandled %s'
             2482  LOAD_FAST                'err'
             2484  LOAD_ATTR                __class__
             2486  LOAD_ATTR                __name__
             2488  BINARY_MODULO    

 L.1048      2490  LOAD_DEREF               'self'
             2492  LOAD_ATTR                form
             2494  LOAD_METHOD              utf2display
             2496  LOAD_GLOBAL              str
             2498  LOAD_FAST                'err'
             2500  CALL_FUNCTION_1       1  ''
             2502  CALL_METHOD_1         1  ''

 L.1045      2504  CALL_FUNCTION_3       3  ''
             2506  POP_TOP          
             2508  POP_BLOCK        
             2510  BEGIN_FINALLY    
           2512_0  COME_FROM_FINALLY  2452  '2452'
             2512  LOAD_CONST               None
             2514  STORE_FAST               'err'
             2516  DELETE_FAST              'err'
             2518  END_FINALLY      
             2520  POP_EXCEPT       
         2522_2524  JUMP_FORWARD       2962  'to 2962'
           2526_0  COME_FROM          2442  '2442'

 L.1051      2526  DUP_TOP          
             2528  LOAD_GLOBAL              ldap0
             2530  LOAD_ATTR                LDAPError
             2532  COMPARE_OP               exception-match
         2534_2536  POP_JUMP_IF_FALSE  2612  'to 2612'
             2538  POP_TOP          
             2540  STORE_FAST               'ldap_err'
             2542  POP_TOP          
             2544  SETUP_FINALLY      2598  'to 2598'

 L.1052      2546  LOAD_GLOBAL              log_exception
             2548  LOAD_DEREF               'self'
             2550  LOAD_ATTR                env
             2552  LOAD_DEREF               'self'
             2554  LOAD_ATTR                ls
             2556  LOAD_DEREF               'self'
             2558  LOAD_ATTR                dn
             2560  LOAD_GLOBAL              web2ldapcnf
             2562  LOAD_ATTR                log_error_details
             2564  CALL_FUNCTION_4       4  ''
             2566  POP_TOP          

 L.1053      2568  LOAD_GLOBAL              exception_message

 L.1054      2570  LOAD_DEREF               'self'

 L.1055      2572  LOAD_STR                 'Unhandled %s'
             2574  LOAD_FAST                'ldap_err'
             2576  LOAD_ATTR                __class__
             2578  LOAD_ATTR                __name__
             2580  BINARY_MODULO    

 L.1056      2582  LOAD_DEREF               'self'
             2584  LOAD_METHOD              ldap_error_msg
             2586  LOAD_FAST                'ldap_err'
             2588  CALL_METHOD_1         1  ''

 L.1053      2590  CALL_FUNCTION_3       3  ''
             2592  POP_TOP          
             2594  POP_BLOCK        
             2596  BEGIN_FINALLY    
           2598_0  COME_FROM_FINALLY  2544  '2544'
             2598  LOAD_CONST               None
             2600  STORE_FAST               'ldap_err'
             2602  DELETE_FAST              'ldap_err'
             2604  END_FINALLY      
             2606  POP_EXCEPT       
         2608_2610  JUMP_FORWARD       2962  'to 2962'
           2612_0  COME_FROM          2534  '2534'

 L.1059      2612  DUP_TOP          
             2614  LOAD_GLOBAL              ErrorExit
             2616  COMPARE_OP               exception-match
         2618_2620  POP_JUMP_IF_FALSE  2680  'to 2680'
             2622  POP_TOP          
             2624  STORE_FAST               'error_exit'
             2626  POP_TOP          
             2628  SETUP_FINALLY      2666  'to 2666'

 L.1060      2630  LOAD_DEREF               'self'
             2632  LOAD_METHOD              log
             2634  LOAD_GLOBAL              logging
             2636  LOAD_ATTR                WARN
             2638  LOAD_STR                 'ErrorExit: %r'
             2640  LOAD_FAST                'error_exit'
             2642  LOAD_ATTR                Msg
             2644  CALL_METHOD_3         3  ''
             2646  POP_TOP          

 L.1061      2648  LOAD_GLOBAL              exception_message

 L.1062      2650  LOAD_DEREF               'self'

 L.1063      2652  LOAD_STR                 'Error'

 L.1064      2654  LOAD_FAST                'error_exit'
             2656  LOAD_ATTR                Msg

 L.1061      2658  CALL_FUNCTION_3       3  ''
             2660  POP_TOP          
             2662  POP_BLOCK        
             2664  BEGIN_FINALLY    
           2666_0  COME_FROM_FINALLY  2628  '2628'
             2666  LOAD_CONST               None
             2668  STORE_FAST               'error_exit'
             2670  DELETE_FAST              'error_exit'
             2672  END_FINALLY      
             2674  POP_EXCEPT       
         2676_2678  JUMP_FORWARD       2962  'to 2962'
           2680_0  COME_FROM          2618  '2618'

 L.1067      2680  DUP_TOP          
             2682  LOAD_GLOBAL              web2ldap
             2684  LOAD_ATTR                web
             2686  LOAD_ATTR                session
             2688  LOAD_ATTR                MaxSessionPerIPExceeded
             2690  COMPARE_OP               exception-match
         2692_2694  POP_JUMP_IF_FALSE  2760  'to 2760'
             2696  POP_TOP          
             2698  STORE_FAST               'session_err'
             2700  POP_TOP          
             2702  SETUP_FINALLY      2748  'to 2748'

 L.1068      2704  LOAD_DEREF               'self'
             2706  LOAD_METHOD              log
             2708  LOAD_GLOBAL              logging
             2710  LOAD_ATTR                WARN
             2712  LOAD_GLOBAL              str
             2714  LOAD_FAST                'session_err'
             2716  CALL_FUNCTION_1       1  ''
             2718  CALL_METHOD_2         2  ''
             2720  POP_TOP          

 L.1069      2722  LOAD_DEREF               'self'
             2724  LOAD_METHOD              simple_msg

 L.1070      2726  LOAD_STR                 'Client %s exceeded limit of max. %d sessions! Try later...'

 L.1071      2728  LOAD_FAST                'session_err'
             2730  LOAD_ATTR                remote_ip

 L.1072      2732  LOAD_FAST                'session_err'
             2734  LOAD_ATTR                max_session_count

 L.1070      2736  BUILD_TUPLE_2         2 
             2738  BINARY_MODULO    

 L.1069      2740  CALL_METHOD_1         1  ''
             2742  POP_TOP          
             2744  POP_BLOCK        
             2746  BEGIN_FINALLY    
           2748_0  COME_FROM_FINALLY  2702  '2702'
             2748  LOAD_CONST               None
             2750  STORE_FAST               'session_err'
             2752  DELETE_FAST              'session_err'
             2754  END_FINALLY      
             2756  POP_EXCEPT       
             2758  JUMP_FORWARD       2962  'to 2962'
           2760_0  COME_FROM          2692  '2692'

 L.1076      2760  DUP_TOP          
             2762  LOAD_GLOBAL              web2ldap
             2764  LOAD_ATTR                web
             2766  LOAD_ATTR                session
             2768  LOAD_ATTR                MaxSessionCountExceeded
             2770  COMPARE_OP               exception-match
         2772_2774  POP_JUMP_IF_FALSE  2828  'to 2828'
             2776  POP_TOP          
             2778  STORE_FAST               'session_err'
             2780  POP_TOP          
             2782  SETUP_FINALLY      2816  'to 2816'

 L.1077      2784  LOAD_DEREF               'self'
             2786  LOAD_METHOD              log
             2788  LOAD_GLOBAL              logging
             2790  LOAD_ATTR                WARN
             2792  LOAD_GLOBAL              str
             2794  LOAD_FAST                'session_err'
             2796  CALL_FUNCTION_1       1  ''
             2798  CALL_METHOD_2         2  ''
             2800  POP_TOP          

 L.1078      2802  LOAD_DEREF               'self'
             2804  LOAD_METHOD              simple_msg
             2806  LOAD_STR                 'Too many web sessions! Try later...'
             2808  CALL_METHOD_1         1  ''
             2810  POP_TOP          
             2812  POP_BLOCK        
             2814  BEGIN_FINALLY    
           2816_0  COME_FROM_FINALLY  2782  '2782'
             2816  LOAD_CONST               None
             2818  STORE_FAST               'session_err'
             2820  DELETE_FAST              'session_err'
             2822  END_FINALLY      
             2824  POP_EXCEPT       
             2826  JUMP_FORWARD       2962  'to 2962'
           2828_0  COME_FROM          2772  '2772'

 L.1080      2828  DUP_TOP          
             2830  LOAD_GLOBAL              web2ldap
             2832  LOAD_ATTR                web
             2834  LOAD_ATTR                session
             2836  LOAD_ATTR                SessionException
             2838  COMPARE_OP               exception-match
         2840_2842  POP_JUMP_IF_FALSE  2886  'to 2886'
             2844  POP_TOP          
             2846  POP_TOP          
             2848  POP_TOP          

 L.1081      2850  LOAD_GLOBAL              log_exception
             2852  LOAD_DEREF               'self'
             2854  LOAD_ATTR                env
             2856  LOAD_DEREF               'self'
             2858  LOAD_ATTR                ls
             2860  LOAD_DEREF               'self'
             2862  LOAD_ATTR                dn
             2864  LOAD_GLOBAL              web2ldapcnf
             2866  LOAD_ATTR                log_error_details
             2868  CALL_FUNCTION_4       4  ''
             2870  POP_TOP          

 L.1082      2872  LOAD_DEREF               'self'
             2874  LOAD_METHOD              url_redirect
             2876  LOAD_STR                 'Session handling error.'
             2878  CALL_METHOD_1         1  ''
             2880  POP_TOP          
             2882  POP_EXCEPT       
             2884  JUMP_FORWARD       2962  'to 2962'
           2886_0  COME_FROM          2840  '2840'

 L.1084      2886  DUP_TOP          
             2888  LOAD_GLOBAL              Exception
             2890  COMPARE_OP               exception-match
         2892_2894  POP_JUMP_IF_FALSE  2960  'to 2960'
             2896  POP_TOP          
             2898  POP_TOP          
             2900  POP_TOP          

 L.1085      2902  LOAD_GLOBAL              hasattr
             2904  LOAD_DEREF               'self'
             2906  LOAD_STR                 'ls'
             2908  CALL_FUNCTION_2       2  ''
         2910_2912  POP_JUMP_IF_FALSE  2922  'to 2922'

 L.1086      2914  LOAD_DEREF               'self'
             2916  LOAD_ATTR                ls
             2918  STORE_FAST               'error_ls'
             2920  JUMP_FORWARD       2926  'to 2926'
           2922_0  COME_FROM          2910  '2910'

 L.1088      2922  LOAD_CONST               None
             2924  STORE_FAST               'error_ls'
           2926_0  COME_FROM          2920  '2920'

 L.1089      2926  LOAD_GLOBAL              log_exception
             2928  LOAD_DEREF               'self'
             2930  LOAD_ATTR                env
             2932  LOAD_FAST                'error_ls'
             2934  LOAD_DEREF               'self'
             2936  LOAD_ATTR                dn
             2938  LOAD_GLOBAL              web2ldapcnf
             2940  LOAD_ATTR                log_error_details
             2942  CALL_FUNCTION_4       4  ''
             2944  POP_TOP          

 L.1090      2946  LOAD_DEREF               'self'
             2948  LOAD_METHOD              simple_msg
             2950  LOAD_STR                 'Unhandled error!'
             2952  CALL_METHOD_1         1  ''
             2954  POP_TOP          
             2956  POP_EXCEPT       
             2958  JUMP_FORWARD       2962  'to 2962'
           2960_0  COME_FROM          2892  '2892'
             2960  END_FINALLY      
           2962_0  COME_FROM          2958  '2958'
           2962_1  COME_FROM          2884  '2884'
           2962_2  COME_FROM          2826  '2826'
           2962_3  COME_FROM          2758  '2758'
           2962_4  COME_FROM          2676  '2676'
           2962_5  COME_FROM          2608  '2608'
           2962_6  COME_FROM          2522  '2522'
           2962_7  COME_FROM          2420  '2420'
           2962_8  COME_FROM          2308  '2308'
           2962_9  COME_FROM          2178  '2178'
          2962_10  COME_FROM          2096  '2096'
          2962_11  COME_FROM          2028  '2028'
          2962_12  COME_FROM          1946  '1946'
          2962_13  COME_FROM          1886  '1886'
          2962_14  COME_FROM          1660  '1660'
          2962_15  COME_FROM          1556  '1556'
          2962_16  COME_FROM          1462  '1462'

Parse error at or near `LOAD_CONST' instruction at offset 214