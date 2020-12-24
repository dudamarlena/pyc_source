# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/edc_fabric/fabfile/files/dmg.py
# Compiled at: 2017-04-21 13:52:06
# Size of source mod 2**32: 1615 bytes
from fabric.api import cd, env, run, local, lcd, warn_only
from fabric.colors import red

def dismount_dmg(volume_name=None):
    """Dismounts a dmg file on the remote host.
    """
    result = run('diskutil unmount {}'.format(volume_name))
    if result.failed:
        print(red('{host} Dismount failed for {volume_name}'.format(host=(env.host),
          volume_name=volume_name)))


def mount_dmg(dmg_path=None, dmg_filename=None, dmg_passphrase=None):
    """Mounts a dmg file on the remote host.
    """
    env.prompts.update({'Enter disk image passphrase:': dmg_passphrase})
    dmg_path = dmg_path or env.dmg_path
    dmg_filename = dmg_filename or env.dmg_filename
    run(('diskutil unmount {}'.format(env.key_volume)), warn_only=True)
    with cd(dmg_path):
        run('hdiutil attach -stdinpass {}'.format(dmg_filename))


def mount_dmg_locally(dmg_path=None, dmg_filename=None, dmg_passphrase=None):
    """Mounts a dmg file on the local host.
    """
    env.prompts.update({'Enter disk image passphrase:': dmg_passphrase})
    dmg_path = dmg_path or env.dmg_path
    dmg_filename = dmg_filename or env.dmg_filename
    with warn_only():
        local('diskutil unmount {}'.format(env.key_volume))
    with lcd(dmg_path):
        local('hdiutil attach -stdinpass {}'.format(dmg_filename))


def dismount_dmg_locally(volume_name=None):
    """Dismounts a dmg file on the local host.
    """
    result = local('diskutil unmount {}'.format(volume_name))
    if result.failed:
        print(red('{host} Dismount failed for {volume_name}'.format(host=(env.host),
          volume_name=volume_name)))