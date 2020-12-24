# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/python/util/PyTypeWildcardWrapper.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 11363 bytes
""" Class description goes here. """
import logging, re, six, traceback
if six.PY2:
    import cPickle as pickle
else:
    if six.PY3:
        import _pickle as pickle
from dataclay.commonruntime.Initializer import size_tracking
import dataclay.serialization.python.DataClayPythonWrapper as DataClayPythonWrapper
import dataclay.serialization.python.lang.BooleanWrapper as BooleanWrapper
import dataclay.serialization.python.lang.IntegerWrapper as IntegerWrapper
import dataclay.serialization.python.lang.StringWrapper as StringWrapper
import six
logger = logging.getLogger(__name__)
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

def safe_wait_if_compss_future(potential_future):
    """Safe approach to COMPSs Futures: compss_wait_on if that is a Future.

    COMPSs may use Future objects, and this function returns the real object
    (after a call to compss_wait_on to the COMPSs API). If the objects was not
    a Future, return the object itself.

    :param potential_future: May be a PyCOMPSs Future instance
    :return: NOT a Future instance. Redirect potential_future
    """
    real_type = type(potential_future)
    if real_type.__name__ == 'Future' and real_type.__module__ == 'pycompss.runtime.binding':
        from pycompss.api.api import compss_wait_on
        logger.info('Received a `Future` PyCOMPSs object, waiting for the real object...')
        param = compss_wait_on(potential_future)
        real_type = type(param)
        logger.info('Using the parameter: %r (type: %s)', param, real_type)
    else:
        param = potential_future
    return param


