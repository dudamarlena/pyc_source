# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__AUTH__/openid_connect/openid_connect.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 4473 bytes
import json, urllib.parse, urllib.request

def get_logged_in_user(context):
    session = context['cs_session_data']
    logintype = context['csm_auth'].get_auth_type_by_name(context, 'login')

    def generate_token():
        return logintype['generate_confirmation_token'](50)

    _get_base_url = logintype['_get_base_url']
    action = context['cs_form'].get('loginaction', None)
    if action == 'logout':
        context['cs_session_data'] = {}
        return {'cs_reload': True}
    elif 'username' in session:
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
                         context['cs_openid_server'])
                    context['cs_content'] = lbox + context['cs_content']

                context['cs_post_load'] = new_postload
                return {}
            context['cs_handler'] = 'passthrough'
            context['cs_content_header'] = 'Please Log In'
            context['cs_content'] = LOGIN_PAGE % (
             _get_base_url(context),
             context['cs_openid_server'])
            return {'cs_render_now': True}
    else:
        if action == 'login':
            redir_url = '%s/_auth/openid_connect/callback' % context['cs_url_root']
            scope = context.get('cs_openid_scope', 'openid profile email')
            state = generate_token()
            nonce = generate_token()
            get_data = {'redirect_uri':redir_url, 
             'state':state, 
             'nonce':nonce, 
             'scope':scope, 
             'client_id':context.get('cs_openid_client_id', None), 
             'response_type':'code'}
            openid_url = context.get('cs_openid_server', None)
            request = urllib.request.Request('%s/.well-known/openid-configuration' % openid_url)
            resp = json.loads(urllib.request.urlopen(request).read())
            session['_openid_course'] = context['cs_course']
            session['_openid_path'] = context['cs_path_info']
            session['_openid_nonce'] = nonce
            session['_openid_state'] = state
            session['_openid_config'] = resp
            qstring = urllib.parse.urlencode(get_data)
            return {'cs_redirect': '%s?%s' % (resp['authorization_endpoint'], qstring)}
        raise Exception('Unknown action: %r' % action)


LOGIN_PAGE = '\n<div id="catsoop_login_box">\nAccess to this page requires logging in via OpenID Connect.  Please <a\nhref="%s?loginaction=login">Log In</a> to continue.<br/>Note that this link\nwill take you to an external site (<tt>%s</tt>) to authenticate, and then you\nwill be redirected back to this page.\n</div>\n'
LOGIN_BOX = '\n<div class="response" id="catsoop_login_box">\n<b><center>You are not logged in.</center></b><br/>\nIf you are a current student, please <a href="%s?loginaction=login">Log\nIn</a> for full access to the web site.<br/>Note that this link will take you to\nan external site (<tt>%s</tt>) to authenticate, and then you will be redirected\nback to this page.\n</div>\n'