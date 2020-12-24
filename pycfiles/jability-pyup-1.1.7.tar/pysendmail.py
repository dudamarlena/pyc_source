# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/pysendmail.py
# Compiled at: 2013-05-25 04:38:30
"""
pySendMail - Fabrice Romand <fabrom AT jability.org> - release under GPL
goal: sending mail from standard input
usage: %s [-dhq] [-f <from>] [-t <to>] [-s <subject>]
               [-S <smtp host>]
               [-F <files list>] [-z <archive name>]
               [-c <charset>]
               [<file]
-h, --help    Display this help message
-d, --debug   Display debug info.
-q, --quiet   Silent mode
-f, --from    Sender email address
-t, --to      Person addressed emails list (comma sep.)
-s, --subject Subject
-F, --files   Attachments list (comma sep.)
-z, --zip     Zip attachments into archive before sending it
-S, --smtphost SMTP host (default=localhost)
-c, --charset Charset unicode à utiliser (utf-8 par défaut)

Retourne :
0 si ok, email envoyé
1 Si email envoyé mais certaines PJ non trouvées
2 Email non envoyé : erreur durant communication SMTP
3 Email non envoyé : erreur inconnue
9 si option incorrecte
"""
__author__ = 'Fabrice Romand'
__copyright__ = 'Copyleft 2008, Fabrice Romand'
__credits__ = ['Fabrice Romand']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'Fabrice Romand'
__email__ = 'fabrom@jability.org'
__status__ = 'Development'
_debug = False
from email import Encoders
from email.Header import Header
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
import getopt, locale, os.path, platform, smtplib, sys, traceback

def send(mfrom, mto, msubject, mbody, files=[], msmtpserver='localhost', charset='UTF-8', zip=False, zipFilename='archive.zip'):
    u"""
    Envoi effectif du mail par SMTP
    > mfrom: adresse de l'expéditeur
    > mto: liste des adresses des destinataires
    > msubject: objet du message
    > mbody: Corps du message (string)
    > files: Liste de pièces jointes
    > msmtpserver: IP ou nom du serveur SMTP
    > charset: code du charset à utiliser pour l'encodage du mail
    > zip: Vrai si les PJ doivent être zippées avant envoi
    > zipFilename: Nom de l'archive zip
    < code de retour :  O=ok,
                        1=warning (PJ pas trouvée),
                        2=Erreur (communication avec le serveur SMTP)
                        3=Erreur (inconnue)
    """
    ressend = 0
    try:
        email = MIMEMultipart()
        email['From'] = mfrom.encode('ascii')
        email['To'] = COMMASPACE.join(mto)
        email['Subject'] = str(Header(msubject, charset))
        email['Date'] = formatdate(localtime=True)
        email.attach(MIMEText(mbody.encode(charset), 'plain', charset))
        if len(files) > 0:
            if zip:
                import zipfile
                zipFile = zipfile.ZipFile(zipFilename, 'w')
                zipok = False
                for file in files:
                    if not os.path.exists(file):
                        ressend = 1
                        print >> sys.stderr, "Attachment '%s' not found !" % file
                        continue
                    zipFile.write(file, file.encode('cp437'))
                    zipok = True

                zipFile.close()
                if zipok:
                    files = [
                     zipFilename]
                else:
                    files = []
            for file in files:
                if not os.path.exists(file):
                    ressend = 1
                    print >> sys.stderr, "Attachment '%s' not found !" % file
                    continue
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(file, 'rb').read())
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file.encode(charset)))
                email.attach(part)

        try:
            server = smtplib.SMTP(msmtpserver)
            server.sendmail(mfrom, mto, email.as_string())
            server.quit()
        except:
            ressend = 2
            if _debug:
                raise
            return ressend

        if zip:
            os.remove(zipFilename)
    except:
        ressend = 3
        if _debug:
            raise

    return ressend


