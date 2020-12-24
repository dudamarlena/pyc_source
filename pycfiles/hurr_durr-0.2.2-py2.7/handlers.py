# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hurr_durr/handlers.py
# Compiled at: 2014-10-26 10:28:00
import sqlite3, time, errno
from json import dumps
import logging
from abc import ABCMeta, abstractmethod
from genericpath import exists
from os import makedirs, sep
logger = logging.getLogger(__name__)
_POSTS_CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS posts(\n          no INTEGER PRIMARY KEY,\n          resto INTEGER,\n          sticky INTEGER,\n          closed INTEGER,\n          archived INTEGER,\n          now TEXT,\n          time INTEGER,\n          name TEXT,\n          trip TEXT,\n          id TEXT,\n          capcode TEXT,\n          country TEXT,\n          country_name TEXT,\n          sub TEXT,\n          com TEXT,\n          tim INTEGER,\n          filename TEXT,\n          ext TEXT,\n          fsize INTEGER,\n          md5 TEXT,\n          w INTEGER,\n          h INTEGER,\n          tn_w INTEGER,\n          tn_h INTEGER,\n          filedeleted INTEGER,\n          spoiler INTEGER,\n          custom_spoiler INTEGER,\n          omitted_posts INTEGER,\n          omitted_images INTEGER,\n          replies INTEGER,\n          images INTEGER,\n          bumplimit INTEGER,\n          imagelimit INTEGER,\n          capcode_replies TEXT,\n          last_modified INTEGER,\n          tag TEXT,\n          semantic_url TEXT\n        );'
_POSTS_INSERT = 'INSERT INTO posts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

def _get_date_string():
    return time.strftime('%Y%m%d')


class Handler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def post(self, thread_id, new_post):
        """Handle a new post.

        thread_id -- the thread's ID
        new_post -- the new post dict that has just arrived. Check 4chan API (https://github.com/4chan/4chan-API)
            for full possible contents, but most notable keys are
            no : post number
            resto : number of post that this post is a response to
            time : a UNIX timestamp of post's time
            com : the text, contains escaped HTML
        """
        raise NotImplementedError('Implement post(thread_id, new_post) in subclass')

    @abstractmethod
    def pruned(self, thread_id):
        """Handles thread pruning.

        thread_id -- the thread ID that was pruned from 4chan
        """
        raise NotImplementedError('Implement pruned(thread_id) in subclass')

    @abstractmethod
    def img(self, thread_id, filename, data):
        """Handles image downloads.

        thread_id -- ID of thread in which image was posted
        filename -- the image's filename with extensions
        data -- bytes, image content
        """
        raise NotImplementedError('Implement img(thread_id, filename, data) in subclass')

    @abstractmethod
    def download_img(self, thread_id, filename):
        """Checks whether the image needs to be downloaded.

        Needed to avoid downloading the same image multiple times. Prime use-case is resumed operation.

        thread_id -- the thread ID for thread containing the image
        filename -- the image's file name
        """
        raise NotImplementedError('Implement download_img(thread_id, filename) in subclass')


class SQLitePersister(object):

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute(_POSTS_CREATE_TABLE)
        self.connection.commit()

    @staticmethod
    def _post_to_data_tuple(post):
        return (
         post.get('no'),
         post.get('resto'),
         post.get('sticky'),
         post.get('closed'),
         post.get('archived'),
         post.get('now'),
         post.get('time'),
         post.get('name'),
         post.get('trip'),
         post.get('id'),
         post.get('capcode'),
         post.get('country'),
         post.get('country_name'),
         post.get('sub'),
         post.get('com'),
         post.get('tim'),
         post.get('filename'),
         post.get('ext'),
         post.get('fsize'),
         post.get('md5'),
         post.get('w'),
         post.get('h'),
         post.get('tn_w'),
         post.get('tn_h'),
         post.get('filedeleted'),
         post.get('spoiler'),
         post.get('custom_spoiler'),
         post.get('omitted_posts'),
         post.get('omitted_images'),
         post.get('replies'),
         post.get('images'),
         post.get('bumplimit'),
         post.get('imagelimit'),
         dumps(post['capcode_replies']) if post.get('capcode_replies') else None,
         post.get('last_modified'),
         post.get('tag'),
         post.get('semantic_url'))

    def persist(self, posts):
        _posts = None
        if isinstance(posts, dict):
            _posts = [
             posts]
        else:
            try:
                _ = iter(posts)
            except TypeError:
                _posts = [
                 posts]
            else:
                _posts = posts

        data = map(self._post_to_data_tuple, _posts)
        try:
            self.cursor.executemany(_POSTS_INSERT, data)
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass
        except sqlite3.Error:
            logger.exception('SQLite error')

        return

    def close(self):
        self.connection.commit()
        self.connection.close()


