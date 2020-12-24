# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/process/vector_space_model.py
# Compiled at: 2012-08-16 08:00:35
__doc__ = '\nMain computation of the Vector Space Model (TF-IDF and related functions).\n'
import numpy, scipy, warnings
from bidict import bidict
import logging, botnee_config
from botnee import debug, errors
from botnee.process.meta_dict import MetaDict
from botnee.process.data_dict import DataDict
from botnee.process.matrix_dict import MatrixDict
from botnee.process.time_dict import TimeDict
from botnee.doc_store import DocStore
process_vsm_logger = logging.getLogger(__name__)

def get_caster(ngram):
    """Used to cast values depending whether they are tokens or ngrams"""
    if ngram == 1:
        return unicode
    else:
        return tuple


class VectorSpaceModel(object):
    """
    Helper class to reduce the number of params flying round, should only be
    used internally.
    """

    def __init__(self, meta_dict, data_dict, matx_dict, time_dict, doc_store):
        check_types(meta_dict, data_dict, matx_dict, time_dict, doc_store)
        self.meta_dict = meta_dict
        self.data_dict = data_dict
        self.matx_dict = matx_dict
        self.time_dict = time_dict
        self.doc_store = doc_store


def check_types(meta_dict, data_dict, matx_dict, time_dict, doc_store):
    if type(meta_dict) is not MetaDict:
        raise TypeError('expected MetaDict got ' + str(type(meta_dict)))
    if type(data_dict) is not DataDict:
        raise TypeError('expected DataDict got ' + str(type(data_dict)))
    if type(matx_dict) is not MatrixDict:
        raise TypeError('expected MatrixDict got ' + str(type(matx_dict)))
    if type(time_dict) is not TimeDict:
        raise TypeError('expected TimeDict got ' + str(type(time_dict)))
    if type(doc_store) is not DocStore:
        raise TypeError('expected DocStore got ' + str(type(doc_store)))


def vector_space_model(meta_dict, data_dict, matx_dict, time_dict, doc_store, reindex=True, job_server=None, verbose=False):
    """
    Performs calculations of Vector Space Model.
    Handles:
        inserts
        deletes
        updates
        pseudos
    where pseudos are docs generated in the retrieval mechanism
    """
    check_types(meta_dict, data_dict, matx_dict, time_dict, doc_store)
    if meta_dict['n_docs'] == 0:
        return
    else:
        matrix_types = botnee_config.MATRIX_TYPES
        ngstrs = [ '_%d' % ng for ng in botnee_config.NGRAMS.keys() ]

        def update_matrix(A, B, name, verbose=False):
            msg = '(matrix: %s)' % name
            with debug.Timer(msg, time_dict, verbose, process_vsm_logger):
                A = A.tolil()
                B = B.tolil()
                return scipy.sparse.vstack([A, B], dtype=A.dtype)

        with debug.Timer(None, time_dict, verbose, process_vsm_logger):
            if reindex:
                matx_dict.reset()
                VSM = VectorSpaceModel(meta_dict, data_dict, matx_dict, time_dict, doc_store)
                for ngram in botnee_config.NGRAMS.keys():
                    ngstr = '_%d' % ngram
                    for suffix in botnee_config.SUFFIXES:
                        calculate_tf(VSM, suffix, job_server, ngram, verbose)

                    for idf_method in ['', '_bm25']:
                        calculate_idf(VSM, idf_method, ngstr, verbose)

                    for suffix in botnee_config.SUFFIXES:
                        calculate_tfidf(VSM, suffix, job_server, '', ngstr, verbose)

            else:
                time_temp = TimeDict()
                guids = meta_dict['inserts'] + meta_dict['updates']
                try:
                    if guids:
                        meta_temp = MetaDict({'guids': bidict((guid, index) for (index, guid) in enumerate(guids)), 
                           'last_index': len(guids) - 1}, verbose=verbose, persistent=False)
                        for ngstr in ngstrs:
                            tm_str = 'tokens_map' + ngstr
                            meta_temp[tm_str] = meta_dict[tm_str]
                            for suffix in botnee_config.SUFFIXES:
                                meta_temp['tokens' + suffix + ngstr] = doc_store.get_tokens_by_guid(guids, suffix, ngstr, verbose)

                        data_temp = DataDict()
                        for ngstr in ngstrs:
                            data_temp.update({'idf' + ngstr: data_dict[('idf' + ngstr)], 
                               'term_freq' + ngstr: data_dict[('term_freq' + ngstr)]}, verbose=verbose, persistent=False)

                        matx_temp = MatrixDict()
                        VSM = VectorSpaceModel(meta_temp, data_temp, matx_temp, time_temp, doc_store)
                        for suffix in botnee_config.SUFFIXES:
                            for ngram in botnee_config.NGRAMS.keys():
                                ngstr = '_%d' % ngram
                                if meta_temp[('tokens' + suffix + ngstr)]:
                                    old_len = len(meta_dict[('tokens_map' + ngstr)])
                                    calculate_tf(VSM, suffix, job_server, ngram, verbose)
                                    new_len = len(meta_dict[('tokens_map' + ngstr)])
                                    if new_len != old_len:
                                        msg = 'tokens_map%s length changed (%d -> %d)' % (ngstr, old_len, new_len)
                                        debug.ProcessWarning(msg, process_vsm_logger)
                                    idf_method = ''
                                    calculate_tfidf(VSM, suffix, job_server, idf_method, ngstr, verbose)

                        for name in matrix_types.keys():
                            for suffix in botnee_config.SUFFIXES:
                                for ngstr in ngstrs:
                                    full_name = name + suffix + ngstr
                                    try:
                                        shape0 = matx_dict[full_name].shape[1]
                                        shape1 = matx_temp[full_name].shape[1]
                                        if shape0 != shape1:
                                            raise errors.ProcessError('Incompatible dimensions')
                                    except AttributeError, e:
                                        msg = '%s matrix update failed' % full_name
                                        errors.ProcessWarning(msg, process_vsm_logger)
                                        debug.debug_here()
                                        continue

                                    matx_dict[full_name] = update_matrix(matx_dict[full_name], matx_temp[full_name], full_name, verbose)

                except Exception, e:
                    debug.ProcessWarning(e.__repr__(), process_vsm_logger)

            if (meta_dict.has_key('deletes') and len(meta_dict['deletes'])) > 0:
                for suffix in botnee_config.SUFFIXES:
                    for ngstr in ngstrs:
                        matx_dict['tf' + suffix + ngstr] = matx_dict[('tf' + suffix + ngstr)].tolil()

                indices = [ meta_dict['guids'][guid] for guid in meta_dict['deletes'] ]
                for suffix in botnee_config.SUFFIXES:
                    for ngstr in ngstrs:
                        scipy.delete(matx_dict[('tf' + suffix + ngstr)], indices, 0)
                        scipy.delete(matx_dict[('tfidf' + suffix + ngstr)], indices, 0)

            for k in meta_dict['pseudos']:
                data_temp = DataDict({}, verbose, persistent=False)
                for ngstr in ngstrs:
                    data_temp['idf' + ngstr] = data_dict[('idf' + ngstr)]

                time_temp = TimeDict()
                matx_temp = MatrixDict()
                VSM = VectorSpaceModel(meta_dict, data_temp, matx_temp, time_temp, doc_store)
                for suffix in botnee_config.SUFFIXES:
                    for ngram in botnee_config.NGRAMS.keys():
                        ngstr = '_%d' % ngram
                        calculate_tf(VSM, suffix, job_server, ngram, verbose)
                        matx_dict['pseudo_tf' + suffix + ngstr] = matx_temp[('tf' + suffix + ngstr)]
                        idf_method = ''
                        calculate_tfidf(VSM, suffix, job_server, idf_method, ngstr, verbose)
                        full_name = 'tfidf' + idf_method + suffix + ngstr
                        matx_dict['pseudo_' + full_name] = matx_temp[full_name]

            for name in matrix_types.keys():
                for suffix in botnee_config.SUFFIXES:
                    for ngstr in ngstrs:
                        full_name = name + suffix + ngstr
                        if matx_dict[full_name] is not None:
                            try:
                                matx_dict[full_name] = matx_dict[full_name].tocsr()
                            except KeyError, e:
                                raise e

        return


def calculate_tf(VSM, suffix='', job_server=None, ngram=1, verbose=False):
    """
    Calculates Term Frequency (TF) matrix. 
    Stores scipy.sparse.lil_matrix in data_dict
    Returns processing time
    """
    meta_dict = VSM.meta_dict
    data_dict = VSM.data_dict
    matx_dict = VSM.matx_dict
    time_dict = VSM.time_dict
    doc_store = VSM.doc_store
    ngstr = '_%d' % ngram
    tokens_map = meta_dict[('tokens_map' + ngstr)]
    if not tokens_map:
        errors.ProcessWarning('Empty tokens_map' + ngstr)
        return
    guids = meta_dict['guids']
    token_str = 'tokens' + suffix + ngstr
    if token_str in meta_dict and meta_dict[token_str]:
        tokens_tuple = [ (guid, guids[guid], th) for (guid, th) in meta_dict[token_str].items() ]
    else:
        tokens_tuple = ((guid, index, doc_store.get_tokens_by_guid(guid, suffix, ngstr, verbose)[guid]) for (guid, index) in meta_dict['guids'].items())
    valid_indices = sorted(guids.values())
    last_index = meta_dict['last_index']
    name = 'tf' + suffix + ngstr
    sparsity = meta_dict['expected_sparsity']

    def preallocate(sparsity):
        with debug.Timer(name, None, verbose, process_vsm_logger):
            estimated_nnz = int(shape[0] * shape[1] * sparsity)
            msg = 'Expected sparsity %.3f, estimated nnz %d' % (
             sparsity, estimated_nnz)
            debug.print_verbose(msg, verbose, process_vsm_logger)
            try:
                data = numpy.zeros(estimated_nnz, dtype=numpy.uint16)
                indices = [
                 numpy.zeros(estimated_nnz, dtype=numpy.uint64),
                 numpy.zeros(estimated_nnz, dtype=numpy.uint64)]
            except MemoryError, e:
                errors.ProcessWarning(e.__repr__(), process_vsm_logger)
                return preallocate(sparsity / 2)

            nnz = 0
        return (data, indices, nnz, estimated_nnz)

    def create_matrix(data, indices, nnz, shape, attempts=0):
        with debug.Timer(name, None, verbose, process_vsm_logger):
            try:
                attempts += 1
                return scipy.sparse.csr_matrix((data, indices), shape=shape, dtype=numpy.uint16)
            except ValueError, e:
                msg = name + ' constuction failed: ' + str(e)
                errors.ProcessWarning(msg, process_vsm_logger)
                new_shape = (
                 max(shape[0], max(indices[0] + 1)), max(shape[1], max(indices[1] + 1)))
                if attempts < 2:
                    return create_matrix(data, indices, nnz, new_shape, attempts)
                return scipy.sparse.csr_matrix(shape, dtype=numpy.uint16)

        return

    def check_matrix(name):
        with debug.Timer(name, None, verbose, process_vsm_logger):
            if matx_dict[name] is None:
                msg = '%s matrix constuction failed (None)'
                raise errors.ProcessError(msg, process_vsm_logger)
            if matx_dict[name].nnz != nnz:
                msg = '%s matrix constuction failed (tf.nnz = %d, nnz = %d)' % (
                 name, matx_dict[name].nnz, nnz)
                raise errors.ProcessError(msg, process_vsm_logger)
            if nnz == 0:
                msg = name + ' matrix constuction failed (nnz = 0)'
                errors.ProcessWarning(msg, process_vsm_logger)
            if botnee_config.DEBUG:
                if 'bmj:seed' in guids and suffix == '':
                    ridx = guids['bmj:seed']
                    row = matx_dict[name][ridx, :]
                    try:
                        ihash = hash(tuple(row.indices.tolist()))
                        dhash = hash(tuple(row.data.tolist()))
                        print 'create_matrix', ihash, dhash
                        assert all(row.toarray().ravel() == meta_dict['seed_freq'])
                        assert ihash == meta_dict['seed_freq_ihash']
                        assert dhash == meta_dict['seed_freq_dhash']
                    except:
                        pass

        return

    def iterate_over_docs(data, indices, nnz, estimated_nnz):
        with debug.Timer(name, None, verbose, process_vsm_logger):
            expand = False
            for (i, (guid, index, tokens)) in enumerate(tokens_tuple):
                debug.print_dot(i, verbose)
                freq = get_frequency(tokens, tokens_map, ngram)
                if botnee_config.DEBUG and guid == 'bmj:seed' and suffix == '':
                    if 'seed_freq' + suffix in meta_dict:
                        pass
                    meta_dict['seed_freq'] = freq
                    meta_dict['seed_freq_hash'] = hash(tuple(freq.tolist()))
                    sfi = numpy.flatnonzero(freq)
                    sfd = freq[sfi]
                    meta_dict['seed_freq_ihash'] = hash(tuple(sfi.tolist()))
                    meta_dict['seed_freq_dhash'] = hash(tuple(sfd.tolist()))
                    print 'iterate_over_docs', meta_dict['seed_freq_ihash'], meta_dict['seed_freq_dhash']
                vec_nnz = numpy.count_nonzero(freq)
                rng = range(nnz, nnz + vec_nnz)
                if not rng:
                    continue
                if rng[(-1)] >= len(data):
                    if not expand:
                        msg = 'Estimated nnz %d too low, appending' % estimated_nnz
                        debug.print_verbose(msg, verbose, process_vsm_logger, logging.WARNING)
                        expand = True
                    expand_len = int(shape[0] * shape[1] * meta_dict['expected_sparsity'])
                    expand_len = max(expand_len, len(freq))
                    data = numpy.append(data, numpy.zeros(expand_len, dtype=numpy.uint16))
                    indices[0] = numpy.append(indices[0], numpy.zeros(expand_len, dtype=numpy.uint64))
                    indices[1] = numpy.append(indices[1], numpy.zeros(expand_len, dtype=numpy.uint64))
                try:
                    indices[1][rng] = numpy.array(numpy.flatnonzero(freq), dtype=numpy.uint64)
                    data[rng] = freq[indices[1][rng]]
                    indices[0][rng] = index
                    nnz += vec_nnz
                except IndexError, e:
                    debug.ProcessWarning(e.__repr__(), process_vsm_logger)
                    raise e

            data = data[0:nnz]
            indices[0] = indices[0][0:nnz]
            indices[1] = indices[1][0:nnz]
            if expand:
                meta_dict['expected_sparsity'] *= 2
                msg = 'Reset estimated sparsity to %.3f' % meta_dict['expected_sparsity']
                debug.print_verbose(msg, verbose, process_vsm_logger)
            return (
             data, indices, nnz)
        return

    shape = (
     meta_dict['last_index'] + 1, len(tokens_map))
    with debug.Timer(name, time_dict, verbose, process_vsm_logger):
        (data, indices, nnz, estimated_nnz) = preallocate(sparsity)
        (data, indices, nnz) = iterate_over_docs(data, indices, nnz, estimated_nnz)
        matx_dict[name] = create_matrix(data, indices, nnz, shape)
        check_matrix(name)


def get_frequency(tokens, tokens_map, ngram=1):
    """
    Given a set of tokens (hashed) and a hash map returns the freqencies
    """
    freq = numpy.zeros(len(tokens_map), dtype=numpy.uint16)
    caster = get_caster(ngram)
    for sentence in tokens:
        for token in sentence:
            if caster(token) in tokens_map:
                freq[tokens_map[caster(token)]] += 1

    return freq


def calculate_doc_freq(VSM, verbose=False):
    """
    Calculates Docuement Frequency vector. 
    Stores doc_freq as numpy.arrays in data_dict
    """
    data_dict = VSM.data_dict
    matx_dict = VSM.matx_dict
    time_dict = VSM.time_dict
    with debug.Timer(None, time_dict, verbose, process_vsm_logger):
        tf = matx_dict['tf']
        data_dict['doc_freq'] = numpy.array((tf / tf).sum(axis=0).ravel(), dtype=numpy.float32)
        if (data_dict['doc_freq'] == 0).any():
            msg = 'Zeros in document frequency vector'
            raise errors.ProcessError(msg, process_vsm_logger)
    return


def calculate_idf(VSM, method='', ngstr='_1', verbose=False):
    """
    Calculates Inverse Docuement Frequency (IDF) vector. 
    Stores doc_freq and idf as numpy.arrays in data_dict
    method=1: method from http://en.wikipedia.org/wiki/Tf%E2%80%93idf
    method=2: method from http://en.wikipedia.org/wiki/Okapi_BM25
    """
    data_dict = VSM.data_dict
    meta_dict = VSM.meta_dict
    matx_dict = VSM.matx_dict
    time_dict = VSM.time_dict
    doc_store = VSM.doc_store
    with debug.Timer('(%s)' % ngstr, time_dict, verbose, process_vsm_logger):
        try:
            tf = matx_dict[('tf' + ngstr)].tocsr()
        except AttributeError, e:
            raise e

        if 'n_docs' in meta_dict:
            n_docs = meta_dict['n_docs']
        else:
            n_docs = tf.shape[0]
        term_freq = numpy.array((tf / tf).sum(axis=0), dtype=float).ravel()
        if any(term_freq == 0):
            msg = 'Zero found in term_freq vector'
            raise errors.ProcessError(msg, process_vsm_logger)
        if botnee_config.DEBUG:
            term_freq_vals = data_dict[('term_freq' + ngstr)]
            term_freq1 = numpy.array(term_freq_vals, dtype=float)
            if not all(term_freq1 == term_freq):
                print term_freq[numpy.where(term_freq != term_freq1)]
                print term_freq1[numpy.where(term_freq != term_freq1)]
                debug.debug_here()
                errors.ProcessWarning('Methods of calculating term frequency differ!')
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('error', category=RuntimeWarning)
                if method == '':
                    idf = numpy.array(numpy.log(n_docs / term_freq))
                elif method == '_bm25':
                    idf = numpy.array(numpy.log((n_docs - term_freq + 0.5) / (term_freq + 0.5)))
                else:
                    msg = 'invalid method specified: ' + str(method)
                    raise errors.ProcessError(msg, process_vsm_logger)
        except RuntimeWarning, w:
            msg = 'Divide by zero. ' + str(w)
            raise errors.ProcessError(msg, process_vsm_logger)

        if (numpy.abs(idf) == numpy.inf).any():
            msg = 'Inf found in IDF vector'
            raise errors.ProcessError(msg, process_vsm_logger)
        if (idf == numpy.nan).any():
            msg = 'NaN found in IDF vector'
            raise errors.ProcessError(msg, process_vsm_logger)
        data_dict['idf' + method + ngstr] = idf


def calculate_tfidf(VSM, suffix, job_server, idf_method, ngstr, verbose):
    """
    Calculates TF-IDF matrix from TF and IDF. Returns scipy.sparse.csr_matrix.
    """
    meta_dict = VSM.meta_dict
    data_dict = VSM.data_dict
    matx_dict = VSM.matx_dict
    time_dict = VSM.time_dict
    doc_store = VSM.doc_store

    def empty_row_msg(i, verbose=0):
        guid = doc_store.get_guids_by_indices([i])
        str_err = 'Document with no tf%s%s data: %d ' % (suffix, ngstr, i)
        if guid:
            str_err += guid[0]
        if verbose == 2:
            debug.print_verbose(str_err, verbose, process_vsm_logger)

    def calculate_block(fninputs):
        block = {'data': numpy.array([], dtype=numpy.float16), 
           'indices': [[], []], 'nnz': 0}
        errors = []
        (irange, tfs, idft, verbose) = fninputs
        if type(tfs) is tuple:
            from scipy import sparse
            tf = sparse.csr_matrix(tfs[0], tfs[1])
        else:
            tf = tfs
        from botnee import debug
        for i in irange:
            debug.print_dot(i, verbose)
            try:
                row = tf[i, :]
                row_nnz = row.nnz
                (_, col_indices) = row.nonzero()
                idft_small = idft[col_indices]
                if row_nnz == 0:
                    errors.append(i)
                    continue
                else:
                    row_data = row.data
                    tfidf_row = calculate_tfidf_row(row_data, idft_small)
                    block['data'] = numpy.append(block['data'], tfidf_row)
                    row_indices = numpy.ones(row_nnz, dtype=numpy.uint64) * i
                    block['indices'][0].extend(row_indices)
                    block['indices'][1].extend(col_indices)
                    block['nnz'] += row_nnz
            except Exception, e:
                debug.ProcessWarning(e.__repr__(), process_vsm_logger)

        return (block, errors)

    with debug.Timer(None, time_dict, verbose, process_vsm_logger):
        tf = matx_dict[('tf' + suffix + ngstr)].tocsr()
        shape = tf.shape
        n_docs = tf.shape[0]
        idf = data_dict[('idf' + idf_method + ngstr)]
        idft = data_dict[('idf' + idf_method + ngstr)][:].transpose()
        try:
            nnz = 0
            data = numpy.array([], dtype=numpy.float16)
            indices = [[], []]
            all_errors = []
            if job_server:
                n_blocks = 20
                ranges = [ (n_docs * i / n_blocks, n_docs * (i + 1) / n_blocks) for i in range(n_blocks)
                         ]
                tfs = (
                 (
                  tf.data, tf.indices, tf.indptr), tf.shape)
                jobs = []
                for idxs in ranges:
                    fninput = (
                     xrange(idxs[0], idxs[1]), tfs, idft, False)
                    job = job_server.submit(calculate_block, (
                     fninput,), (
                     calculate_tfidf_row,), ('numpy', 'scipy', 'botnee_config', 'botnee'))
                    if job:
                        jobs.append((fninput, job))
                    else:
                        debug.debug_here()

                for (fninput, job) in jobs:
                    (block, errors) = job()
                    all_errors.extend(errors)
                    data = numpy.append(data, block['data'])
                    indices[0].extend(block['indices'][0])
                    indices[1].extend(block['indices'][1])
                    nnz += block['nnz']

            n_blocks = 1
            ranges = [ (n_docs * i / n_blocks, n_docs * (i + 1) / n_blocks) for i in range(n_blocks)
                     ]
            for idxs in ranges:
                fninputs = (
                 xrange(idxs[0], idxs[1]), tf, idft, verbose)
                (block, errors) = calculate_block(fninputs)
                all_errors.extend(errors)
                data = numpy.append(data, block['data'])
                indices[0].extend(block['indices'][0])
                indices[1].extend(block['indices'][1])
                nnz += block['nnz']

            debug.print_verbose('\n', verbose, process_vsm_logger)
            for error in errors:
                empty_row_msg(error, verbose)

        except ValueError, e:
            raise e
        except IndexError, e:
            raise e

        try:
            dtype = botnee_config.MATRIX_TYPES['tfidf']
            tfidf = scipy.sparse.csr_matrix((data, indices), tf.shape, dtype)
            matx_dict['tfidf' + idf_method + suffix + ngstr] = tfidf
        except Exception, e:
            debug.ProcessWarning(e.__repr__(), process_vsm_logger)

    return


def calculate_tfidf_row(row, idft):
    """
    Calculates single row of TFIDF matrix. 
    Used for job_server processing
    idf vector should be passed in transposed like so:
        idft = idf[:].transpose()
    """
    vec = numpy.multiply(row, idft)
    if botnee_config.NORMALISE:
        norm = numpy.linalg.norm(vec)
        if norm > 0:
            vec[:] = numpy.divide(vec, norm)
    return vec


def calculate_kernel(VSM, verbose=False):
    """Calculates Kernel Matrix from TF-IDF matrix. Returns scipy.sparse.csr_matrix,
       although in reality the Kernel matrix is never (rarely) sparse!"""
    data_dict = VSM.data_dict
    matx_dict = VSM.matx_dict
    time_dict = VSM.time_dict
    with debug.Timer(None, time_dict, verbose, process_vsm_logger):
        matx_dict['K'] = matx_dict['tfidf'] * matx_dict['tfidf'].transpose()
        I = scipy.sparse.lil_matrix(matx_dict['K'].shape)
        I.setdiag(numpy.ones(matx_dict['K'].shape[0]))
        matx_dict['K'] -= matx_dict['K'].multiply(I)
    return