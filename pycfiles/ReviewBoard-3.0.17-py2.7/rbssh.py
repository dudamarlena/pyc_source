# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/bzr/plugins/bzrlib/plugins/rbssh.py
# Compiled at: 2020-02-11 04:03:56
"""rbssh plugin for Bazaar.

This registers :command:`rbssh` as a SSH plugin for Bazaar. It's run entirely
outside of the Review Board process, and is invoked exclusively by
:command:`bzr`.
"""
from __future__ import unicode_literals
from bzrlib.transport.ssh import SubprocessVendor, register_default_ssh_vendor, register_ssh_vendor
from django.utils import six

class RBSSHVendor(SubprocessVendor):
    """SSH vendor class for using rbssh."""
    executable_path = b'rbssh'

    def _get_vendor_specific_argv(self, username, host, port=None, subsystem=None, command=None):
        """Return arguments to pass to rbssh.

        Args:
            username (unicode):
                The username to connect with.

            host (unicode):
                The hostname to connect to.

            port (int, optional):
                The custom port to connect to.

            subsystem (unicode, optional):
                The SSH subsystem to use.

            command (unicode, optional):
                The command to invoke through the SSH connection.

        Returns:
            list of unicode:
            The list of arguments to pass to :command:`rbssh`.
        """
        args = [
         self.executable_path]
        if port is not None:
            args.extend([b'-p', six.text_type(port)])
        if username is not None:
            args.extend([b'-l', username])
        if subsystem is not None:
            args.extend([b'-s', host, subsystem])
        else:
            args.extend([host] + command)
        return args


vendor = RBSSHVendor()
register_ssh_vendor(b'rbssh', vendor)
register_default_ssh_vendor(vendor)