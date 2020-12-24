# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/handler.py
# Compiled at: 2020-05-04 07:51:44
# Size of source mod 2**32: 39432 bytes
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

 L. 709   104_106  SETUP_FINALLY      1462  'to 1462'

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
              192  LOAD_CONST               {'', 'locate', 'monitor', 'metrics', 'urlredirect'}
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
          586_588  POP_JUMP_IF_FALSE   792  'to 792'

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

 L. 789   626_628  POP_JUMP_IF_FALSE   792  'to 792'
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
              702  LOAD_CONST               -1
              704  CALL_METHOD_2         2  ''

 L. 805       706  LOAD_DEREF               'self'
              708  LOAD_ATTR                ldap_url
              710  LOAD_METHOD              get_starttls_extop

 L. 806       712  LOAD_DEREF               'self'
              714  LOAD_METHOD              cfg_param
              716  LOAD_STR                 'starttls'
              718  LOAD_GLOBAL              web2ldap
              720  LOAD_ATTR                ldapsession
              722  LOAD_ATTR                START_TLS_NO
              724  CALL_METHOD_2         2  ''

 L. 805       726  CALL_METHOD_1         1  ''

 L. 808       728  LOAD_DEREF               'self'
              730  LOAD_ATTR                env

 L. 809       732  LOAD_DEREF               'self'
              734  LOAD_METHOD              cfg_param
              736  LOAD_STR                 'session_track_control'
              738  LOAD_CONST               0
              740  CALL_METHOD_2         2  ''

 L. 810       742  LOAD_DEREF               'self'
              744  LOAD_METHOD              cfg_param
              746  LOAD_STR                 'tls_options'
              748  BUILD_MAP_0           0 
              750  CALL_METHOD_2         2  ''

 L. 802       752  LOAD_CONST               ('tls_options',)
              754  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              756  POP_TOP          

 L. 813       758  LOAD_DEREF               'self'
              760  LOAD_METHOD              cfg_param
              762  LOAD_STR                 'timeout'
              764  LOAD_CONST               60
              766  CALL_METHOD_2         2  ''
              768  LOAD_DEREF               'self'
              770  LOAD_ATTR                ls
              772  LOAD_ATTR                l
              774  STORE_ATTR               timeout

 L. 816       776  LOAD_GLOBAL              session_store
              778  LOAD_METHOD              save
              780  LOAD_DEREF               'self'
              782  LOAD_ATTR                sid
              784  LOAD_DEREF               'self'
              786  LOAD_ATTR                ls
              788  CALL_METHOD_2         2  ''
              790  POP_TOP          
            792_0  COME_FROM           626  '626'
            792_1  COME_FROM           586  '586'

 L. 819       792  LOAD_DEREF               'self'
              794  LOAD_ATTR                ls
              796  LOAD_CONST               None
              798  COMPARE_OP               is
          800_802  POP_JUMP_IF_FALSE   820  'to 820'

 L. 821       804  LOAD_DEREF               'self'
              806  LOAD_METHOD              url_redirect
              808  LOAD_STR                 'No valid session!'
              810  CALL_METHOD_1         1  ''
              812  POP_TOP          

 L. 822       814  POP_BLOCK        
              816  LOAD_CONST               None
              818  RETURN_VALUE     
            820_0  COME_FROM           800  '800'

 L. 824       820  LOAD_DEREF               'self'
              822  LOAD_ATTR                ls
              824  LOAD_ATTR                uri
              826  LOAD_CONST               None
              828  COMPARE_OP               is
          830_832  POP_JUMP_IF_FALSE   878  'to 878'

 L. 825       834  LOAD_GLOBAL              session_store
              836  LOAD_METHOD              delete
              838  LOAD_DEREF               'self'
              840  LOAD_ATTR                sid
              842  CALL_METHOD_1         1  ''
              844  POP_TOP          

 L. 826       846  LOAD_CONST               None
              848  LOAD_DEREF               'self'
              850  STORE_ATTR               sid

 L. 827       852  LOAD_GLOBAL              web2ldap
              854  LOAD_ATTR                app
              856  LOAD_ATTR                connect
              858  LOAD_ATTR                w2l_connect

 L. 828       860  LOAD_DEREF               'self'

 L. 829       862  LOAD_STR                 'Connect failed'

 L. 830       864  LOAD_STR                 'No valid LDAP connection.'

 L. 827       866  LOAD_CONST               ('h1_msg', 'error_msg')
              868  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              870  POP_TOP          

 L. 832       872  POP_BLOCK        
              874  LOAD_CONST               None
              876  RETURN_VALUE     
            878_0  COME_FROM           830  '830'

 L. 836       878  LOAD_GLOBAL              session_store
              880  LOAD_METHOD              save
              882  LOAD_DEREF               'self'
              884  LOAD_ATTR                sid
              886  LOAD_DEREF               'self'
              888  LOAD_ATTR                ls
              890  CALL_METHOD_2         2  ''
              892  POP_TOP          

 L. 837       894  LOAD_DEREF               'self'
              896  LOAD_ATTR                dn
              898  LOAD_DEREF               'self'
              900  STORE_ATTR               dn

 L. 839       902  LOAD_DEREF               'self'
              904  LOAD_ATTR                form
              906  LOAD_METHOD              getInputValue

 L. 840       908  LOAD_STR                 'login_mech'

 L. 841       910  LOAD_DEREF               'self'
              912  LOAD_ATTR                ldap_url
              914  LOAD_ATTR                saslMech
          916_918  JUMP_IF_TRUE_OR_POP   922  'to 922'
              920  LOAD_STR                 ''
            922_0  COME_FROM           916  '916'
              922  BUILD_LIST_1          1 

 L. 839       924  CALL_METHOD_2         2  ''

 L. 842       926  LOAD_CONST               0

 L. 839       928  BINARY_SUBSCR    
              930  LOAD_METHOD              upper
              932  CALL_METHOD_0         0  ''
          934_936  JUMP_IF_TRUE_OR_POP   940  'to 940'

 L. 842       938  LOAD_CONST               None
            940_0  COME_FROM           934  '934'

 L. 839       940  STORE_FAST               'login_mech'

 L. 845       942  LOAD_FAST                'who'
              944  LOAD_CONST               None
              946  COMPARE_OP               is-not

 L. 844   948_950  POP_JUMP_IF_FALSE  1024  'to 1024'

 L. 846       952  LOAD_FAST                'cred'
              954  LOAD_CONST               None
              956  COMPARE_OP               is

 L. 844   958_960  POP_JUMP_IF_FALSE  1024  'to 1024'

 L. 847       962  LOAD_FAST                'login_mech'
          964_966  JUMP_IF_TRUE_OR_POP   970  'to 970'
              968  LOAD_STR                 ''
            970_0  COME_FROM           964  '964'
              970  LOAD_METHOD              encode
              972  LOAD_STR                 'ascii'
              974  CALL_METHOD_1         1  ''
              976  LOAD_GLOBAL              ldap0
              978  LOAD_ATTR                sasl
              980  LOAD_ATTR                SASL_NONINTERACTIVE_MECHS
              982  COMPARE_OP               not-in

 L. 844   984_986  POP_JUMP_IF_FALSE  1024  'to 1024'

 L. 850       988  LOAD_GLOBAL              web2ldap
              990  LOAD_ATTR                app
              992  LOAD_ATTR                login
              994  LOAD_ATTR                w2l_login

 L. 851       996  LOAD_DEREF               'self'

 L. 852       998  LOAD_STR                 ''

 L. 853      1000  LOAD_FAST                'who'

 L. 853      1002  LOAD_CONST               0

 L. 853      1004  LOAD_CONST               1

 L. 854      1006  LOAD_DEREF               'self'
             1008  LOAD_ATTR                ldap_url
             1010  LOAD_ATTR                saslMech

 L. 850      1012  LOAD_CONST               ('login_msg', 'who', 'relogin', 'nomenu', 'login_default_mech')
             1014  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1016  POP_TOP          

 L. 856      1018  POP_BLOCK        
             1020  LOAD_CONST               None
             1022  RETURN_VALUE     
           1024_0  COME_FROM           984  '984'
           1024_1  COME_FROM           958  '958'
           1024_2  COME_FROM           948  '948'

 L. 859      1024  LOAD_FAST                'who'
             1026  LOAD_CONST               None
             1028  COMPARE_OP               is-not

 L. 858  1030_1032  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 859      1034  LOAD_FAST                'cred'
             1036  LOAD_CONST               None
             1038  COMPARE_OP               is-not

 L. 858  1040_1042  POP_JUMP_IF_TRUE   1074  'to 1074'
           1044_0  COME_FROM          1030  '1030'

 L. 860      1044  LOAD_FAST                'login_mech'
             1046  LOAD_CONST               None
             1048  COMPARE_OP               is-not

 L. 858  1050_1052  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 860      1054  LOAD_FAST                'login_mech'
             1056  LOAD_METHOD              encode
             1058  LOAD_STR                 'ascii'
             1060  CALL_METHOD_1         1  ''
             1062  LOAD_GLOBAL              ldap0
             1064  LOAD_ATTR                sasl
             1066  LOAD_ATTR                SASL_NONINTERACTIVE_MECHS
             1068  COMPARE_OP               in

 L. 858  1070_1072  POP_JUMP_IF_FALSE  1298  'to 1298'
           1074_0  COME_FROM          1040  '1040'

 L. 862      1074  LOAD_DEREF               'self'
             1076  LOAD_ATTR                dn
             1078  LOAD_DEREF               'self'
             1080  STORE_ATTR               dn

 L. 864      1082  LOAD_DEREF               'self'
             1084  LOAD_ATTR                form
             1086  LOAD_METHOD              getInputValue

 L. 865      1088  LOAD_STR                 'login_search_root'

 L. 866      1090  LOAD_DEREF               'self'
             1092  LOAD_ATTR                naming_context
             1094  BUILD_LIST_1          1 

 L. 864      1096  CALL_METHOD_2         2  ''

 L. 867      1098  LOAD_CONST               0

 L. 864      1100  BINARY_SUBSCR    
             1102  STORE_FAST               'login_search_root'

 L. 868      1104  SETUP_FINALLY      1222  'to 1222'

 L. 869      1106  LOAD_DEREF               'self'
             1108  LOAD_ATTR                ls
             1110  LOAD_ATTR                bind

 L. 870      1112  LOAD_FAST                'who'

 L. 871      1114  LOAD_FAST                'cred'
         1116_1118  JUMP_IF_TRUE_OR_POP  1122  'to 1122'
             1120  LOAD_STR                 ''
           1122_0  COME_FROM          1116  '1116'

 L. 872      1122  LOAD_FAST                'login_mech'

 L. 873      1124  LOAD_STR                 ''
             1126  LOAD_METHOD              join

 L. 874      1128  LOAD_DEREF               'self'
             1130  LOAD_ATTR                form
             1132  LOAD_METHOD              getInputValue
             1134  LOAD_STR                 'login_authzid_prefix'
             1136  LOAD_STR                 ''
             1138  BUILD_LIST_1          1 
             1140  CALL_METHOD_2         2  ''
             1142  LOAD_CONST               0
             1144  BINARY_SUBSCR    

 L. 875      1146  LOAD_DEREF               'self'
             1148  LOAD_ATTR                form
             1150  LOAD_METHOD              getInputValue

 L. 876      1152  LOAD_STR                 'login_authzid'

 L. 877      1154  LOAD_DEREF               'self'
             1156  LOAD_ATTR                ldap_url
             1158  LOAD_ATTR                saslAuthzId
         1160_1162  JUMP_IF_TRUE_OR_POP  1166  'to 1166'
             1164  LOAD_STR                 ''
           1166_0  COME_FROM          1160  '1160'
             1166  BUILD_LIST_1          1 

 L. 875      1168  CALL_METHOD_2         2  ''

 L. 878      1170  LOAD_CONST               0

 L. 875      1172  BINARY_SUBSCR    

 L. 873      1174  BUILD_TUPLE_2         2 
             1176  CALL_METHOD_1         1  ''
         1178_1180  JUMP_IF_TRUE_OR_POP  1184  'to 1184'

 L. 879      1182  LOAD_CONST               None
           1184_0  COME_FROM          1178  '1178'

 L. 880      1184  LOAD_DEREF               'self'
             1186  LOAD_ATTR                form
             1188  LOAD_METHOD              getInputValue
             1190  LOAD_STR                 'login_realm'
             1192  LOAD_DEREF               'self'
             1194  LOAD_ATTR                ldap_url
             1196  LOAD_ATTR                saslRealm
             1198  BUILD_LIST_1          1 
             1200  CALL_METHOD_2         2  ''
             1202  LOAD_CONST               0
             1204  BINARY_SUBSCR    

 L. 881      1206  LOAD_DEREF               'self'
             1208  LOAD_ATTR                binddn_mapping

 L. 882      1210  LOAD_FAST                'login_search_root'

 L. 869      1212  LOAD_CONST               ('loginSearchRoot',)
             1214  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1216  POP_TOP          
             1218  POP_BLOCK        
             1220  JUMP_FORWARD       1296  'to 1296'
           1222_0  COME_FROM_FINALLY  1104  '1104'

 L. 884      1222  DUP_TOP          
             1224  LOAD_GLOBAL              ldap0
             1226  LOAD_ATTR                NO_SUCH_OBJECT
             1228  COMPARE_OP               exception-match
         1230_1232  POP_JUMP_IF_FALSE  1294  'to 1294'
             1234  POP_TOP          
             1236  STORE_FAST               'err'
             1238  POP_TOP          
             1240  SETUP_FINALLY      1282  'to 1282'

 L. 885      1242  LOAD_GLOBAL              web2ldap
             1244  LOAD_ATTR                app
             1246  LOAD_ATTR                login
             1248  LOAD_ATTR                w2l_login

 L. 886      1250  LOAD_DEREF               'self'

 L. 887      1252  LOAD_DEREF               'self'
             1254  LOAD_METHOD              ldap_error_msg
             1256  LOAD_FAST                'err'
             1258  CALL_METHOD_1         1  ''

 L. 888      1260  LOAD_FAST                'who'

 L. 888      1262  LOAD_CONST               True

 L. 885      1264  LOAD_CONST               ('login_msg', 'who', 'relogin')
             1266  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1268  POP_TOP          

 L. 890      1270  POP_BLOCK        
             1272  POP_EXCEPT       
             1274  CALL_FINALLY       1282  'to 1282'
             1276  POP_BLOCK        
             1278  LOAD_CONST               None
             1280  RETURN_VALUE     
           1282_0  COME_FROM          1274  '1274'
           1282_1  COME_FROM_FINALLY  1240  '1240'
             1282  LOAD_CONST               None
             1284  STORE_FAST               'err'
             1286  DELETE_FAST              'err'
             1288  END_FINALLY      
             1290  POP_EXCEPT       
             1292  JUMP_FORWARD       1296  'to 1296'
           1294_0  COME_FROM          1230  '1230'
             1294  END_FINALLY      
           1296_0  COME_FROM          1292  '1292'
           1296_1  COME_FROM          1220  '1220'
             1296  JUMP_FORWARD       1308  'to 1308'
           1298_0  COME_FROM          1070  '1070'
           1298_1  COME_FROM          1050  '1050'

 L. 893      1298  LOAD_DEREF               'self'
             1300  LOAD_ATTR                ls
             1302  LOAD_METHOD              init_rootdse
             1304  CALL_METHOD_0         0  ''
             1306  POP_TOP          
           1308_0  COME_FROM          1296  '1296'

 L. 898      1308  LOAD_GLOBAL              isinstance
             1310  LOAD_DEREF               'self'
             1312  LOAD_ATTR                ls
             1314  LOAD_GLOBAL              LDAPSession
             1316  CALL_FUNCTION_2       2  ''
         1318_1320  POP_JUMP_IF_FALSE  1336  'to 1336'
             1322  LOAD_DEREF               'self'
             1324  LOAD_ATTR                ls
             1326  LOAD_ATTR                uri
             1328  LOAD_CONST               None
             1330  COMPARE_OP               is
         1332_1334  POP_JUMP_IF_FALSE  1352  'to 1352'
           1336_0  COME_FROM          1318  '1318'

 L. 899      1336  LOAD_DEREF               'self'
             1338  LOAD_METHOD              url_redirect
             1340  LOAD_STR                 'No valid LDAP connection!'
             1342  CALL_METHOD_1         1  ''
             1344  POP_TOP          

 L. 900      1346  POP_BLOCK        
             1348  LOAD_CONST               None
             1350  RETURN_VALUE     
           1352_0  COME_FROM          1332  '1332'

 L. 903      1352  LOAD_GLOBAL              session_store
             1354  LOAD_METHOD              save
             1356  LOAD_DEREF               'self'
             1358  LOAD_ATTR                sid
             1360  LOAD_DEREF               'self'
             1362  LOAD_ATTR                ls
             1364  CALL_METHOD_2         2  ''
             1366  POP_TOP          

 L. 906      1368  LOAD_DEREF               'self'
             1370  LOAD_ATTR                dn
             1372  LOAD_DEREF               'self'
             1374  STORE_ATTR               dn

 L. 909      1376  SETUP_FINALLY      1390  'to 1390'

 L. 910      1378  LOAD_DEREF               'self'
             1380  LOAD_METHOD              dispatch
             1382  CALL_METHOD_0         0  ''
             1384  POP_TOP          
             1386  POP_BLOCK        
             1388  JUMP_FORWARD       1440  'to 1440'
           1390_0  COME_FROM_FINALLY  1376  '1376'

 L. 911      1390  DUP_TOP          
             1392  LOAD_GLOBAL              ldap0
             1394  LOAD_ATTR                SERVER_DOWN
             1396  COMPARE_OP               exception-match
         1398_1400  POP_JUMP_IF_FALSE  1438  'to 1438'
             1402  POP_TOP          
             1404  POP_TOP          
             1406  POP_TOP          

 L. 913      1408  LOAD_DEREF               'self'
             1410  LOAD_ATTR                ls
             1412  LOAD_ATTR                l
             1414  LOAD_METHOD              reconnect
             1416  LOAD_DEREF               'self'
             1418  LOAD_ATTR                ls
             1420  LOAD_ATTR                uri
             1422  CALL_METHOD_1         1  ''
             1424  POP_TOP          

 L. 914      1426  LOAD_DEREF               'self'
             1428  LOAD_METHOD              dispatch
             1430  CALL_METHOD_0         0  ''
             1432  POP_TOP          
             1434  POP_EXCEPT       
             1436  JUMP_FORWARD       1456  'to 1456'
           1438_0  COME_FROM          1398  '1398'
             1438  END_FINALLY      
           1440_0  COME_FROM          1388  '1388'

 L. 917      1440  LOAD_GLOBAL              session_store
             1442  LOAD_METHOD              save
             1444  LOAD_DEREF               'self'
             1446  LOAD_ATTR                sid
             1448  LOAD_DEREF               'self'
             1450  LOAD_ATTR                ls
             1452  CALL_METHOD_2         2  ''
             1454  POP_TOP          
           1456_0  COME_FROM          1436  '1436'
             1456  POP_BLOCK        
         1458_1460  JUMP_FORWARD       2958  'to 2958'
           1462_0  COME_FROM_FINALLY   104  '104'

 L. 919      1462  DUP_TOP          
             1464  LOAD_GLOBAL              web2ldap
             1466  LOAD_ATTR                web
             1468  LOAD_ATTR                forms
             1470  LOAD_ATTR                FormException
             1472  COMPARE_OP               exception-match
         1474_1476  POP_JUMP_IF_FALSE  1556  'to 1556'
             1478  POP_TOP          
             1480  STORE_FAST               'form_error'
             1482  POP_TOP          
             1484  SETUP_FINALLY      1542  'to 1542'

 L. 920      1486  LOAD_GLOBAL              log_exception
             1488  LOAD_DEREF               'self'
             1490  LOAD_ATTR                env
             1492  LOAD_DEREF               'self'
             1494  LOAD_ATTR                ls
             1496  LOAD_DEREF               'self'
             1498  LOAD_ATTR                dn
             1500  LOAD_GLOBAL              web2ldapcnf
             1502  LOAD_ATTR                log_error_details
             1504  CALL_FUNCTION_4       4  ''
             1506  POP_TOP          

 L. 921      1508  LOAD_GLOBAL              exception_message

 L. 922      1510  LOAD_DEREF               'self'

 L. 923      1512  LOAD_STR                 'Error parsing form'

 L. 924      1514  LOAD_STR                 'Error parsing form:<br>%s'

 L. 925      1516  LOAD_DEREF               'self'
             1518  LOAD_ATTR                form
             1520  LOAD_METHOD              utf2display
             1522  LOAD_GLOBAL              str
             1524  LOAD_FAST                'form_error'
             1526  CALL_FUNCTION_1       1  ''
             1528  CALL_METHOD_1         1  ''

 L. 924      1530  BUILD_TUPLE_1         1 
             1532  BINARY_MODULO    

 L. 921      1534  CALL_FUNCTION_3       3  ''
             1536  POP_TOP          
             1538  POP_BLOCK        
             1540  BEGIN_FINALLY    
           1542_0  COME_FROM_FINALLY  1484  '1484'
             1542  LOAD_CONST               None
             1544  STORE_FAST               'form_error'
             1546  DELETE_FAST              'form_error'
             1548  END_FINALLY      
             1550  POP_EXCEPT       
         1552_1554  JUMP_FORWARD       2958  'to 2958'
           1556_0  COME_FROM          1474  '1474'

 L. 929      1556  DUP_TOP          
             1558  LOAD_GLOBAL              ldap0
             1560  LOAD_ATTR                SERVER_DOWN
             1562  COMPARE_OP               exception-match
         1564_1566  POP_JUMP_IF_FALSE  1660  'to 1660'
             1568  POP_TOP          
             1570  STORE_FAST               'err'
             1572  POP_TOP          
             1574  SETUP_FINALLY      1646  'to 1646'

 L. 931      1576  LOAD_GLOBAL              session_store
             1578  LOAD_METHOD              delete
             1580  LOAD_DEREF               'self'
             1582  LOAD_ATTR                sid
             1584  CALL_METHOD_1         1  ''
             1586  POP_TOP          

 L. 932      1588  LOAD_CONST               None
             1590  LOAD_DEREF               'self'
             1592  STORE_ATTR               sid

 L. 934      1594  LOAD_GLOBAL              web2ldap
             1596  LOAD_ATTR                app
             1598  LOAD_ATTR                connect
             1600  LOAD_ATTR                w2l_connect

 L. 935      1602  LOAD_DEREF               'self'

 L. 936      1604  LOAD_STR                 'Connect failed'

 L. 937      1606  LOAD_STR                 'Connecting to %s impossible!<br>%s'

 L. 938      1608  LOAD_DEREF               'self'
             1610  LOAD_ATTR                form
             1612  LOAD_METHOD              utf2display
             1614  LOAD_FAST                'init_uri'
         1616_1618  JUMP_IF_TRUE_OR_POP  1622  'to 1622'
             1620  LOAD_STR                 '-'
           1622_0  COME_FROM          1616  '1616'
             1622  CALL_METHOD_1         1  ''

 L. 939      1624  LOAD_DEREF               'self'
             1626  LOAD_METHOD              ldap_error_msg
             1628  LOAD_FAST                'err'
             1630  CALL_METHOD_1         1  ''

 L. 937      1632  BUILD_TUPLE_2         2 
             1634  BINARY_MODULO    

 L. 934      1636  LOAD_CONST               ('h1_msg', 'error_msg')
             1638  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1640  POP_TOP          
             1642  POP_BLOCK        
             1644  BEGIN_FINALLY    
           1646_0  COME_FROM_FINALLY  1574  '1574'
             1646  LOAD_CONST               None
             1648  STORE_FAST               'err'
             1650  DELETE_FAST              'err'
             1652  END_FINALLY      
             1654  POP_EXCEPT       
         1656_1658  JUMP_FORWARD       2958  'to 2958'
           1660_0  COME_FROM          1564  '1564'

 L. 943      1660  DUP_TOP          
             1662  LOAD_GLOBAL              ldap0
             1664  LOAD_ATTR                NO_SUCH_OBJECT
             1666  COMPARE_OP               exception-match
         1668_1670  POP_JUMP_IF_FALSE  1886  'to 1886'
             1672  POP_TOP          
             1674  STORE_FAST               'ldap_err'
             1676  POP_TOP          
             1678  SETUP_FINALLY      1872  'to 1872'

 L. 946      1680  LOAD_GLOBAL              web2ldap
             1682  LOAD_ATTR                ldaputil
             1684  LOAD_ATTR                dns
             1686  LOAD_METHOD              dc_dn_lookup
             1688  LOAD_DEREF               'self'
             1690  LOAD_ATTR                dn
             1692  CALL_METHOD_1         1  ''
             1694  STORE_FAST               'host_list'

 L. 947      1696  LOAD_DEREF               'self'
             1698  LOAD_METHOD              log
             1700  LOAD_GLOBAL              logging
             1702  LOAD_ATTR                DEBUG
             1704  LOAD_STR                 'host_list = %r'
             1706  LOAD_FAST                'host_list'
             1708  CALL_METHOD_3         3  ''
             1710  POP_TOP          

 L. 948      1712  LOAD_FAST                'host_list'
         1714_1716  POP_JUMP_IF_FALSE  1764  'to 1764'
             1718  LOAD_GLOBAL              ExtendedLDAPUrl
             1720  LOAD_DEREF               'self'
             1722  LOAD_ATTR                ls
             1724  LOAD_ATTR                uri
             1726  CALL_FUNCTION_1       1  ''
             1728  LOAD_ATTR                hostport
             1730  LOAD_FAST                'host_list'
             1732  COMPARE_OP               not-in
         1734_1736  POP_JUMP_IF_FALSE  1764  'to 1764'

 L. 950      1738  LOAD_GLOBAL              web2ldap
             1740  LOAD_ATTR                app
             1742  LOAD_ATTR                srvrr
             1744  LOAD_METHOD              w2l_chasesrvrecord
             1746  LOAD_DEREF               'self'
             1748  LOAD_FAST                'host_list'
             1750  CALL_METHOD_2         2  ''
             1752  POP_TOP          

 L. 951      1754  POP_BLOCK        
             1756  POP_EXCEPT       
             1758  CALL_FINALLY       1872  'to 1872'
             1760  LOAD_CONST               None
             1762  RETURN_VALUE     
           1764_0  COME_FROM          1734  '1734'
           1764_1  COME_FROM          1714  '1714'

 L. 954      1764  LOAD_GLOBAL              log_exception
             1766  LOAD_DEREF               'self'
             1768  LOAD_ATTR                env
             1770  LOAD_DEREF               'self'
             1772  LOAD_ATTR                ls
             1774  LOAD_DEREF               'self'
             1776  LOAD_ATTR                dn
             1778  LOAD_GLOBAL              web2ldapcnf
             1780  LOAD_ATTR                log_error_details
             1782  CALL_FUNCTION_4       4  ''
             1784  POP_TOP          

 L. 955      1786  LOAD_DEREF               'self'
             1788  LOAD_ATTR                dn
             1790  STORE_FAST               'failed_dn'

 L. 956      1792  LOAD_STR                 'matched'
             1794  LOAD_FAST                'ldap_err'
             1796  LOAD_ATTR                args
             1798  LOAD_CONST               0
             1800  BINARY_SUBSCR    
             1802  COMPARE_OP               in
         1804_1806  POP_JUMP_IF_FALSE  1834  'to 1834'

 L. 957      1808  LOAD_FAST                'ldap_err'
             1810  LOAD_ATTR                args
             1812  LOAD_CONST               0
             1814  BINARY_SUBSCR    
             1816  LOAD_STR                 'matched'
             1818  BINARY_SUBSCR    
             1820  LOAD_METHOD              decode
             1822  LOAD_DEREF               'self'
             1824  LOAD_ATTR                ls
             1826  LOAD_ATTR                charset
             1828  CALL_METHOD_1         1  ''
             1830  LOAD_DEREF               'self'
             1832  STORE_ATTR               dn
           1834_0  COME_FROM          1804  '1804'

 L. 958      1834  LOAD_GLOBAL              exception_message

 L. 959      1836  LOAD_DEREF               'self'

 L. 960      1838  LOAD_STR                 'No such object'

 L. 961      1840  LOAD_DEREF               'self'
             1842  LOAD_ATTR                ldap_error_msg

 L. 962      1844  LOAD_FAST                'ldap_err'

 L. 963      1846  LOAD_STR                 '{{error_msg}}<br>{0}{{matched_dn}}'
             1848  LOAD_METHOD              format

 L. 964      1850  LOAD_DEREF               'self'
             1852  LOAD_METHOD              display_dn
             1854  LOAD_FAST                'failed_dn'
             1856  CALL_METHOD_1         1  ''

 L. 963      1858  CALL_METHOD_1         1  ''

 L. 961      1860  LOAD_CONST               ('template',)
             1862  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 958      1864  CALL_FUNCTION_3       3  ''
             1866  POP_TOP          
             1868  POP_BLOCK        
             1870  BEGIN_FINALLY    
           1872_0  COME_FROM          1758  '1758'
           1872_1  COME_FROM_FINALLY  1678  '1678'
             1872  LOAD_CONST               None
             1874  STORE_FAST               'ldap_err'
             1876  DELETE_FAST              'ldap_err'
             1878  END_FINALLY      
             1880  POP_EXCEPT       
         1882_1884  JUMP_FORWARD       2958  'to 2958'
           1886_0  COME_FROM          1668  '1668'

 L. 969      1886  DUP_TOP          
             1888  LOAD_GLOBAL              ldap0
             1890  LOAD_ATTR                PARTIAL_RESULTS
             1892  LOAD_GLOBAL              ldap0
             1894  LOAD_ATTR                REFERRAL
             1896  BUILD_TUPLE_2         2 
             1898  COMPARE_OP               exception-match
         1900_1902  POP_JUMP_IF_FALSE  1946  'to 1946'
             1904  POP_TOP          
             1906  STORE_FAST               'err'
             1908  POP_TOP          
             1910  SETUP_FINALLY      1932  'to 1932'

 L. 970      1912  LOAD_GLOBAL              web2ldap
             1914  LOAD_ATTR                app
             1916  LOAD_ATTR                referral
             1918  LOAD_METHOD              w2l_chasereferral
             1920  LOAD_DEREF               'self'
             1922  LOAD_FAST                'err'
             1924  CALL_METHOD_2         2  ''
             1926  POP_TOP          
             1928  POP_BLOCK        
             1930  BEGIN_FINALLY    
           1932_0  COME_FROM_FINALLY  1910  '1910'
             1932  LOAD_CONST               None
             1934  STORE_FAST               'err'
             1936  DELETE_FAST              'err'
             1938  END_FINALLY      
             1940  POP_EXCEPT       
         1942_1944  JUMP_FORWARD       2958  'to 2958'
           1946_0  COME_FROM          1900  '1900'

 L. 972      1946  DUP_TOP          

 L. 973      1948  LOAD_GLOBAL              ldap0
             1950  LOAD_ATTR                INSUFFICIENT_ACCESS

 L. 974      1952  LOAD_GLOBAL              ldap0
             1954  LOAD_ATTR                STRONG_AUTH_REQUIRED

 L. 975      1956  LOAD_GLOBAL              ldap0
             1958  LOAD_ATTR                INAPPROPRIATE_AUTH

 L. 976      1960  LOAD_GLOBAL              web2ldap
             1962  LOAD_ATTR                ldapsession
             1964  LOAD_ATTR                UsernameNotFound

 L. 972      1966  BUILD_TUPLE_4         4 
             1968  COMPARE_OP               exception-match
         1970_1972  POP_JUMP_IF_FALSE  2028  'to 2028'
             1974  POP_TOP          
             1976  STORE_FAST               'err'
             1978  POP_TOP          
             1980  SETUP_FINALLY      2014  'to 2014'

 L. 978      1982  LOAD_GLOBAL              web2ldap
             1984  LOAD_ATTR                app
             1986  LOAD_ATTR                login
             1988  LOAD_ATTR                w2l_login

 L. 979      1990  LOAD_DEREF               'self'

 L. 980      1992  LOAD_STR                 ''

 L. 981      1994  LOAD_DEREF               'self'
             1996  LOAD_METHOD              ldap_error_msg
             1998  LOAD_FAST                'err'
             2000  CALL_METHOD_1         1  ''

 L. 982      2002  LOAD_CONST               True

 L. 978      2004  LOAD_CONST               ('who', 'login_msg', 'relogin')
             2006  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2008  POP_TOP          
             2010  POP_BLOCK        
             2012  BEGIN_FINALLY    
           2014_0  COME_FROM_FINALLY  1980  '1980'
             2014  LOAD_CONST               None
             2016  STORE_FAST               'err'
             2018  DELETE_FAST              'err'
             2020  END_FINALLY      
             2022  POP_EXCEPT       
         2024_2026  JUMP_FORWARD       2958  'to 2958'
           2028_0  COME_FROM          1970  '1970'

 L. 985      2028  DUP_TOP          

 L. 986      2030  LOAD_GLOBAL              ldap0
             2032  LOAD_ATTR                INVALID_CREDENTIALS

 L. 985      2034  BUILD_TUPLE_1         1 
             2036  COMPARE_OP               exception-match
         2038_2040  POP_JUMP_IF_FALSE  2096  'to 2096'
             2042  POP_TOP          
             2044  STORE_FAST               'err'
             2046  POP_TOP          
             2048  SETUP_FINALLY      2082  'to 2082'

 L. 988      2050  LOAD_GLOBAL              web2ldap
             2052  LOAD_ATTR                app
             2054  LOAD_ATTR                login
             2056  LOAD_ATTR                w2l_login

 L. 989      2058  LOAD_DEREF               'self'

 L. 990      2060  LOAD_DEREF               'self'
             2062  LOAD_METHOD              ldap_error_msg
             2064  LOAD_FAST                'err'
             2066  CALL_METHOD_1         1  ''

 L. 991      2068  LOAD_FAST                'who'

 L. 991      2070  LOAD_CONST               True

 L. 988      2072  LOAD_CONST               ('login_msg', 'who', 'relogin')
             2074  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2076  POP_TOP          
             2078  POP_BLOCK        
             2080  BEGIN_FINALLY    
           2082_0  COME_FROM_FINALLY  2048  '2048'
             2082  LOAD_CONST               None
             2084  STORE_FAST               'err'
             2086  DELETE_FAST              'err'
             2088  END_FINALLY      
             2090  POP_EXCEPT       
         2092_2094  JUMP_FORWARD       2958  'to 2958'
           2096_0  COME_FROM          2038  '2038'

 L. 994      2096  DUP_TOP          

 L. 995      2098  LOAD_GLOBAL              web2ldap
             2100  LOAD_ATTR                ldapsession
             2102  LOAD_ATTR                InvalidSimpleBindDN

 L. 996      2104  LOAD_GLOBAL              web2ldap
             2106  LOAD_ATTR                ldapsession
             2108  LOAD_ATTR                UsernameNotUnique

 L. 994      2110  BUILD_TUPLE_2         2 
             2112  COMPARE_OP               exception-match
         2114_2116  POP_JUMP_IF_FALSE  2178  'to 2178'
             2118  POP_TOP          
             2120  STORE_FAST               'err'
             2122  POP_TOP          
             2124  SETUP_FINALLY      2164  'to 2164'

 L. 998      2126  LOAD_GLOBAL              web2ldap
             2128  LOAD_ATTR                app
             2130  LOAD_ATTR                login
             2132  LOAD_ATTR                w2l_login

 L. 999      2134  LOAD_DEREF               'self'

 L.1000      2136  LOAD_DEREF               'self'
             2138  LOAD_ATTR                form
             2140  LOAD_METHOD              utf2display
             2142  LOAD_GLOBAL              str
             2144  LOAD_FAST                'err'
             2146  CALL_FUNCTION_1       1  ''
             2148  CALL_METHOD_1         1  ''

 L.1001      2150  LOAD_FAST                'who'

 L.1001      2152  LOAD_CONST               True

 L. 998      2154  LOAD_CONST               ('login_msg', 'who', 'relogin')
             2156  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2158  POP_TOP          
             2160  POP_BLOCK        
             2162  BEGIN_FINALLY    
           2164_0  COME_FROM_FINALLY  2124  '2124'
             2164  LOAD_CONST               None
             2166  STORE_FAST               'err'
             2168  DELETE_FAST              'err'
             2170  END_FINALLY      
             2172  POP_EXCEPT       
         2174_2176  JUMP_FORWARD       2958  'to 2958'
           2178_0  COME_FROM          2114  '2114'

 L.1004      2178  DUP_TOP          
             2180  LOAD_GLOBAL              PasswordPolicyExpirationWarning
             2182  COMPARE_OP               exception-match
         2184_2186  POP_JUMP_IF_FALSE  2308  'to 2308'
             2188  POP_TOP          
             2190  STORE_FAST               'err'
             2192  POP_TOP          
             2194  SETUP_FINALLY      2294  'to 2294'

 L.1006      2196  LOAD_DEREF               'self'
             2198  LOAD_ATTR                ls
             2200  LOAD_ATTR                l
             2202  LOAD_METHOD              whoami_s
             2204  CALL_METHOD_0         0  ''
             2206  LOAD_CONST               3
             2208  LOAD_CONST               None
             2210  BUILD_SLICE_2         2 
             2212  BINARY_SUBSCR    
         2214_2216  JUMP_IF_TRUE_OR_POP  2222  'to 2222'
             2218  LOAD_FAST                'err'
             2220  LOAD_ATTR                who
           2222_0  COME_FROM          2214  '2214'
             2222  LOAD_DEREF               'self'
             2224  STORE_ATTR               dn

 L.1008      2226  LOAD_GLOBAL              web2ldap
             2228  LOAD_ATTR                app
             2230  LOAD_ATTR                passwd
             2232  LOAD_METHOD              passwd_form

 L.1009      2234  LOAD_DEREF               'self'

 L.1010      2236  LOAD_STR                 ''

 L.1011      2238  LOAD_DEREF               'self'
             2240  LOAD_ATTR                dn

 L.1012      2242  LOAD_CONST               None

 L.1013      2244  LOAD_STR                 'Password change needed'

 L.1014      2246  LOAD_DEREF               'self'
             2248  LOAD_ATTR                form
             2250  LOAD_METHOD              utf2display

 L.1015      2252  LOAD_STR                 'Password will expire in %s!'

 L.1016      2254  LOAD_GLOBAL              web2ldap
             2256  LOAD_ATTR                app
             2258  LOAD_ATTR                gui
             2260  LOAD_METHOD              ts2repr

 L.1017      2262  LOAD_GLOBAL              web2ldap
             2264  LOAD_ATTR                app
             2266  LOAD_ATTR                schema
             2268  LOAD_ATTR                syntaxes
             2270  LOAD_ATTR                Timespan
             2272  LOAD_ATTR                time_divisors

 L.1018      2274  LOAD_STR                 ' '

 L.1019      2276  LOAD_FAST                'err'
             2278  LOAD_ATTR                timeBeforeExpiration

 L.1016      2280  CALL_METHOD_3         3  ''

 L.1015      2282  BINARY_MODULO    

 L.1014      2284  CALL_METHOD_1         1  ''

 L.1008      2286  CALL_METHOD_6         6  ''
             2288  POP_TOP          
             2290  POP_BLOCK        
             2292  BEGIN_FINALLY    
           2294_0  COME_FROM_FINALLY  2194  '2194'
             2294  LOAD_CONST               None
             2296  STORE_FAST               'err'
             2298  DELETE_FAST              'err'
             2300  END_FINALLY      
             2302  POP_EXCEPT       
         2304_2306  JUMP_FORWARD       2958  'to 2958'
           2308_0  COME_FROM          2184  '2184'

 L.1025      2308  DUP_TOP          
             2310  LOAD_GLOBAL              PasswordPolicyException
             2312  COMPARE_OP               exception-match
         2314_2316  POP_JUMP_IF_FALSE  2420  'to 2420'
             2318  POP_TOP          
             2320  STORE_FAST               'err'
             2322  POP_TOP          
             2324  SETUP_FINALLY      2406  'to 2406'

 L.1027      2326  LOAD_DEREF               'self'
             2328  LOAD_ATTR                ls
             2330  LOAD_ATTR                l
             2332  LOAD_METHOD              whoami_s
             2334  CALL_METHOD_0         0  ''
             2336  LOAD_CONST               3
             2338  LOAD_CONST               None
             2340  BUILD_SLICE_2         2 
             2342  BINARY_SUBSCR    
         2344_2346  JUMP_IF_TRUE_OR_POP  2352  'to 2352'
             2348  LOAD_FAST                'err'
             2350  LOAD_ATTR                who
           2352_0  COME_FROM          2344  '2344'
             2352  LOAD_METHOD              decode
             2354  LOAD_DEREF               'self'
             2356  LOAD_ATTR                ls
             2358  LOAD_ATTR                charset
             2360  CALL_METHOD_1         1  ''
             2362  LOAD_DEREF               'self'
             2364  STORE_ATTR               dn

 L.1029      2366  LOAD_GLOBAL              web2ldap
             2368  LOAD_ATTR                app
             2370  LOAD_ATTR                passwd
             2372  LOAD_METHOD              passwd_form

 L.1030      2374  LOAD_DEREF               'self'

 L.1031      2376  LOAD_STR                 ''

 L.1032      2378  LOAD_DEREF               'self'
             2380  LOAD_ATTR                dn

 L.1033      2382  LOAD_CONST               None

 L.1034      2384  LOAD_STR                 'Password change needed'

 L.1035      2386  LOAD_DEREF               'self'
             2388  LOAD_ATTR                form
             2390  LOAD_METHOD              utf2display
             2392  LOAD_FAST                'err'
             2394  LOAD_ATTR                desc
             2396  CALL_METHOD_1         1  ''

 L.1029      2398  CALL_METHOD_6         6  ''
             2400  POP_TOP          
             2402  POP_BLOCK        
             2404  BEGIN_FINALLY    
           2406_0  COME_FROM_FINALLY  2324  '2324'
             2406  LOAD_CONST               None
             2408  STORE_FAST               'err'
             2410  DELETE_FAST              'err'
             2412  END_FINALLY      
             2414  POP_EXCEPT       
         2416_2418  JUMP_FORWARD       2958  'to 2958'
           2420_0  COME_FROM          2314  '2314'

 L.1038      2420  DUP_TOP          

 L.1039      2422  LOAD_GLOBAL              socket
             2424  LOAD_ATTR                error

 L.1040      2426  LOAD_GLOBAL              socket
             2428  LOAD_ATTR                gaierror

 L.1041      2430  LOAD_GLOBAL              IOError

 L.1042      2432  LOAD_GLOBAL              UnicodeError

 L.1038      2434  BUILD_TUPLE_4         4 
             2436  COMPARE_OP               exception-match
         2438_2440  POP_JUMP_IF_FALSE  2522  'to 2522'
             2442  POP_TOP          
             2444  STORE_FAST               'err'
             2446  POP_TOP          
             2448  SETUP_FINALLY      2508  'to 2508'

 L.1044      2450  LOAD_GLOBAL              log_exception
             2452  LOAD_DEREF               'self'
             2454  LOAD_ATTR                env
             2456  LOAD_DEREF               'self'
             2458  LOAD_ATTR                ls
             2460  LOAD_DEREF               'self'
             2462  LOAD_ATTR                dn
             2464  LOAD_GLOBAL              web2ldapcnf
             2466  LOAD_ATTR                log_error_details
             2468  CALL_FUNCTION_4       4  ''
             2470  POP_TOP          

 L.1045      2472  LOAD_GLOBAL              exception_message

 L.1046      2474  LOAD_DEREF               'self'

 L.1047      2476  LOAD_STR                 'Unhandled %s'
             2478  LOAD_FAST                'err'
             2480  LOAD_ATTR                __class__
             2482  LOAD_ATTR                __name__
             2484  BINARY_MODULO    

 L.1048      2486  LOAD_DEREF               'self'
             2488  LOAD_ATTR                form
             2490  LOAD_METHOD              utf2display
             2492  LOAD_GLOBAL              str
             2494  LOAD_FAST                'err'
             2496  CALL_FUNCTION_1       1  ''
             2498  CALL_METHOD_1         1  ''

 L.1045      2500  CALL_FUNCTION_3       3  ''
             2502  POP_TOP          
             2504  POP_BLOCK        
             2506  BEGIN_FINALLY    
           2508_0  COME_FROM_FINALLY  2448  '2448'
             2508  LOAD_CONST               None
             2510  STORE_FAST               'err'
             2512  DELETE_FAST              'err'
             2514  END_FINALLY      
             2516  POP_EXCEPT       
         2518_2520  JUMP_FORWARD       2958  'to 2958'
           2522_0  COME_FROM          2438  '2438'

 L.1051      2522  DUP_TOP          
             2524  LOAD_GLOBAL              ldap0
             2526  LOAD_ATTR                LDAPError
             2528  COMPARE_OP               exception-match
         2530_2532  POP_JUMP_IF_FALSE  2608  'to 2608'
             2534  POP_TOP          
             2536  STORE_FAST               'ldap_err'
             2538  POP_TOP          
             2540  SETUP_FINALLY      2594  'to 2594'

 L.1052      2542  LOAD_GLOBAL              log_exception
             2544  LOAD_DEREF               'self'
             2546  LOAD_ATTR                env
             2548  LOAD_DEREF               'self'
             2550  LOAD_ATTR                ls
             2552  LOAD_DEREF               'self'
             2554  LOAD_ATTR                dn
             2556  LOAD_GLOBAL              web2ldapcnf
             2558  LOAD_ATTR                log_error_details
             2560  CALL_FUNCTION_4       4  ''
             2562  POP_TOP          

 L.1053      2564  LOAD_GLOBAL              exception_message

 L.1054      2566  LOAD_DEREF               'self'

 L.1055      2568  LOAD_STR                 'Unhandled %s'
             2570  LOAD_FAST                'ldap_err'
             2572  LOAD_ATTR                __class__
             2574  LOAD_ATTR                __name__
             2576  BINARY_MODULO    

 L.1056      2578  LOAD_DEREF               'self'
             2580  LOAD_METHOD              ldap_error_msg
             2582  LOAD_FAST                'ldap_err'
             2584  CALL_METHOD_1         1  ''

 L.1053      2586  CALL_FUNCTION_3       3  ''
             2588  POP_TOP          
             2590  POP_BLOCK        
             2592  BEGIN_FINALLY    
           2594_0  COME_FROM_FINALLY  2540  '2540'
             2594  LOAD_CONST               None
             2596  STORE_FAST               'ldap_err'
             2598  DELETE_FAST              'ldap_err'
             2600  END_FINALLY      
             2602  POP_EXCEPT       
         2604_2606  JUMP_FORWARD       2958  'to 2958'
           2608_0  COME_FROM          2530  '2530'

 L.1059      2608  DUP_TOP          
             2610  LOAD_GLOBAL              ErrorExit
             2612  COMPARE_OP               exception-match
         2614_2616  POP_JUMP_IF_FALSE  2676  'to 2676'
             2618  POP_TOP          
             2620  STORE_FAST               'error_exit'
             2622  POP_TOP          
             2624  SETUP_FINALLY      2662  'to 2662'

 L.1060      2626  LOAD_DEREF               'self'
             2628  LOAD_METHOD              log
             2630  LOAD_GLOBAL              logging
             2632  LOAD_ATTR                WARN
             2634  LOAD_STR                 'ErrorExit: %r'
             2636  LOAD_FAST                'error_exit'
             2638  LOAD_ATTR                Msg
             2640  CALL_METHOD_3         3  ''
             2642  POP_TOP          

 L.1061      2644  LOAD_GLOBAL              exception_message

 L.1062      2646  LOAD_DEREF               'self'

 L.1063      2648  LOAD_STR                 'Error'

 L.1064      2650  LOAD_FAST                'error_exit'
             2652  LOAD_ATTR                Msg

 L.1061      2654  CALL_FUNCTION_3       3  ''
             2656  POP_TOP          
             2658  POP_BLOCK        
             2660  BEGIN_FINALLY    
           2662_0  COME_FROM_FINALLY  2624  '2624'
             2662  LOAD_CONST               None
             2664  STORE_FAST               'error_exit'
             2666  DELETE_FAST              'error_exit'
             2668  END_FINALLY      
             2670  POP_EXCEPT       
         2672_2674  JUMP_FORWARD       2958  'to 2958'
           2676_0  COME_FROM          2614  '2614'

 L.1067      2676  DUP_TOP          
             2678  LOAD_GLOBAL              web2ldap
             2680  LOAD_ATTR                web
             2682  LOAD_ATTR                session
             2684  LOAD_ATTR                MaxSessionPerIPExceeded
             2686  COMPARE_OP               exception-match
         2688_2690  POP_JUMP_IF_FALSE  2756  'to 2756'
             2692  POP_TOP          
             2694  STORE_FAST               'session_err'
             2696  POP_TOP          
             2698  SETUP_FINALLY      2744  'to 2744'

 L.1068      2700  LOAD_DEREF               'self'
             2702  LOAD_METHOD              log
             2704  LOAD_GLOBAL              logging
             2706  LOAD_ATTR                WARN
             2708  LOAD_GLOBAL              str
             2710  LOAD_FAST                'session_err'
             2712  CALL_FUNCTION_1       1  ''
             2714  CALL_METHOD_2         2  ''
             2716  POP_TOP          

 L.1069      2718  LOAD_DEREF               'self'
             2720  LOAD_METHOD              simple_msg

 L.1070      2722  LOAD_STR                 'Client %s exceeded limit of max. %d sessions! Try later...'

 L.1071      2724  LOAD_FAST                'session_err'
             2726  LOAD_ATTR                remote_ip

 L.1072      2728  LOAD_FAST                'session_err'
             2730  LOAD_ATTR                max_session_count

 L.1070      2732  BUILD_TUPLE_2         2 
             2734  BINARY_MODULO    

 L.1069      2736  CALL_METHOD_1         1  ''
             2738  POP_TOP          
             2740  POP_BLOCK        
             2742  BEGIN_FINALLY    
           2744_0  COME_FROM_FINALLY  2698  '2698'
             2744  LOAD_CONST               None
             2746  STORE_FAST               'session_err'
             2748  DELETE_FAST              'session_err'
             2750  END_FINALLY      
             2752  POP_EXCEPT       
             2754  JUMP_FORWARD       2958  'to 2958'
           2756_0  COME_FROM          2688  '2688'

 L.1076      2756  DUP_TOP          
             2758  LOAD_GLOBAL              web2ldap
             2760  LOAD_ATTR                web
             2762  LOAD_ATTR                session
             2764  LOAD_ATTR                MaxSessionCountExceeded
             2766  COMPARE_OP               exception-match
         2768_2770  POP_JUMP_IF_FALSE  2824  'to 2824'
             2772  POP_TOP          
             2774  STORE_FAST               'session_err'
             2776  POP_TOP          
             2778  SETUP_FINALLY      2812  'to 2812'

 L.1077      2780  LOAD_DEREF               'self'
             2782  LOAD_METHOD              log
             2784  LOAD_GLOBAL              logging
             2786  LOAD_ATTR                WARN
             2788  LOAD_GLOBAL              str
             2790  LOAD_FAST                'session_err'
             2792  CALL_FUNCTION_1       1  ''
             2794  CALL_METHOD_2         2  ''
             2796  POP_TOP          

 L.1078      2798  LOAD_DEREF               'self'
             2800  LOAD_METHOD              simple_msg
             2802  LOAD_STR                 'Too many web sessions! Try later...'
             2804  CALL_METHOD_1         1  ''
             2806  POP_TOP          
             2808  POP_BLOCK        
             2810  BEGIN_FINALLY    
           2812_0  COME_FROM_FINALLY  2778  '2778'
             2812  LOAD_CONST               None
             2814  STORE_FAST               'session_err'
             2816  DELETE_FAST              'session_err'
             2818  END_FINALLY      
             2820  POP_EXCEPT       
             2822  JUMP_FORWARD       2958  'to 2958'
           2824_0  COME_FROM          2768  '2768'

 L.1080      2824  DUP_TOP          
             2826  LOAD_GLOBAL              web2ldap
             2828  LOAD_ATTR                web
             2830  LOAD_ATTR                session
             2832  LOAD_ATTR                SessionException
             2834  COMPARE_OP               exception-match
         2836_2838  POP_JUMP_IF_FALSE  2882  'to 2882'
             2840  POP_TOP          
             2842  POP_TOP          
             2844  POP_TOP          

 L.1081      2846  LOAD_GLOBAL              log_exception
             2848  LOAD_DEREF               'self'
             2850  LOAD_ATTR                env
             2852  LOAD_DEREF               'self'
             2854  LOAD_ATTR                ls
             2856  LOAD_DEREF               'self'
             2858  LOAD_ATTR                dn
             2860  LOAD_GLOBAL              web2ldapcnf
             2862  LOAD_ATTR                log_error_details
             2864  CALL_FUNCTION_4       4  ''
             2866  POP_TOP          

 L.1082      2868  LOAD_DEREF               'self'
             2870  LOAD_METHOD              url_redirect
             2872  LOAD_STR                 'Session handling error.'
             2874  CALL_METHOD_1         1  ''
             2876  POP_TOP          
             2878  POP_EXCEPT       
             2880  JUMP_FORWARD       2958  'to 2958'
           2882_0  COME_FROM          2836  '2836'

 L.1084      2882  DUP_TOP          
             2884  LOAD_GLOBAL              Exception
             2886  COMPARE_OP               exception-match
         2888_2890  POP_JUMP_IF_FALSE  2956  'to 2956'
             2892  POP_TOP          
             2894  POP_TOP          
             2896  POP_TOP          

 L.1085      2898  LOAD_GLOBAL              hasattr
             2900  LOAD_DEREF               'self'
             2902  LOAD_STR                 'ls'
             2904  CALL_FUNCTION_2       2  ''
         2906_2908  POP_JUMP_IF_FALSE  2918  'to 2918'

 L.1086      2910  LOAD_DEREF               'self'
             2912  LOAD_ATTR                ls
             2914  STORE_FAST               'error_ls'
             2916  JUMP_FORWARD       2922  'to 2922'
           2918_0  COME_FROM          2906  '2906'

 L.1088      2918  LOAD_CONST               None
             2920  STORE_FAST               'error_ls'
           2922_0  COME_FROM          2916  '2916'

 L.1089      2922  LOAD_GLOBAL              log_exception
             2924  LOAD_DEREF               'self'
             2926  LOAD_ATTR                env
             2928  LOAD_FAST                'error_ls'
             2930  LOAD_DEREF               'self'
             2932  LOAD_ATTR                dn
             2934  LOAD_GLOBAL              web2ldapcnf
             2936  LOAD_ATTR                log_error_details
             2938  CALL_FUNCTION_4       4  ''
             2940  POP_TOP          

 L.1090      2942  LOAD_DEREF               'self'
             2944  LOAD_METHOD              simple_msg
             2946  LOAD_STR                 'Unhandled error!'
             2948  CALL_METHOD_1         1  ''
             2950  POP_TOP          
             2952  POP_EXCEPT       
             2954  JUMP_FORWARD       2958  'to 2958'
           2956_0  COME_FROM          2888  '2888'
             2956  END_FINALLY      
           2958_0  COME_FROM          2954  '2954'
           2958_1  COME_FROM          2880  '2880'
           2958_2  COME_FROM          2822  '2822'
           2958_3  COME_FROM          2754  '2754'
           2958_4  COME_FROM          2672  '2672'
           2958_5  COME_FROM          2604  '2604'
           2958_6  COME_FROM          2518  '2518'
           2958_7  COME_FROM          2416  '2416'
           2958_8  COME_FROM          2304  '2304'
           2958_9  COME_FROM          2174  '2174'
          2958_10  COME_FROM          2092  '2092'
          2958_11  COME_FROM          2024  '2024'
          2958_12  COME_FROM          1942  '1942'
          2958_13  COME_FROM          1882  '1882'
          2958_14  COME_FROM          1656  '1656'
          2958_15  COME_FROM          1552  '1552'
          2958_16  COME_FROM          1458  '1458'

Parse error at or near `LOAD_CONST' instruction at offset 214