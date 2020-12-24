# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/terragon/loader.py
# Compiled at: 2016-11-08 11:49:39
import sys, time, pickle
from six import string_types
from .terragon import loads_from_base64, loads_spark_from_base64, load_pom_from_base64

def load_object(name, base64_pickle, sc=None):
    pickle_error, terragon_error, spark_error, pom_error = ('', '', '', '')
    strategies = []
    try:
        strategies.append('pickle')
        if isinstance(base64_pickle, string_types):
            base64_pickle = base64_pickle.encode()
        return pickle.loads(base64_pickle)
    except Exception as e:
        pickle_error = e

    try:
        strategies.append('terragon')
        return loads_from_base64(base64_pickle)
    except Exception as e:
        terragon_error = e

    if sc:
        try:
            strategies.append('spark')
            return loads_spark_from_base64(sc, base64_pickle)
        except Exception as e:
            spark_error = e

    import pomegranate
    try:
        strategies.append('pomegranate')
        return load_pom_from_base64(base64_pickle)
    except Exception as e:
        pom_error = e

    sys.stderr.write('Attempted to load object %s using the following methods:\n')
    for strategy in strategies:
        sys.stderr.write('- %s\n' % strategy)

    sys.stderr.write('See stack traces below for more details:\n')
    if 'pickle' in strategies:
        sys.stderr.write('pickle: %s\n' % pickle_error)
    if 'terragon' in strategies:
        sys.stderr.write('terragon: %s\n' % terragon_error)
    if 'spark' in strategies:
        sys.stderr.write('spark: %s\n' % spark_error)
    if 'pomegranate' in strategies:
        sys.stderr.write('pomegranate: %s\n' % pom_error)