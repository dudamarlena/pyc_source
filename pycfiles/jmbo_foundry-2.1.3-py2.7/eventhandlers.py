# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/eventhandlers.py
# Compiled at: 2015-01-27 08:59:34
from urllib import urlretrieve
import dateutil.parser
from django.core.files import File
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from social_auth.backends.google import GoogleOAuth2Backend

def facebook_extra_values(sender, user, response, details, **kwargs):
    mapping = {'email': 'email', 
       'first_name': 'first_name', 
       'last_name': 'last_name', 
       'bio': 'about_me', 
       'gender': 'gender', 
       'birthday': 'dob'}
    for key, fieldname in mapping.items():
        value = details.get(key, None)
        if key == 'gender':
            if value:
                value = value[0]
        elif key == 'birthday':
            if value:
                try:
                    value = dateutil.parser.parse(value)
                except ValueError:
                    pass

        if value:
            setattr(user, fieldname, value)

    username = details['username']
    url = 'http://graph.facebook.com/%s/picture' % username
    tempfile = urlretrieve(url)
    user.image.save('%s.jpg' % username, File(open(tempfile[0])))
    return True


pre_update.connect(facebook_extra_values, sender=FacebookBackend)

def twitter_extra_values(sender, user, response, details, **kwargs):
    username = details['username']
    url = 'https://api.twitter.com/1/users/profile_image/%s?size=bigger' % username
    tempfile = urlretrieve(url)
    user.image.save('%s.jpg' % username, File(open(tempfile[0])))
    return True


pre_update.connect(twitter_extra_values, sender=TwitterBackend)

def google_extra_values(sender, user, response, details, **kwargs):
    mapping = {'email': 'email', 
       'given_name': 'first_name', 
       'family_name': 'last_name', 
       'gender': 'gender'}
    for key, fieldname in mapping.items():
        value = details.get(key, None)
        if key == 'gender':
            if value:
                value = value[0]
        if value:
            setattr(user, fieldname, value)

    url = details.get('picture', None)
    if url:
        tempfile = urlretrieve(url)
        user.image.save('%s.jpg' % username, File(open(tempfile[0])))
    return True


pre_update.connect(google_extra_values, sender=GoogleOAuth2Backend)