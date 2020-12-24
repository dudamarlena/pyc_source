# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/runner/runner.py
# Compiled at: 2014-11-25 17:55:11
import os
from multiprocessing import Process
import pyrowire.config.configuration as config
from pyrowire.tasks.tasks import process_queue_item

def run():
    """
    called once per application launch. loads profanity, and starts either the web process, a worker, or both.
    If a run type is specified by the "RUN" environment variable, runs only that process. Otherwise, runs web
    and worker processes together for a standalone application server.
    """
    if 'RUN' in os.environ.keys():
        if os.environ['RUN'].lower() == 'web':
            server()
        elif os.environ['RUN'].lower() == 'worker':
            assert 'TOPIC' in os.environ.keys(), 'You must provide a topic as an env var (TOPIC=my_topic)'
            work(topic=os.environ['TOPIC'])
    else:
        for topic in config.topics().keys():
            Process(target=work, kwargs={'topic': topic}).start()

        Process(target=server).run()


def server():
    """
    runs the web server; if the port defined in self.config is 0, grabs environment variable "PORT" to determine
    the port on which to run (for Heroku, mainly)
    """
    port = os.environ['PORT'] if config.port() == 0 else config.port()
    config.app().run(config.host(), port)


def work(topic=None, persist=True):
    """
   starts a worker for a given topic
   :param topic: the topic for which to start a worker
   :param persist: boolean, mainly for testing. if persist is False, the worker will exit the process after
                   one pass. In production mode, this should always be True, and True is what it defaults to.
   """
    return process_queue_item(topic=topic, persist=persist)