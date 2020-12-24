# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zed/venvs/4ch/lib/python2.7/site-packages/fourch/thread.py
# Compiled at: 2014-09-20 11:32:19
import requests
from .reply import Reply

class Thread(object):
    """ This object stores information about the given thread.
        It has a list of fourch.replies, as well as options to
        easily pull in updates (new posts), and create an instance
        with the json of a thread.
    """

    def __init__(self, board, res):
        """ Create the thread instance and initialize variables.

            :param board: the :class:`fourch.Board` parent instance
            :type board: :class:`fourch.Board`
            :param res: the given threads number
            :type res: str or int
        """
        self._board = board
        self.res = res
        self.alive = True
        self.op = None
        self.replies = []
        self.omitted_posts = 0
        self.omitted_images = 0
        self._should_update = False
        self._last_modified = None
        return

    def __repr__(self):
        end = ''
        if self.omitted_posts or self.omitted_images:
            end = (', {0} omitted posts, {1} omitted images').format(self.omitted_posts, self.omitted_images)
        return ('<{0} /{1}/{2}, {3} replies{4}>').format(self.__class__.__name__, self._board.name, self.res, len(self.replies), end)

    @staticmethod
    def from_req(board, res, r):
        """ Create a thread object from the given request.
            If the thread has 404d, this will return None,
            and if it isn't 200 OK, it will raise_for_status().
            Actually creates the thread by calling :func:`from_json`.

            :param board: the :class:`fourch.Board` parent instance
            :type board: :class:`fourch.Board`
            :param res: the given threads number
            :type res: str or int
            :param r: the requests object
            :type r: requests.models.Response
        """
        if r.status_code == requests.codes.not_found:
            return
        else:
            if r.status_code == requests.codes.ok:
                return Thread.from_json(board, r.json(), res=res, last_modified=r.headers['last-modified'])
            r.raise_for_status()
            return

    @staticmethod
    def from_json(board, json, res=None, last_modified=None):
        """ Create a thread object from the given JSON data.

            :param board: the :class:`fourch.Board` parent instance
            :type board: :class:`fourch.Board`
            :param json: the json data from the 4chan API
            :type board: dict
            :param res: the given threads number
            :type res: str or int
            :param last_modified: when was the page last modified
            :type last_modified: int or None
            :return: the created :class:`fourch.Thread`
            :rtype: :class:`fourch.Thread`
        """
        t = Thread(board, res)
        t._last_modified = last_modified
        replies = json['posts']
        t.op = Reply(t, replies.pop(0))
        t.replies = [ Reply(t, r) for r in replies ]
        if res is None:
            t._should_update = True
            t.res = t.op.number
            t.omitted_posts = t.op._json.get('omitted_posts', 0)
            t.omitted_images = t.op._json.get('omitted_images', 0)
        return t

    @property
    def sticky(self):
        """ Is this thread stuck?

            :return: whether or not the thread is stuck
            :rtype: bool
        """
        return self.op.sticky

    @property
    def closed(self):
        """ Is the thread closed?

            :return: whether or not the thread is closed
            :rtype: bool
        """
        return self.op.closed

    @property
    def last_reply(self):
        """ Return the last :class:`fourch.Reply` to the thread, or the op
            if there are no replies.

            :return: the last :class:`fourch.Reply` to the thread.
            :rtype: :class:`fourch.Reply`
        """
        if not self.replies:
            return self.op
        return self.replies[(-1)]

    @property
    def images(self):
        """ Create a generator which yields all of the image urls for the thread.

            :return: a generator yieling all image urls
            :rtype: generator
        """
        yield self.op.file.url
        for r in self.replies:
            if not r.has_file:
                continue
            yield r.file.url

    def update(self, force=False):
        """ Update the thread, pulling in new replies,
            appending them to the reply pool.

            :param force: should replies be replaced with fresh reply objects
            :type force: bool
            :return: the number of new replies
            :rtype: int
        """
        if not self.alive and not force:
            return 0
        else:
            url = self._board.url('api_thread', board=self._board.name, thread=self.res)
            headers = None
            if self._last_modified:
                headers = {'If-Modified-Since': self._last_modified}
            r = self._board._session.get(url, headers=headers)
            if r.status_code == requests.codes.not_modified:
                return 0
            if r.status_code == requests.codes.not_found:
                self.alive = False
                self._board._cache.pop(self.res, None)
                return 0
            if r.status_code == requests.codes.ok:
                if not self.alive:
                    self.alive = True
                    self._board._cache[self.res] = self
                self._should_update = False
                self.omitted_posts = 0
                self.omitted_images = 0
                self._last_modified = r.headers['last-modified']
                replies = r.json()['posts']
                post_count = len(self.replies)
                self.op = Reply(self, replies.pop(0))
                if not force:
                    self.replies.extend([ Reply(self, p) for p in replies if p['no'] > self.last_reply.number
                                        ])
                else:
                    self.replies = [ Reply(self, p) for p in replies ]
                post_count_new = len(self.replies)
                post_count_diff = post_count_new - post_count
                if post_count_diff < 0:
                    raise Exception('post count delta is somehow negative...')
                return post_count_diff
            r.raise_for_status()
            return