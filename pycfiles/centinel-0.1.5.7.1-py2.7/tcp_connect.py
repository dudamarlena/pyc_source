# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/primitives/tcp_connect.py
# Compiled at: 2017-02-27 23:23:39
from datetime import datetime
import logging, socket, time, threading
MAX_THREAD_START_RETRY = 10
THREAD_START_DELAY = 3

def tcp_connect(host, port, external=None, log_prefix=''):
    result = {'host': host, 
       'port': port}
    logging.debug(log_prefix + 'Testing TCP connect to %s:%s...' % (host, port))
    try:
        ip = socket.gethostbyname(host)
        if ip is not None:
            result['ip'] = ip
    except Exception as err:
        result['ip_err'] = str(err)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(True)
        sock.settimeout(5)
        start_time = datetime.now()
        sock.connect((host, int(port)))
        end_time = datetime.now()
        elapsed = int((end_time - start_time).total_seconds() * 1000)
        sock.close()
        result['success'] = 'true'
    except Exception as err:
        end_time = datetime.now()
        elapsed = int((end_time - start_time).total_seconds() * 1000)
        result['failure'] = str(err)

    result['time'] = str(elapsed)
    if external is not None and type(external) is dict:
        external[host + ':' + str(port)] = result
    return result


def tcp_connect_batch(input_list, results={}, delay_time=0.1, max_threads=100):
    """
    This is a parallel version of the TCP connect primitive.

    :param input_list: the input is a list of host/port pairs
    :param delay_time: delay before starting each thread
    :param max_threads: maximum number of concurrent threads
    :return:
    """
    threads = []
    thread_error = False
    thread_wait_timeout = 200
    ind = 1
    total_item_count = len(input_list)
    for host, port in input_list:
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
        thread = threading.Thread(target=tcp_connect, args=(
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