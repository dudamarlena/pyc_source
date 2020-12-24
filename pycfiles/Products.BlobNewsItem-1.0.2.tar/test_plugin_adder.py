# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/tests/test_plugin_adder.py
# Compiled at: 2012-02-27 07:41:53
import os
from paste.script import pluginlib
egg_dir = os.path.join(os.path.dirname(__file__), 'fake_packages', 'FakePlugin.egg')
plugin_file = os.path.join(egg_dir, 'paster_plugins.txt')

def plugin_lines():
    if not os.path.exists(plugin_file):
        return []
    f = open(plugin_file)
    lines = f.readlines()
    f.close()
    return [ l.strip() for l in lines if l.strip() ]


def test_add_remove():
    prev = plugin_lines()
    pluginlib.add_plugin(egg_dir, 'Test')
    assert 'Test' in plugin_lines()
    pluginlib.remove_plugin(egg_dir, 'Test')
    assert 'Test' not in plugin_lines()
    assert prev == plugin_lines()
    if not prev and os.path.exists(plugin_file):
        os.unlink(plugin_file)