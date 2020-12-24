# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/logreporter.py
# Compiled at: 2015-04-21 06:48:01
"""
Module d'extraction des messages significatifs des journaux d'activité
et envoi par email de l'extraction
"""
__author__ = 'Fabrice Romand'
__copyright__ = 'Copyleft 2009, Fabrice Romand'
__credits__ = ['Fabrice Romand']
__license__ = 'GPL'
__version__ = '1.2'
__maintainer__ = 'Fabrice Romand'
__email__ = 'fabrice.romand@gmail.com'
__status__ = 'Development'
import os, filescollector, logging, time, pysendmail, toolbox, sys
log = logging.getLogger('jabilitypyup.logreporter')

class logReporter:
    """
    Classe d'extraction des messages significatifs des journaux d'activité
    et envoi par email de l'extraction
    """

    def __init__(self, logspath='.', fromdate='19800101', logsfilter='^.*\\.log$', logdateformat='%Y%m%d', logdatepos=1, loglevels=('CRITICAL', 'ERROR', 'WARNING'), loglevelpos=3, charset='UTF-8'):
        u"""
        ''logspath'': chemin des journaux à analyser
        ''fromdate'': date de début des entrées à analyser (format %Y%m%d)
        ''logsfilter'': expr. régulière de collecter des fichiers journaux
        ''logdateformat'': format des dates dans les journaux
        ''logdatepos'': position de la date dans une entrée de journal
        ''loglevels'': liste des niveaux à rapporter
        ''loglevelpos'': position du niveau dans une entrée de journal
        ''charset'': encodage des journaux
        """
        self.logdir = os.path.abspath(logspath)
        self.logdateformat = logdateformat
        self.logdatepos = logdatepos
        self.loglevelpos = loglevelpos
        self.loglevels = loglevels
        self.logsfilter = logsfilter
        self.fromdate = time.mktime(time.strptime(fromdate, logdateformat))
        self.extractedlines = list()
        self.charset = charset
        if self.charset is None:
            self.charset = toolbox.get_stream_encoding(sys.stdout)
        return

    def extract(self):
        u""" Analyse des logs
        Renvoie la liste des lignes sélectionnées
        """
        reslines = list()
        fc = filescollector.FilesCollector()
        fc.setSourceDir(self.logdir)
        fc.setFileFilter(self.logsfilter)
        fc.run(True)
        log.debug('%d log file(s) find' % len(fc.files))
        for ffile in fc.files:
            if ffile[1] < self.fromdate:
                log.debug('%s too old : ignored' % os.path.basename(ffile[0]))
                continue
            try:
                tfl = open(ffile[0], 'r')
                lines = tfl.readlines()
                tfl.close()
            except OSError:
                log.debug("Can't read %s : ignored" % os.path.basename(ffile[0]))
                reslines.append("** Cannot read log '%s'" % ffile[0])
                continue

            numline = 0
            for line in lines:
                numline += 1
                sline = line.split()
                if len(sline) >= self.loglevelpos and len(sline) >= self.logdatepos:
                    try:
                        dline = time.mktime(time.strptime(sline[(self.logdatepos - 1)], self.logdateformat))
                        if dline >= self.fromdate:
                            if sline[(self.loglevelpos - 1)] in self.loglevels:
                                reslines.append(line.decode(self.charset))
                    except Exception:
                        log.debug("Can't read %s line %d : ignored" % (os.path.basename(ffile[0]), numline))
                        reslines.append("** Bad file format '%s' line %d" % (ffile[0], numline))
                        continue

                else:
                    log.debug('Bad file format %s line %d : ignored' % (os.path.basename(ffile[0]), numline))
                    reslines.append("** Bad file format '%s' line %d" % (ffile[0], numline))
                    continue

        self.extractedlines = reslines
        log.debug('%d lines to report' % len(self.extractedlines))
        return reslines

    def email_report(self, mfrom, mto, msubject, msmtpserver='localhost'):
        u"""Envoi du rapport par email
        ''mfrom'': adresse mail de l'expéditeur
        ''mto'': liste des destinataires
        ''msubject'': sujet du mail à envoyer
        ''msmtpserver'': adresse du serveur SMTP

        Voir jabilipyup.pysendmail.send() pour les codes renvoyés.
        """
        mbody = 'logs directory : ' + self.logdir + '\n'
        slevels = ''
        for level in self.loglevels:
            slevels += level + ' '

        mbody += 'required level(s) : ' + slevels + '\n\n'
        for line in self.extractedlines:
            mbody += line

        return pysendmail.send(mfrom, mto, msubject, mbody, list(), msmtpserver)