# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/fabrant.py
# Compiled at: 2016-03-02 08:29:51
from contextlib import contextmanager
from fabric.api import local, lcd, settings
__version__ = '0.0.6'
__all__ = ['vagrant']

def _parse_ssh_config(config):
    lines = config.split('\n')

    def dequote(parts):
        return [ part[1:-1] if part.startswith('"') and part.endswith('"') else part for part in parts
               ]

    return dict(dequote(line.strip().partition(' ')[::2]) for line in lines)


@contextmanager
def vagrant(directory, up=True, halt=False, **kwargs):
    """ Contextmanager to set up a vagrant session, interact with it and
    optionally halt the box afterwards. All commands within this context
    (such as ``sudo``, ``run``, ``get`` or ``put``) arenow configured to target
    the vagrant box.
    The path to the vagrant ``directory`` (i.e: the path to the directory where
    the Vagrantfile resides) is mandatory.
    When ``up`` is ``True`` (which is the default), then the box will be started
    beforehand, using a local ``vagrant up``. Similarly, when ``halt`` is set
    (which is *not* the default) then the box will be stopped using
    ``vagrant halt``.

    Additional fabric ``env`` settings can be passed as keyword arguments.

    Example::

        with vagrant('path/to/dir'):
            run('ls /vagrant')

    .. note::
        ``vagrant`` does *not* ``lcd`` into the vagrant ``directory``.
    """
    with lcd(directory):
        if up:
            local('vagrant up')
        config = _parse_ssh_config(local('vagrant ssh-config', capture=True))
    settings_dict = dict(user=config['User'], key_filename=config['IdentityFile'], host_string='%s:%s' % (config['HostName'], config['Port']), gateway=None)
    settings_dict.update(kwargs)
    with settings(**settings_dict):
        yield
    with lcd(directory):
        if halt:
            local('vagrant halt')
    return