# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/local_repo.py
# Compiled at: 2020-01-02 17:45:38
import logging, os, git, dateutil.parser
from .util.filetypes import IGNORE_FILES
logger = logging.getLogger(__name__)
img_exts = ('jpg', 'jpeg', 'png', 'gif')
old_files = ['.travis.yml', '.travis.deploy.api_key.txt']

class LocalRepo(object):
    """ A class for interacting with a git repo """

    def __init__(self, repo_path, cloned_repo=None):
        if cloned_repo:
            self.git = cloned_repo
            self.repo_path = self.git.working_dir
            return
        self.repo_path = repo_path
        try:
            self.git = git.Repo(self.repo_path)
        except git.exc.InvalidGitRepositoryError:
            self.git = git.Repo.init(self.repo_path)

    def add_file(self, path):
        logger.debug('Staging this file: ' + str(self.git.untracked_files))
        self.git.index.add([path])

    def add_all_files(self):
        untracked_files = [ _file for _file in self.git.untracked_files if os.path.splitext(_file)[(-1)] not in IGNORE_FILES
                          ]
        logger.debug('Staging the following files: ' + str(untracked_files))
        self.git.index.add(untracked_files)
        return len(untracked_files)

    def remove_old_files(self):
        message = ''
        for old_file in old_files:
            path = os.path.join(self.repo_path, old_file)
            if os.path.exists(path):
                self.git.git.rm(path)
                message = 'Removed old files. '

        return message

    def commit(self, message):
        return self.git.index.commit(message)

    def update(self, message):
        self.git.git.add(update=True)
        self.git.index.commit(message)

    def tag(self, version):
        return self.git.create_tag(version, message='bump version')

    def no_tags(self):
        for tag in self.git.tags:
            return False

        return True

    def mod_date(self, path):
        if not path:
            return dateutil.parser.parse('1901-01-01 00:00:00+00:00')
        return dateutil.parser.parse(self.git.git.log('-1', '--format=%aI', '--', path))

    def cover_files(self):
        covers = []
        for root, dirs, files in os.walk(self.repo_path):
            files = [ f for f in files if not f[0] == '.' ]
            dirs[:] = [ d for d in dirs if not d[0] == '.' ]
            covers = covers + [ os.path.join(root, f)[len(self.repo_path) + 1:] for f in files if 'cover' in f and f.lower().split('.')[(-1)] in img_exts
                              ]

        return covers

    @property
    def metadata_file(self):
        if self.repo_path and os.path.isfile(os.path.join(self.repo_path, 'metadata.yaml')):
            return os.path.join(self.repo_path, 'metadata.yaml')
        else:
            return
            return