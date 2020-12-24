# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/vyper/errors.py
# Compiled at: 2019-11-07 11:42:47
# Size of source mod 2**32: 1587 bytes


class ConfigFileNotFoundError(Exception):
    __doc__ = 'Denotes failing to find configuration file.'

    def __init__(self, message, locations, *args):
        self.message = message
        self.locations = ', '.join((str(l) for l in locations))
        (super(ConfigFileNotFoundError, self).__init__)(message, locations, *args)

    def __str__(self):
        return 'Config File {0} Not Found in {1}'.format(self.message, self.locations)


class RemoteConfigError(Exception):
    __doc__ = 'Denotes encountering an error while trying to\n    pull the configuration from the remote provider.\n    '

    def __init__(self, message, *args):
        self.message = message
        (super(RemoteConfigError, self).__init__)(message, *args)

    def __str__(self):
        return 'Remote Configuration Error {0}'.format(self.message)


class UnsupportedConfigError(Exception):
    __doc__ = 'Denotes encountering an unsupported configuration file type.'

    def __init__(self, message, *args):
        self.message = message
        (super(UnsupportedConfigError, self).__init__)(message, *args)

    def __str__(self):
        return 'Unsupported Config Type {0}'.format(self.message)


class UnsupportedRemoteProviderError(Exception):
    __doc__ = 'Denotes encountering an unsupported remote provider.\n    Currently only etcd, consul and zookeeper are supported.\n    '

    def __init__(self, message, *args):
        self.message = message
        (super(UnsupportedRemoteProviderError, self).__init__)(message, *args)

    def __str__(self):
        return 'Unsupported Remote Provider Type {0}'.format(self.message)