# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/auto_add.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.extensions.hooks import SignalHook
from reviewboard.reviews.models import Group

class AutoAddMode(object):
    DISABLED = b'disabled'
    ALL_NEW = b'all-new'
    GROUPS = b'groups'
    CHOICES = (
     (
      DISABLED, _(b'Disabled')),
     (
      ALL_NEW, _(b'All new users')),
     (
      GROUPS, _(b'Users who join groups:')))


def _add_licensed_users(extension, users):
    """Adds a list of users to the license.

    This will attempt to add the users to the license, trimming away any
    provided users that exceed the license's user cap.

    If that cap is hit or exceeded, the administrators will be e-mailed,
    notifying them that the license cap has been hit and listing all users
    who weren't able to be added to the cap.
    """
    license = extension.license
    if not license:
        return
    license_settings = extension.license_settings
    extra_users = []
    hit_limit = False
    users = [ user for user in users if not license_settings.is_user_licensed(user)
            ]
    if extension.license.has_user_cap:
        remaining = license_settings.licensed_users_remaining
        if len(users) >= remaining:
            extra_users = users[remaining:]
            users = users[:remaining]
            hit_limit = True
    if users:
        extension.license_settings.add_licensed_users(users)
    if hit_limit:
        assert license.product
        siteconfig = SiteConfiguration.objects.get_current()
        body = render_to_string(b'beanbag_licensing/license_limit_email.txt', {b'product_name': license.product, 
           b'max_users': license.num_users, 
           b'extra_users': extra_users})
        send_mail(b'%s license limit reached' % license.product, body, siteconfig.get(b'mail_default_from'), [
         siteconfig.get(b'site_admin_email')], fail_silently=True)


def _on_user_saved(instance, created, extension, **kwargs):
    """Handler for when a User object is saved.

    If the User is new, and we're auto-adding all new users, then we'll
    attempt to add the user to the license.

    If the User is inactive, it'll be removed from the license.

    Args:
        instance (django.contrib.auth.models.User):
            The user instance being saved.

        created (bool):
            Whether this is a newly-created user.

        extension (beanbag_licensing.extensions.LicensedExtension):
            The extension instance.

        **kwargs (dict, unused):
            Additional keyword arguments passed to the signal handler.
    """
    if created and instance.is_active and extension.settings[b'auto_add_mode'] == AutoAddMode.ALL_NEW:
        _add_licensed_users(extension, [instance])
    elif not created and not instance.is_active:
        extension.license_settings.remove_licensed_users([instance.pk])


def _on_user_deleted(instance, extension, **kwargs):
    """Handler for when a User is deleted.

    This will remove the user from the license, if they're currently in
    the license.

    Args:
        instance (django.contrib.auth.models.User):
            The user instance being deleted.

        extension (beanbag_licensing.extensions.LicensedExtension):
            The extension instance.

        **kwargs (dict, unused):
            Additional keyword arguments passed to the signal handler.
    """
    extension.license_settings.remove_licensed_users([instance.pk])


def _on_group_m2m_changed(instance, extension, action, pk_set, reverse, **kwargs):
    """Handler for when one or more users are added to a Group.

    If we're auto-adding users to this group, then we'll attempt to add as
    many users as allowed to the license.
    """
    if not reverse and action == b'post_add' and extension.settings[b'auto_add_mode'] == AutoAddMode.GROUPS and instance.pk in extension.settings[b'auto_add_groups']:
        _add_licensed_users(extension, User.objects.filter(id__in=pk_set))


def setup_auto_add_remove(extension):
    """Sets up auto-add/remove support for users.

    This will set up hooks to listen for new users on the system or within
    a group. Depending on the setting, these users may be added to the
    license.

    It will also listen for deleted users or users made inactive, and will
    remove them from the license.

    Args:
        extension (beanbag_licensing.extensions.LicensedExtension):
            The extension instance.
    """
    SignalHook(extension, post_save, _on_user_saved, sender=User)
    SignalHook(extension, pre_delete, _on_user_deleted, sender=User)
    SignalHook(extension, m2m_changed, _on_group_m2m_changed, sender=Group.users.through)