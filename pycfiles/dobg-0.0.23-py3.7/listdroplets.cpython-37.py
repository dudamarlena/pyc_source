# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/commands/listdroplets.py
# Compiled at: 2019-08-25 16:23:30
# Size of source mod 2**32: 1161 bytes
import sys
sys.path.append('..')
import digitalocean
from digitalocean import DataReadError, TokenError
from dobg.helper.confighandler import ConfigHandler
from dobg.exceptions.configexceptions import InvalidTokenException

def list_droplets(args):
    """ Lists all of Droplets """
    token = ConfigHandler.get_config_setting('token')
    manager = digitalocean.Manager(token=token)
    try:
        droplets = manager.get_all_droplets()
    except (DataReadError, TokenError):
        raise InvalidTokenException

    if len(droplets) == 0:
        print('No droplets.')
        return
    result = '{:15}{:40}{:10}{:18}{:37}{}'.format('ID:', 'Name:', 'Region:', 'Size:', 'Image:', 'Status:\n')
    for droplet in droplets:
        image = droplet.image['slug'] if droplet.image['slug'] else 'None'
        result += '{:<15}{:40}{:10}{:18}{:37}{}\n'.format(droplet.id, droplet.name, droplet.region['slug'], droplet.size_slug, image, droplet.status)

    print(result)