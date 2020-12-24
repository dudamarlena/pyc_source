# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__AUTH__/login/login.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 45367 bytes
import os, re, struct, random, string, hashlib

def user_menu_options(context):
    url = _get_base_url(context)
    return [
     {'text':'Change Password', 
      'link':'%s?loginaction=change_password' % url}]


def get_logged_in_user(context):
    base_context = context['csm_base_context']
    logging = context['csm_cslog']
    form = context.get('cs_form', {})
    mail = context['csm_mail']
    session = context['cs_session_data']
    action = form.get('loginaction', '')
    hash_iterations = context.get('cs_password_hash_iterations', 500000)
    url = _get_base_url(context)
    if action == 'logout':
        context['cs_session_data'] = {}
        return {'cs_reload': True}
    if action == 'change_password':
        uname = session.get('username', None)
        if uname is None:
            base = _get_base_url(context)
            context['cs_content_header'] = 'Please Log In'
            context['cs_content'] = 'You cannot change your password until you have logged in.<br/><a href="%s">Go Back</a>' % base
            context['cs_handler'] = 'passthrough'
            return {'cs_render_now': True}
        login_info = logging.most_recent('_logininfo', [], uname, {})
        if not login_info.get('confirmed', False):
            context['cs_content_header'] = 'Your E-mail Has Not Been Confirmed'
            context['cs_content'] = "Your registration is not yet complete.  Please check your e-mail for instructions on how to complete the process.  If you did not receive a confirmation e-mail, please <a href='%s?loginaction=reconfirm_reg&username=%s'>click here</a> to re-send the email." % (
             url, uname)
            context['cs_handler'] = 'passthrough'
            return {'cs_render_now': True}
        if 'cs_hashed_2' in form:
            errors = []
            if not check_password(context, form['cs_hashed_2'], uname, hash_iterations):
                errors.append('Incorrect password entered.')
            else:
                passwd = form['cs_hashed_0']
                passwd2 = form['cs_hashed_1']
                if passwd != passwd2:
                    errors.append('New passwords do not match.')
                if len(errors) > 0:
                    errs = '\n'.join(('<li>%s</li>' % i for i in errors))
                    lmsg = '<font color="red">Your password was not changed:\n<ul>%s</ul></font>' % errs
                    session['login_message'] = lmsg
                else:
                    clear_session_vars(context, 'login_message')
                    salt = get_new_password_salt()
                    phash = compute_password_hash(context, passwd, salt, hash_iterations)
                    login_info['password_salt'] = salt
                    login_info['password_hash'] = phash
                    logging.update_log('_logininfo', [], uname, login_info)
                    context['cs_content_header'] = 'Password Changed!'
                    base = _get_base_url(context)
                    context['cs_content'] = 'Your password has been successfully changed.<br/><a href="%s">Continue</a>' % base
                    context['cs_handler'] = 'passthrough'
                    return {'cs_render_now': True}
        context['cs_content_header'] = 'Change Password'
        context['cs_content'] = generate_password_change_form(context)
        context['cs_handler'] = 'passthrough'
        return {'cs_render_now': True}
    if action == 'confirm_reg':
        u = form.get('username', None)
        t = form.get('token', None)
        stored_token = logging.most_recent('_confirmation_token', [], u, '')
        login_info = logging.most_recent('_logininfo', [], u, {})
        context['cs_handler'] = 'passthrough'
        retval = {'cs_render_now': True}
        url = _get_base_url(context)
        if login_info.get('confirmed', False):
            context['cs_content_header'] = 'Already Confirmed'
            context['cs_content'] = "This account has already been confirmed.  Please <a href='%s'>click here</a> to log in." % url
        elif t == stored_token and 'confirmed' in login_info:
            login_info['confirmed'] = True
            logging.update_log('_logininfo', [], u, login_info)
            context['cs_content_header'] = 'Account Confirmation Succeeded'
            context['cs_content'] = 'Please <a href="%s">click here</a> to log in.' % url
            clear_session_vars(context, 'login_message', 'last_form')
            retval.update(login_info)
            session.update(login_info)
            session['username'] = u
            session['course'] = context.get('cs_course', None)
        else:
            cs_debug(t, stored_token, login_info)
            context['cs_content_header'] = 'Account Confirmation Failed'
            context['cs_content'] = 'Please double-check the details from the confirmation e-mail you received.'
        return retval
    if 'username' in session:
        uname = session['username']
        clear_session_vars(context, 'login_message', 'last_form')
        return {'username':uname, 
         'name':session.get('name', uname), 
         'email':session.get('email', uname)}
    if action == 'forgot_password' and not mail.can_send_email(context):
        context['cs_content_header'] = 'Password Reset: Error'
        context['cs_content'] = 'This feature is not available on this CAT-SOOP instance.'
        context['cs_handler'] = 'passthrough'
        return {'cs_render_now': True}
        if 'uname' in form:
            uname = form['uname']
            email = form.get('email', None)
            login_info = logging.most_recent('_logininfo', [], uname, {})
            if email != login_info.get('email', ''):
                lmsg = '<font color="red">The information you provided does not match any known accounts.</font>'
                session['login_message'] = lmsg
                session['last_form'] = form
            else:
                clear_session_vars(context, 'login_message', 'last_form')
                token = generate_confirmation_token()
                logging.update_log('_password_reset_token', [], uname, token)
                mail.send_email(context, email, 'CAT-SOOP: Confirm Password Reset', passwd_confirm_emails(context, uname, token)[0])
                context['cs_content_header'] = 'Password Reset: Confirm'
                context['cs_content'] = 'Please check your e-mail for instructions on how to complete the process.'
                context['cs_handler'] = 'passthrough'
                return {'cs_render_now': True}
        context['cs_content_header'] = 'Forgot Password'
        context['cs_content'] = 'Please enter your information below to reset your password.'
        context['cs_content'] += generate_forgot_password_form(context)
        context['cs_handler'] = 'passthrough'
        return {'cs_render_now': True}
    if action == 'reset_password' and not mail.can_send_email(context):
        context['cs_content_header'] = 'Password Reset: Error'
        context['cs_content'] = 'This feature is not available on this CAT-SOOP instance.'
        context['cs_handler'] = 'passthrough'
        return {'cs_render_now': True}
        if 'cs_hashed_0' in form:
            errors = []
            u = form.get('username', None)
            t = form.get('token', None)
            stored_token = logging.most_recent('_password_reset_token', [], u, '')
            if stored_token != t or stored_token == '':
                errors.append('Unknown user, or incorrect confirmation token.')
            passwd = form['cs_hashed_0']
            passwd2 = form['cs_hashed_1']
            if passwd != passwd2:
                errors.append('New passwords do not match.')
            elif len(errors) > 0:
                errs = '\n'.join(('<li>%s</li>' % i for i in errors))
                lmsg = '<font color="red">Your password was not reset:\n<ul>%s</ul></font>' % errs
                session['login_message'] = lmsg
            else:
                clear_session_vars(context, 'login_message')
                login_info = logging.most_recent('_logininfo', [], u, {})
                salt = get_new_password_salt()
                phash = compute_password_hash(context, passwd, salt, hash_iterations)
                login_info['password_salt'] = salt
                login_info['password_hash'] = phash
                logging.update_log('_logininfo', [], u, login_info)
                context['cs_content_header'] = 'Password Changed!'
                base = _get_base_url(context)
                context['cs_content'] = 'Your password has been successfully changed.<br/><a href="%s">Continue</a>' % base
                context['cs_handler'] = 'passthrough'
                email = login_info.get('email', u)
                name = login_info.get('name', u)
                info = {'username':u,  'name':name,  'email':email}
                session.update(info)
                session['course'] = context.get('cs_course', None)
                return {'cs_render_now': True}
        context['cs_content_header'] = 'Reset Password'
        context['cs_content'] = generate_password_reset_form(context)
        context['cs_handler'] = 'passthrough'
        return {'cs_render_now': True}
        if action == 'login':
            uname = form.get('login_uname', '')
            if uname == '':
                clear_session_vars(context, 'login_message')
            entered_password = form.get('cs_hashed_0', '')
            valid_uname = True
            if _validate_email(context, uname) is None:
                data_root = context.get('cs_data_root', base_context.cs_data_root)
                global_log_dir = os.path.join(data_root, '_logs')
                for d in os.listdir(global_log_dir):
                    if not d.endswith('.db'):
                        pass
                    else:
                        u = d[:-3]
                        e = logging.most_recent('_logininfo', [], u, {})
                        e = e.get('email', None)

                if e == uname:
                    uname = u
                    break
        else:
            vmsg = _validate_username(context, uname)
            if vmsg is not None:
                valid_uname = False
                lmsg = '<font color="red">' + vmsg + '</font>'
                session.update({'login_message':lmsg,  'last_form':form})
            valid_pwd = check_password(context, entered_password, uname, hash_iterations)
            if valid_uname:
                if valid_pwd:
                    login_info = logging.most_recent('_logininfo', [], uname, {})
                    if not login_info.get('confirmed', False):
                        context['cs_content_header'] = 'Your E-mail Has Not Been Confirmed'
                        context['cs_content'] = "Your registration is not yet complete.  Please check your e-mail for instructions on how to complete the process.  If you did not receive a confirmation e-mail, please <a href='%s?loginaction=reconfirm_reg&username=%s'>click here</a> to re-send the email." % (
                         url, uname)
                        context['cs_handler'] = 'passthrough'
                        return {'cs_render_now': True}
                    email = login_info.get('email', uname)
                    name = login_info.get('name', uname)
                    info = {'username':uname,  'name':name,  'email':email}
                    session.update(info)
                    session['course'] = context.get('cs_course', None)
                    clear_session_vars(context, 'login_message')
                    info['cs_reload'] = True
                    return info
            if valid_uname:
                lmsg = '<font color="red">Incorrect username or password.</font>'
                session.update({'login_message':lmsg,  'last_form':form})
    else:
        if action == 'reconfirm_reg':
            uname = form.get('username', None)
            token = logging.most_recent('_confirmation_token', [], uname, None)
            login_info = logging.most_recent('_logininfo', [], uname, {})
            if login_info.get('confirmed', False):
                context['cs_content_header'] = 'Already Confirmed'
                context['cs_content'] = "This account has already been confirmed.  Please <a href='%s'>click here</a> to log in." % url
            elif token is None:
                context['cs_content_header'] = 'Error'
                context['cs_content'] = 'The provided information is complete.  Please check your e-mail for instructions on how to complete the process.'
            else:
                print('TRYING TO SEND TO', login_info['email'])
                mail.send_email(context, login_info['email'], 'CAT-SOOP: Confirm E-mail Address', reg_confirm_emails(context, uname, token)[0])
                print('DONE')
                context['cs_content_header'] = 'Confirmation E-mail Sent'
                context['cs_content'] = "Your registration is almost complete.  Please check your e-mail for instructions on how to complete the process.  If you do not receive a confirmation e-mail within 5 minutes, please <a href='%s?loginaction=reconfirm_reg&username=%s'>click here</a> to re-send the email." % (
                 url, uname)
        else:
            context['cs_handler'] = 'passthrough'
            return {'cs_render_now': True}
            if action == 'register' and not context.get('cs_allow_registration', True):
                return {'cs_render_now': True}
                uname = form.get('uname', '').strip()
                if uname != '':
                    email = form.get('email', '').strip()
                    email2 = form.get('email2', '').strip()
                    passwd = form.get('cs_hashed_0', '')
                    passwd2 = form.get('cs_hashed_1', '')
                    name = form.get('name', '').strip()
                    if name == '':
                        name = uname
                    errors = []
                    if len(email) == 0:
                        errors.append('No e-mail address entered.')
                    elif email != email2:
                        errors.append('E-mail addresses do not match.')
                    else:
                        e_check_result = _validate_email(context, email)
                    if e_check_result is not None:
                        errors.append(e_check_result)
                    uname_okay = True
                    if len(uname) == 0:
                        errors.append('No username entered.')
                        uname_okay = False
                    else:
                        u_check_result = _validate_username(context, uname)
                    if u_check_result is not None:
                        errors.append(u_check_result)
                        uname_okay = False
                    elif uname_okay:
                        login_info = logging.most_recent('_logininfo', [], uname, default=None)
                        if uname.lower() == 'none' or login_info is not None:
                            errors.append('Username %s is not available.' % uname)
                        if passwd != passwd2:
                            errors.append('Passwords do not match.')
                        if len(errors) > 0:
                            errs = '\n'.join(('<li>%s</li>' % i for i in errors))
                            lmsg = '<font color="red">Your account was not created:\n<ul>%s</ul></font>' % errs
                            session['login_message'] = lmsg
                            session['last_form'] = form
                    else:
                        clear_session_vars(context, 'login_message', 'last_form')
                        salt = get_new_password_salt()
                        phash = compute_password_hash(context, passwd, salt, hash_iterations)
                        if mail.can_send_email(context) and context.get('cs_require_confirm_email', True):
                            token = generate_confirmation_token()
                            logging.overwrite_log('_confirmation_token', [], uname, token)
                            (mail.send_email)(context, email, 'CAT-SOOP: Confirm E-mail Address', *reg_confirm_emails(context, uname, token))
                            confirmed = False
                        else:
                            confirmed = True
                        uinfo = {'password_salt':salt, 
                         'password_hash':phash, 
                         'email':email, 
                         'name':name, 
                         'confirmed':confirmed}
                        logging.overwrite_log('_logininfo', [], uname, uinfo)
                        if confirmed:
                            info = {'username':uname,  'name':name,  'email':email}
                            session.update(info)
                            session['course'] = context.get('cs_course', None)
                            info['cs_reload'] = True
                            return info
                        context['cs_content_header'] = 'Thank You!'
                        context['cs_content'] = "Your registration is almost complete.  Please check your e-mail for instructions on how to complete the process.  If you do not receive a confirmation e-mail within 5 minutes, please <a href='%s?loginaction=reconfirm_reg&username=%s'>click here</a> to re-send the email." % (
                         url, uname)
                        context['cs_handler'] = 'passthrough'
                        return {'cs_render_now': True}
                context['cs_content_header'] = 'Register'
                context['cs_content'] = generate_registration_form(context)
                context['cs_handler'] = 'passthrough'
                return {'cs_render_now': True}
            if action != 'login':
                clear_session_vars(context, 'login_message')
            if context.get('cs_view_without_auth', True) and action != 'login':
                old_postload = context.get('cs_post_load', None)

                def new_postload(context):
                    if old_postload is not None:
                        old_postload(context)
                    elif 'cs_login_box' in context:
                        lbox = context['cs_login_box'](context)
                    else:
                        lbox = LOGIN_BOX % _get_base_url(context)
                    context['cs_content'] = lbox + context['cs_content']

                context['cs_post_load'] = new_postload
                return {}
        uname = form.get('login_uname', '')
        if uname == '':
            clear_session_vars(context, 'login_message')
        context['cs_content_header'] = 'Please Log In To Continue'
        context['cs_content'] = generate_login_form(context)
        context['cs_handler'] = 'passthrough'
        return {'cs_render_now': True}


