# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\DownloadTool\download.py
# Compiled at: 2014-12-10 07:44:53
"""
默认读取md5.txt文件 创建download文件夹，启用多线程下载，我很懒不写命令行
"""
import os, threading, st_log as log
log = log.init_log('log/download')
log.debug('init download.log')
file_name = 'md5.txt'
line = 0
finish_num = 0
mutex = threading.Lock()
base_path = os.path.dirname(os.path.abspath(__file__))
download_dir = 'download'
download_abs_dir = os.path.join(base_path, download_dir)
abs_filename = os.path.join(base_path, file_name)
wget_path = os.path.join(base_path, '../bin/wget.exe')
wget_path = ('').join(['"', wget_path, '"'])
wget_argv = '-c'
download_url = 'store.bav.baidu.com/cgi-bin/download_av_sample.cgi?hash=%s'
command = (' ').join([wget_path, wget_argv, download_url])

def _create_dir(download_abs_dir):
    if os.path.exists(download_abs_dir):
        pass
    else:
        try:
            os.mkdir(download_abs_dir)
        except Exception as e:
            log.error(e)
            import sys
            sys.exit(0)


def _total_line(file_name):
    global line
    with open(file_name) as (f):
        for i in f:
            line = line + 1


def _readline_and_download(md5):
    global finish_num
    cmd = command % md5
    log.debug('cmd is %s...' % cmd)
    os.system(cmd)
    mutex.acquire()
    finish_num += 1
    log.debug('completed %.2f%%.' % (float(finish_num) / line * 100))
    mutex.release()


def main():
    u"""默认读取md5.txt文件 创建download文件夹，启用多线程下载，我很懒不写命令行
    参数了

    :returns: None

    """
    _create_dir(download_abs_dir)
    _total_line(file_name)
    from multiprocessing.dummy import Pool as ThreadPool
    threading_num = 9
    pool = ThreadPool(threading_num)
    os.chdir(download_abs_dir)
    with open(abs_filename) as (f):
        pool.map(_readline_and_download, f)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()