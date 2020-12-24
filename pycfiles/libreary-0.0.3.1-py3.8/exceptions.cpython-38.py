# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/exceptions.py
# Compiled at: 2020-03-19 14:48:15
# Size of source mod 2**32: 715 bytes


class IngestionFailedException(Exception):
    pass


class ChecksumMismatchException(Exception):
    pass


class MetadataUnavailableException(Exception):
    pass


class AdapterConnectionFailureException(Exception):
    pass


class RestorationFailedException(Exception):
    pass


class AdapterCreationFailedException(Exception):
    pass


class StorageFailedException(Exception):
    pass


class OptionalModuleMissingException(Exception):
    pass


class ResourceNotIngestedException(Exception):
    pass


class NoCopyExistsException(Exception):
    pass


class AdapterRestored(Exception):
    pass


class ConfigurationError(Exception):
    pass


class NoSuchMetadataFieldExeption(Exception):
    pass