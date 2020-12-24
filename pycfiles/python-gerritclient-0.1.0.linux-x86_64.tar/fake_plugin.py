# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/tests/utils/fake_plugin.py
# Compiled at: 2017-04-12 12:05:03


def get_fake_plugin(plugin_id='fake-plugin'):
    """Creates a fake plugin

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """
    return {'id': plugin_id, 
       'version': '1.0', 
       'index_url': ('plugins/{0}/').format(plugin_id), 
       'disabled': None}


def get_fake_plugins(plugins_count):
    """Creates a random fake plugins map."""
    fake_plugins = {}
    for i in range(1, plugins_count + 1):
        fake_plugins[('fake-plugin-{}').format(i)] = get_fake_plugin(('fake-plugin-{}').format(i))

    return fake_plugins