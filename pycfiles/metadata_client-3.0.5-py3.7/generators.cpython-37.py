# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/common/generators.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 2117 bytes
"""Generators Class with helper methods to generate dummy data"""
import logging, socket, time
from random import randrange
from common.util import Util

class Generators(object):

    @staticmethod
    def generate_unique_id(min_value=1, max_value=9999):
        unique_id = randrange(min_value, max_value)
        logging.debug('generate::unique_id == {0}'.format(unique_id))
        return unique_id

    @staticmethod
    def generate_unique_name(prefix):
        dt_str = Util.get_formatted_date('%Y-%m-%d %H:%M:%S')
        host = socket.gethostname()
        rand = randrange(999)
        unique_str = '{0} {1} {2} {3}'.format(prefix, host, dt_str, rand)
        if len(unique_str) > 60:
            unique_str = '{0}..'.format(unique_str[:58])
        logging.debug('generate::unique_name == {0}'.format(unique_str))
        return unique_str

    @staticmethod
    def generate_unique_identifier(sleep_time=0):
        if sleep_time > 0:
            time.sleep(sleep_time)
        unique_str = Util.get_formatted_date('%y%m%d%H%M%S')
        if len(unique_str) > 12:
            unique_str = '{0}..'.format(unique_str[:10])
        logging.debug('generate::unique_name == {0}'.format(unique_str))
        return unique_str

    @staticmethod
    def generate_unique_file_name():
        epoch_str = str(time.time())
        host = socket.gethostname()
        unique_file = 'cal.{0}_{1}.h5'.format(epoch_str, host)
        logging.debug('generate::unique_file_name == {0}'.format(unique_file))
        return unique_file

    @staticmethod
    def generate_timestamp_str(secs=None):
        epoch_time = int(time.time())
        if secs is None:
            additional_secs = -randrange(60)
        else:
            additional_secs = secs
        begin_epoch_at = epoch_time + additional_secs
        dt_str = Util.get_formatted_date('%Y-%m-%dT%H:%M:%S', epoch_val=begin_epoch_at,
          dt_extra='.000+00:00')
        logging.debug('generate_timestamp_str == {0}'.format(dt_str))
        return dt_str