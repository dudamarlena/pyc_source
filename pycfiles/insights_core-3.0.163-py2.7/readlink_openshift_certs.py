# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/readlink_openshift_certs.py
# Compiled at: 2020-03-26 13:06:46
"""
ReadLink parsers for Openshift certificate symbolic file links
==============================================================

This module contains the following parsers:

ReadLinkEKubeletClientCurrent - command ``/usr/bin/readlink -e /etc/origin/node/certificates/kubelet-client-current.pem``
-------------------------------------------------------------------------------------------------------------------------
ReadLinkEKubeletServerCurrent - command ``/usr/bin/readlink -e /etc/origin/node/certificates/kubelet-server-current.pem``
-------------------------------------------------------------------------------------------------------------------------
"""
from insights.specs import Specs
from insights.parsers import SkipException
from insights import parser, CommandParser

@parser(Specs.readlink_e_shift_cert_client)
class ReadLinkEKubeletClientCurrent(CommandParser):
    """
    Class for command: /usr/bin/readlink -e /etc/origin/node/certificates/kubelet-client-current.pem

    Sample content from command is::

        /etc/origin/node/certificates/kubelet-client-2019-10-18-23-17-35.pem

    Examples:
        >>> client.path
        '/etc/origin/node/certificates/kubelet-client-2019-10-18-23-17-35.pem'

    Raises:
        SkipException: When input content is empty
    """

    def parse_content(self, content):
        if content is None or len(content) == 0:
            raise SkipException('No Data from command: /usr/bin/readlink -e /etc/origin/node/certificates/kubelet-client-current.pem')
        self._path = content[(-1)]
        return

    @property
    def path(self):
        """Returns real file path of /etc/origin/node/certificates/kubelet-client-current.pem"""
        return self._path


@parser(Specs.readlink_e_shift_cert_server)
class ReadLinkEKubeletServerCurrent(CommandParser):
    """
    Class for command: /usr/bin/readlink -e /etc/origin/node/certificates/kubelet-server-current.pem

    Sample content from command is::

        /etc/origin/node/certificates/kubelet-server-2018-10-18-23-29-14.pem

    Examples:
        >>> server.path
        '/etc/origin/node/certificates/kubelet-server-2018-10-18-23-29-14.pem'

    Raises:
        SkipException: When input content is empty
    """

    def parse_content(self, content):
        if content is None or len(content) == 0:
            raise SkipException('No Data from command: /usr/bin/readlink -e /etc/origin/node/certificates/kubelet-server-current.pem')
        self._path = content[(-1)]
        return

    @property
    def path(self):
        """Returns real file path of /etc/origin/node/certificates/kubelet-server-current.pem"""
        return self._path