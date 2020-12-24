# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/commands/listimages.py
# Compiled at: 2019-07-25 08:05:24
# Size of source mod 2**32: 851 bytes
import sys
sys.path.append('..')
import digitalocean
from digitalocean import DataReadError, TokenError
from dobg.helper.confighandler import ConfigHandler
from dobg.exceptions.configexceptions import InvalidTokenException

def list_images(args):
    """ Lists all of Droplets """
    token = ConfigHandler.get_config_setting('token')
    manager = digitalocean.Manager(token=token)
    try:
        images = manager.get_all_images()
    except (DataReadError, TokenError):
        raise InvalidTokenException

    result = '{:10}{:46}{:15}{:37}{}\n'.format('Id:', 'Name:', 'Distribution:', 'slug:', 'Regions:\n')
    for image in images:
        result += '{:<10}{:46}{:15}{:37}{}\n'.format(image.id, image.name, image.distribution, image.slug if image.slug else 'N/A', ', '.join(image.regions))

    print(result)