def clear_session_vars(context, *args):
    """
    Helper function to clear session variables
    """
    session = context['cs_session_data']
    for i in args:
        try:
            del session[i]
        except:
            pass


def check_password(context, provided, uname, iterations=500000):
    """
    Compare the provided password against a stored hash.
    """
    logging = context['csm_cslog']
    user_login_info = logging.most_recent('_logininfo', [], uname, {})
    pass_hash = user_login_info.get('password_hash', None)
    if pass_hash is not None:
        if context['csm_cslog'].ENCRYPT_KEY is not None:
            pass_hash = context['csm_cslog'].FERNET.decrypt(pass_hash)
        salt = user_login_info.get('password_salt', None)
        hashed_pass = compute_password_hash(context,
          provided, salt, iterations, encrypt=False)
        return hashed_pass == pass_hash
    return False


def get_new_password_salt(length=128):
    """
    Generate a new salt of length length.  Tries to use os.urandom, and
    falls back on random if that doesn't work for some reason.
    """
    try:
        out = os.urandom(length)
    except:
        out = ''.join((chr(random.randint(1, 127)) for i in range(length))).encode()
    else:
        return out


def _ensure_bytes(x):
    try:
        return x.encode()
    except:
        return x


def compute_password_hash(context, password, salt=None, iterations=500000, encrypt=True):
    """
    Given a password, and (optionally) an associated salt, return a hash value.
    """
    hash_ = hashlib.pbkdf2_hmac('sha512', _ensure_bytes(password), _ensure_bytes(salt), iterations)
    if encrypt:
        if context['csm_cslog'].ENCRYPT_KEY is not None:
            hash_ = context['csm_cslog'].FERNET.encrypt(hash_)
    return hash_


