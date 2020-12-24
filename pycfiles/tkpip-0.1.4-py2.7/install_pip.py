# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkpip\install_pip.py
# Compiled at: 2013-07-17 13:09:30
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, os, tempfile, logging
if sys.version_info >= (3, ):
    import urllib.request as urllib2, urllib.parse as urlparse
else:
    import urllib2, urlparse

def step_1():
    logging.info(b'Checking Setuptools/Distribute')
    try:
        import setuptools
        logging.info(b'Setuptools/Distribute installed!')
    except ImportError:
        logging.info(b'Installing Setuptools...')
        url = b'https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py'
        dtemp = tempfile.mkdtemp()
        filename = download_file(url, dtemp)
        os.system((b'{0} {1}').format(sys.executable, filename))


def step_2():
    logging.info(b'Checking Pip')
    try:
        import pip
        logging.info(b'Pip installed!')
    except ImportError:
        logging.info(b'Installing Pip...')
        from pkg_resources import load_entry_point
        packages_list = [
         b'pip']
        install_func = load_entry_point(b'setuptools', b'console_scripts', b'easy_install')
        return install_func(packages_list)


def download_file(url, desc=None):
    u = urllib2.urlopen(url)
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = b'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)
    with open(filename, b'wb') as (f):
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, b'getheaders') else meta.get_all
        meta_length = meta_func(b'Content-Length')
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print((b'Downloading: {0} Bytes: {1}').format(url, file_size))
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = (b'{0:16}').format(file_size_dl)
            if file_size:
                status += (b'   [{0:6.2f}%]').format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end=b'')

        print()
    return filename


if __name__ == b'__main__':
    logging.basicConfig(level=logging.INFO)
    step = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    func_name = (b'step_{0}').format(step)
    f = globals()[func_name] if func_name in globals() else None
    if f:
        logging.info((b'=== Step {0} ===').format(step))
        res = f()
        os.system((b'{0} {1} {2}').format(sys.executable, os.path.basename(__file__), step + 1))