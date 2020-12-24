# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/basico.py
# Compiled at: 2019-03-31 15:31:47
# Size of source mod 2**32: 5155 bytes
"""
# File: basico.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Main entry point por Basico app
"""
import os, sys, signal
from gi.repository import GObject
from basico.core.mod_env import APP, LPATH, GPATH, FILE
from basico.core.mod_log import get_logger
from basico.services.srv_utils import Utils
from basico.services.srv_gui import GUI
from basico.services.srv_iconmgt import IconManager
from basico.services.srv_bnr import BackupRestoreMan
from basico.services.srv_sap import SAP
from basico.services.srv_settings import Settings
from basico.services.srv_uif import UIFuncs
from basico.services.srv_callbacks import Callback
from basico.services.srv_notify import Notification
from basico.services.srv_db import Database
from basico.services.srv_driver import SeleniumDriver
from basico.services.srv_cols import Collections
from basico.services.srv_annot import Annotation
from basico.services.srv_notify import Notification
signal.signal(signal.SIGINT, signal.SIG_DFL)

class Basico(object):
    __doc__ = '\n    Basico Application class\n    '

    def __init__(self):
        """
        Basico class
        """
        self.setup_environment()
        self.setup_logging()
        self.setup_services()

    def setup_environment(self):
        """
        Setup Basico environment
        """
        os.environ['PATH'] += os.pathsep + LPATH['DRIVERS']
        for entry in LPATH:
            if not os.path.exists(LPATH[entry]):
                os.makedirs(LPATH[entry])

    def setup_logging(self):
        if os.path.exists(FILE['LOG']):
            with open(FILE['LOG'], 'w') as (flog):
                pass
        self.log = get_logger(__class__.__name__)
        self.log.info('Basico %s started', APP['version'])
        self.log.debug('Global path: %s', GPATH['ROOT'])
        self.log.debug('Local path: %s', LPATH['ROOT'])
        self.log.debug('Logging all messages to file: %s', FILE['LOG'])
        self.log.debug('Logging only events: %s', FILE['EVENTS'])

    def setup_services(self):
        """
        Setup Basico Services
        """
        self.services = {}
        try:
            services = {'GUI':GUI(), 
             'Utils':Utils(), 
             'UIF':UIFuncs(), 
             'SAP':SAP(), 
             'Settings':Settings(), 
             'Notify':Notification(), 
             'IM':IconManager(), 
             'Callbacks':Callback(), 
             'DB':Database(), 
             'Driver':SeleniumDriver(), 
             'Collections':Collections(), 
             'Annotation':Annotation(), 
             'BNR':BackupRestoreMan(), 
             'Notify':Notification()}
            for name in services:
                self.register_service(name, services[name])

        except Exception as error:
            self.log.error(error)
            raise

    def get_service(self, name):
        """
        Get/Start a registered service
        """
        try:
            service = self.services[name]
            logname = service.__class__.__name__
            if not service.is_started():
                service.start(self, logname, name)
            return service
        except KeyError as service:
            self.log.error('Service %s not registered or not found', service)
            raise

    def register_service(self, name, service):
        """
        Register a new service
        """
        try:
            self.services[name] = service
        except KeyError as error:
            self.log.error(error)

    def deregister_service(self, name):
        """
        Deregister a running service
        """
        self.services[name].end()
        self.services[name] = None

    def stop(self):
        """
        For each service registered, it executes the 'end' method
        (if any) to finalize them properly.
        """
        self.deregister_service('GUI')
        for name in self.services:
            try:
                if name != 'GUI':
                    self.deregister_service(name)
            except Exception as error:
                self.log.error(error)
                raise

        self.log.info('Basico %s finished', APP['version'])

    def run(self):
        """
        Start Basico
        """
        self.srvdrv = self.get_service('Driver')
        self.srvgui = self.get_service('GUI')
        self.srvgui.run()


def main():
    """
    Entry point
    """
    basico = Basico()
    basico.run()