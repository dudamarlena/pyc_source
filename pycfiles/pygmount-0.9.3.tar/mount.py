# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simo/Projects/pygmount/pygmount/utils/mount.py
# Compiled at: 2014-04-03 08:05:48
from __future__ import unicode_literals, absolute_import
import datetime, sys, os, os.path, subprocess, time, apt, logging
from apt.cache import LockFailedException
from PyZenity import Question, GetText, InfoMessage, ErrorMessage, Progress
from pygmount.utils.utils import get_sudo_username, read_config, get_home_dir
FILE_RC = b'.pygmount.rc'

class MountSmbShares(object):
    """
    Classe di utilità per gestire il processo di montaggio di cartelle di rete
    condivise da server samba/windows.
    """

    def __init__(self, verbose=False, file=None, dry_run=False, shell_mode=False):
        self.verbose = verbose
        self.file = file
        self.dry_run = dry_run
        self.shell_mode = shell_mode
        self.pkgs_required = [b'smbfs']
        self.samba_shares = []
        self.sudo_env, self.host_username = get_sudo_username()
        self.cmd_mount = b'mount -t cifs //%(hostname)s/%(share)s %(mountpoint)s -o username="%(domain_username)s",uid=%(host_username)s,password="%(domain_password)s"'
        self.username = self.host_username if self.host_username else os.environ[b'USER']
        self.cmd_umount = b'umount %(mountpoint)s'
        self.msg_error = b'Impossibile collegare le unità di rete [%s].'
        self.home_dir = get_home_dir()
        logging.basicConfig(filename=(b'{}{}/.pygmount.log').format(self.home_dir, self.username), filemode=b'a', level=logging.INFO)

    def requirements(self):
        """
        Verifica che tutti i pacchetti apt necessari al "funzionamento" della
        classe siano installati. Se cosi' non fosse li installa.
        """
        cache = apt.cache.Cache()
        for pkg in self.pkgs_required:
            try:
                pkg = cache[pkg]
                if not pkg.is_installed:
                    try:
                        pkg.mark_install()
                        cache.commit()
                    except LockFailedException as lfe:
                        logging.error((b'Errore "{}" probabilmente l\'utente {} non ha i diritti di amministratore').format(lfe, self.username))
                        raise lfe
                    except Exception as e:
                        logging.error((b'Errore non classificato "{}"').format(e))

                    raise e
            except KeyError as ke:
                logging.error((b'Il pacchetto "{}" non e\' presente in questa distribuzione').format(pkg))

    def set_shares(self):
        """
        Setta la variabile membro 'self.samba_shares' il quale e' una lista
        di dizionari con i dati da passare ai comandi di "umount" e "mount".
        I vari dizionari sono popolati o da un file ~/.pygmount.rc e da un
        file passato dall'utente.
        """
        if self.file is None:
            self.file = os.path.expanduser(b'~%s/%s' % (self.host_username,
             FILE_RC))
        if not os.path.exists(self.file):
            error_msg = b"Impossibile trovare il file di configurazione '%s'.\nLe unità di rete non saranno collegate." % FILE_RC.lstrip(b'.')
            if not self.shell_mode:
                ErrorMessage(error_msg)
            logging.error(error_msg)
            sys.exit(5)
        if self.verbose:
            logging.warning(b'File RC utilizzato: %s', self.file)
        self.samba_shares = read_config(self.file)
        return

    def run(self):
        """
        Esegue il montaggio delle varie condivisioni chiedendo all'utente
        username e password di dominio.
        """
        logging.info((b'start run with "{}" at {}').format(self.username, datetime.datetime.now()))
        progress = Progress(text=b'Controllo requisiti software...', pulsate=True, auto_close=True)
        progress(1)
        try:
            self.requirements()
        except LockFailedException as lfe:
            ErrorMessage((b'Errore "{}" probabilmente l\'utente {} non ha i diritti di amministratore').format(lfe, self.username))
            sys.exit(20)
        except Exception as e:
            ErrorMessage((b"Si e' verificato un errore generico: {}").format(e))
            sys.exit(21)

        progress(100)
        self.set_shares()
        insert_msg = b"Inserisci l'utente del Dominio/Posta Elettronica"
        default_username = self.host_username if self.host_username else os.environ[b'USER']
        self.domain_username = GetText(text=insert_msg, entry_text=self.username)
        if self.domain_username is None or len(self.domain_username) == 0:
            error_msg = b'Inserimento di un username di dominio vuoto'
            ErrorMessage(self.msg_error % error_msg)
            sys.exit(2)
        insert_msg = b'Inserisci la password del Dominio/Posta Elettronica'
        self.domain_password = GetText(text=insert_msg, entry_text=b'password', password=True)
        if self.domain_password is None or len(self.domain_password) == 0:
            error_msg = b'Inserimento di una password di dominio vuota'
            ErrorMessage(self.msg_error % error_msg)
            sys.exit(3)
        progress_msg = b'Collegamento unità di rete in corso...'
        progress = Progress(text=progress_msg, pulsate=True, auto_close=True)
        progress(1)
        result = []
        for share in self.samba_shares:
            print b'#######'
            print share
            if b'mountpoint' not in share.keys():
                mountpoint = os.path.expanduser(b'~%s/%s/%s' % (self.host_username,
                 share[b'hostname'],
                 share[b'share']))
                share.update({b'mountpoint': mountpoint})
            elif not share[b'mountpoint'].startswith(b'/'):
                mountpoint = os.path.expanduser(b'~%s/%s' % (self.host_username, share[b'mountpoint']))
                share.update({b'mountpoint': mountpoint})
            share.update({b'host_username': self.host_username, 
               b'domain_username': share.get(b'username', self.domain_username), 
               b'domain_password': share.get(b'password', self.domain_password)})
            if not os.path.exists(share[b'mountpoint']):
                if self.verbose:
                    logging.warning(b'Mountpoint "%s" not exist.' % share[b'mountpoint'])
                if not self.dry_run:
                    os.makedirs(share[b'mountpoint'])
            umont_cmd = self.cmd_umount % share
            if self.verbose:
                logging.warning(b'Umount command: %s' % umont_cmd)
            if not self.dry_run:
                umount_p = subprocess.Popen(umont_cmd, shell=True)
                returncode = umount_p.wait()
                time.sleep(2)
            mount_cmd = self.cmd_mount % share
            if self.verbose:
                placeholder = b',password='
                logging.warning(b'Mount command: %s%s' % (
                 mount_cmd.split(placeholder)[0], placeholder + b'******"'))
            print mount_cmd
            print b'#######'

        progress(100)
        if self.verbose:
            logging.warning(b'Risultati: %s' % result)
        return