# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/downloader.py
# Compiled at: 2015-10-03 06:58:58
"""

File downloader with progress bar and download speed

"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from ..console import Console
from ..progress import Progress
import hashlib, requests
from time import time

class DownloaderError(Exception):
    pass


def _filesize(size):
    try:
        size = int(size)
    except:
        raise ValueError((b'filesize requires a numeric value, not {!r}').format(size))

    suffixes = ('kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    base = 1024
    if size == 1:
        return b'1 byte'
    if size < base:
        return (b'{:,} bytes').format(size)
    for i, suffix in enumerate(suffixes):
        unit = base ** (i + 2)
        if size < unit:
            return (b'{:,.01f} {}').format(base * size / unit, suffix)

    return (b'{:,.01f} {}').format(base * size / unit, suffix)


def download(url, store_file, filename=None, console=None, chunk_size=16384, auth=None, verify_ssl=True, msg=b'contacting server'):
    """Download a url and render a progress bar"""
    if console is None:
        console = Console()
    if filename is None:
        filename = url.rsplit(b'/')[(-1)]
    console.show_cursor(False)
    try:
        progress_width = 24
        progress = Progress(console, (b'{}').format(filename), width=progress_width, vanish=False)
        progress.update(0, msg=msg)
        try:
            response = requests.get(url, stream=True, auth=auth, verify=verify_ssl)
            start = time()
            length = response.headers.get(b'content-length')
            if response.status_code != 200:
                raise DownloaderError((b'downloader received bad status code ({})').format(response.status_code))
            m = hashlib.md5()
            bytes_read = 0
            if length is None:
                console((b'downloading {}').format(filename))
                console.flush()
                for data in response.iter_content(chunk_size):
                    store_file.write(data)
                    m.update(data)

                console.nl()
            else:
                length = int(length)
                progress.set_num_steps(length)
                for data in response.iter_content(chunk_size):
                    store_file.write(data)
                    m.update(data)
                    bytes_read += len(data)
                    bytes_per_second = int(float(bytes_read) / (time() - start))
                    speed = (b'{filename}').format(filename=filename, speed=(_filesize(bytes_per_second) + b'/s').ljust(16))
                    progress.step(len(data), msg=speed)

        finally:
            progress.done()

    finally:
        console.show_cursor(True)

    return m.hexdigest()