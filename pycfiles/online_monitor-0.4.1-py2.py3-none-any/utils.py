# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/utils/utils.py
# Compiled at: 2019-06-26 08:16:22
import os, logging, argparse, yaml, json, ast, base64, sys, numpy as np
from importlib import import_module
from inspect import getmembers, isclass
import struct
from array import array
if sys.version_info < (3, 0):
    import cPickle as pickle, imp

    def frombytes(v, b):
        return v.fromstring(b)


    def tobytes(v):
        return v.tostring()


else:
    import pickle
    from importlib.machinery import SourceFileLoader

    def frombytes(v, b):
        return v.frombytes(b)


    def tobytes(v):
        return v.tobytes()


try:
    import blosc
    has_blosc = True
except ImportError:
    has_blosc = False

from online_monitor.utils import settings

def parse_arguments():
    args = parse_args(sys.argv[1:])
    return args


def parse_args(args):
    """ Parse an argument string

        http://stackoverflow.com/questions/18160078/
        how-do-you-write-tests-for-the-argparse-portion-of-a-python-module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', nargs='?', help='Configuration yaml file', default=None)
    parser.add_argument('--log', '-l', help='Logging level (e.g. DEBUG, INFO, WARNING, ERROR, CRITICAL)', default='INFO')
    args_parsed = parser.parse_args(args)
    if not args_parsed.config_file:
        parser.error('You have to specify a configuration file')
    return args_parsed


def parse_config_file(config_file, expect_receiver=False):
    with open(config_file, 'r') as (in_config_file):
        configuration = yaml.safe_load(in_config_file)
        if expect_receiver:
            try:
                configuration['receiver']
            except KeyError:
                logging.warning('No receiver specified, thus no data can be plotted. Change %s!', config_file)

        return configuration


def setup_logging(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)
    return


def _factory(importname, base_class_type, path=None, *args, **kargs):
    """ Load a module of a given base class type

        Parameter
        --------
        importname: string
            Name of the module, etc. converter
        base_class_type: class type
            E.g converter
        path: Absoulte path of the module
            Neede for extensions. If not given module is in online_monitor
            package
        *args, **kargs:
            Arguments to pass to the object init

        Return
        ------
        Object of given base class type
    """

    def is_base_class(item):
        return isclass(item) and item.__module__ == importname

    if path:
        sys.path.append(path)
        absolute_path = os.path.join(path, importname) + '.py'
        if sys.version_info < (3, 0):
            module = imp.load_source(importname, absolute_path)
        else:
            module = SourceFileLoader(importname, absolute_path).load_module()
    else:
        module = import_module(importname)
    clsmembers = getmembers(module, is_base_class)
    if not len(clsmembers):
        raise ValueError('Found no matching class in %s.' % importname)
    else:
        cls = clsmembers[0][1]
    return cls(*args, **kargs)


def load_producer_sim(importname, base_class_type, *args, **kargs):
    for producer_sim_path in settings.get_producer_sim_path():
        try:
            return _factory(importname, base_class_type, producer_sim_path, *args, **kargs)
        except IOError:
            pass

    raise RuntimeError('Producer simulation %s in paths %s not found!', importname, settings.get_producer_sim_path())


def load_converter(importname, base_class_type, *args, **kargs):
    try:
        return _factory(('online_monitor.converter.' + importname), base_class_type, path=None, *args, **kargs)
    except ImportError:
        pass

    for converter_path in settings.get_converter_path():
        try:
            return _factory(importname, base_class_type, converter_path, *args, **kargs)
        except IOError:
            pass

    raise RuntimeError('Converter %s in paths %s not found!', importname, settings.get_converter_path())
    return


def load_receiver(importname, base_class_type, *args, **kargs):
    try:
        return _factory(('online_monitor.receiver.' + importname), base_class_type, path=None, *args, **kargs)
    except ImportError:
        pass

    for receiver_path in settings.get_receiver_path():
        try:
            return _factory(importname, base_class_type, receiver_path, *args, **kargs)
        except IOError:
            pass

    raise RuntimeError('Receiver %s in paths %s not found!', importname, settings.get_receiver_path())
    return


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
            if has_blosc:
                obj_data = blosc.compress(obj_data, typesize=8)
            data_b64 = base64.b64encode(obj_data)
            if sys.version_info >= (3, 0):
                data_b64 = data_b64.decode('utf-8')
            return dict(__ndarray__=data_b64, dtype=str(obj.dtype), shape=obj.shape)
        return json.JSONEncoder.default(self, obj)


def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.
    And decompresses the data with blosc

    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        a = dct['__ndarray__']
        if sys.version_info >= (3, 0):
            a = a.encode('utf-8')
        data = base64.b64decode(a)
        if has_blosc:
            data = blosc.decompress(data)
        try:
            dtype = np.dtype(ast.literal_eval(dct['dtype']))
        except ValueError:
            dtype = dct['dtype']

        return np.frombuffer(data, dtype).reshape(dct['shape'])
    return dct


def simple_enc(data=None, meta={}):
    data_buffer = array('B', [])
    if data is not None:
        meta['data_meta'] = {'dtype': data.dtype, 'shape': data.shape}
        frombytes(data_buffer, data.tobytes())
    meta_json = pickle.dumps(meta)
    meta_json_buffer = array('B', [])
    frombytes(meta_json_buffer, meta_json)
    meta_len = len(meta_json)
    meta_len_byte = struct.unpack('4B', struct.pack('I', meta_len))
    data_buffer.extend(meta_json_buffer)
    data_buffer.extend(meta_len_byte)
    return tobytes(data_buffer)


def simple_dec(data_buffer):
    len_buffer = data_buffer[-4:]
    length = struct.unpack('I', len_buffer)[0]
    meta = pickle.loads(data_buffer[-4 - length:-4])
    if 'data_meta' in meta:
        dtype = meta['data_meta']['dtype']
        shape = meta['data_meta']['shape']
        data = np.frombuffer(data_buffer[:-4 - length], dtype).reshape(shape)
    else:
        data = None
    return (data, meta)