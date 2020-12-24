# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/clients/file.py
# Compiled at: 2018-03-02 16:08:04
# Size of source mod 2**32: 3929 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import io, os
from wasp_general.uri import WSchemeSpecification
from wasp_general.network.clients.base import WBasicNetworkClientProto
from wasp_general.network.clients.base import WBasicNetworkClientListDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientChangeDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientMakeDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientCurrentDirCapability
from wasp_general.network.clients.base import WBasicNetworkClientUploadFileCapability
from wasp_general.network.clients.base import WBasicNetworkClientRemoveFileCapability

class WLocalFile(WBasicNetworkClientProto):

    def __init__(self, uri):
        WBasicNetworkClientProto.__init__(self, uri)
        self._WLocalFile__session_path = uri.path() if uri.path() is not None else '/'

    def session_path(self, value=None):
        if value is not None:
            self._WLocalFile__session_path = value
        return self._WLocalFile__session_path

    def _close(self):
        self._WLocalFile__session_path = None

    @classmethod
    def scheme_specification(cls):
        return WSchemeSpecification('file', path=WSchemeSpecification.ComponentDescriptor.required)

    @classmethod
    def agent_capabilities(cls):
        return (WLocalFileListDirCapability,
         WLocalFileMakeDirCapability,
         WLocalFileChangeDirCapability,
         WLocalFileUploadFileCapability,
         WLocalFileRemoveFileCapability)


class WLocalFileChangeDirCapability(WBasicNetworkClientChangeDirCapability):

    def request(self, path, *args, exec_cmd=None, **kwargs):
        if os.path.isdir(path) is True:
            self.network_agent().session_path(path)
            return True
        return False


class WLocalFileCurrentDirCapability(WBasicNetworkClientCurrentDirCapability):

    def request(self, *args, **kwargs):
        return self.network_agent().session_path()


class WLocalFileListDirCapability(WBasicNetworkClientListDirCapability):

    def request(self, *args, **kwargs):
        return tuple(os.listdir(self.network_agent().session_path()))


class WLocalFileMakeDirCapability(WBasicNetworkClientMakeDirCapability):

    def request(self, directory_name, *args, **kwargs):
        os.mkdir(os.path.join(self.network_agent().session_path(), directory_name))
        return True


class WLocalFileUploadFileCapability(WBasicNetworkClientUploadFileCapability):

    def request(self, file_name, file_obj, *args, **kwargs):
        with open(os.path.join(self.network_agent().session_path(), file_name), mode='wb') as (f):
            chunk = file_obj.read(io.DEFAULT_BUFFER_SIZE)
            while len(chunk) > 0:
                f.write(chunk)
                chunk = file_obj.read(io.DEFAULT_BUFFER_SIZE)

        return True


class WLocalFileRemoveFileCapability(WBasicNetworkClientRemoveFileCapability):

    def request(self, file_name, *args, **kwargs):
        os.unlink(os.path.join(self.network_agent().session_path(), file_name))
        return True