# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/djangosampler/test_plugins.py
# Compiled at: 2015-11-17 05:08:04
from django.conf import settings
from django.test import TestCase
from plugins import install_plugins

class DummyPlugin(object):

    @staticmethod
    def install():
        DummyPlugin.install_called = True


class TestPlugins(TestCase):

    def setUp(self):
        DummyPlugin.install_called = False
        DummyPlugin.tag_trace_called = None
        return

    def test_install_plugins(self):
        settings.DJANGO_SAMPLER_PLUGINS = ('djangosampler.test_plugins.DummyPlugin', )
        install_plugins()
        self.assertTrue(DummyPlugin.install_called)