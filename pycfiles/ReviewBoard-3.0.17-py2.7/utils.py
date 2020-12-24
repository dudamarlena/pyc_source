# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/ssh/utils.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, paramiko
from django.utils import six
from reviewboard.ssh.client import SSHClient
from reviewboard.ssh.errors import BadHostKeyError, SSHAuthenticationError, SSHError, SSHInvalidPortError
from reviewboard.ssh.policy import RaiseUnknownHostKeyPolicy
SSH_PORT = 22
try:
    import urlparse
    uses_netloc = urlparse.uses_netloc
    urllib_parse = urlparse.urlparse
except ImportError:
    import urllib.parse
    uses_netloc = urllib.parse.uses_netloc
    urllib_parse = urllib.parse.urlparse

ssh_uri_schemes = [
 b'ssh', b'sftp']
uses_netloc.extend(ssh_uri_schemes)

def humanize_key(key):
    """Returns a human-readable key as a series of hex characters."""
    return (b':').join([ b'%02x' % ord(c) for c in key.get_fingerprint() ])


def is_ssh_uri(url):
    """Returns whether or not a URL represents an SSH connection."""
    return urllib_parse(url)[0] in ssh_uri_schemes


def check_host(netloc, username=None, password=None, namespace=None):
    """
    Checks if we can connect to a host with a known key.

    This will raise an exception if we cannot connect to the host. The
    exception will be one of BadHostKeyError, UnknownHostKeyError, or
    SCMError.
    """
    from django.conf import settings
    client = SSHClient(namespace=namespace)
    client.set_missing_host_key_policy(RaiseUnknownHostKeyPolicy())
    kwargs = {}
    if b':' in netloc:
        hostname, port = netloc.split(b':')
        try:
            port = int(port)
        except ValueError:
            raise SSHInvalidPortError(port)

    else:
        hostname = netloc
        port = SSH_PORT
    if getattr(settings, b'RUNNING_TEST', False):
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        kwargs[b'allow_agent'] = False
    try:
        client.connect(hostname, port, username=username, password=password, pkey=client.get_user_key(), **kwargs)
    except paramiko.BadHostKeyException as e:
        raise BadHostKeyError(e.hostname, e.key, e.expected_key)
    except paramiko.AuthenticationException as e:
        allowed_types = getattr(e, b'allowed_types', [])
        if b'publickey' in allowed_types:
            key = client.get_user_key()
        else:
            key = None
        raise SSHAuthenticationError(allowed_types=allowed_types, user_key=key)
    except paramiko.SSHException as e:
        msg = six.text_type(e)
        if msg == b'No authentication methods available':
            raise SSHAuthenticationError
        else:
            raise SSHError(msg)

    return


def register_rbssh(envvar):
    """Registers rbssh in an environment variable.

    This is a convenience method for making sure that rbssh is set properly
    in the environment for different tools. In some cases, we need to
    specifically place it in the system environment using ``os.putenv``,
    while in others (Mercurial, Bazaar), we need to place it in ``os.environ``.
    """
    envvar = envvar.encode(b'utf-8')
    os.putenv(envvar, b'rbssh')
    os.environ[envvar] = b'rbssh'