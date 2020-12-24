# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialauth/models.py
# Compiled at: 2010-07-01 06:52:01
from django.db import models
from django.contrib.auth.models import User

class AuthMeta(models.Model):
    """Metadata for Authentication"""

    def __unicode__(self):
        return '%s - %s' % (self.user, self.provider)

    user = models.ForeignKey(User)
    provider = models.CharField(max_length=200)
    is_email_filled = models.BooleanField(default=False)
    is_profile_modified = models.BooleanField(default=False)


class OpenidProfile(models.Model):
    """A class associating an User to a Openid"""
    openid_key = models.CharField(max_length=200, unique=True, db_index=True)
    user = models.ForeignKey(User, related_name='openid_profiles')
    is_username_valid = models.BooleanField(default=False)
    email = models.EmailField()
    nickname = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.openid_key)

    def __repr__(self):
        return unicode(self.openid_key)


class LinkedInUserProfile(models.Model):
    """
    For users who login via Linkedin.
    """
    linkedin_uid = models.CharField(max_length=50, unique=True, db_index=True)
    user = models.ForeignKey(User, related_name='linkedin_profiles')
    headline = models.CharField(max_length=120, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True, editable=False)

    def __unicode__(self):
        return "%s's profile" % self.user


class TwitterUserProfile(models.Model):
    """
    For users who login via Twitter.
    """
    screen_name = models.CharField(max_length=200, unique=True, db_index=True)
    user = models.ForeignKey(User, related_name='twitter_profiles')
    access_token = models.CharField(max_length=255, blank=True, null=True, editable=False)
    profile_image_url = models.URLField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return "%s's profile" % self.user


class FacebookUserProfile(models.Model):
    """
    For users who login via Facebook.
    """
    facebook_uid = models.CharField(max_length=20, unique=True, db_index=True)
    user = models.ForeignKey(User, related_name='facebook_profiles')
    profile_image_url = models.URLField(blank=True, null=True)
    profile_image_url_big = models.URLField(blank=True, null=True)
    profile_image_url_small = models.URLField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    about_me = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return "%s's profile" % self.user