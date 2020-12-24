# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/clients/collection.py
# Compiled at: 2018-03-02 16:15:07
# Size of source mod 2**32: 1753 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.verify import verify_subclass
from wasp_general.network.clients.proto import WNetworkClientProto
from wasp_general.network.clients.ftp import WFTPClient
from wasp_general.network.clients.file import WLocalFile
from wasp_general.uri import WSchemeCollection

class WNetworkClientCollectionProto(WSchemeCollection):

    @verify_subclass(scheme_handler_cls=WNetworkClientProto)
    def add(self, scheme_handler_cls):
        return WSchemeCollection.add(self, scheme_handler_cls)


__default_client_collection__ = WNetworkClientCollectionProto(WLocalFile, WFTPClient, default_handler_cls=WLocalFile)