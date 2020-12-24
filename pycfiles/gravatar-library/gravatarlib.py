# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Documents and Settings/Damjan/Desktop/GRavatar\GRavatarLib.py
# Compiled at: 2011-01-28 00:54:15
"""
    GRavatar Library - Python
    http://en.gravatar.com/
    This module will help you to communicate with the web services from the GRavatar!
    The module will allows you to get the avatars and profile information from GRavatar.
    FeedBack: krstevsky[at]gmail[dot]com

    Usage:
    import GRavatarLib
    try:
        grav = GRavatarLib.GRavatar()
        avatar = grav.avatar(email)
        profil = grav.profile(user) # or email
    except Exception as ex:
        print str( ex )

    Exceptions:
        GRavatarException()
"""
__all__ = [
 'avatar', 'profile', 'data']
__version__ = '1.0.0'
import re, sys, hashlib
try:
    if sys.version[0] == '2':
        import urllib2, urllib
    else:
        import urllib.request as urllib2
except:
    raise ImportError('Some modules can not be imported!')

class GRavatarException(Exception):
    """ Class GRavatarException. Exception Message """
    pass


class GRavatar(object):
    """ Class GRavatar """

    def __init__(self):
        """ Class Constructor """
        self.data = None
        return

    def __del__(self):
        """ Class Destructor """
        self.data = None
        return

    def __set_data(self, data):
        """ Set the data value """
        self.__data = data

    def data(self):
        """ Get the data value """
        return self.__data

    def __set_error(error):
        """ Set the exception message """
        raise GRavatarException(error)

    def __get_opener(self, ua='GRavatar Agent - Python'):
        """ Get the opener """
        opener = None
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', ua)]
        except Exception as ex:
            raise GRavatarException(str(ex))

        return opener

    def __read(self, url=None):
        """ Read the data from URL """
        if not url:
            raise GRavatarException('URL must have a value!')
        try:
            req = self.__get_opener()
            tdata = req.open(url).read()
            req.close()
            self.__set_data(tdata)
            return tdata
        except Exception as ex:
            raise GRavatarException(str(ex))

    def __is_email(self, email, minlen=7, maxlen=45):
        """ E-Mail Validation """
        _len = len(email)
        if _len > minlen and _len < maxlen:
            regex = '^(\\[?)[a-zA-Z0-9\\-\\.\\_]+\\@(\\[?)[a-zA-Z0-9\\-]+\\.([a-zA-Z]{2,4})(\\]?)$'
            if re.match(regex, email) != None:
                return True
        return False

    def avatar(self, email=None, size=40, default='http://www.example.com/default.jpg'):
        """ Get the user's avatar from the gravatar """
        if not email:
            raise GRavatarException('User must have a value!')
        try:
            if self.__is_email(email) == False:
                raise GRavatarException('Invalid E-Mail address!')
            gurl = 'http://www.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest() + '?'
            gurl += urllib.urlencode({'d': default, 's': str(size)})
            self.__set_data(gurl)
            return gurl
        except Exception as ex:
            raise GRavatarException(str(ex))

    def profile(self, user=None):
        """ Get the user's profile from the gravatar (XML Format)"""
        if not user:
            raise GRavatarException('User must have a value!')
        try:
            gurl = None
            if self.__is_email(user) == True:
                gurl = 'http://www.gravatar.com/' + hashlib.md5(user.lower()).hexdigest() + '.xml'
                return self.__read(gurl)
            gurl = 'http://www.gravatar.com/' + user.lower().strip() + '.xml'
            return self.__read(gurl)
        except Exception as ex:
            raise GRavatarException(str(ex))

        return