class RotatingSQLitePostPersister(object):

    def __init__(self, root_dir):
        if root_dir.endswith(sep):
            root_dir = root_dir[:len(sep)]
        try:
            makedirs(root_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self.curr_date_str = _get_date_string()
        self.root_dir = root_dir
        self.db = SQLitePersister(self._make_db_path())

    def _make_db_path(self):
        return ('{root}{sep}{date_str}.db').format(root=self.root_dir, sep=sep, date_str=self.curr_date_str)

    def _rotate_db_if_new_day(self):
        date_str = _get_date_string()
        if self.curr_date_str != date_str:
            self.curr_date_str = date_str
            self.db.close()
            self.db = SQLitePersister(self._make_db_path())

    def persist_post(self, post):
        self._rotate_db_if_new_day()
        self.db.persist(post)


class SQLiteHandler(Handler):
    """Handler that writes posts to an SQLite DB. Doesn't handle images.

    Posts are persisted as they come in.
    """

    def __init__(self, root_dir):
        self.persister = RotatingSQLitePostPersister(root_dir)

    def pruned(self, thread_id):
        pass

    def post(self, thread_id, new_post):
        self.persister.persist_post(new_post)

    def download_img(self, thread_id, filename):
        raise TypeError('SQLiteHandler does not support images')

    def img(self, thread_id, filename, data):
        raise TypeError('SQLiteHandler does not support images')


class FileHandler(Handler):
    """Handler that writes things to the file system.

    Threads are purged to disk when they get pruned from 4chan and held in-memory before they are.

    The directory structure is root/thread_id/[thread_id.json | thread images].
    """

    def __init__(self, file_root):
        """Makes a new FileHandler

        file_root -- the directory to which data will be purged. If it does not exist, it will be created.
        """
        if file_root.endswith(sep):
            file_root = file_root[:len(sep)]
        self._file_root = file_root
        try:
            makedirs(self._file_root)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        self._active_threads = dict()
        self._thread_roots = dict()

    def _get_thread_root(self, thread_id):
        if thread_id not in self._thread_roots:
            return ('{file_root}{sep}{date}{sep}{thread_id}').format(file_root=self._file_root, thread_id=thread_id, date=_get_date_string(), sep=sep)
        else:
            return self._thread_roots[thread_id]

    def post(self, thread_id, new_post):
        if thread_id not in self._active_threads:
            thread_file_root = self._get_thread_root(thread_id)
            try:
                makedirs(thread_file_root)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e

            self._active_threads[thread_id] = []
            self._thread_roots[thread_id] = thread_file_root
        self._active_threads[thread_id].append(new_post)

    def pruned(self, thread_id):
        """Handles thread pruning, writes content to JSON on disk.

        thread_id -- the thread ID that was pruned from 4chan
        """
        if thread_id in self._active_threads:
            filename = ('{thread_root}{sep}{thread_id}.json').format(thread_root=self._get_thread_root(thread_id), thread_id=thread_id, sep=sep)
            with open(filename, 'w') as (f):
                f.write(dumps({'posts': self._active_threads[thread_id]}))
            del self._active_threads[thread_id]
            del self._thread_roots[thread_id]

    def img(self, thread_id, filename, data):
        """Handles image downloads, writes content to disk in thread_id directory.

        thread_id -- ID of thread in which image was posted
        filename -- the image's filename with extensions
        data -- bytes, image content
        """
        full_filename = ('{thread_root}{sep}{img_filename}').format(thread_root=self._get_thread_root(thread_id), img_filename=filename, sep=sep)
        with open(full_filename, 'w') as (f):
            f.write(data)

    def download_img(self, thread_id, filename):
        """Checks whether the image already exists.

        Needed to avoid downloading the same image multiple times. Prime use-case is resumed operation.

        thread_id -- the thread ID for thread containing the image
        filename -- the image's file name
        """
        return not exists(('{file_root}{sep}{thread_id}{sep}{filename}').format(file_root=self._file_root, thread_id=thread_id, filename=filename, sep=sep))