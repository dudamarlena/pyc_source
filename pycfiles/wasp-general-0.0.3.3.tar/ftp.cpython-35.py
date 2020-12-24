# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/clients/ftp.py
# Compiled at: 2018-03-06 13:04:31
# Size of source mod 2**32: 5473 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import ftplib
from wasp_general.uri import WSchemeSpecification
from wasp_general.network.clients.proto import WNetworkClientProto
from wasp_general.network.clients.base import WBasicNetworkClientProto
from wasp_general.network.clients.base import WBasicNetworkClientListDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientChangeDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientMakeDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientCurrentDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientUploadFileCapability
from wasp_general.network.clients.base import WBasicNetworkClientRemoveFileCapability

class WFTPClient(WBasicNetworkClientProto):

    def __init__(self, uri):
        WBasicNetworkClientProto.__init__(self, uri)
        try:
            ftp_args = {'host': uri.hostname()}
            ftp_client = ftplib.FTP(**ftp_args)
            login_args = {}
            if uri.username() is not None:
                login_args['user'] = uri.username()
            if uri.password():
                login_args['passwd'] = uri.password()
            ftp_client.login(**login_args)
            ftp_client.cwd(uri.path() if uri.path() is not None else '/')
            self._WFTPClient__ftp_client = ftp_client
        except (ftplib.error_perm, ftplib.error_proto, ftplib.error_reply, ftplib.error_temp):
            raise WNetworkClientProto.ConnectionError('Unable to connect to %s' % str(uri))
        except OSError:
            raise WNetworkClientProto.ConnectionError('Unable to connect to %s' % str(uri))

    def ftp_client(self):
        return self._WFTPClient__ftp_client

    def _close(self):
        self._WFTPClient__ftp_client.close()

    @classmethod
    def scheme_specification(cls):
        return WSchemeSpecification('ftp', username=WSchemeSpecification.ComponentDescriptor.optional, password=WSchemeSpecification.ComponentDescriptor.optional, hostname=WSchemeSpecification.ComponentDescriptor.required, path=WSchemeSpecification.ComponentDescriptor.required)

    @classmethod
    def agent_capabilities(cls):
        return (WFTPClientListDirCapability,
         WFTPClientMakeDirCapability,
         WFTPClientChangeDirCapability,
         WFTPClientUploadFileCapability,
         WFTPClientRemoveFileCapability)


class WFTPClientChangeDirCapability(WBasicNetworkClientChangeDirCapability):

    def request(self, path, *args, exec_cmd=None, **kwargs):
        try:
            self.network_agent().ftp_client().cwd(path)
            if exec_cmd is not None:
                return self.network_agent().request(exec_cmd, *args, **kwargs)
            else:
                return True
        except (ftplib.error_perm, ftplib.error_proto, ftplib.error_reply, ftplib.error_temp):
            if exec_cmd is not None:
                return
            else:
                return False


class WFTPClientCurrentDirCapability(WBasicNetworkClientCurrentDirCapability):

    def request(self, *args, **kwargs):
        return self.network_agent().ftp_client().pwd()


class WFTPClientListDirCapability(WBasicNetworkClientListDirCapability):

    def request(self, *args, **kwargs):
        try:
            return tuple(self.network_agent().ftp_client().nlst())
        except (ftplib.error_perm, ftplib.error_proto, ftplib.error_reply, ftplib.error_temp):
            return


class WFTPClientMakeDirCapability(WBasicNetworkClientMakeDirCapability):

    def request(self, directory_name, *args, **kwargs):
        try:
            return len(self.network_agent().ftp_client().mkd(directory_name)) > 0
        except (ftplib.error_perm, ftplib.error_proto, ftplib.error_reply, ftplib.error_temp):
            return False


class WFTPClientUploadFileCapability(WBasicNetworkClientUploadFileCapability):

    def request(self, file_name, file_obj, *args, **kwargs):
        try:
            self.network_agent().ftp_client().storbinary('STOR ' + file_name, file_obj)
            return True
        except (ftplib.error_perm, ftplib.error_proto, ftplib.error_reply, ftplib.error_temp):
            return False


class WFTPClientRemoveFileCapability(WBasicNetworkClientRemoveFileCapability):

    def request(self, file_name, *args, **kwargs):
        try:
            self.network_agent().ftp_client().delete(file_name)
            return True
        except (ftplib.error_perm, ftplib.error_proto, ftplib.error_reply, ftplib.error_temp):
            return False