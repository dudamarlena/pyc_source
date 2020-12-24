# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/tests/test_egg_finder.py
# Compiled at: 2012-02-27 07:41:53
import os
from paste.script import pluginlib

def test_egg_info():
    egg_dir = os.path.join(os.path.dirname(__file__), 'fake_packages', 'FakePlugin.egg')
    found = pluginlib.find_egg_info_dir(os.path.join(egg_dir, 'fakeplugin'))
    assert found == os.path.join(egg_dir, 'FakePlugin.egg-info')
    found = pluginlib.find_egg_info_dir(os.path.dirname(__file__))
    assert found == os.path.join(os.path.dirname(os.path.dirname(__file__)), 'PasteScript.egg-info')


def test_resolve_plugins():
    plugins = [
     'FakePlugin']
    all = pluginlib.resolve_plugins(plugins)
    assert all
    assert len(all) == 2


def test_find_commands():
    all = pluginlib.resolve_plugins(['PasteScript', 'FakePlugin'])
    commands = pluginlib.load_commands_from_plugins(all)
    print commands
    assert 'testcom' in commands