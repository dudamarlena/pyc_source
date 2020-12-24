# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/yellowencom/dauth/backends.py
# Compiled at: 2012-06-29 07:21:55
import pickle, json, hashlib
from urllib import urlencode
import urllib2
from django.conf import settings
from django.contrib.auth.models import User, check_password

class DaarmaanBackend(object):
    """
    Authenticate against the Daarmaan gauth.
    """
    service = settings.SERVICE_NAME
    key = settings.SERVICE_KEY
    daarmaan = settings.DAARMAAN_SERVER

    def authenticate(self, **kwargs):
        """
        Try to authenticate to daarmaan SSO using provided informations.
        kwargs dictionary should contains below keys:

        token: Actual ticket from daarmaan
        request: current request object
        hash_: the SHA1 checksum provided by daarmaan.
        """
        token = kwargs.get('token', None)
        request = kwargs.get('request', None)
        hash_ = kwargs.get('hash_', None)
        if not token or not hash_ or not request:
            raise ValueError("You should provide 'request', 'token' and 'hash_' parameters")
        if self.is_valid(token, hash_):
            data = self.validate(token)
            user, created = User.objects.get_or_create(username=data['username'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            if created:
                user.pk = data['id']
                user.save()
            return user
        return
        return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return

        return

    def is_valid(self, token, hash_):
        """
        Check for token and hash integrity.
        """
        key = settings.SERVICE_KEY
        m = hashlib.sha1()
        m.update(token + key)
        if hash_ == m.hexdigest():
            return True
        return False

    def validate(self, token):
        """
        Try to validate the given token for a valid user.
        """
        url = '%s/verification/' % self.daarmaan.lstrip('/')
        m = hashlib.sha1()
        m.update(token + self.key)
        hash_ = m.hexdigest()
        params = {'token': token, 'hash': hash_, 
           'service': self.service}
        url = '%s?%s' % (url, urlencode(params))
        response = urllib2.urlopen(url)
        if response.code == 200:
            json_data = json.loads(response.read())
            if json_data['hash']:
                hash_ = json_data['hash']
                data = json_data['data']
                m = hashlib.sha1()
                m.update(data['username'] + self.key)
                if m.hexdigest() == hash_:
                    return data
                return False
            else:
                return False