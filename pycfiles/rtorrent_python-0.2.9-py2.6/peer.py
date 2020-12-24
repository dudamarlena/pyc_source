# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/rtorrent/peer.py
# Compiled at: 2012-04-10 19:50:56
import rtorrent.rpc
Method = rtorrent.rpc.Method

class Peer:
    """Represents an individual peer within a L{Torrent} instance."""

    def __init__(self, _rt_obj, info_hash, **kwargs):
        self._rt_obj = _rt_obj
        self.info_hash = info_hash
        for k in kwargs.keys():
            setattr(self, k, kwargs.get(k, None))

        self.rpc_id = ('{0}:p{1}').format(self.info_hash, self.id)
        return

    def __repr__(self):
        return ('<Peer id={0}>').format(self.id)

    def update(self):
        """Refresh peer data
        
        @note: All fields are stored as attributes to self.

        @return: None
        """
        multicall = rtorrent.rpc.Multicall(self)
        retriever_methods = [ m for m in methods if m.is_retriever() if m.is_available(self._rt_obj)
                            ]
        for method in retriever_methods:
            multicall.add(method, self.rpc_id)

        multicall.call()


methods = [
 Method(Peer, 'is_preferred', 'p.is_preferred', boolean=True),
 Method(Peer, 'get_down_rate', 'p.get_down_rate'),
 Method(Peer, 'is_unwanted', 'p.is_unwanted', boolean=True),
 Method(Peer, 'get_peer_total', 'p.get_peer_total'),
 Method(Peer, 'get_peer_rate', 'p.get_peer_rate'),
 Method(Peer, 'get_port', 'p.get_port'),
 Method(Peer, 'is_snubbed', 'p.is_snubbed', boolean=True),
 Method(Peer, 'get_id_html', 'p.get_id_html'),
 Method(Peer, 'get_up_rate', 'p.get_up_rate'),
 Method(Peer, 'is_banned', 'p.banned', boolean=True),
 Method(Peer, 'get_completed_percent', 'p.get_completed_percent'),
 Method(Peer, 'completed_percent', 'p.completed_percent'),
 Method(Peer, 'get_id', 'p.get_id'),
 Method(Peer, 'is_obfuscated', 'p.is_obfuscated', boolean=True),
 Method(Peer, 'get_down_total', 'p.get_down_total'),
 Method(Peer, 'get_client_version', 'p.get_client_version'),
 Method(Peer, 'get_address', 'p.get_address'),
 Method(Peer, 'is_incoming', 'p.is_incoming', boolean=True),
 Method(Peer, 'is_encrypted', 'p.is_encrypted', boolean=True),
 Method(Peer, 'get_options_str', 'p.get_options_str'),
 Method(Peer, 'get_client_version', 'p.client_version'),
 Method(Peer, 'get_up_total', 'p.get_up_total')]