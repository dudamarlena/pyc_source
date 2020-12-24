# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qgispluginci/exceptions.py
# Compiled at: 2020-05-01 10:08:01
# Size of source mod 2**32: 357 bytes


class TranslationFailed(Exception):
    pass


class TransifexNoResource(Exception):
    pass


class TransifexManyResources(Warning):
    pass


class GithubReleaseNotFound(Exception):
    pass


class GithubReleaseCouldNotUploadAsset(Exception):
    pass


class UncommitedChanges(Exception):
    pass


class ConfigurationNotFound(Exception):
    pass