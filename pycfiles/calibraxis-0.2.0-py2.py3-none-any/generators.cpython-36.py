# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/common/generators.py
# Compiled at: 2019-08-15 17:48:17
# Size of source mod 2**32: 1602 bytes
__doc__ = 'Generators Class with helper methods to generate dummy data'
import logging, socket, time
from random import randrange
from ...common.util import Util

class Generators(object):

    @staticmethod
    def generate_unique_name(prefix):
        dt_str = Util.get_formatted_date('%Y-%m-%d %H:%M:%S')
        host = socket.gethostname()
        rand = randrange(999)
        unique_str = '{0} {1} {2} {3}'.format(prefix, dt_str, rand, host)
        if len(unique_str) > 60:
            unique_str = '{0}..'.format(unique_str[:58])
        logging.debug('generate::unique_name == {0}'.format(unique_str))
        return unique_str

    @staticmethod
    def generate_unique_file_name():
        epoch_str = str(time.time())
        host = str(socket.gethostname())[0:34]
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