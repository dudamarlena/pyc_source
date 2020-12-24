# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/app_plugins/models.py
# Compiled at: 2008-10-17 15:50:05
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from library import get_library
import re
ENABLED = 0
DISABLED = 1
REMOVED = 2
STATUS_CHOICES = (
 (
  ENABLED, _('Enabled')),
 (
  DISABLED, _('Disabled')),
 (
  REMOVED, _('Removed')))
LABEL_RE = re.compile('^[a-zA-Z_][a-zA-Z_0-9.]*$')

def is_valid_label(name):
    return bool(LABEL_RE.match(name))


def construct_template_path(app, name, ext='.html'):
    if not is_valid_label(name):
        raise RuntimeError, 'invalid label: ' + name
    if not is_valid_label(app):
        raise RuntimeError, 'invalid label: ' + app
    return ('/').join([app.split('.')[(-1)], 'plugins', name.replace('.', '/')]) + ext


class PluginPoint(models.Model):
    label = models.CharField(max_length=255, unique=True, help_text=_('The label for the plugin point.'))
    index = models.IntegerField(default=0)
    registered = models.BooleanField(default=False, help_text=_('is this a registered plugin point with a library entry?'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED)

    class Meta:
        ordering = ('index', 'id')

    def __unicode__(self):
        return 'plugin_point:' + self.label

    @property
    def app(self):
        if not self.registered:
            return ''
        return self.label.rsplit('.', 1)[0]

    @property
    def name(self):
        return self.label.rsplit('.', 1)[(-1)]

    def get_plugins(self, user=None):
        """get all the plugins in appropriate order"""
        if self.status:
            return []
        if user is None:
            return self.plugin_set.filter(status=ENABLED).order_by('index', 'id')
        upref = user.userpluginpreference_set.filter(plugin__status=ENABLED, plugin__point=self)
        visible = [ up.plugin for up in upref.filter(Q(visible=True) | Q(plugin__required=True))
                  ]
        plugins = self.plugin_set.filter(status=ENABLED).exclude(id__in=[ x['plugin'] for x in upref.values('plugin') ]).order_by('index', 'id')
        return visible + list(plugins)

    def get_options(self):
        if not self.registered:
            return {}
        lib = get_library(self.app)
        call = lib.get_plugin_point_call(self.name)
        return call.options

    def call(self, context, user, **args):
        if not self.registered:
            return {}
        lib = get_library(self.app)
        call = lib.get_plugin_point_call(self.name)
        options = call.options
        base = [self]
        if options.get('takes_context', False):
            base.append(context)
        if options.get('takes_user', False):
            base.append(user)
        if options.get('takes_args', False):
            return call(*base, **args)
        return call(self, *base)


class Plugin(models.Model):
    point = models.ForeignKey(PluginPoint)
    label = models.CharField(max_length=255, unique=True, help_text=_('The label for the plugin point.'))
    index = models.IntegerField(default=0)
    registered = models.BooleanField(default=False, help_text=_('is this a registered plugin?'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED)
    required = models.BooleanField(default=False, help_text=_('users can not remove this plugin.'))
    template = models.TextField(help_text=_('template to load for the plugin.'))

    class Meta:
        order_with_respect_to = 'point'
        ordering = ('point', 'index', 'id')

    def __unicode__(self):
        return 'plugin:' + self.label

    @property
    def app(self):
        return self.label[:-(len(self.point.label) + 1)]

    @property
    def name(self):
        return self.point.label

    def get_options(self):
        if not self.registered:
            return {}
        lib = get_library(self.app)
        call = lib.get_plugin_call(self.name)
        return call.options

    def call(self, context, user, **args):
        if not self.registered:
            return {}
        lib = get_library(self.app)
        call = lib.get_plugin_call(self.name)
        options = call.options
        base = [self]
        if options.get('takes_context', False):
            base.append(context)
        if options.get('takes_user', False):
            base.append(user)
        if options.get('takes_args', False):
            return call(*base, **args)
        return call(self, *base)


class UserPluginPreference(models.Model):
    user = models.ForeignKey(User)
    plugin = models.ForeignKey(Plugin)
    visible = models.BooleanField(default=True)
    index = models.IntegerField(default=0)

    class Meta:
        unique_together = [
         'user', 'plugin']
        order_with_respect_to = 'plugin'
        ordering = ('plugin', 'user', 'index', 'id')

    def __unicode__(self):
        return (':').join(['pluginpref', self.user.username, self.plugin.label])