class PyTypeWildcardWrapper(DataClayPythonWrapper):
    __doc__ = 'Generic catch-all for Python types (including custom-signature binary types).'
    __slots__ = ('_signature', '_pickle_fallback')
    PYTHON_PREFIX = 'python.'
    SEQUENCE_REGEX = re.compile('(?P<base_type>(list)|(tuple)|(set))\\s*(?:[<\\[]\\s*(?P<subtype>.*?)\\s*[>\\]])?\\s*$')
    MAPPING_REGEX = re.compile('(?P<base_type>dict)\\s*(?:[<\\[]\\s*(?P<keytype>.*?)\\s*,\\s*(?P<valuetype>.*?)\\s*[>\\]])?\\s*$')
    STR_SIGNATURE = 'str'
    UNICODE_SIGNATURE = 'unicode'
    STORAGEOBJECT_SIGNATURE = 'storageobject'
    ANYTHING_SIGNATURE = 'anything'
    NUMPY_SIGNATURE = 'numpy'

    def __init__(self, signature, pickle_fallback=False):
        self._signature = signature
        self._pickle_fallback = pickle_fallback

    def read(self, io_file):
        from dataclay.util.management.classmgr.Utils import serialization_types
        try:
            return serialization_types[self._signature].read(io_file)
        except KeyError:
            pass

        if self._signature.startswith(self.NUMPY_SIGNATURE):
            import numpy as np
            _ = IntegerWrapper(32).read(io_file)
            return np.load(io_file, allow_pickle=False)
        elif not self._signature == self.ANYTHING_SIGNATURE:
            if self._signature == self.STORAGEOBJECT_SIGNATURE:
                field_size = IntegerWrapper(32).read(io_file)
                logger.debug('Deserializing DataClayObject from pickle')
                return pickle.loads(io_file.read(field_size))
            if not self._signature.startswith(self.PYTHON_PREFIX):
                field_size = IntegerWrapper(32).read(io_file)
                return pickle.loads(io_file.read(field_size))
            subtype = self._signature[len(self.PYTHON_PREFIX):]
            sequence_match = self.SEQUENCE_REGEX.match(subtype)
            mapping_match = self.MAPPING_REGEX.match(subtype)
            if sequence_match:
                gd = sequence_match.groupdict()
                logger.debug('Deserializing a Python Sequence with the following match: %s', gd)
                if gd['subtype']:
                    instances_type = PyTypeWildcardWrapper((gd['subtype']), pickle_fallback=True)
        else:
            instances_type = PyTypeWildcardWrapper(self.ANYTHING_SIGNATURE)
        ret = list()
        size = IntegerWrapper(32).read(io_file)
        logger.debug('### READ SIZE OF SEQUENCE MATCH: %i', size)
        for i in range(size):
            if BooleanWrapper().read(io_file):
                ret.append(instances_type.read(io_file))
            else:
                ret.append(None)

        if gd['base_type'] == 'tuple':
            logger.debug('Returning deserialized Python tuple')
            return tuple(ret)
            logger.debug('Returning deserialized Python list')
            return ret
        elif mapping_match:
            gd = mapping_match.groupdict()
            logger.debug('Deserializing a Python mapping with the following match: %s', gd)
            if gd['keytype'] and gd['valuetype']:
                key_type = PyTypeWildcardWrapper((gd['keytype']), pickle_fallback=True)
                value_type = PyTypeWildcardWrapper((gd['valuetype']), pickle_fallback=True)
            else:
                key_type = PyTypeWildcardWrapper(self.ANYTHING_SIGNATURE)
                value_type = PyTypeWildcardWrapper(self.ANYTHING_SIGNATURE)
            ret = dict()
            size = IntegerWrapper(32).read(io_file)
            for i in range(size):
                if BooleanWrapper().read(io_file):
                    key = key_type.read(io_file)
                else:
                    key = None
                if BooleanWrapper().read(io_file):
                    ret[key] = value_type.read(io_file)
                else:
                    ret[key] = None

            logger.debug('Returning deserialized Python map')
            return ret
            if subtype == self.STR_SIGNATURE:
                if six.PY2:
                    return StringWrapper('binary').read(io_file)
                if six.PY3:
                    return StringWrapper('utf-8').read(io_file)
        else:
            if subtype == self.UNICODE_SIGNATURE:
                return StringWrapper('utf-16').read(io_file)
            raise NotImplementedError('Python types supported at the moment: list and mappings (but not `%s`), sorry' % subtype)

    def write(self, io_file, value):
        value = safe_wait_if_compss_future(value)
        from dataclay.util.management.classmgr.Utils import serialization_types
        try:
            serialization_types[self._signature].write(io_file, value)
            return
        except KeyError:
            pass

        if self._signature.startswith(self.NUMPY_SIGNATURE):
            import numpy as np
            with size_tracking(io_file):
                np.save(io_file, value)
            return
        if self._signature == self.ANYTHING_SIGNATURE or self._signature == self.STORAGEOBJECT_SIGNATURE:
            s = pickle.dumps(value, protocol=(-1))
            IntegerWrapper(32).write(io_file, len(s))
            io_file.write(s)
            return
        if not self._signature.startswith(self.PYTHON_PREFIX):
            s = pickle.dumps(value, protocol=(-1))
            IntegerWrapper(32).write(io_file, len(s))
            io_file.write(s)
            return
        if not self._signature.startswith(self.PYTHON_PREFIX):
            raise AssertionError("Signature for Python types is expected to start with 'python'. Found signature: %s" % self._signature)
        else:
            subtype = self._signature[len(self.PYTHON_PREFIX):]
            sequence_match = self.SEQUENCE_REGEX.match(subtype)
            mapping_match = self.MAPPING_REGEX.match(subtype)
            if sequence_match:
                gd = sequence_match.groupdict()
                logger.debug('Serializing a Python Sequence with the following match: %s', gd)
                if gd['subtype']:
                    instances_type = PyTypeWildcardWrapper((gd['subtype']), pickle_fallback=True)
                else:
                    instances_type = PyTypeWildcardWrapper(self.ANYTHING_SIGNATURE)
                IntegerWrapper(32).write(io_file, len(value))
                for elem in value:
                    if elem is None:
                        BooleanWrapper().write(io_file, False)
                    else:
                        BooleanWrapper().write(io_file, True)
                        instances_type.write(io_file, elem)

            else:
                if mapping_match:
                    gd = mapping_match.groupdict()
                    logger.debug('Serializing a Python Mapping with the following match: %s', gd)
                    if gd['keytype'] and gd['valuetype']:
                        key_type = PyTypeWildcardWrapper((gd['keytype']), pickle_fallback=True)
                        value_type = PyTypeWildcardWrapper((gd['valuetype']), pickle_fallback=True)
                    else:
                        key_type = PyTypeWildcardWrapper(self.ANYTHING_SIGNATURE)
                        value_type = PyTypeWildcardWrapper(self.ANYTHING_SIGNATURE)
                    IntegerWrapper(32).write(io_file, len(value))
                    for k, v in value.items():
                        if k is None:
                            BooleanWrapper().write(io_file, False)
                        else:
                            BooleanWrapper().write(io_file, True)
                            key_type.write(io_file, k)
                        if v is None:
                            BooleanWrapper().write(io_file, False)
                        else:
                            v = safe_wait_if_compss_future(v)
                            BooleanWrapper().write(io_file, True)
                            value_type.write(io_file, v)

                else:
                    if subtype == self.STR_SIGNATURE:
                        if six.PY2:
                            StringWrapper('utf-8').write(io_file, value)
                        else:
                            if six.PY3:
                                StringWrapper('binary').write(io_file, value)
                    else:
                        if subtype == self.UNICODE_SIGNATURE:
                            StringWrapper('utf-16').write(io_file, value)
                        else:
                            raise NotImplementedError('Python types supported at the moment: list and mappings (but not `%s`), sorry' % subtype)