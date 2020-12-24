# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/airbrakepy/test/integration/test-logging.py
# Compiled at: 2011-10-26 03:38:23
import logging, ConfigParser, os, time
from airbrakepy.logging.handlers import AirbrakeHandler

def method_three():
    raise StandardError('bam, pow')


def method_two():
    method_three()


def method_one():
    method_two()


if __name__ == '__main__':
    configFilePath = os.path.join(os.path.expanduser('~'), '.airbrakepy')
    print configFilePath
    parser = ConfigParser.SafeConfigParser()
    parser.read(configFilePath)
    api_key = parser.get('airbrake', 'api_key')
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('test-logger')
    handler = AirbrakeHandler(api_key, environment='dev', component_name='integration-test', node_name='server')
    logger.addHandler(handler)
    logger.error('before exception')
    try:
        method_one()
    except StandardError:
        logger.error('test with exception', exc_info=True)
        logger.error('test without exception', exc_info=False)

    logger.error('after exception')
    logging.shutdown()