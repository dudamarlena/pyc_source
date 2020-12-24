# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/commands/createdroplet.py
# Compiled at: 2019-07-25 10:24:01
# Size of source mod 2**32: 865 bytes
import sys
sys.path.append('..')
import digitalocean
from dobg.helper.confighandler import ConfigHandler

def create_droplet(args):
    """ Creates Droplet """
    token = ConfigHandler.get_config_setting('token')
    droplet = digitalocean.Droplet(token=token, name=(args.name),
      region=(args.region),
      image=(args.image),
      size_slug=(args.size),
      backups=True)
    droplet.create()
    print('You have successfuly created Droplet!        \nId: {}, Name: {}, Size: {}, Image: {}, Region: {}'.format(droplet.id, droplet.name, droplet.size_slug, droplet.image, droplet.region))