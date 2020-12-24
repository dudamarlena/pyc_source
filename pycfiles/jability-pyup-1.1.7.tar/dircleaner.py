# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/dircleaner.py
# Compiled at: 2015-04-21 06:36:16
"""
Module de nettoyage des fichiers d'un dossier
en conservant les fichiers les plus récents exprimés
en nombre de fichiers à conserver ou en nombre de jours.
Ne nettoie pas les sous-dossiers.
"""
__author__ = 'Fabrice Romand'
__copyright__ = 'Copyleft 2008 - Fabrice Romand'
__credits__ = ['Fabrice Romand']
__license__ = 'GPL'
__version__ = '1.2'
__maintainer__ = 'Fabrice Romand'
__email__ = 'fabrice.romand@gmail.com'
__status__ = 'Development'
import logging, operator, os, time, filescollector
log = logging.getLogger('jabilitypyup.dircleaner')

class dirCleaner:
    """Classe de nettoyage des dossiers d'un fichier"""

    def __init__(self, dir2clean='.'):
        u"""''dir2clean'' est le dossier à nettoyer
        """
        self.setDir(dir2clean)
        self.setFilter()
        self.setCleanLastest()

    def setDir(self, dir2clean):
        u"""positionne le dossier à nettoyer.
        ''dir2clean'' est le dossier à nettoyer
        """
        self.dir = os.path.abspath(dir2clean)
        log.debug('set %s for cleaning' % dir2clean)

    def setFilter(self, pattern='^.*$'):
        u"""définition du filtre (expression régulière).
        ''pattern'' est l'expression de régulière pour filtrage'"""
        self.filefilter = pattern
        log.debug("set filter '%s'" % pattern)

    def setCleanLastest(self, lastest=True, qty=0):
        u"""positionne le type de nettoyage :
        lastest = True ne conserve que les qty derniers fichiers
        si = False conserve les fichiers créés les qty derniers jours
        """
        self.lastest = lastest
        self.qty = qty
        log.debug('set cleaning method : Lastest: %r - Quantity: %d' % (lastest, qty))

    def filedelete(self, filepath):
        """Suppression du fichier ''filepath''"""
        if os.path.exists(filepath):
            testflag = True
            testcount = 0
            while testflag and testcount < 10:
                try:
                    os.remove(filepath)
                except OSError as e:
                    time.sleep(1)
                    testcount += 1
                    log.warning('cannot delete %s : retry #%d...' % (filepath, testcount))
                    log.exception(e)
                    continue

                testflag = False

            if os.path.exists(filepath):
                log.error('cannot delete %s' % filepath)
                return False
        return True

    def clean(self):
        u"""Effectue le nettoyage
        Renvoie le nb de fichiers supprimés
        """
        res = 0
        if not os.path.isdir(self.dir):
            log.error('directory not found (%s)' % self.dir)
            return
        fcoll = filescollector.FilesCollector()
        fcoll.setSourceDir(self.dir)
        fcoll.setFileFilter(self.filefilter)
        fcoll.run(True)
        log.debug('%d file(s) found in directory to clean' % len(fcoll.files))
        if len(fcoll.files) > 0:
            fl2a = sorted(fcoll.files, key=operator.itemgetter(1))
            if self.lastest:
                if self.qty > 0:
                    bfin = fl2a[:self.qty * -1]
                else:
                    bfin = fl2a
                for ffile in bfin:
                    if os.path.isfile(ffile[0]):
                        if self.filedelete(ffile[0]):
                            res += 1
                        else:
                            log.error("Can't delete file %s" % file[0])

            else:
                now = time.time() - self.qty * 86400
                for ffile in fl2a:
                    if ffile[1] <= now and os.path.isfile(ffile[0]):
                        if self.filedelete(ffile[0]):
                            res += 1
                        else:
                            log.error("Can't delete file %s" % ffile[0])

        log.debug('%d file(s) deleted' % res)
        return res