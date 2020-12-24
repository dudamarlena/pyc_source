# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/smr/shared.py
# Compiled at: 2014-08-02 17:35:20
from __future__ import absolute_import, division, print_function, unicode_literals
import boto, curses, os
from Queue import Empty
GLOBAL_SHARED_DATA = {b'files_processed': 0, 
   b'bytes_processed': 0, 
   b'last_file_processed': b'', 
   b'messages': []}

def reduce_thread(reduce_process, output_queue, abort_event):
    while not abort_event.is_set():
        try:
            result = output_queue.get(timeout=2)
            if reduce_process.poll() is not None:
                abort_event.set()
                break
            reduce_process.stdin.write(result)
            reduce_process.stdin.flush()
            output_queue.task_done()
        except Empty:
            pass

    return


def print_pid(process, window, line_num, process_name):
    try:
        cpu_percent = process.cpu_percent(0.1)
    except:
        cpu_percent = 0.0

    add_str(window, line_num, (b'  {} pid {} CPU {}').format(process_name, process.pid, cpu_percent))


def add_str(window, line_num, str):
    """ attempt to draw str on screen and ignore errors if they occur """
    try:
        window.addstr(line_num, 0, str)
    except curses.error:
        pass


def progress_thread(processed_files_queue, abort_event):
    while not abort_event.is_set():
        try:
            file_name, file_size = processed_files_queue.get(timeout=2)
            GLOBAL_SHARED_DATA[b'files_processed'] += 1
            GLOBAL_SHARED_DATA[b'bytes_processed'] += file_size
            GLOBAL_SHARED_DATA[b'last_file_processed'] = file_name
            processed_files_queue.task_done()
        except Empty:
            pass


def get_param(param):
    return GLOBAL_SHARED_DATA[param]


def add_message(message):
    GLOBAL_SHARED_DATA[b'messages'].append(message)


def write_file_to_descriptor(input_queue, descriptor):
    """
    get item from input_queue and write it to descriptor
    returns True if and only if it was successfully written
    """
    try:
        file_name = input_queue.get(timeout=2)
        descriptor.write((b'{}\n').format(file_name))
        descriptor.flush()
        input_queue.task_done()
        return True
    except Empty:
        descriptor.close()
        return False
    except IOError:
        return False


def ensure_dir_exists(path):
    dir_name = os.path.dirname(path)
    if dir_name != b'' and not os.path.exists(dir_name):
        os.makedirs(dir_name)


def get_args(process, config, config_path=None):
    args = [process]
    if config.aws_access_key:
        args.append(b'--aws-access-key')
        args.append(config.aws_access_key)
    elif boto.config.get(b'Credentials', b'aws_access_key_id'):
        args.append(b'--aws-access-key')
        args.append(boto.config.get(b'Credentials', b'aws_access_key_id'))
    if config.aws_secret_key:
        args.append(b'--aws-secret-key')
        args.append(config.aws_secret_key)
    elif boto.config.get(b'Credentials', b'aws_secret_access_key'):
        args.append(b'--aws-secret-key')
        args.append(boto.config.get(b'Credentials', b'aws_secret_access_key'))
    if not config_path:
        config_path = config.config
    args.append(config_path)
    return args