# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/twitter/feed.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import Queue, threading, json
from pyalgotrade import observer
import pyalgotrade.logger, tweepy
from tweepy import streaming
logger = pyalgotrade.logger.getLogger('twitter')

class Listener(streaming.StreamListener):

    def __init__(self, queue):
        super(Listener, self).__init__()
        self.__queue = queue

    def on_connect(self):
        logger.info('Connected.')

    def on_timeout(self):
        logger.error('Timeout.')

    def on_data(self, data):
        self.__queue.put(data)
        return True

    def on_error(self, status):
        logger.error(status)
        return False


class TwitterFeed(observer.Subject):
    """Class responsible for connecting to Twitter's public stream API and dispatching events.
    Check https://dev.twitter.com/docs/streaming-apis/streams/public for more information.

    :param consumerKey: Consumer key.
    :type consumerKey: string.
    :param consumerSecret: Consumer secret.
    :type consumerSecret: string.
    :param accessToken: Access token.
    :type accessToken: string.
    :param accessTokenSecret: Access token secret.
    :type accessTokenSecret: string.
    :param track: A list of phrases which will be used to determine what Tweets will be delivered
        on the stream. A phrase may be one or more terms separated by spaces, and a phrase will match
        if all of the terms in the phrase are present in the Tweet, regardless of order and ignoring case.
    :type track: list.
    :param follow: A list of user IDs, indicating the users whose Tweets should be delivered on the
        stream. Following protected users is not supported.
    :type follow: list.
    :param languages: A list of language IDs a defined in http://tools.ietf.org/html/bcp47.
    :type languages: list.

    .. note::
        * Go to http://dev.twitter.com and create an app. The consumer key and secret will be generated for you after that.
        * Create an access token under the "Your access token" section.
        * At least **track** or **follow** have to be set.
    """
    QUEUE_TIMEOUT = 0.01
    MAX_EVENTS_PER_DISPATCH = 50

    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret, track=[], follow=[], languages=[]):
        assert isinstance(track, list), 'track must be a list'
        assert isinstance(follow, list), 'follow must be a list'
        assert isinstance(languages, list), 'languages must be a list'
        super(TwitterFeed, self).__init__()
        self.__event = observer.Event()
        self.__queue = Queue.Queue()
        self.__thread = None
        self.__running = False
        listener = Listener(self.__queue)
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        self.__stream = tweepy.Stream(auth, listener)
        self.__track = track
        self.__follow = follow
        self.__languages = languages
        return

    def __threadMain(self):
        try:
            logger.info('Initializing client.')
            self.__stream.filter(track=self.__track, follow=self.__follow, languages=self.__languages)
        finally:
            logger.info('Client finished.')
            self.__running = False

    def __dispatchImpl(self):
        ret = False
        try:
            nextTweet = json.loads(self.__queue.get(True, TwitterFeed.QUEUE_TIMEOUT))
            ret = True
            self.__event.emit(nextTweet)
        except Queue.Empty:
            pass

        return ret

    def subscribe(self, callback):
        """Subscribe to Twitter events. The event handler will receive a dictionary with the data as defined in:
        https://dev.twitter.com/docs/streaming-apis/messages#Public_stream_messages.
        """
        return self.__event.subscribe(callback)

    def start(self):
        super(TwitterFeed, self).start()
        if self.__thread is not None:
            raise Exception('Already running')
        self.__thread = threading.Thread(target=self.__threadMain)
        self.__thread.start()
        self.__running = True
        return

    def stop(self):
        try:
            if self.__thread is not None and self.__thread.is_alive():
                logger.info('Shutting down client.')
                self.__stream.disconnect()
        except Exception as e:
            logger.error('Error disconnecting stream: %s.' % str(e))

        return

    def join(self):
        if self.__thread is not None:
            self.__thread.join()
        assert not self.__running
        return

    def eof(self):
        return not self.__running

    def dispatch(self):
        ret = False
        dispatched = TwitterFeed.MAX_EVENTS_PER_DISPATCH
        while self.__dispatchImpl() and dispatched > 0:
            ret = True
            dispatched -= 1

        return ret

    def peekDateTime(self):
        return