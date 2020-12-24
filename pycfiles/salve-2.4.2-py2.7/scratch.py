# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/util/scratch.py
# Compiled at: 2015-11-06 23:45:35
import os, tempfile, shutil, mock, textwrap
from salve import paths
from tests.util import MockedGlobals

class ScratchContainer(MockedGlobals):
    default_settings_content = textwrap.dedent("\n        [global]\n        backup_dir=$HOME/backups\n        backup_log=$HOME/backup.log\n\n        log_level=DEBUG\n        # run_log=$HOME/.salve/run_log\n\n        [default]\n        user=$USER # an inline comment\n        group=$SALVE_USER_PRIMARY_GROUP'\n\n        [file]\n        action=copy\n        mode=600\n\n        [directory]\n        action=copy\n        mode=755\n\n        [manifest]\n        ")

    def __init__(self):
        MockedGlobals.__init__(self)
        self.patches = set()
        self.scratch_dir = tempfile.mkdtemp()
        mock_env = {'SUDO_USER': 'user1', 
           'USER': 'user1', 
           'HOME': self.get_fullname('home/user1')}
        self.username = 'user1'
        self.sudouser = 'user1'
        self.userhome = 'home/user1'
        os.makedirs(mock_env['HOME'])
        self.patches.add(mock.patch.dict('os.environ', mock_env))

        def get_groupname(user):
            if user == 'user1':
                return 'group1'
            else:
                return 'nogroup'

        real_expanduser = os.path.expanduser

        def expanduser(path):
            if path.strip() == '~user1':
                return mock_env['HOME']
            else:
                return real_expanduser(path)

        settings_loc = os.path.join(mock_env['HOME'], 'settings.ini')
        self.write_file(settings_loc, self.default_settings_content)
        real_open = open

        def mock_open(path, *args, **kwargs):
            if os.path.abspath(path) == paths.get_default_config():
                return real_open(settings_loc, *args, **kwargs)
            else:
                return real_open(path, *args, **kwargs)

        self.patches.add(mock.patch('salve.ugo.get_group_from_username', get_groupname))
        real_uid = os.geteuid()
        real_gid = os.getegid()
        self.patches.add(mock.patch('salve.ugo.name_to_uid', lambda x: real_uid))
        self.patches.add(mock.patch('salve.ugo.name_to_gid', lambda x: real_gid))
        self.patches.add(mock.patch('os.path.expanduser', expanduser))
        try:
            import builtins
            self.patches.add(mock.patch('builtins.open', mock_open))
        except ImportError:
            import __builtin__ as builtins
            self.patches.add(mock.patch('__builtin__.open', mock_open))

    def setUp(self):
        MockedGlobals.setUp(self)
        for p in self.patches:
            p.start()

    def tearDown(self):
        MockedGlobals.tearDown(self)

        def recursive_chmod(d):
            os.chmod(d, 511)
            for f in os.listdir(d):
                fullname = os.path.join(d, f)
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    recursive_chmod(fullname)

        recursive_chmod(self.scratch_dir)
        shutil.rmtree(self.scratch_dir)
        for p in self.patches:
            p.stop()

    def get_backup_path(self, backup_dir):
        return os.path.join(self.get_fullname(backup_dir), 'files')

    def make_dir(self, relpath):
        full_path = self.get_fullname(relpath)
        try:
            os.makedirs(full_path)
        except OSError as e:
            if e.errno == 17:
                return
            raise

    def exists(self, relpath):
        return os.path.exists(self.get_fullname(relpath))

    def listdir(self, relpath):
        return os.listdir(self.get_fullname(relpath))

    def write_file(self, relpath, content):
        with open(self.get_fullname(relpath), 'w') as (f):
            f.write(content)

    def read_file(self, relpath):
        filename = os.path.join(self.scratch_dir, relpath)
        with open(filename, 'r') as (f):
            return f.read()

    def get_mode(self, relpath):
        return os.stat(self.get_fullname(relpath)).st_mode & 511

    def get_fullname(self, relpath):
        return os.path.join(self.scratch_dir, relpath)