# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/checkers.py
# Compiled at: 2019-04-28 04:54:30
import gzip, re, sys, tarfile, zipfile
from six import BytesIO
from six.moves import filter
from galaxy import util
from galaxy.util.image_util import image_type
if sys.version_info < (3, 3):
    gzip.GzipFile.read1 = gzip.GzipFile.read
    try:
        import bz2file as bz2
    except ImportError:
        import bz2

else:
    import bz2
HTML_CHECK_LINES = 100

def check_html(file_path, chunk=None):
    if chunk is None:
        temp = open(file_path, mode='rb')
    else:
        if hasattr(chunk, 'splitlines'):
            temp = chunk.splitlines()
        else:
            temp = chunk
        regexp1 = re.compile('<A\\s+[^>]*HREF[^>]+>', re.I)
        regexp2 = re.compile('<IFRAME[^>]*>', re.I)
        regexp3 = re.compile('<FRAMESET[^>]*>', re.I)
        regexp4 = re.compile('<META[\\W][^>]*>', re.I)
        regexp5 = re.compile('<SCRIPT[^>]*>', re.I)
        lineno = 0
        for line in temp:
            line = util.unicodify(line)
            lineno += 1
            matches = regexp1.search(line) or regexp2.search(line) or regexp3.search(line) or regexp4.search(line) or regexp5.search(line)
            if matches:
                if chunk is None:
                    temp.close()
                return True
            if HTML_CHECK_LINES and lineno > HTML_CHECK_LINES:
                break

    if chunk is None:
        temp.close()
    return False


def check_binary(name, file_path=True):
    if file_path:
        temp = open(name, 'rb')
    else:
        temp = BytesIO(name)
    try:
        return util.is_binary(temp.read(1024))
    finally:
        temp.close()


def check_gzip(file_path, check_content=True):
    try:
        with open(file_path, 'rb') as (temp):
            magic_check = temp.read(2)
        if magic_check != util.gzip_magic:
            return (False, False)
    except Exception:
        return (
         False, False)

    try:
        with gzip.open(file_path, 'rb') as (fh):
            header = fh.read(4)
        if header == '.sff':
            return (True, True)
    except Exception:
        return (
         False, False)

    if not check_content:
        return (True, True)
    CHUNK_SIZE = 32768
    gzipped_file = gzip.GzipFile(file_path, mode='rb')
    chunk = gzipped_file.read(CHUNK_SIZE)
    gzipped_file.close()
    if check_html(file_path, chunk=chunk):
        return (True, False)
    return (
     True, True)


def check_bz2(file_path, check_content=True):
    try:
        with open(file_path, 'rb') as (temp):
            magic_check = temp.read(3)
        if magic_check != util.bz2_magic:
            return (False, False)
    except Exception:
        return (
         False, False)

    if not check_content:
        return (True, True)
    CHUNK_SIZE = 32768
    bzipped_file = bz2.BZ2File(file_path, mode='rb')
    chunk = bzipped_file.read(CHUNK_SIZE)
    bzipped_file.close()
    if check_html(file_path, chunk=chunk):
        return (True, False)
    return (
     True, True)


def check_zip(file_path, check_content=True, files=1):
    if not zipfile.is_zipfile(file_path):
        return (False, False)
    else:
        if not check_content:
            return (True, True)
        CHUNK_SIZE = 32768
        chunk = None
        for filect, member in enumerate(iter_zip(file_path)):
            handle, name = member
            chunk = handle.read(CHUNK_SIZE)
            if chunk and check_html(file_path, chunk):
                return (True, False)
            if filect >= files:
                break

        return (
         True, True)


def is_bz2(file_path):
    is_bz2, is_valid = check_bz2(file_path, check_content=False)
    return is_bz2


def is_gzip(file_path):
    is_gzipped, is_valid = check_gzip(file_path, check_content=False)
    return is_gzipped


def is_zip(file_path):
    is_zipped, is_valid = check_zip(file_path, check_content=False)
    return is_zipped


def is_single_file_zip(file_path):
    for i, member in enumerate(iter_zip(file_path)):
        if i > 1:
            return False

    return True


def is_tar(file_path):
    return tarfile.is_tarfile(file_path)


def iter_zip(file_path):
    with zipfile.ZipFile(file_path) as (z):
        for f in filter(lambda x: not x.endswith('/'), z.namelist()):
            yield (
             z.open(f), f)


def check_image(file_path):
    """ Simple wrapper around image_type to yield a True/False verdict """
    if image_type(file_path):
        return True
    return False


__all__ = ('check_binary', 'check_bz2', 'check_gzip', 'check_html', 'check_image',
           'check_zip', 'is_gzip', 'is_bz2', 'is_zip')