def generate_confirmation_token(n=20):
    chars = string.ascii_uppercase + string.digits
    return ''.join((random.choice(chars) for i in range(n)))


def _get_base_url(context):
    return '/'.join([context['cs_url_root']] + context['cs_path_info'])


def generate_forgot_password_form(context):
    """
    Generate a "forgot password" form.
    """
    base = _get_base_url(context)
    req_url = base + '?loginaction=forgot_password'
    out = INCLUDE_HASHLIB
    out += '<form method="POST" action="%s">' % req_url
    msg = context['cs_session_data'].get('login_message', None)
    if msg is not None:
        out += '\n%s<p>' % msg
    last = context['cs_session_data'].get('last_form', {})
    last_uname = last.get('uname', '').replace('"', '&quot;')
    last_email = last.get('email', '').replace('"', '&quot;')
    out += '\n<table>\n<tr>\n<td style="text-align:right;">Username:</td>\n<td style="text-align:right;">\n<input type="text" name="uname" id="uname" value="%s"/>\n</td>\n</tr>' % last_uname
    out += '\n<tr>\n<td style="text-align:right;">Email Address:</td>\n<td style="text-align:right;">\n<input type="text" name="email" id="email" value="%s" />\n</td>\n</tr>' % last_email
    out += '\n<tr>\n<td style="text-align:right;"></td>\n<td style="text-align:right;">\n<input type="submit" value="Reset Password" class="btn btn-catsoop"></td>\n</tr>'
    out += '\n</table>\n</form>'
    return out


