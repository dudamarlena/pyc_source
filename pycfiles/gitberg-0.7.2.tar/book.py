# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/book.py
# Compiled at: 2020-01-02 21:47:21
from __future__ import print_function
import gc, logging, os, shutil, github3, semver, sh
from re import sub
from six import text_type as unicodestr
import unicodedata
from . import config
from .clone import clone
from .fetch import BookFetcher
from .make import NewFilesHandler
from .local_repo import LocalRepo
from .parameters import GITHUB_ORG
from .push import GithubRepo
from .util import tenprintcover
from .util.catalog import BookMetadata, get_repo_name, NoRDFError
from .util.pg import source_start
logger = logging.getLogger(__name__)

class Book:
    """ An index card tells you where a book lives
        `book_id` is PG's unique book id
        `remote_path` is where it should live on PG servers
        `repo_name` is the name the repo should have on GitHub
        `local_path` is where it IS stored locally
        `local_repo` the repo at `local_path`
        `library_path` local directory where repos will live
        `rdf_library` local directory where rdf has been cached
    """

    def __init__(self, book_id, repo_name=None, library_path='./library', rdf_library=None, local=False, cache={}):
        arg_repo_name = repo_name
        self.local_path = None
        self.repo_name = None
        self.rdf_library = rdf_library
        self.local_repo = None
        self.cache = cache
        self.local = local
        self._repo = None
        self.library_path = config.get_library_path(library_path)
        if not self.rdf_library:
            self.rdf_library = config.data.get('rdf_library', '')
        if arg_repo_name and not book_id:
            maybe_book_id = arg_repo_name.split('_')[(-1)]
            try:
                book_id = str(int(maybe_book_id))
            except ValueError:
                pass

        if book_id:
            self.book_id = str(book_id)
            self.set_local_path_ifexists(self.book_id)
            try:
                self.parse_book_metadata()
            except NoRDFError:
                logger.error(('no rdf file exists for {}').format(self.book_id))
                raise NoRDFError

        else:
            self.book_id = None
        if arg_repo_name and not self.local_path:
            self.set_local_path_ifexists(arg_repo_name)
        if self.repo_name and not self.local_path:
            self.set_local_path_ifexists(self.repo_name)
        if not local:
            self.github_repo = self.get_github()
        return

    def get_github(self):
        gh = self.cache.get('github', None)
        if gh:
            gh.book = self
        else:
            gh = GithubRepo(self)
            self.cache['github'] = gh
        return gh

    def set_local_repo(self):
        if self.local_repo:
            return
        else:
            if self.local_path:
                self.local_repo = LocalRepo(self.local_path)
            else:
                self.local_repo = None
            return

    def set_local_path_ifexists(self, name):
        if self.local_path:
            return
        path = os.path.join(self.library_path, name)
        if os.path.exists(path):
            self.local_path = path
            logger.info(('local_path set to {}').format(path))
            self.parse_book_metadata()
        self.set_local_repo()

    def make_local_path(self):
        path = os.path.join(self.library_path, self.book_id)
        if not os.path.exists(path):
            try:
                try:
                    os.makedirs(path)
                    self.local_path = path
                except OSError:
                    logger.error(("couldn't make path: {}").format(path))

            finally:
                os.chmod(path, 511)

    def parse_book_metadata(self):
        if self.local_repo and self.local_repo.metadata_file:
            logger.debug('using %s' % self.local_repo.metadata_file)
            self.meta = BookMetadata(self, datafile=self.local_repo.metadata_file)
            self.repo_name = self.meta._repo
            return 'update metadata '
        if self.repo_name:
            named_path = os.path.join(self.library_path, self.repo_name, 'metadata.yaml')
            logger.info('trying %s' % named_path)
            if os.path.exists(named_path):
                self.meta = BookMetadata(self, datafile=named_path)
                self.repo_name = self.meta._repo
                return 'update metadata '
        logger.debug('using RDF')
        self.meta = BookMetadata(self, rdf_library=self.rdf_library, enrich=not self.local)
        if self.repo_name:
            self.meta.metadata['_repo'] = self.repo_name
            logger.debug(('using existing repo name: {}').format(self.repo_name))
            return 'existing repo'
        if self.book_id:
            self.repo_name = get_repo_name(self.book_id)
            self.meta.metadata['_repo'] = self.repo_name
            if self.repo_name != self.book_id:
                return 'redone repo'
        self.repo_name = self.format_title()
        return 'new repo '

    @property
    def remote_path(self):
        """ turns an ebook_id into a path on PG's server(s)
            4443  -> 4/4/4/4443/ """
        if len(self.book_id) > 1:
            path_parts = list(self.book_id[:-1])
        else:
            path_parts = [
             '0']
        path_parts.append(self.book_id)
        return os.path.join(*path_parts) + '/'

    def fetch(self):
        """ just pull files from PG
        """
        if not self.local_path:
            self.make_local_path()
        fetcher = BookFetcher(self)
        fetcher.fetch()

    def clone_from_github(self):
        if self.local_repo:
            pass
        else:
            self.local_repo = clone(self.repo_name)
            self.local_path = self.local_repo.repo_path
        self.parse_book_metadata()

    def make(self):
        """ turn fetched files into a local repo, make auxiliary files
        """
        logger.debug('preparing to add all git files')
        num_added = self.local_repo.add_all_files()
        if num_added:
            self.local_repo.commit('Initial import from Project Gutenberg')
        file_handler = NewFilesHandler(self)
        file_handler.add_new_files()
        num_added = self.local_repo.add_all_files()
        if num_added:
            self.local_repo.commit('Updates Readme, contributing, license files, cover, metadata.')

    def save_meta(self):
        self.meta.dump_file(os.path.join(self.local_path, 'metadata.yaml'))

    def push(self):
        """ create a github repo and push the local repo into it
        """
        self.github_repo.create_and_push()
        self._repo = self.github_repo.repo
        return self._repo

    def update(self, message='Update files'):
        """ commit changes
        """
        self.github_repo.update(message)

    def tag(self, version='bump', message=''):
        """ tag and commit
        """
        self.clone_from_github()
        self.github_repo.tag(version, message=message)

    def repo(self):
        if self._repo:
            return self._repo
        if self.repo_name:
            self._repo = self.github_repo.github.repository(GITHUB_ORG, self.repo_name)
            return self._repo

    def all(self):
        try:
            try:
                self.fetch()
                if not self.local_repo:
                    self.local_repo = LocalRepo(self.local_path)
                self.make()
                self.push()
                logger.info(('{0} {1} added').format(self.book_id, self.meta._repo))
                self.github_repo.tag('0.1.0', message='initial tag from Project Gutenberg')
            except sh.ErrorReturnCode_12:
                logger.error(('{0} {1} timeout').format(self.book_id, self.meta._repo))
            except sh.ErrorReturnCode_23:
                logger.error(('{0} {1} notfound').format(self.book_id, self.meta._repo))
            except github3.GitHubError as e:
                logger.error(('{0} {1} already').format(self.book_id, self.meta._repo))
            except sh.ErrorReturnCode_1:
                logger.error(('{0} {1} nopush').format(self.book_id, self.meta._repo))

        finally:
            self.remove()

    def remove(self):
        gc.collect()
        if self.local_repo:
            self.local_repo.git.git.clear_cache()
            shutil.rmtree(self.local_path)

    def format_title(self):

        def asciify(_title):
            _title = unicodedata.normalize('NFD', unicodestr(_title))
            ascii = True
            out = []
            ok = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM- ',"
            for ch in _title:
                if ch in ok:
                    out.append(ch)
                elif unicodedata.category(ch)[0] == 'L':
                    out.append(hex(ord(ch)))
                    ascii = False
                elif ch in '\r\n\t':
                    out.append('-')

            return (
             ascii, sub("[ ',-]+", '-', ('').join(out)))

        ascii, _title = asciify(self.meta.title)
        if not ascii and self.meta.alternative_title:
            ascii, _title2 = asciify(self.meta.alternative_title)
            if ascii:
                _title = _title2
        title_length = 99 - len(str(self.book_id)) - 1
        if len(_title) > title_length:
            repo_title = ('{0}__{1}').format(_title[:title_length], self.book_id)
        else:
            repo_title = ('{0}_{1}').format(_title[:title_length], self.book_id)
        logger.debug('%s %s' % (len(repo_title), repo_title))
        self.meta.metadata['_repo'] = repo_title
        return repo_title

    def generate_cover(self):
        if not self.meta:
            self.parse_book_metadata()
        try:
            cover_image = tenprintcover.draw(self.meta.title_no_subtitle, self.meta.subtitle, self.meta.authors_short())
            return cover_image
        except OSError:
            logger.error('OSError, probably Cairo not installed.')
            return

        return

    def add_covers(self):
        new_covers = []
        comment = ''
        for cover in self.meta.covers:
            cover_path = os.path.join(self.local_path, cover.get('image_path', ''))
            if os.path.isfile(cover_path):
                new_covers.append(cover)

        if len(new_covers) == 0:
            cover_files = self.local_repo.cover_files() if self.local_repo else []
            if cover_files:
                new_covers.append({'image_path': cover_files[0], 'cover_type': 'archival'})
                comment = 'Added archival cover. '
            else:
                with open(('{}/cover.png').format(self.local_path), 'wb+') as (cover):
                    self.generate_cover().save(cover)
                    new_covers.append({'image_path': 'cover.png', 'cover_type': 'generated'})
                comment = 'Generated cover. '
            if '_version' in self.meta.metadata:
                self.meta.metadata['_version'] = semver.bump_minor(self.meta._version)
            else:
                self.meta.metadata['_version'] = '0.1.0'
        self.meta.metadata['covers'] = new_covers
        return comment

    def source_mod_date(self):
        if not self.book_id or not self.local_path:
            return
        source_file = source_start(self.local_path, self.book_id)
        return self.local_repo.mod_date(source_file)