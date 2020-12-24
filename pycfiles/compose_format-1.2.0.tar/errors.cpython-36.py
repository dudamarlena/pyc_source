# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/errors.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 2789 bytes


class CommandError(Exception):
    """CommandError"""
    pass


class BackendError(Exception):
    """BackendError"""
    pass


class DockerError(CommandError):
    """DockerError"""
    pass


class ErrorMessage(Exception):
    """ErrorMessage"""
    pass


class AlreadyConnected(ErrorMessage):
    """AlreadyConnected"""
    pass


class EnvError(ErrorMessage):
    """EnvError"""
    pass


class NoSuchConfig(Exception):
    """NoSuchConfig"""
    pass


class NoSuchProfile(Exception):
    """NoSuchProfile"""
    pass


class NotConnected(Exception):
    """NotConnected"""
    pass


class NoContainer(Exception):
    """NoContainer"""
    pass


class ProfileError(ErrorMessage):
    """ProfileError"""
    pass


class RemoteUndefined(ErrorMessage):
    """RemoteUndefined"""
    pass


class RuntimeEnvError(ErrorMessage):
    """RuntimeEnvError"""
    pass


class TagVersionError(Exception):
    """TagVersionError"""

    def __init__(self, message: str, shell_exception: Exception, tag_version: str=None):
        self.message = message
        self.shell_exception = shell_exception
        self.tag_version = tag_version


class InvalidTargetCluster(ErrorMessage):
    """InvalidTargetCluster"""
    pass


class MissingManifest(ErrorMessage):
    """MissingManifest"""
    pass


class ManifestCheck(ErrorMessage):
    """ManifestCheck"""
    pass


class MissingKubeContext(ErrorMessage):
    """MissingKubeContext"""
    pass


class MissingRancherProject(ErrorMessage):
    """MissingRancherProject"""
    pass


class RancherNamespaceAlreadyExists(ErrorMessage):
    """RancherNamespaceAlreadyExists"""
    pass


class PodNotFound(ErrorMessage):
    """PodNotFound"""
    pass


class PublishMajorMinorTagsError(ErrorMessage):
    """PublishMajorMinorTagsError"""
    pass