def generate_password_reset_form(context):
    """
    Generate a "reset password" form.
    """
    base = _get_base_url(context)
    req_url = base + '?loginaction=reset_password'
    req_url += '&username=%s' % context['cs_form']['username']
    req_url += '&token=%s' % context['cs_form']['token']
    out = INCLUDE_HASHLIB
    out += '<form method="POST" action="%s" id="pwdform">' % req_url
    msg = context['cs_session_data'].get('login_message', None)
    if msg is not None:
        out += '\n%s<p>' % msg
    safe_uname = context['cs_form']['username'].replace('"', '&quot;')
    out += '\n<input type="hidden" name="uname" id="uname" value="%s" />' % safe_uname
    out += '\n<table>'
    out += '\n<tr>\n<td style="text-align:right;">New Password:</td>\n<td style="text-align:right;">\n<input type="password" name="passwd" id="passwd" />\n</td>\n</tr>'
    out += '\n<tr>\n<td style="text-align:right;">Confirm New Password:</td>\n<td style="text-align:right;">\n<input type="password" name="passwd2" id="passwd2" />\n</td>\n<td><span id="pwd_check"></span></td>\n</tr>'
    out += '\n<tr>\n<td style="text-align:right;"></td>\n<td style="text-align:right;">'
    out += _submit_button([
     'passwd', 'passwd2'], 'uname', [], 'pwdform', 'Change Password')
    out += '</td>\n</tr>'
    out += '\n</table>\n</form>'
    out += CHANGE_PASSWORD_FORM_CHECKER
    return out


