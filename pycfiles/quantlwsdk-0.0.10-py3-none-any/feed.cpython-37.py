# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\twitter\feed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5802 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import threading, json
from six.moves import queue
import tweepy
from tweepy import streaming
from pyalgotrade import observer
import pyalgotrade.logger
logger = pyalgotrade.logger.getLogger('twitter')

class Listener(streaming.StreamListener):

    def __init__(self, queue):
        super(Listener, self).__init__()
        self._Listener__queue = queue

    def on_connect(self):
        logger.info('Connected.')

    def on_timeout(self):
        logger.error('Timeout.')

    def on_data(self, data):
        self._Listener__queue.put(data)
        return True

    def on_error(self, status):
        logger.error(status)
        return False


class TwitterFeed(observer.Subject):
    __doc__ = 'Class responsible for connecting to Twitter\'s public stream API and dispatching events.\n    Check https://dev.twitter.com/docs/streaming-apis/streams/public for more information.\n\n    :param consumerKey: Consumer key.\n    :type consumerKey: string.\n    :param consumerSecret: Consumer secret.\n    :type consumerSecret: string.\n    :param accessToken: Access token.\n    :type accessToken: string.\n    :param accessTokenSecret: Access token secret.\n    :type accessTokenSecret: string.\n    :param track: A list of phrases which will be used to determine what Tweets will be delivered\n        on the stream. A phrase may be one or more terms separated by spaces, and a phrase will match\n        if all of the terms in the phrase are present in the Tweet, regardless of order and ignoring case.\n    :type track: list.\n    :param follow: A list of user IDs, indicating the users whose Tweets should be delivered on the\n        stream. Following protected users is not supported.\n    :type follow: list.\n    :param languages: A list of language IDs a defined in http://tools.ietf.org/html/bcp47.\n    :type languages: list.\n\n    .. note::\n        * Go to http://dev.twitter.com and create an app. The consumer key and secret will be generated for you after that.\n        * Create an access token under the "Your access token" section.\n        * At least **track** or **follow** have to be set.\n    '
    QUEUE_TIMEOUT = 0.01
    MAX_EVENTS_PER_DISPATCH = 50

    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret, track=[], follow=[], languages=[]):
        assert isinstance(track, list), 'track must be a list'
        assert isinstance(follow, list), 'follow must be a list'
        assert isinstance(languages, list), 'languages must be a list'
        super(TwitterFeed, self).__init__()
        self._TwitterFeed__event = observer.Event()
        self._TwitterFeed__queue = queue.Queue()
        self._TwitterFeed__thread = None
        self._TwitterFeed__running = False
        listener = Listener(self._TwitterFeed__queue)
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        self._TwitterFeed__stream = tweepy.Stream(auth, listener)
        self._TwitterFeed__track = track
        self._TwitterFeed__follow = follow
        self._TwitterFeed__languages = languages

    def __threadMain(self):
        try:
            logger.info('Initializing client.')
            self._TwitterFeed__stream.filter(track=(self._TwitterFeed__track), follow=(self._TwitterFeed__follow), languages=(self._TwitterFeed__languages))
        finally:
            logger.info('Client finished.')
            self._TwitterFeed__running = False

    def __dispatchImpl(self):
        ret = False
        try:
            nextTweet = json.loads(self._TwitterFeed__queue.get(True, TwitterFeed.QUEUE_TIMEOUT))
            ret = True
            self._TwitterFeed__event.emit(nextTweet)
        except queue.Empty:
            pass

        return ret

    def subscribe(self, callback):
        """Subscribe to Twitter events. The event handler will receive a dictionary with the data as defined in:
        https://dev.twitter.com/docs/streaming-apis/messages#Public_stream_messages.
        """
        return self._TwitterFeed__event.subscribe(callback)

    def start(self):
        super(TwitterFeed, self).start()
        if self._TwitterFeed__thread is not None:
            raise Exception('Already running')
        self._TwitterFeed__thread = threading.Thread(target=(self._TwitterFeed__threadMain))
        self._TwitterFeed__thread.start()
        self._TwitterFeed__running = True

    def stop(self):
        try:
            if self._TwitterFeed__thread is not None:
                if self._TwitterFeed__thread.is_alive():
                    logger.info('Shutting down client.')
                    self._TwitterFeed__stream.disconnect()
        except Exception as e:
            try:
                logger.error('Error disconnecting stream: %s.' % str(e))
            finally:
                e = None
                del e

    def join(self):
        if self._TwitterFeed__thread is not None:
            self._TwitterFeed__thread.join()
        assert not self._TwitterFeed__running

    def eof(self):
        return not self._TwitterFeed__running

    def dispatch(self):
        ret = False
        dispatched = TwitterFeed.MAX_EVENTS_PER_DISPATCH
        while self._TwitterFeed__dispatchImpl() and dispatched > 0:
            ret = True
            dispatched -= 1

        return ret

    def peekDateTime(self):
        pass