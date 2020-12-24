# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modify_history/backends/base.py
# Compiled at: 2011-06-10 23:28:22
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
USER_ATTRS = settings.HISTORY_USER_ATTRS

class BaseHistoryBackend(object):
    """
    Generic backend for history application
    """

    def setUp(self, model):
        pass

    def tearDown(self, model):
        pass

    def get_user(self, timeline):
        """
        get user name from auth.user object with permalink
        """
        if timeline.user and timeline.user.is_authenticated():
            if hasattr(timeline.user, 'get_profile'):
                profile = timeline.user.get_profile()
                if hasattr(profile, 'get_absolute_url'):
                    href = profile.get_absolute_url()
                else:
                    href = ''
                kwargs = {'href': href, 'title': timeline.user.get_profile().__unicode__(), 
                   'label': timeline.user.get_profile().__unicode__()}
            else:
                if hasattr(timeline.user, 'get_absolute_url'):
                    href = timeline.user.get_absolute_url()
                else:
                    href = ''
                kwargs = {'href': href, 'title': timeline.user.__unicode__(), 
                   'label': timeline.user.__unicode__()}
            return mark_safe('<a href="%(href)s" title="%(title)s">%(label)s</a>' % kwargs)
        else:
            return _('Anonymous User')

    def get_label(self, timeline):
        kwargs = {'href': timeline.url, 
           'label': timeline.label}
        return mark_safe('<a href="%(href)s">%(label)s</a>' % kwargs)

    def _get_url_from_instance(self, instance):
        if instance is None:
            return ''
        else:
            return instance.get_absolute_url()

    def _get_label_from_instance(self, instance):
        if instance is None:
            return ''
        else:
            return instance.__unicode__()

    def _get_user_from_instance(self, instance):
        if instance is None:
            return ''
        else:
            for attr in USER_ATTRS:
                user = getattr(instance, attr, None)
                if user:
                    break

            return user

    def get_message(self, timeline):
        """
        get message for timeline object from content_object with permalinks
        """
        kwargs = {'user': self.get_user(timeline), 
           'label': self.get_label(timeline)}
        if timeline.action == 'create':
            return mark_safe(_("%(user)s create '%(label)s'") % kwargs)
        if timeline.action == 'update':
            return mark_safe(_("%(user)s update '%(label)s'") % kwargs)
        return mark_safe(_("%(user)s delete '%(label)s'") % kwargs)

    def autodiscover(self, instance, action, url=None, label=None, user=None):
        raise NotImplementedError