def generate_password_change_form(context):
    """
    Generate a "change password" form.
    """
    base = _get_base_url(context)
    req_url = base + '?loginaction=change_password'
    out = INCLUDE_HASHLIB
    out += '<form method="POST" action="%s" id="pwdform">' % req_url
    msg = context['cs_session_data'].get('login_message', None)
    if msg is not None:
        out += '\n%s<p>' % msg
    safe_uname = context['cs_session_data']['username'].replace('"', '&quot;')
    out += '\n<input type="hidden" name="uname" id="uname" value="%s" />' % safe_uname
    out += '\n<table>'
    out += '\n<tr>\n<td style="text-align:right;">Current Password:</td>\n<td style="text-align:right;">\n<input type="password" name="oldpasswd" id="oldpasswd" />\n</td>\n</tr>'
    out += '\n<tr>\n<td style="text-align:right;">New Password:</td>\n<td style="text-align:right;">\n<input type="password" name="passwd" id="passwd" />\n</td>\n</tr>'
    out += '\n<tr>\n<td style="text-align:right;">Confirm New Password:</td>\n<td style="text-align:right;">\n<input type="password" name="passwd2" id="passwd2" />\n</td>\n<td><span id="pwd_check"></span></td>\n</tr>'
    out += '\n<tr>\n<td style="text-align:right;"></td>\n<td style="text-align:right;">'
    out += _submit_button([
     'passwd', 'passwd2', 'oldpasswd'], 'uname', [], 'pwdform', 'Change Password')
    out += '</td>\n</tr>'
    out += '\n</table>\n</form>'
    out += CHANGE_PASSWORD_FORM_CHECKER
    return out


