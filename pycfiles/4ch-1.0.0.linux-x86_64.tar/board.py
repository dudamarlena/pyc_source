# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zed/venvs/4ch/lib/python2.7/site-packages/fourch/board.py
# Compiled at: 2014-09-20 11:39:14
import requests, fourch
from .thread import Thread

class Board(object):
    """ fourch.Board is the master instance which allows easy access to the
        creation of thread objects.
    """

    def __init__(self, name, https=False):
        """ Create the board instance, and initialize internal variables.

            :param name: The board name, minus slashes. e.g., 'b', 'x', 'tv'
            :type name: string
            :param https: Should we use HTTPS or HTTP?
            :type https: bool
        """
        self.name = name
        self.https = https
        self._session = None
        self._cache = {}
        return

    def __repr__(self):
        return ('<{0} /{1}/>').format(self.__class__.__name__, self.name)

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            uaf = 'fourch/{0} (@https://github.com/sysr-q/4ch)'
            self._session.headers.update({'User-agent': uaf.format(fourch.__version__)})
        return self._session

    @property
    def proto(self):
        if self.https:
            return 'https://'
        return 'http://'

    def url(self, endpoint, *k, **v):
        return self.proto + fourch.urls['api'] + fourch.urls[endpoint].format(*k, **v)

    def catalog(self):
        """ Get a list of all the thread OPs and last replies.
        """
        url = self.url('api_catalog', board=self.name)
        r = self.session.get(url)
        return r.json()

    def threads(self):
        """ Get a list of all the threads alive, and which page they're on.

            You can cross-reference this with a threads number to see which
            page it's on at the time of calling.
        """
        url = self.url('api_threads', board=self.name)
        r = self.session.get(url)
        return r.json()

    def thread(self, res, update_cache=True):
        """ Create a :class:`fourch.thread` object.
            If the thread has already been fetched, return the cached thread.

            :param res: the thread number to fetch
            :type res: str or int
            :param update_cache: should we update if it's cached?
            :type update_cache: bool
            :return: the :class:`fourch.Thread` object
            :rtype: :class:`fourch.Thread` or None
        """
        if res in self._cache:
            t = self._cache[res]
            if update_cache:
                t.update()
            return t
        url = self.url('api_thread', board=self.name, thread=res)
        r = self.session.get(url)
        t = Thread.from_req(self, res, r)
        if t is not None:
            self._cache[res] = t
        return t

    def page(self, page=1, update_each=False):
        """ Return all the threads in a single page.
            The page number is one-indexed. First page is 1, second is 2, etc.

            If a thread has already been cached, return the cache entry rather
            than making a new thread.

            :param page: page to pull threads from
            :type page: int
            :param update_each: should each thread be updated, to pull all
                                replies
            :type update_each: bool
            :return: a list of :class:`fourch.Thread` objects, corresponding to
                     all threads on given page
            :rtype: list
        """
        url = self.url('api_board', board=self.name, page=page)
        r = self.session.get(url)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        json = r.json()
        threads = []
        for thj in json['threads']:
            t = None
            res = thj['posts'][0]['no']
            if res in self._cache:
                t = self._cache[res]
                t._should_update = True
            else:
                t = Thread.from_json(self, thj, last_modified=r.headers['last-modified'])
                self._cache[res] = t
            if update_each:
                t.update()
            threads.append(t)

        return threads

    def thread_exists(self, res):
        """ Figure out whether or not a thread exists.
            This is as easy as checking if it 404s.

            :param res: the thread number to fetch
            :type res: str or int
            :return: whether or not the given thread exists
            :rtype: bool
        """
        url = self.url('api_thread', board=self.name, thread=res)
        return self.session.head(url).status_code == requests.codes.ok