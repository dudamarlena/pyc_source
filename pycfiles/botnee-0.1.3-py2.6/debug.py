# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/debug.py
# Compiled at: 2012-08-16 08:16:29
"""
Some useful debugging functions.
"""
import logging
from scipy import sparse
import numpy as np, sys
from time import time
import csv, os, botnee_config
try:
    __IPYTHON__
    try:
        from IPython.core.debugger import Tracer
        debug_here = Tracer()
    except ImportError:

        def empty():
            pass


        debug_here = empty

except NameError:
    print 'Not inside ipython'
    if not botnee_config.DEBUG:

        def debug_here():
            return


    else:
        import ipdb
        debug_here = ipdb.set_trace

def write_csv(filename, list_of_tuples, verbose=False, logger=None):
    """ Writes a list of tuples as a comma seperated variable file """
    with Timer('(%s)' % filename, None, verbose, logger):
        with open(filename, 'w') as (the_file):
            csv.register_dialect('custom', delimiter=',', skipinitialspace=True)
            writer = csv.writer(the_file, dialect='custom')
            for (i, tup) in enumerate(list_of_tuples):
                print_dot(i, verbose)
                writer.writerow(tup)

    return


def print_verbose(statement, verbose=False, logger=None, logtype=logging.INFO):
    """ Simply prints the statement if verbose is True """
    if type(statement) is list:
        for x in statement:
            print_verbose(x, verbose, logger, logtype)

        return
    if verbose:
        try:
            sys.stdout.write(unicode(statement) + '\n')
            sys.stdout.flush()
        except TypeError, e:
            print e
        except UnicodeEncodeError, e:
            print e
        except Exception, e:
            print e

    if logger:
        logger.log(logtype, statement)


def print_dot(i=-1, verbose=False):
    """ Prints a dot '.' to the screen """
    if i == 0:
        return
    if verbose and np.mod(i, 1000) == 0:
        sys.stdout.write('%d\n' % i)
        sys.stdout.flush()
        return
    if verbose and (np.mod(i, 100) == 0 or i == -1):
        sys.stdout.write('.')
        sys.stdout.flush()


class Timer(object):

    def __init__(self, message=None, time_dict=None, verbose=False, logger=None):
        self.message = message
        self.time_dict = time_dict
        self.logger = logger
        self.verbose = verbose
        frame = sys._current_frames().values()[0]
        back = frame.f_back
        flocals = back.f_locals
        try:
            class_name = str(type(flocals['self']))[8:-2]
            func_name = back.f_code.co_name
            self.caller = module_name + '.' + class_name
        except:
            module_name = back.f_globals['__name__']
            func_name = back.f_code.co_name
            self.caller = module_name + '.' + func_name

    def __enter__(self):
        self.t_start = time()
        message = str(self.caller) + ' started. '
        if self.message:
            message += self.message
        print_verbose(message, self.verbose, self.logger)
        return self

    def __exit__(self, type, value, traceback):
        self.t_end = time() - self.t_start
        self.t_str = ' done. %.2f seconds' % self.t_end
        print_verbose(str(self.caller) + self.t_str, self.verbose, self.logger)
        try:
            self.time_dict[str(self.caller)] = self.t_end
        except TypeError:
            pass


def get_size(object):
    if sparse.isspmatrix(object):
        return get_size(object.data) + get_size(object.indptr) + get_size(object.indices)
    if type(object) == np.ndarray:
        return float(object.nbytes)
    return float(sys.getsizeof(object))


def get_size_as_string(object):
    return '%.1fMb' % (get_size(object) / 1024 / 1024)


def get_sparsity(object):
    return np.float32(object.nnz) / np.product(object.shape)


def dump_dictionaries(start_time, meta_dict, data_dict, verbose=False, logger=None):
    """
    Dumps good and bad ids to csv with document frequency, proportion, and idf
    """
    retval = [
     '--------------', 'Files Written:', '--------------', '']
    with Timer(None, None, verbose, logger):
        for (i, ngram) in enumerate(botnee_config.NGRAMS.keys()):
            ngstr = '_%d' % ngram
            fname = 'tokens_good' + ngstr + '_' + start_time + '.csv'
            print_verbose(fname, verbose, logger)
            n_docs = meta_dict['n_docs']
            tokens_map = meta_dict[('tokens_map' + ngstr)]
            freq = data_dict[('term_freq' + ngstr)]
            idf = data_dict[('idf' + ngstr)]
            idf_bm25 = data_dict[('idf_bm25' + ngstr)]
            try:
                lot = ((k, freq[v], '%.4f' % (float(freq[v]) / n_docs,), '%.4f' % idf[v], '%.4f' % idf_bm25[v]) for (k, v) in tokens_map.items())
            except KeyError, e:
                print e.__repr__()
                print 'ngstr: ', ngstr

            fullname = os.path.join(botnee_config.LOG_DIRECTORY, fname)
            write_csv(fullname, lot)
            retval.append(fullname)
            if 'bad_ids' + ngstr in meta_dict and 'term_freq_bad' + ngstr in data_dict and len(data_dict[('term_freq_bad' + ngstr)]) > 0:
                fname = 'tokens_bad' + ngstr + '_' + start_time + '.csv'
                print_verbose(fname, verbose, logger)
                tokens_map = meta_dict[('bad_ids' + ngstr)]
                freq = data_dict[('term_freq_bad' + ngstr)]
                lot = ((k, freq[v], '%.2f' % (float(freq[v]) / n_docs,)) for (k, v) in tokens_map.items())
                fullname = os.path.join(botnee_config.LOG_DIRECTORY, fname)
                write_csv(fullname, lot)
                retval.append(fullname)

    return retval