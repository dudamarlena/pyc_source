# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoLogin.py
# Compiled at: 2014-06-19 10:55:27
import json
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.template import loader
from protoAuth import getUserProfile
from utilsWeb import JsonError, JsonSuccess
from django.utils.translation import gettext as _

def protoGetUserRights(request):
    """ return usr rights 
    """
    if request.method != 'POST':
        return JsonError('invalid message')
    else:
        userName = request.POST['login']
        userPwd = request.POST['password']
        errMsg = ''
        success = False
        language = None
        try:
            pUser = authenticate(username=userName, password=userPwd)
        except:
            pUser = None

        userInfo = {'userName': userName}
        if pUser is not None:
            if pUser.is_active:
                login(request, pUser)
                success = True
                userInfo['isStaff'] = pUser.is_staff
                userInfo['isSuperUser'] = pUser.is_superuser
                userInfo['fullName'] = pUser.get_full_name()
                language = getUserProfile(pUser, 'login', userName)
            else:
                errMsg = 'Cet utilisateur est desactiv&eacute;'
        else:
            errMsg = 'Mauvais utilisateur ou mot de passe'
        jsondict = {'success': success, 
           'message': errMsg, 
           'userInfo': userInfo, 
           'language': language}
        context = json.dumps(jsondict)
        return HttpResponse(context, content_type='application/json')


def protoGetPasswordRecovery(request):
    baseURI = request.build_absolute_uri('..')
    if request.POST.get('email') and request.POST.get('login'):
        try:
            u = User.objects.get(email=request.POST['email'], username=request.POST['login'])
            token = user_token(u)
            if settings.HOST_DOMAIN:
                baseURI = 'http://' + settings.HOST_DOMAIN + '/protoLib/'
            link = baseURI + 'resetpassword?a=%s&t=%s' % (u.pk, token)
            email_template_name = 'recovery/recovery_email.txt'
            body = loader.render_to_string(email_template_name).strip()
            message = _(body)
            message += ' %s\n\n%s : %s' % (link, _('Utilisateur'), request.POST['login'])
            message += ' \n\n%s' % _("Si vous ne voulez pas réinitialiser votre mot de passe, il suffit d'ignorer ce message et il va rester inchangé")
            u.email_user(_('Nouveau mot de passe'), message)
            return JsonSuccess()
        except:
            return JsonError(_('Utilisateur non trouvé'))

    return HttpResponseRedirect('/')


def resetpassword(request):
    link = '../protoExtReset'
    if request.GET.get('a') and request.GET.get('t'):
        user = User.objects.get(pk=request.GET['a'])
        token = user_token(user)
        if request.GET['t'] == token:
            newpass = User.objects.make_random_password(length=8)
            user.set_password(newpass)
            user.save()
            message = _('Votre mot de passe a été réinitialisé ') + ' : %s' % newpass
            message += ' \n\n%s : %s' % (_('Utilisateur'), user)
            user.email_user(_('Nouveau mot de passe'), message)
            response = HttpResponseRedirect(link)
            return response
    return HttpResponseRedirect(link)


def changepassword(request):
    if request.method != 'POST':
        return JsonError('invalid message')
    else:
        newpass1 = request.POST['newPassword1']
        newpass2 = request.POST['newPassword2']
        userName = request.POST['login']
        userPwd = request.POST['current']
        try:
            pUser = authenticate(username=userName, password=userPwd)
        except:
            pUser = None

        errMsg = 'Mauvais utilisateur ou mot de passe'
        if pUser is not None:
            if newpass1 == newpass2:
                user = User.objects.get(username=userName)
                user.set_password(newpass1)
                user.save()
                if user.email:
                    try:
                        message = _('Votre mot de passe a été réinitialisé ') + ' : %s' % newpass1
                        message += ' \n\n%s : %s' % (_('Utilisateur'), user)
                        user.email_user(_('Nouveau mot de passe'), message)
                    except:
                        pass

                return JsonSuccess()
            errMsg = 'Les mots de passe ne correspondent pas!'
        return JsonError(_(errMsg))


def user_token(user):
    import hashlib
    salt = settings.SECRET_KEY
    localHash = hashlib.md5(user.email + salt).hexdigest()
    return localHash


def protoLogout(request):
    logout(request)
    return JsonSuccess({'message': 'Ok'})