# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cecdaemon/cecdaemon.py
# Compiled at: 2018-09-22 12:16:54
# Size of source mod 2**32: 3183 bytes
""" cecdaemon: Manages CEC for a linux htpc
"""
import os, sys, logging
from time import sleep
from argparse import ArgumentParser
from configparser import ConfigParser
import cec
from .custom_cmd import CustomCommand
from .remote import Remote
from .tv import Tv
from .trigger import Trigger

class CecDaemon:
    __doc__ = ' Creates instances of Tv, Remote, CustomCommand and Trigger\n        Manages configuration parsing and command line args\n    '

    def __init__(self):
        self.cec = cec
        self._parse_args()
        self._setup_logging()
        logging.info('Initializing CEC device, please wait...')
        cec.init()
        logging.info('CEC Initialized')
        if os.path.isfile(self.args.conffile):
            conf = ConfigParser()
            logging.info('Using config file %s', self.args.conffile)
            conf.read(self.args.conffile)
        else:
            logging.warning('Config file not found')
            conf = None
        try:
            tvconf = conf._sections['tv']
            television = Tv(cec, tvconf)
        except AttributeError:
            television = Tv(cec, None)

        try:
            triggerconf = conf._sections['triggers']
            trigger = Trigger(cec, triggerconf)
        except AttributeError:
            logging.warning('No triggers section found in config, triggers disabled')

        try:
            keymap = conf._sections['keymap']
            remote = Remote(cec, keymap)
        except AttributeError:
            remote = Remote(cec, None)

        if conf is not None:
            for name in [x for x in conf.sections() if x[:4] == 'cmd_']:
                logging.debug('Creating callback for %s', name)
                try:
                    cmd = conf[name]['command']
                    htime = conf[name]['holdtime']
                    key = conf[name]['key']
                    callback = CustomCommand(cmd, htime)
                    remote.add_callback(callback.run_command, int(key))
                except AttributeError:
                    logging.warning('Callback for %s not created, check format', name)

    def _setup_logging(self):
        """ Configure logging
        """
        logging.basicConfig(stream=(sys.stdout), level=(self.args.loglevel))

    def _parse_args(self):
        """ Parse the command line arguments
        """
        parser = ArgumentParser()
        parser.add_argument('-d', '--debug', help='Print debug messages', action='store_const',
          dest='loglevel',
          const=(logging.DEBUG),
          default=(logging.INFO))
        parser.add_argument('-c', '--config', help='Configuration file', metavar='FILE',
          dest='conffile',
          default='/etc/cecdaemon.conf')
        self.args = parser.parse_args()

    def run(self):
        """ Keeps the instance of CecDaemon running while python-cec threads
            do callbacks
        """
        logging.info('Running...')
        while True:
            sleep(1)


def run():
    """ Run the daemon
    """
    daemon = CecDaemon()
    daemon.run()


if __name__ == '__main__':
    run()