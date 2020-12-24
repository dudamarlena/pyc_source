# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s3am/__init__.py
# Compiled at: 2016-11-03 16:06:47
import logging, os, sys
me = os.path.basename(sys.argv[0])
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN, format='%(asctime)-15s %(module)s(%(process)d) %(message)s')

class UserError(Exception):
    status_code = 2


def user_error(_status_code):
    assert _status_code > UserError.status_code

    class _UserError(UserError):
        status_code = _status_code

    return _UserError


ObjectExistsError = user_error(3)
UploadExistsError = user_error(4)
InvalidSourceURLError = user_error(5)
InvalidDestinationURLError = user_error(6)
InvalidS3URLError = user_error(7)
IncompatiblePartSizeError = user_error(8)
InvalidChecksumAlgorithmError = user_error(9)
InvalidEncryptionKeyError = user_error(10)
FileExistsError = user_error(11)
DownloadExistsError = user_error(12)
MultipleUploadsExistError = user_error(13)

class WorkerException(Exception):
    """
    An exception where we let other workers finish
    """
    pass