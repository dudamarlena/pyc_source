# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/errors.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 2789 bytes


class CommandError(Exception):
    __doc__ = '\n    Raised when a problem with the command run is encountered\n    '


class BackendError(Exception):
    __doc__ = '\n    Backend error\n    '


class DockerError(CommandError):
    __doc__ = '\n    Raised when a problem running a docker command is encountered\n    '


class ErrorMessage(Exception):
    __doc__ = '\n    Subclass to print out error message instead of entire stack trace\n    '


class AlreadyConnected(ErrorMessage):
    __doc__ = '\n    Error raised when already connected to remote\n    '


class EnvError(ErrorMessage):
    __doc__ = '\n    Error for when environment variables are not found\n    '


class NoSuchConfig(Exception):
    __doc__ = '\n    Raised when a requested config is not in the docker swarm\n    '


class NoSuchProfile(Exception):
    __doc__ = '\n    Raised when a requested profile is not listed in dc.yml\n    '


class NotConnected(Exception):
    __doc__ = '\n    Raised when not connected to a remote host\n    '


class NoContainer(Exception):
    __doc__ = '\n    Raised when a desired container is not found\n    '


class ProfileError(ErrorMessage):
    __doc__ = '\n    Raised when there is a problem with a Profile\n    '


class RemoteUndefined(ErrorMessage):
    __doc__ = '\n    Raised when no remote is defined\n    '


class RuntimeEnvError(ErrorMessage):
    __doc__ = '\n    Raised when variable substitution at runtime fails\n    '


class TagVersionError(Exception):
    __doc__ = '\n    Raised when there is a problem running tag-version\n    '

    def __init__(self, message: str, shell_exception: Exception, tag_version: str=None):
        self.message = message
        self.shell_exception = shell_exception
        self.tag_version = tag_version


class InvalidTargetCluster(ErrorMessage):
    __doc__ = '\n    Raised when a profile is provided with the -e flag\n    which would target an invalid Rancher cluster,\n    such as the local cluster where Rancher itself runs\n    '


class MissingManifest(ErrorMessage):
    __doc__ = '\n    Raised when a YAML manifest path is specified but not found\n    '


class ManifestCheck(ErrorMessage):
    __doc__ = '\n    Raised when a rendered YAML manifest fails to pass a check\n    '


class MissingKubeContext(ErrorMessage):
    __doc__ = '\n    Raised when a kubeconfig context is missing.\n    '


class MissingRancherProject(ErrorMessage):
    __doc__ = '\n    Raised when no Rancher project is configured or the configured project is not found.\n    '


class RancherNamespaceAlreadyExists(ErrorMessage):
    __doc__ = '\n    Raised when a namespace is specified for creation but that namespace already exists.\n    '


class PodNotFound(ErrorMessage):
    __doc__ = 'Raised when no pod is found matching a certain set of criteria.'


class PublishMajorMinorTagsError(ErrorMessage):
    __doc__ = 'Raised when publish_with_major_minor_tags is called on an invalid PrivateImage'