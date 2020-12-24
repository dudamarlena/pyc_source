# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/rtorrent/file.py
# Compiled at: 2012-04-10 19:50:49
import rtorrent.rpc
Method = rtorrent.rpc.Method

class File:
    """Represents an individual file within a L{Torrent} instance."""

    def __init__(self, _rt_obj, info_hash, index, **kwargs):
        self._rt_obj = _rt_obj
        self.info_hash = info_hash
        self.index = index
        for k in kwargs.keys():
            setattr(self, k, kwargs.get(k, None))

        self.rpc_id = ('{0}:f{1}').format(self.info_hash, self.index)
        return

    def update(self):
        """Refresh file data
        
        @note: All fields are stored as attributes to self.

        @return: None
        """
        multicall = rtorrent.rpc.Multicall(self)
        retriever_methods = [ m for m in methods if m.is_retriever() if m.is_available(self._rt_obj)
                            ]
        for method in retriever_methods:
            multicall.add(method, self.rpc_id)

        multicall.call()

    def __repr__(self):
        return ('<File index={0} path="{1}">').format(self.index, self.path)


methods = [
 Method(File, 'get_last_touched', 'f.get_last_touched'),
 Method(File, 'get_range_second', 'f.get_range_second'),
 Method(File, 'get_size_bytes', 'f.get_size_bytes'),
 Method(File, 'get_priority', 'f.get_priority'),
 Method(File, 'get_match_depth_next', 'f.get_match_depth_next'),
 Method(File, 'is_resize_queued', 'f.is_resize_queued', boolean=True),
 Method(File, 'get_range_first', 'f.get_range_first'),
 Method(File, 'get_match_depth_prev', 'f.get_match_depth_prev'),
 Method(File, 'get_path', 'f.get_path'),
 Method(File, 'get_completed_chunks', 'f.get_completed_chunks'),
 Method(File, 'get_path_components', 'f.get_path_components'),
 Method(File, 'is_created', 'f.is_created', boolean=True),
 Method(File, 'is_open', 'f.is_open', boolean=True),
 Method(File, 'get_size_chunks', 'f.get_size_chunks'),
 Method(File, 'get_offset', 'f.get_offset'),
 Method(File, 'get_frozen_path', 'f.get_frozen_path'),
 Method(File, 'get_path_depth', 'f.get_path_depth'),
 Method(File, 'is_create_queued', 'f.is_create_queued', boolean=True)]