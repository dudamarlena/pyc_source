# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/minio_storage/errors.py
# Compiled at: 2019-10-28 02:17:19
# Size of source mod 2**32: 773 bytes
import minio.error as merr

class MinIOError(OSError):

    def __init__(self, msg, cause):
        super().__init__(msg)
        self.cause = cause


reraise = {}
for v in (
 merr.APINotImplemented,
 merr.AccessDenied,
 merr.AccountProblem,
 merr.CredentialNotSupported,
 merr.CrossLocationLoggingProhibited,
 merr.ExpiredToken,
 merr.InvalidAccessKeyId,
 merr.InvalidAddressingHeader,
 merr.InvalidBucketError,
 merr.InvalidBucketName,
 merr.InvalidDigest,
 merr.InvalidEncryptionAlgorithmError,
 merr.InvalidEndpointError,
 merr.InvalidSecurity,
 merr.InvalidToken,
 merr.NoSuchBucket):
    reraise[v] = {'err': v}

def minio_error(msg, e):
    if e.__class__ in reraise:
        return e
    return MinIOError(msg, e)