def generate_login_form(context):
    """
    Generate a login form.
    """
    base = _get_base_url(context)
    out = INCLUDE_HASHLIB
    out += '<form method="POST" id="loginform" action="%s">' % (base + '?loginaction=login')
    msg = context['cs_session_data'].get('login_message', None)
    last_uname = context['cs_session_data'].get('last_form', {}).get('login_uname', '')
    if msg is not None:
        out += '\n%s<p>' % msg
    last_uname = last_uname.replace('"', '&quot;')
    out += '\n<table>\n<tr>\n<td style="text-align:right;">Username:</td>\n<td style="text-align:right;">\n<input type="text" name="login_uname" id="login_uname" value="%s"/>\n</td>\n</tr>\n<tr>\n<td style="text-align:right;">Password:</td>\n<td style="text-align:right;">\n<input type="password" name="login_passwd" id="login_passwd" />\n</td>\n</tr>\n<tr>\n<td style="text-align:right;"></td>\n<td style="text-align:right;">' % last_uname
    out += _submit_button([
     'login_passwd'], 'login_uname', ['login_uname'], 'loginform', 'Log In')
    out += '<td>\n</tr>\n</table>'
    out += '<p>'
    if context['csm_mail'].can_send_email(context):
        base = _get_base_url(context)
        loc = base + '?loginaction=forgot_password'
        out += '\nForgot your password?  Click <a href="%s">here</a>.<br/>' % loc
    if context.get('cs_allow_registration', True):
        loc = _get_base_url(context)
        loc += '?loginaction=register'
        link = '<a href="%s">create one</a>' % loc
        out += '\nIf you do not already have an account, please %s.' % link
    out += '</p>'
    return out + '</form>'


def generate_registration_form(context):
    """
    Generate a registration form.
    """
    base = _get_base_url(context)
    qstring = '?loginaction=register'
    out = INCLUDE_HASHLIB
    out += '<form method="POST" action="%s" id="regform">' % (base + qstring)
    last = context['cs_session_data'].get('last_form', {})
    msg = context['cs_session_data'].get('login_message', None)
    if msg is not None:
        out += '\n%s<p>' % msg
    last_name = last.get('name', '').replace('"', '&quot;')
    last_uname = last.get('uname', '').replace('"', '&quot;')
    last_email = last.get('email', '').replace('"', '&quot;')
    last_email2 = last.get('email2', '').replace('"', '&quot;')
    out += '\n<table>\n<tr>\n<td style="text-align:right;">Username:</td>\n<td style="text-align:right;">\n<input type="text" name="uname" id="uname" value="%s"/>\n</td>\n<td><span id="uname_check"></span></td>\n</tr>' % last_uname
    out += '\n<tr>\n<td style="text-align:right;">Email Address:</td>\n<td style="text-align:right;">\n<input type="text" name="email" id="email" value="%s" />\n</td>\n</tr>' % last_email
    out += '\n<tr>\n<td style="text-align:right;">Confirm Email Address:</td>\n<td style="text-align:right;">\n<input type="text" name="email2" id="email2" value="%s"/>\n</td>\n<td><span id="email_check"></span></td>\n</tr>' % last_email2
    out += '\n<tr>\n<td style="text-align:right;">Password:</td>\n<td style="text-align:right;">\n<input type="password" name="passwd" id="passwd" />\n</td>\n</tr>'
    out += '\n<tr>\n<td style="text-align:right;">Confirm Password:</td>\n<td style="text-align:right;">\n<input type="password" name="passwd2" id="passwd2" />\n</td>\n<td><span id="pwd_check"></span></td>\n</tr>'
    out += '\n<tr>\n<td style="text-align:right;">Name (Optional):</td>\n<td style="text-align:right;">\n<input type="text" name="name" id="name" value="%s"/>\n</td>\n</tr>' % last_name
    out += '\n<tr>\n<td style="text-align:right;"></td>\n<td style="text-align:right;">'
    out += _submit_button([
     'passwd', 'passwd2'], 'uname', [
     'uname', 'email', 'email2', 'name'], 'regform', 'Register')
    out += '\n</td>\n</tr>'
    out += REGISTRATION_FORM_CHECKER
    return out + '</table></form>'


def _run_validators(validators, x):
    for extra_validator_regexp, error_msg in validators:
        if not re.match(extra_validator_regexp, x):
            return error_msg


