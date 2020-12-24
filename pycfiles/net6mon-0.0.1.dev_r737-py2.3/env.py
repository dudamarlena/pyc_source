# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/env.py
# Compiled at: 2006-06-19 03:29:49
import sys, os
from net6mon.config import Config, DaemonConfig
from net6mon.logger import Logger, logger_factory

class Environment:
    """
    Cette classe représente l'environnement global de notre application. 
    Cet environnement est instancié dans l'instance principale de l'application 
    puis doit être passé au constructeur de chaque classe nécessitant un accès à l'environnement global

    L'environnement global couvre principalement 2 fonctions :
        - La gestion des logs, de leurs destination et le fait de garder la configuration 
          du logging persistante au fil des instantiations de tous les modules de l'application 
        - La gestion du chargement de la conf et le fait de garder la configuration 
          persistante et accessible par tous les modules/classes
     
    """
    __module__ = __name__

    def __init__(self, configfile):
        if not self._check_conffile(configfile):
            raise 'Bad configuration file'
        self.config = DaemonConfig(configfile)
        if self.config.debug.lower() == 'yes':
            self.log = logger_factory(logtype='file', logfile=self.config.logfile, stdlog='yes', logid='net6mon')
        else:
            self.log = logger_factory(logtype='file', logfile=self.config.logfile, logid='net6mon')
        self.log.debug('Daemon started')
        self.log.info('Host=' + str(self.config.host) + ', port=' + str(self.config.port))

    def _check_conffile(self, filename):
        """ 
                Vérifie la validité du fichier de configuration principal
        
                @type filename: string 
                @param filename: filename to check      
        """
        if os.path.exists(filename) and os.path.isfile(filename):
            return 1
        return 0