# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\twitter_monitor\stream.py
# Compiled at: 2015-09-15 18:34:59
from time import sleep, time
import logging, tweepy
logger = logging.getLogger(__name__)

class DynamicTwitterStream(object):
    """
    A wrapper around Tweepy's Stream class that causes
    streaming to be executed in a secondary thread.

    Meanwhile the primary thread sleeps for an interval between checking for
    term list updates.
    """
    STOP_TIMEOUT = 1

    def __init__(self, auth, listener, term_checker, **options):
        self.auth = auth
        self.listener = listener
        self.term_checker = term_checker
        self.polling = False
        self.stream = None
        self.retry_count = options.get('retry_count', 5)
        self.unfiltered = options.get('unfiltered', False)
        self.languages = options.get('languages', None)
        return

    def start_polling(self, interval):
        """
        Start polling for term updates and streaming.
        """
        interval = float(interval)
        self.polling = True
        self.term_checker.reset()
        logger.info('Starting polling for changes to the track list')
        while self.polling:
            loop_start = time()
            self.update_stream()
            self.handle_exceptions()
            elapsed = time() - loop_start
            sleep(max(0.1, interval - elapsed))

        logger.warning('Term poll ceased!')

    def stop_polling(self):
        """Halts the polling loop and streaming"""
        logger.info('Stopping polling loop')
        self.polling = False
        self.stop_stream()

    def update_stream(self):
        """
        Restarts the stream with the current list of tracking terms.
        """
        need_to_restart = False
        if self.stream is not None and not self.stream.running:
            logger.warning("Stream exists but isn't running")
            self.listener.error = False
            self.listener.streaming_exception = None
            need_to_restart = True
        if self.term_checker.check():
            logger.info('Terms have changed')
            need_to_restart = True
        if self.stream is None and self.unfiltered:
            need_to_restart = True
        if not need_to_restart:
            return
        else:
            logger.info('Restarting stream...')
            self.stop_stream()
            self.start_stream()
            return

    def start_stream(self):
        """Starts a stream with teh current tracking terms"""
        tracking_terms = self.term_checker.tracking_terms()
        if len(tracking_terms) > 0 or self.unfiltered:
            self.stream = tweepy.Stream(self.auth, self.listener, stall_warnings=True, timeout=90, retry_count=self.retry_count)
            if len(tracking_terms) > 0:
                logger.info('Starting new twitter stream with %s terms:', len(tracking_terms))
                logger.info('  %s', repr(tracking_terms))
                self.stream.filter(track=tracking_terms, async=True, languages=self.languages)
            else:
                logger.info('Starting new unfiltered stream')
                self.stream.sample(async=True, languages=self.languages)

    def stop_stream(self):
        """
        Stops the current stream. Blocks until this is done.
        """
        if self.stream is not None:
            logger.warning('Stopping twitter stream...')
            self.stream.disconnect()
            self.stream = None
            sleep(self.STOP_TIMEOUT)
        return

    def handle_exceptions(self):
        if self.listener.streaming_exception is not None:
            exc = self.listener.streaming_exception
            self.listener.streaming_exception = None
            logger.warning('Streaming exception: %s', exc)
            raise exc
        return