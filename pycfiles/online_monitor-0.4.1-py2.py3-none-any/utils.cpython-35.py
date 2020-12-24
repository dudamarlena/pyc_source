# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/utils.py
# Compiled at: 2015-10-09 09:18:17
# Size of source mod 2**32: 3776 bytes
import logging, argparse, yaml, blosc, json, base64, numpy as np
from importlib import import_module
from inspect import getmembers, isclass
import sys

def parse_arguments():
    args = parse_args(sys.argv[1:])
    return args


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', nargs='?', help='Configuration yaml file', default=None)
    parser.add_argument('--log', '-l', help='Logging level (e.g. DEBUG, INFO, WARNING, ERROR, CRITICAL)', default='INFO')
    args_parsed = parser.parse_args(args)
    if not args_parsed.config_file:
        parser.error('You have to specify a configuration file')
    return args_parsed


def parse_config_file(config_file, expect_receiver=False):
    try:
        with open(config_file, 'r') as (in_config_file):
            configuration = yaml.safe_load(in_config_file)
            if expect_receiver:
                try:
                    if not configuration['receiver']:
                        logging.warning('No receiver specified, thus no data can be plotted. Change %s!', config_file)
                except KeyError:
                    logging.warning('No receiver specified, thus no data can be plotted. Change %s!', config_file)

            return configuration
    except IOError:
        logging.error('Cannot open configuration file')


def setup_logging(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)


def factory(importname, base_class_type, *args, **kargs):

    def is_base_class(item):
        return isclass(item) and item.__module__ == importname

    mod = import_module(importname)
    clsmembers = getmembers(mod, is_base_class)
    if not len(clsmembers):
        raise ValueError('Found no matching class in %s.' % importname)
    else:
        cls = clsmembers[0][1]
    return cls(*args, **kargs)


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        """If input object is an ndarray it will be converted into a dict 
        holding dtype, shape and the data, base64 encoded and blosc compressed.
        """
        if isinstance(obj, np.ndarray):
            if obj.flags['C_CONTIGUOUS']:
                obj_data = obj.data
            else:
                cont_obj = np.ascontiguousarray(obj)
                assert cont_obj.flags['C_CONTIGUOUS']
                obj_data = cont_obj.data
            obj_data = blosc.compress(obj_data, typesize=8)
            data_b64 = base64.b64encode(obj_data)
            return dict(__ndarray__=data_b64, dtype=str(obj.dtype), shape=obj.shape)
        return json.JSONEncoder(self, obj)


def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.
    And decompresses the data with blosc

    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        data = blosc.decompress(data)
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct