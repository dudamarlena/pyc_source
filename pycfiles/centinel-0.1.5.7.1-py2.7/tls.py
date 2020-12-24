# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/primitives/tls.py
# Compiled at: 2017-02-27 23:23:39
import logging
try:
    import M2Crypto
    m2crypto_imported = True
except ImportError:
    logging.warning('M2Crypto could not be imported. TLS fingerprinting will be disabled.')
    m2crypto_imported = False

import ssl, socket, threading, time
MAX_THREAD_START_RETRY = 10
THREAD_START_DELAY = 3

def get_fingerprint(host, port=443, external=None, log_prefix=''):
    tls_error = None
    fingerprint_error = None
    cert = None
    logging.debug('%sGetting TLS certificate for %s:%d.' % (
     log_prefix, host, port))
    socket.setdefaulttimeout(10)
    try:
        cert = ssl.get_server_certificate((host, port), ssl_version=ssl.PROTOCOL_TLSv1)
    except ssl.SSLError:
        try:
            cert = ssl.get_server_certificate((host, port), ssl_version=ssl.PROTOCOL_SSLv23)
        except Exception as exp:
            tls_error = str(exp)

    except Exception as exp:
        tls_error = str(exp)

    if type(cert) == unicode:
        cert = cert.encode('ascii', 'ignore')
    if tls_error is None and m2crypto_imported:
        try:
            x509 = M2Crypto.X509.load_cert_string(cert, M2Crypto.X509.FORMAT_PEM)
            fingerprint = x509.get_fingerprint('sha1')
        except Exception as exp:
            fingerprint_error = str(exp)

    if not m2crypto_imported:
        fingerprint_error = 'M2Crypto could not be imported.'
    row = '%s:%s' % (host, port)
    if tls_error is None and fingerprint_error is None:
        if external is not None and type(external) is dict:
            external[row] = {'cert': cert, 'fingerprint': fingerprint.lower()}
        return (fingerprint.lower(), cert)
    else:
        if tls_error is None and fingerprint_error is not None:
            if external is not None and type(external) is dict:
                external[row] = {'cert': cert, 'fingerprint_error': fingerprint_error}
            return (fingerprint_error, cert)
        else:
            if external is not None and type(external) is dict:
                external[row] = {'tls_error': tls_error, 'fingerprint_error': fingerprint_error}
            return (
             fingerprint_error, tls_error)

        return


def get_fingerprint_batch(input_list, results={}, default_port=443, delay_time=0.5, max_threads=100):
    """
    This is a parallel version of the TLS fingerprint primitive.

    :param input_list: the input is a list of host:ports.
    :param default_port: default port to use when no port specified
    :param delay_time: delay before starting each thread
    :param max_threads: maximum number of concurrent threads
    :return:
    """
    threads = []
    thread_error = False
    thread_wait_timeout = 200
    ind = 1
    total_item_count = len(input_list)
    for row in input_list:
        if len(row.split(':')) == 2:
            host, port = row.split(':')
        else:
            if len(row.split(':')) == 1:
                host = row
                port = default_port
            else:
                continue
            port = int(port)
            wait_time = 0
            while threading.active_count() > max_threads:
                time.sleep(1)
                wait_time += 1
                if wait_time > thread_wait_timeout:
                    thread_error = True
                    break

            if thread_error:
                results['error'] = 'Threads took too long to finish.'
                break
            time.sleep(delay_time)
            log_prefix = '%d/%d: ' % (ind, total_item_count)
            thread = threading.Thread(target=get_fingerprint, args=(
             host, port,
             results, log_prefix))
            ind += 1
            thread.setDaemon(1)
            thread_open_success = False
            retries = 0
            while not thread_open_success and retries < MAX_THREAD_START_RETRY:
                try:
                    thread.start()
                    threads.append(thread)
                    thread_open_success = True
                except:
                    retries += 1
                    time.sleep(THREAD_START_DELAY)
                    logging.error('%sThread start failed for %s, retrying... (%d/%d)' % (log_prefix, host, retries, MAX_THREAD_START_RETRY))

        if retries == MAX_THREAD_START_RETRY:
            logging.error("%sCan't start a new thread for %s after %d retries." % (log_prefix, host, retries))

    for thread in threads:
        thread.join(thread_wait_timeout)

    return results