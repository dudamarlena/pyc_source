# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/koansys/django/authradius.py
# Compiled at: 2009-02-25 14:26:20
from django.conf import settings
from django.contrib.auth.models import User
from StringIO import StringIO
import logging
DICTIONARY = '\nATTRIBUTE User-Name\t1 string\nATTRIBUTE User-Password\t2 string encrypt=1\n'

class AuthRadius(object):
    """
    Authenticate against a backend RADIUS server; return User object or None.
    RADIUS servers include the interface provided by RSA SecurID ACE server
    for one-time-password hardware-token authentication, but also common
    ones used by ISPs like FreeRADIUS.
    If we detect any error, return None so that sites without RADIUS
    or with bad configs fail gracefully, rather than preventing login.
    """

    def authenticate(self, username=None, password=None):
        """Check username against RADIUS server and return a User object or None.
        """
        try:
            import pyrad.packet
            from pyrad.client import Client, Timeout
            from pyrad.dictionary import Dictionary
        except ImportError, e:
            logging.error("RADIUS couldn't import pyrad, need to install the egg: %s", e)
            return
        else:
            username = username.encode('utf-8')
            password = password.encode('utf-8')
            try:
                client = Client(server=settings.RADIUS_SERVER, authport=settings.RADIUS_AUTHPORT, secret=settings.RADIUS_SECRET.encode('utf-8'), dict=Dictionary(StringIO(DICTIONARY)))
            except AttributeError, e:
                logging.error("RADIUS couldn't find settings (check [local_]settings.py): %s" % e)
                return

            req = client.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name=username)
            req['User-Password'] = req.PwCrypt(password)
            logging.debug('RADIUS authenticate sending packet req=%s' % req)
            try:
                reply = client.SendPacket(req)
            except Timeout, e:
                logging.error('RADIUS Timeout contacting RADIUS_SERVER=%s RADIUS_PORT=%s: %s' % (
                 settings.RADIUS_SERVER, settings.RADIUS_AUTHPORT, e))
                return
            except Exception, e:
                logging.error('RADIUS Unknown error sending to RADIUS_SERVER=%s RADIUS_PORT=%s: %s' % (
                 settings.RADIUS_SERVER, settings.RADIUS_AUTHPORT, e))
                return

        logging.debug('RADIUS Authenticate check reply.code=%s' % reply.code)
        if reply.code == pyrad.packet.AccessReject:
            logging.warning('RADIUS Reject username=%s', username)
            return
        else:
            if reply.code != pyrad.packet.AccessAccept:
                logging.error('RADIUS Unknown Code username=%s reply.code=%s' % (username, reply.code))
                return
            logging.info('RADIUS Accept username=%s' % username)
            try:
                logging.debug('RADIUS looking for existing DB username=%s' % username)
                user = User.objects.get(username=username)
                logging.info('RADIUS found existing DB user=%s' % user)
            except User.DoesNotExist:
                logging.info('RADIUS user username=%s did not exist, creating...' % username)
                user = User(username=username)
                user.set_unusable_password()
                logging.info('RADIUS created user username=%s' % username)
                user.save()

            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logging.warning('RADIUS get_user DoesNotExist user_id=%s' % user_id)
            return

        return