_pwd_too_short_msg = 'Passwords must be at least 8 characters long.'
_validate_password_javascript = '\nfunction _validate_password(p){\n    if (p.length < 8){\n        return %r;\n    }\n    return null;\n}\n' % _pwd_too_short_msg
_re_valid_email_string = '^[A-Za-z0-9._%+-]{1,64}@(?:[A-Za-z0-9-]{1,63}\\.){1,125}[A-Za-z]{2,63}$'
RE_VALID_EMAIL = re.compile(_re_valid_email_string)
_eml_too_long_msg = 'E-mail addresses must be less than 255 characters long.'
_eml_invalid_msg = 'Please make sure you have entered a valid e-mail address.'
_validate_email_javascript = '\nvar _re_valid_email = /%s/;\nfunction _validate_email(e){\n    if (e.length > 254) {\n        return %r;\n    } else if (!_re_valid_email.test(e)){\n        return %r;\n    }\n    return null;\n}\n' % (
 _re_valid_email_string,
 _eml_too_long_msg,
 _eml_invalid_msg)

def _validate_email(context, e):
    if len(e) > 254:
        return _eml_too_long_msg
    else:
        return RE_VALID_EMAIL.match(e) or _eml_invalid_msg
    return _run_validators(context.get('cs_extra_email_validators', []), e)


_re_valid_username_string = '^[A-Za-z0-9][A-Za-z0-9_.-]*$'
RE_VALID_USERNAME = re.compile(_re_valid_username_string)
_uname_too_short_msg = 'Usernames must contain at least one character.'
_uname_wrong_start_msg = 'Usernames must begin with an ASCII letter or number.'
_uname_invalid_msg = 'Usernames must contain only letters and numbers, dashes (-), underscores (_), and periods (.).'
_validate_username_javascript = '\nvar _re_valid_uname = /%s/;\nfunction _validate_username(u){\n    if (u.length < 1){\n        return %r;\n    } else if (!_re_valid_uname.test(u)){\n        if (!_re_valid_uname.test(u.charAt(0))){\n            return %r;\n        }else{\n            return %r;\n        }\n    }\n    return null;\n}\n' % (
 _re_valid_username_string,
 _uname_too_short_msg,
 _uname_wrong_start_msg,
 _uname_invalid_msg)

def _validate_username(context, u):
    if len(u) < 1:
        return _uname_too_short_msg
    else:
        return RE_VALID_USERNAME.match(u) or RE_VALID_USERNAME.match(u[0]) or _uname_wrong_start_msg
        return _uname_invalid_msg
    return _run_validators(context.get('cs_extra_username_validators', []), u)


REGISTRATION_FORM_CHECKER = '<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\n%s\n%s\n%s\nfunction check_form(){\n    var e_msg = "";\n    var u_msg = "";\n    var p_msg = "";\n\n    // validate email\n    var e_val = document.getElementById("email").value;\n    if(e_val.length == 0){\n        e_msg = "Please enter an email address.";\n    }else if(e_val != document.getElementById("email2").value){\n        e_msg = "E-mail addresses do not match.";\n    }else{\n        var e_check_result = _validate_email(e_val);\n        if (e_check_result !== null){\n            e_msg = e_check_result;\n        }\n    }\n    document.getElementById("email_check").innerHTML = \'<font color="red">\' + e_msg + \'</font>\';\n\n    // validate username\n    var u_val = document.getElementById("uname").value;\n    if(u_val.length == 0){\n        u_msg = "Please enter a username.";\n    }else{\n        var u_check_result = _validate_username(u_val);\n        if (u_check_result !== null){\n            u_msg = u_check_result;\n        }\n    }\n    document.getElementById("uname_check").innerHTML = \'<font color="red">\' + u_msg + \'</font>\';\n\n    // validate password\n    var p_val = document.getElementById("passwd").value;\n    if(p_val != document.getElementById("passwd2").value){\n        p_msg = "Passwords do not match.";\n    }else{\n        var p_check_result = _validate_password(p_val);\n        if (p_check_result !== null){\n            p_msg = p_check_result;\n        }\n    }\n    document.getElementById("pwd_check").innerHTML = \'<font color="red">\' + p_msg + \'</font>\';\n    document.getElementById(\'regform_submitter\').disabled = !!(e_msg || u_msg || p_msg);\n}\ndocument.addEventListener(\'DOMContentLoaded\', check_form);\ndocument.getElementById("regform").addEventListener(\'keyup\', check_form);\n// @license-end\n</script>' % (
 _validate_email_javascript,
 _validate_username_javascript,
 _validate_password_javascript)
