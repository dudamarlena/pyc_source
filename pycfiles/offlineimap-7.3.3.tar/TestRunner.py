# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/official_packages/gitrepos/offlineimap/test/OLItest/TestRunner.py
# Compiled at: 2019-02-02 10:37:08
import offlineimap.virtual_imaplib2 as imaplib, unittest, logging, os, re, sys, shutil, subprocess, tempfile, random
random.seed()
from offlineimap.CustomConfig import CustomConfigParser
from . import default_conf

class OLITestLib:
    cred_file = None
    testdir = None
    cmd = None

    def __init__(self, cred_file=None, cmd='offlineimap'):
        """

        :param cred_file: file of the configuration
            snippet for authenticating against the test IMAP server(s).
        :param cmd: command that will be executed to invoke offlineimap"""
        OLITestLib.cred_file = cred_file
        if not os.path.isfile(cred_file):
            raise UserWarning("Please copy 'credentials.conf.sample' to '%s' and set your credentials there." % cred_file)
        OLITestLib.cmd = cmd

    @classmethod
    def create_test_dir(cls, suffix=''):
        """Creates a test directory and places OLI config there

        Note that this is a class method. There can only be one test
        directory at a time. OLITestLib is not suited for running
        several tests in parallel.  The user is responsible for
        cleaning that up herself."""
        assert cls.cred_file != None
        cls.testdir = os.path.abspath(tempfile.mkdtemp(prefix='tmp_%s_' % suffix, dir=os.path.dirname(cls.cred_file)))
        cls.write_config_file()
        return cls.testdir

    @classmethod
    def get_default_config(cls):
        """Creates a default ConfigParser file and returns it

        The returned config can be manipulated and then saved with
        write_config_file()"""
        assert cls.cred_file != None
        assert cls.testdir != None
        config = CustomConfigParser()
        config.readfp(default_conf)
        default_conf.seek(0)
        config.read(cls.cred_file)
        config.set('general', 'metadata', cls.testdir)
        return config

    @classmethod
    def write_config_file(cls, config=None):
        """Creates a OLI configuration file

        It is created in testdir (so create_test_dir has to be called
        earlier) using the credentials information given (so they had
        to be set earlier). Failure to do either of them will raise an
        AssertionException. If config is None, a default one will be
        used via get_default_config, otherwise it needs to be a config
        object derived from that."""
        if config is None:
            config = cls.get_default_config()
        localfolders = os.path.join(cls.testdir, 'mail')
        config.set('Repository Maildir', 'localfolders', localfolders)
        with open(os.path.join(cls.testdir, 'offlineimap.conf'), 'wt') as (f):
            config.write(f)
        return

    @classmethod
    def delete_test_dir(cls):
        """Deletes the current test directory

        The users is responsible for cleaning that up herself."""
        if os.path.isdir(cls.testdir):
            shutil.rmtree(cls.testdir)

    @classmethod
    def run_OLI(cls):
        """Runs OfflineImap

        :returns: (rescode, stdout (as unicode))
        """
        try:
            output = subprocess.check_output([
             cls.cmd,
             '-c%s' % os.path.join(cls.testdir, 'offlineimap.conf')], shell=False)
        except subprocess.CalledProcessError as e:
            return (
             e.returncode, e.output.decode('utf-8'))

        return (
         0, output.decode('utf-8'))

    @classmethod
    def delete_remote_testfolders(cls, reponame=None):
        """Delete all INBOX.OLITEST* folders on the remote IMAP repository

        reponame: All on `reponame` or all IMAP-type repositories if None"""
        config = cls.get_default_config()
        if reponame:
            sections = [
             ('Repository {0}').format(reponame)]
        else:
            sections = [ r for r in config.sections() if r.startswith('Repository')
                       ]
            sections = [ s for s in sections if config.get(s, 'Type').lower() == 'imap' ]
        for sec in sections:
            host = config.get(sec, 'remotehost')
            user = config.get(sec, 'remoteuser')
            passwd = config.get(sec, 'remotepass')
            imapobj = imaplib.IMAP4(host)
            imapobj.login(user, passwd)
            res_t, data = imapobj.list()
            assert res_t == 'OK'
            dirs = []
            for d in data:
                if d == '':
                    continue
                if isinstance(d, tuple):
                    folder = '"%s"' % d[1].replace('"', '\\"')
                else:
                    m = re.search('\n                        [ ]                     # space\n                        (?P<dir>\n                        (?P<quote>"?)           # starting quote\n                        ([^"]|\\\\")*             # a non-quote or a backslashded quote\n                        (?P=quote))$            # ending quote\n                        ', d, flags=re.VERBOSE)
                    folder = bytearray(m.group('dir'))
                    if not m.group('quote'):
                        folder = '"%s"' % folder
                dirs.append(folder)

            dirs = [ d for d in dirs if d.startswith('"INBOX.OLItest') or d.startswith('"INBOX/OLItest') ]
            for folder in dirs:
                res_t, data = imapobj.delete(folder)
                assert res_t == 'OK', ('Folder deletion of {0} failed with error:\n{1} {2}').format(folder.decode('utf-8'), res_t, data)

            imapobj.logout()

    @classmethod
    def create_maildir(cls, folder):
        """Create empty maildir 'folder' in our test maildir

        Does not fail if it already exists"""
        assert cls.testdir != None
        maildir = os.path.join(cls.testdir, 'mail', folder)
        for subdir in ('', 'tmp', 'cur', 'new'):
            try:
                os.makedirs(os.path.join(maildir, subdir))
            except OSError as e:
                if e.errno != 17:
                    raise

        return

    @classmethod
    def delete_maildir(cls, folder):
        """Delete maildir 'folder' in our test maildir

        Does not fail if not existing"""
        assert cls.testdir != None
        maildir = os.path.join(cls.testdir, 'mail', folder)
        shutil.rmtree(maildir, ignore_errors=True)
        return

    @classmethod
    def create_mail(cls, folder, mailfile=None, content=None):
        """Create a mail in  maildir 'folder'/new

        Use default mailfilename if not given.
        Use some default content if not given"""
        assert cls.testdir != None
        while True:
            mailfile = ('{0}:2,').format(random.randint(0, 999999999))
            mailfilepath = os.path.join(cls.testdir, 'mail', folder, 'new', mailfile)
            if not os.path.isfile(mailfilepath):
                break

        with open(mailfilepath, 'wb') as (mailf):
            mailf.write('From: test <test@offlineimap.org>\nSubject: Boo\nDate: 1 Jan 1980\nTo: test@offlineimap.org\n\nContent here.')
        return

    @classmethod
    def count_maildir_mails(cls, folder):
        """Returns the number of mails in maildir 'folder'

        Counting only those in cur&new (ignoring tmp)."""
        assert cls.testdir != None
        maildir = os.path.join(cls.testdir, 'mail', folder)
        boxes, mails = (0, 0)
        for dirpath, dirs, files in os.walk(maildir, False):
            if set(dirs) == set(['cur', 'new', 'tmp']):
                boxes += 1
            if dirpath.endswith(('/cur', '/new')):
                mails += len(files)

        return (
         boxes, mails)

    re_uidmatch = re.compile(',U=(\\d+)')

    @classmethod
    def get_maildir_uids(cls, folder):
        """Returns a list of maildir mail uids, 'None' if no valid uid"""
        assert cls.testdir != None
        mailfilepath = os.path.join(cls.testdir, 'mail', folder)
        assert os.path.isdir(mailfilepath)
        ret = []
        for dirpath, dirs, files in os.walk(mailfilepath):
            if not dirpath.endswith((os.path.sep + 'new', os.path.sep + 'cur')):
                continue
            for file in files:
                m = cls.re_uidmatch.search(file)
                uid = m.group(1) if m else None
                ret.append(uid)

        return ret