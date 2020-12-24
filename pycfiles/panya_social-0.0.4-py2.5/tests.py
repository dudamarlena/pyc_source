# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/social/tests.py
# Compiled at: 2010-09-19 02:55:46
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from post.models import Post
from social import models
from social.models import SocialObjectPermission
from friends.models import Friendship

class SocialObjectPermissionBackendTestCase(TestCase):
    fixtures = [
     'users.json']

    def setUp(self):
        self.backend_str = 'social.backends.SocialObjectPermissionBackend'
        if self.backend_str not in settings.AUTHENTICATION_BACKENDS:
            settings.AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS + (self.backend_str,)
        self.target_user = User.objects.create(username='target_user')
        self.intermediate_user = User.objects.create(username='intermediate_user')
        self.requesting_user = User.objects.create(username='requesting_user')
        self.post = Post.objects.create(title='Post Title', owner=self.target_user)
        self.post.target_user = self.target_user

    def test_has_perm(self):
        SocialObjectPermission.objects.all().delete()
        settings.DEFAULT_SOCIAL_PERMISSION_GROUP = 0
        self.requesting_user.has_perm(perm='view', obj=self.post)
        self.failIf(self.requesting_user.has_perm(perm='view', obj=self.post))
        settings.DEFAULT_SOCIAL_PERMISSION_GROUP = 3
        self.failUnless(self.requesting_user.has_perm(perm='view', obj=self.post))
        settings.DEFAULT_SOCIAL_PERMISSION_GROUP = 1
        direct_friendship = Friendship(to_user=self.requesting_user, from_user=self.target_user)
        direct_friendship.save()
        self.failUnless(self.requesting_user.has_perm(perm='view', obj=self.post))
        direct_friendship.delete()
        settings.DEFAULT_SOCIAL_PERMISSION_GROUP = 2
        Friendship(to_user=self.intermediate_user, from_user=self.target_user).save()
        indirect_friendship = Friendship(to_user=self.requesting_user, from_user=self.intermediate_user)
        indirect_friendship.save()
        self.failUnless(self.requesting_user.has_perm(perm='view', obj=self.post))
        indirect_friendship.delete()
        del settings.DEFAULT_SOCIAL_PERMISSION_GROUP
        SocialObjectPermission.objects.all().delete()
        self.failUnlessRaises(ImproperlyConfigured, self.requesting_user.has_perm, perm='view', obj=self.post)
        nobody_perm = SocialObjectPermission(user=self.target_user, can_view=True, social_group=0, content_type=ContentType.objects.get_for_model(self.post))
        nobody_perm.save()
        self.failIf(self.requesting_user.has_perm(perm='view', obj=self.post))
        nobody_perm.delete()
        everyone_perm = SocialObjectPermission(user=self.target_user, can_view=True, social_group=3, content_type=ContentType.objects.get_for_model(self.post))
        everyone_perm.save()
        self.failUnless(self.requesting_user.has_perm(perm='view', obj=self.post))
        everyone_perm.delete()
        nobody_perm = SocialObjectPermission(user=self.target_user, can_view=True, social_group=0, content_type=ContentType.objects.get_for_model(self.post))
        nobody_perm.save()
        everyone_perm = SocialObjectPermission(user=self.target_user, can_view=True, social_group=3, content_type=ContentType.objects.get_for_model(self.post))
        everyone_perm.save()
        self.failIf(self.requesting_user.has_perm(perm='view', obj=self.post))

    def test_is_member_everyone(self):
        self.failUnless(models.is_member_everyone(self.target_user, self.requesting_user))

    def test_is_member_nobody(self):
        self.failIf(models.is_member_nobody(self.target_user, self.requesting_user))

    def test_is_member_friends(self):
        self.failIf(models.is_member_friends(self.target_user, self.requesting_user))
        Friendship(to_user=self.requesting_user, from_user=self.target_user).save()
        self.failUnless(models.is_member_friends(self.target_user, self.requesting_user))

    def test_is_member_friends_of_friends(self):
        direct_friendship = Friendship(to_user=self.requesting_user, from_user=self.target_user)
        direct_friendship.save()
        self.failUnless(models.is_member_friends_of_friends(self.target_user, self.requesting_user))
        direct_friendship.delete()
        Friendship(to_user=self.intermediate_user, from_user=self.target_user).save()
        indirect_friendship = Friendship(to_user=self.requesting_user, from_user=self.intermediate_user)
        indirect_friendship.save()
        self.failUnless(models.is_member_friends_of_friends(self.target_user, self.requesting_user))
        indirect_friendship.delete()
        self.failIf(models.is_member_friends_of_friends(self.target_user, self.requesting_user))