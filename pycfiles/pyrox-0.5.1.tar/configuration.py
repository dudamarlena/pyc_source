# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/config/configuration.py
# Compiled at: 2014-11-25 17:55:10
import os
PYROWIRE = None

def configure(settings, flask):
    """
    sets up the global PYROWIRE object, containing all of the settings needed to run pyrowire.
    :param settings: the settings module that should be used to parse the settings
    :param flask: the underlying flask application that will be attached to pyrowire
    """
    global PYROWIRE
    PYROWIRE = {'profile': settings.PROFILES[os.environ['ENV'].lower()], 
       'topics': settings.TOPICS, 
       'app': flask, 
       'validators': {}}


def topics(topic=None):
    if topic:
        return PYROWIRE['topics'][topic]
    return PYROWIRE['topics']


def validators(topic=None):
    if topic:
        return PYROWIRE['topics'][topic]['validators']
    return PYROWIRE['validators']


def properties(topic=None, key=None):
    if key:
        return PYROWIRE['topics'][topic]['properties'][key]
    return PYROWIRE['topics'][topic]['properties']


def twilio(topic=None):
    return PYROWIRE['topics'][topic]['twilio']


def handler(topic=None):
    if 'handler' in PYROWIRE['topics'][topic].keys():
        return PYROWIRE['topics'][topic]['handler']


def max_message_length(topic=None):
    return PYROWIRE['topics'][topic]['max_message_length']


def send_on_accept(topic=None):
    return PYROWIRE['topics'][topic]['send_on_accept']


def accept_response(topic=None):
    return PYROWIRE['topics'][topic]['accept_response']


def error_response(topic=None):
    return PYROWIRE['topics'][topic]['error_response']


def add_validator(validator=None):
    PYROWIRE['validators'][validator.__name__] = validator


def add_handler(topic=None, handler=None):
    PYROWIRE['topics'][topic]['handler'] = handler


def debug():
    return PYROWIRE['profile']['debug']


def host():
    return PYROWIRE['profile']['host']


def log_level():
    return PYROWIRE['profile']['log_level']


def port():
    return PYROWIRE['profile']['port']


def redis(key=None):
    if key:
        return PYROWIRE['profile']['redis'][key]
    return PYROWIRE['profile']['redis']


def app():
    return PYROWIRE['app']