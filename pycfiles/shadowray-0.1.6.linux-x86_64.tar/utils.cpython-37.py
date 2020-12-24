# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/common/utils.py
# Compiled at: 2019-06-22 22:55:59
# Size of source mod 2**32: 1835 bytes
import re, subprocess, requests, time

def parse_yes_or_no(text):
    text = str(text).lower()
    if text == 'yes' or text == 'y':
        return True
    if text == 'no' or text == 'n':
        return False
    return


def print_progress(percent, width=60, extra=''):
    if percent > 100:
        percent = 100
    format_str = '[%%-%ds]' % width % ('#' * int(percent * width / 100.0))
    print(('\r%s  %.2f%%  %s' % (format_str, percent, extra)), end='')


def download_file(url, filename, show_progress=False):
    r = requests.get(url, stream=True)
    length = float(r.headers['content-length'])
    f = open(filename, 'wb')
    count = 0
    time_s = time.time()
    speed = 0
    count_s = 0
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if show_progress:
                percent = count / length * 100.0
                time_e = time.time()
                if time_e - time_s > 1:
                    speed = (count - count_s) / (time_e - time_s) / 1024 / 1024
                    count_s = count
                    time_s = time_e
                print_progress(percent, extra=('%.2fM/S' % speed))

    f.close()


def find_arg_in_opts(opts, key):
    for k, v in opts:
        if k == key:
            return v


def write_to_file(filename, mode, content):
    f = open(filename, mode)
    f.write(content)
    f.close()


def ping(host, times=3, timeout=1):
    command = [
     'ping', '-c', str(times), host, '-W', str(timeout)]
    r = subprocess.run(command, stdout=(subprocess.PIPE))
    reg = 'min/avg/max/mdev = ([0-9]+.[0-9]+)/([0-9]+.[0-9]+)'
    s = re.search(reg, str(r.stdout))
    if s is not None:
        return s.group(1)
    return -1