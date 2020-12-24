# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/commands/shutdowndroplet.py
# Compiled at: 2019-08-09 13:14:25
# Size of source mod 2**32: 824 bytes
import sys
sys.path.append('..')
import digitalocean
from digitalocean import DataReadError, TokenError
from dobg.helper.confighandler import ConfigHandler
from dobg.exceptions.configexceptions import InvalidTokenException
from dobg.exceptions.dropletexceptions import InvalidIdException

def shutdown_droplet(args):
    """ Turns off a Droplet with given id """
    token = ConfigHandler.get_config_setting('token')
    manager = digitalocean.Manager(token=token)
    try:
        droplet = manager.get_droplet(int(args.id))
    except (DataReadError, TokenError):
        raise InvalidTokenException
    except Exception:
        raise InvalidIdException

    action = droplet.shutdown()
    print('Droplet shutdown status: {}\n'.format(action['action']['status']))