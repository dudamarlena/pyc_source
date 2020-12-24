# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/olympo/log.py
# Compiled at: 2012-03-22 06:35:08
import hashlib, logging, logging.handlers as loghandlers, random
LEVELS = dict(debug=logging.DEBUG, info=logging.INFO, warning=logging.WARNING, error=logging.ERROR, critical=logging.CRITICAL)

class NeptunoLogger(object):

    def __init__(self, nombre, fichero, nivel, tamanyo):
        self.nombre = nombre
        self.fichero = fichero
        self.nivel = nivel
        self.tamanyo = tamanyo
        if self.nivel:
            self.logger = logging.getLogger(self.nombre)
            self.logger.setLevel(LEVELS.get(self.nivel, logging.NOTSET))
            fh = loghandlers.RotatingFileHandler(self.fichero, maxBytes=self.tamanyo, backupCount=5)
            self.logger.addHandler(fh)
            fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(fmt)

    def debug(self, msg):
        if self.nivel:
            self.logger.debug(msg)

    def info(self, msg):
        if self.nivel:
            self.logger.info(msg)

    def warning(self, msg):
        if self.nivel:
            self.logger.warning(msg)

    def error(self, msg):
        if self.nivel:
            self.logger.error(msg)

    def critical(self, msg):
        if self.nivel:
            self.logger.critical(msg)

    @staticmethod
    def get_logger(nombre):
        random.seed()
        m = hashlib.md5()
        m.update('%6.6d' % random.randint(0, 999999))