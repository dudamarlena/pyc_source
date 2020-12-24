# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fsdb/utils.py
# Compiled at: 2016-03-24 13:25:59
import os, errno, tempfile, platform

def calc_dir_mode(mode):
    R_OWN = int('0400', 8)
    R_GRP = int('0040', 8)
    R_OTH = int('0004', 8)
    X_OWN = int('0100', 8)
    X_GRP = int('0010', 8)
    X_OTH = int('0001', 8)
    if mode & R_OWN:
        mode |= X_OWN
    if mode & R_GRP:
        mode |= X_GRP
    if mode & R_OTH:
        mode |= X_OTH
    return mode


def copy_content(origin, dstPath, blockSize, mode):
    """ copy the content of `origin` to `dstPath` in a safe manner.

        this function will first copy the content to a temporary file
        and then move it atomically to the requested destination.

        if some error occurred during content copy or file movement
        the temporary file will be deleted.
    """
    tmpFD, tmpPath = tempfile.mkstemp(prefix=os.path.basename(dstPath) + '_', suffix='.tmp', dir=os.path.dirname(dstPath))
    try:
        try:
            oldmask = os.umask(0)
            try:
                os.chmod(tmpPath, mode)
            finally:
                os.umask(oldmask)

            while True:
                chunk = origin.read(blockSize)
                if not chunk:
                    break
                os.write(tmpFD, chunk)

        finally:
            os.close(tmpFD)

        try:
            os.rename(tmpPath, dstPath)
        except OSError as e:
            if platform.system() is 'Windows' and e.errno is errno.EEXIST:
                pass
            else:
                raise

    except:
        os.remove(tmpPath)
        raise