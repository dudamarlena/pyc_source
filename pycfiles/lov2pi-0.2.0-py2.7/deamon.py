# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/lov2pi/deamon.py
# Compiled at: 2015-08-16 20:40:47
from time import sleep
from lov2pi import Lov2pi
from daemons.prefab import run
import os.path, json

class Counters(run.RunDaemon):

    def run(self):
        config_path = os.path.expanduser('~') + '/.lov2pi'
        if os.path.isfile(config_path):
            config = json.load(open(self.config_path))
            print config
            client = Lov2pi(config['appkey'], config['name'])
            while True:
                client.sync_counter()
                sleep(1)

        else:
            raise ValueError('config not_found, you should register your lov2pi first')