CHANGE_PASSWORD_FORM_CHECKER = '<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\n%s\nfunction check_form(){\n    var p_msg = "";\n\n    // validate password\n    var p_val = document.getElementById("passwd").value;\n    if(p_val != document.getElementById("passwd2").value){\n        p_msg = "Passwords do not match.";\n    }else{\n        var p_check_result = _validate_password(p_val);\n        if (p_check_result !== null){\n            p_msg = p_check_result;\n        }\n    }\n    document.getElementById("pwd_check").innerHTML = \'<font color="red">\' + p_msg + \'</font>\';\n    document.getElementById(\'pwdform_submitter\').disabled = !!p_msg;\n}\ndocument.addEventListener(\'DOMContentLoaded\', check_form);\ndocument.getElementById("pwdform").addEventListener(\'keyup\', check_form);\n// @license-end\n</script>' % _validate_password_javascript

def reg_confirm_emails(context, username, confirmation_code):
    """
    @param context: The context associated with this request
    @param username: The username of the user who needs to confirm
    @param confirmation_code: The user's confirmation token (from
    L{generate_confirmation_token})
    @return: A 2-tuple representing the message to be sent.  The first element
    is the plain-text version of the e-mail, and the second is the HTML
    version.
    """
    base = _get_base_url(context)
    u = '%s?loginaction=confirm_reg&username=%s&token=%s' % (
     base,
     username,
     confirmation_code)
    url_root = context['cs_url_root']
    return (
     _reg_confirm_msg_base_plain % (username, url_root, u),
     _reg_confirm_msg_base_html % (username, url_root, u, u))


_reg_confirm_msg_base_plain = 'You recently signed up for an account with username %s at the CAT-SOOP instance at %s.\n\nIn order to confirm your account, please visit the following URL:\n%s\n\nIf you did not sign up for this account, or if you otherwise feel that you\nare receiving this message in error, please ignore or delete it.'
_reg_confirm_msg_base_html = '<p>You recently signed up for an account with username <tt>%s</tt> at the CAT-SOOP instance at <tt>%s</tt>.</p>\n\n<p>In order to confirm your account, please click on the following link:<br/>\n<a href="%s">%s</a></p>\n\n<p>If you did not sign up for this account, or if you otherwise feel that you\nare receiving this message in error, please ignore or delete it.</p>'

def passwd_confirm_emails(context, username, code):
    """
    @param context: The context associated with this request
    @param username: The username of the user who needs to confirm
    @param confirmation: The user's confirmation token (from
    L{generate_confirmation_token})
    @return: A 2-tuple representing the message to be sent.  The first element
    is the plain-text version of the e-mail, and the second is the HTML
    version.
    """
    base = _get_base_url(context)
    u = '%s?loginaction=reset_password&username=%s&token=%s' % (base, username, code)
    url_root = context['cs_url_root']
    return (
     _passwd_confirm_msg_base_plain % (username, url_root, u),
     _passwd_confirm_msg_base_html % (username, url_root, u, u))


_passwd_confirm_msg_base_plain = 'You recently submitted a request to reset the password for an account with username %s at the CAT-SOOP instance at %s.\n\nIn order to reset your password, please visit the following URL:\n%s\n\nIf you did not submit this request, or if you otherwise feel that you\nare receiving this message in error, please ignore or delete it.'
_passwd_confirm_msg_base_html = '<p>You recently submitted a request to reset the password for an account with username <tt>%s</tt> at the CAT-SOOP instance at <tt>%s</tt>.</p>\n\n<p>In order to reset your password, please click on the following link:<br/>\n<a href="%s">%s</a></p>\n\n<p>If you did not submit this request, or if you otherwise feel that you\nare receiving this message in error, please ignore or delete it.</p>'

def _submit_button(fields, username, preserve, form, value='Submit'):
    base = '<input type="button" class="btn btn-catsoop" id="%s_submitter" value="%s" onclick="catsoop.hashlib.hash_passwords(%r, %r, %r, %r)" />'
    base += '<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ndocument.querySelectorAll("#%s input").forEach(function(a){\n    a.addEventListener("keypress",function(e){\n        if(e.which == 13) document.getElementById("%s_submitter").click();\n    });\n});\n// @license-end\n</script>'
    return base % (form, value, fields, username, preserve, form, form, form)


LOGIN_BOX = '\n<div class="response" id="catsoop_login_box">\n<b><center>You are not logged in.</center></b><br/>\nIf you are a current student, please <a href="%s?loginaction=login">Log In</a> for full access to this page.\n</div>\n'
INCLUDE_HASHLIB = '\n<script type="text/javascript" src="_auth/login/cs_hash.js"></script>\n'
# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break (2)
#      0.  L. 310      1772  POP_TOP          
#      1.          1774_1776  BREAK_LOOP         1782  'to 1782'