def usage(name):
    """Affichage du mode d'emploi"""
    print >> sys.stderr, 'pySendMail %s - Fabrice Romand ' % __version__ + '<fabrom AT jability.org> - release under GPL'
    print >> sys.stderr, 'goal: sending mail from standard input'
    print >> sys.stderr, 'usage: %s [-dhq] [-f <from>] [-t <to>] ' % name + '[-s <subject>] [-S <smtp host>] [-F <attachments list>] ' + '[-c <charset>] [-z <archive name>] [< file]'
    print >> sys.stderr, '\t-f, --from\t\tSender email address'
    print >> sys.stderr, '\t-t, --to\t\tPerson addressed emails list ' + '(comma sep.)'
    print >> sys.stderr, '\t-s, --subject\t\tSubject'
    print >> sys.stderr, '\t-F, --files\t\tAttachments list (comma sep.)'
    print >> sys.stderr, '\t-z, --zip\t\tzip all attachments in an archive'
    print >> sys.stderr, '\t-S, --smtphost\t\tSMTP host (default=localhost)'
    print >> sys.stderr, '\t-c, --charset\t\tcharset to encode email ' + '(utf-8 by default)'
    print >> sys.stderr, '\t-h, --help\t\tDisplay this help message'
    print >> sys.stderr, '\t-d, --debug\t\tDisplay debug info.'
    print >> sys.stderr, '\t-q, --quiet\t\tSilent mode'


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:df:F:hqs:S:t:z:', [
         'charset=', 'help', 'debug', 'from=',
         'files=', 'to=', 'subject=', 'smtphost=',
         'quiet', 'zip='])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(9)

    mfrom = ''
    mto = ''
    files = ''
    msubject = ''
    msmtphost = ''
    charset = 'UTF-8'
    zip = False
    zipFilename = 'archive.zip'
    quiet = False
    dftlocale = locale.getdefaultlocale()[1]
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(sys.argv[0])
            sys.exit(1)
        if o in ('-d', '--debug'):
            _debug = True
        if o in ('-f', '--from'):
            mfrom = unicode(a, dftlocale)
        elif o in ('-t', '--to'):
            mto = unicode(a, dftlocale)
        elif o in ('-s', '--subject'):
            msubject = unicode(a, dftlocale)
        elif o in ('-S', '--smtphost'):
            msmtphost = a
        elif o in ('-F', '--files'):
            files = unicode(a, dftlocale)
        elif o in ('-c', '--charset'):
            charset = a
        elif o in ('-q', '--quiet'):
            quiet = True
            _debug = False
        elif o in ('-z', '--zip'):
            zip = True
            zipFilename = unicode(a, dftlocale)

    try:
        if sys.stdin.isatty() and not quiet:
            if mfrom == '':
                mfrom = unicode(raw_input('From: '), dftlocale)
            if mto == '':
                mto = unicode(raw_input('To: '), dftlocale)
            if msubject == '':
                msubject = unicode(raw_input('Subject: '), dftlocale)
            if files == '':
                files = unicode(raw_input('Attachments: '), dftlocale)
            if msmtphost == '':
                msmtphost = raw_input('SMTP host: ')
            if platform.system() == 'Windows':
                helpmsg = 'C-z'
            else:
                helpmsg = 'C-d'
            print >> sys.stdout, 'Body (%s to end): ' % helpmsg
        lines = sys.stdin.readlines()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print >> sys.stderr, 'Cannot read file !'
        if _debug:
            print >> sys.stderr, traceback.print_exc()
        sys.exit(2)

    mbody = ''
    for line in lines:
        mbody = mbody + unicode(line, dftlocale)

    if not files == '':
        lfiles = files.split(',')
    else:
        zip = False
        lfiles = []
    lmto = mto.encode('ascii').split(',')
    res = send(mfrom, lmto, msubject, mbody, lfiles, msmtphost, charset, zip, zipFilename)
    if not quiet:
        if res == 0:
            print >> sys.stdout, 'Email send.'
        elif res == 1:
            print >> sys.stdout, 'Email send (Warning detected).'
        elif res == 2:
            print >> sys.stderr, 'Email NOT send (SMTP error)'
        else:
            print >> sys.stderr, 'Email NOT send (Error) !'
    sys.exit(res)