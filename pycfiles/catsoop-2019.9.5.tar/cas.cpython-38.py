# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__AUTH__/cas/cas.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 4529 bytes
"""
Authenticate using CAS (https://en.wikipedia.org/wiki/Central_Authentication_Service)
"""
import urllib.parse, urllib.request
from catsoop import debug_log
LOGGER = debug_log.LOGGER

def get_logged_in_user(context):
    """
    Authenticate using CAS
    """
    session = context['cs_session_data']
    logintype = context['csm_auth'].get_auth_type_by_name(context, 'login')
    _get_base_url = logintype['_get_base_url']
    cas_url = context['cs_cas_server']
    redir_url = '%s/_auth/cas/callback' % context['cs_url_root']
    action = context['cs_form'].get('loginaction', None)
    LOGGER.info('[auth.cas] login action=%s' % action)
    if action == 'logout':
        ticket = context['cs_session_data'].get('cas_ticket', '')
        logout_url = cas_url + '/logout' + '?service=' + urllib.parse.quote(redir_url) + '&ticket=' + urllib.parse.quote(ticket)
        try:
            ret = urllib.request.urlopen(logout_url).read()
            LOGGER.info('[auth.cas] CAS server logout returnd ret=%s' % ret)
        except Exception as err:
            try:
                LOGGER.error('[auth.cas] CAS server rejected logout request, err=%s' % str(err))
            finally:
                err = None
                del err

    else:
        context['cs_session_data'] = {}
        return {'cs_reload': True}
        if 'username' in session:
            uname = session['username']
            return {'username':uname, 
             'name':session.get('name', uname), 
             'email':session.get('email', uname)}
            if action is None:
                if context.get('cs_view_without_auth', True):
                    old_postload = context.get('cs_post_load', None)

                    def new_postload(context):
                        if old_postload is not None:
                            old_postload(context)
                        elif 'cs_login_box' in context:
                            lbox = context['cs_login_box'](context)
                        else:
                            lbox = LOGIN_BOX % (
                             _get_base_url(context),
                             context['cs_cas_server'])
                        context['cs_content'] = lbox + context['cs_content']

                    context['cs_post_load'] = new_postload
                    return {}
                context['cs_handler'] = 'passthrough'
                context['cs_content_header'] = 'Please Log In'
                context['cs_content'] = LOGIN_PAGE % (_get_base_url(context), cas_url)
                return {'cs_render_now': True}
        elif action == 'login':
            login_url = cas_url + '/login' + '?service=' + urllib.parse.quote(redir_url)
            LOGGER.info('no auth, reditecting to %s' % login_url)
            session['_cas_course'] = context['cs_course']
            session['_cas_path'] = context['cs_path_info']
            return {'cs_redirect': login_url}
        raise Exception('Unknown action: %r' % action)


LOGIN_PAGE = '\n<div id="catsoop_login_box">\nAccess to this page requires logging in via CAS.  Please <a\nhref="%s?loginaction=login">Log In</a> to continue.<br/>Note that this link\nwill take you to an external site (<tt>%s</tt>) to authenticate, and then you\nwill be redirected back to this page.\n</div>\n'
LOGIN_BOX = '\n<div class="response" id="catsoop_login_box">\n<b><center>You are not logged in.</center></b><br/>\nIf you are a current student, please <a href="%s?loginaction=login">Log\nIn</a> for full access to the web site.<br/>Note that this link will take you to\nan external site (<tt>%s</tt>) to authenticate, and then you will be redirected\nback to this page.\n</div>\n'