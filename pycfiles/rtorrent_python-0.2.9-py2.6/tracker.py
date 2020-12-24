# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/rtorrent/tracker.py
# Compiled at: 2012-04-10 19:51:07
import rtorrent.rpc
Method = rtorrent.rpc.Method

class Tracker:
    """Represents an individual tracker within a L{Torrent} instance."""

    def __init__(self, _rt_obj, info_hash, **kwargs):
        self._rt_obj = _rt_obj
        self.info_hash = info_hash
        for k in kwargs.keys():
            setattr(self, k, kwargs.get(k, None))

        self.index = self.group
        self.rpc_id = ('{0}:t{1}').format(self.info_hash, self.index)
        return

    def __repr__(self):
        return ('<Tracker index={0}, url="{1}">').format(self.index, self.url)

    def enable(self):
        """Alias for set_enabled("yes")"""
        self.set_enabled('yes')

    def disable(self):
        """Alias for set_enabled("no")"""
        self.set_enabled('no')

    def update(self):
        """Refresh tracker data
        
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
 Method(Tracker, 'is_enabled', 't.is_enabled', boolean=True),
 Method(Tracker, 'get_id', 't.get_id'),
 Method(Tracker, 'get_scrape_incomplete', 't.get_scrape_incomplete'),
 Method(Tracker, 'is_open', 't.is_open', boolean=True),
 Method(Tracker, 'get_min_interval', 't.get_min_interval'),
 Method(Tracker, 'get_scrape_downloaded', 't.get_scrape_downloaded'),
 Method(Tracker, 'get_group', 't.get_group'),
 Method(Tracker, 'get_scrape_time_last', 't.get_scrape_time_last'),
 Method(Tracker, 'get_type', 't.get_type'),
 Method(Tracker, 'get_normal_interval', 't.get_normal_interval'),
 Method(Tracker, 'get_url', 't.get_url'),
 Method(Tracker, 'get_scrape_complete', 't.get_scrape_complete', min_version=(0, 8,
                                                                             9)),
 Method(Tracker, 'get_activity_time_last', 't.activity_time_last', min_version=(0, 8,
                                                                               9)),
 Method(Tracker, 'get_activity_time_next', 't.activity_time_next', min_version=(0, 8,
                                                                               9)),
 Method(Tracker, 'get_failed_time_last', 't.failed_time_last', min_version=(0, 8, 9)),
 Method(Tracker, 'get_failed_time_next', 't.failed_time_next', min_version=(0, 8, 9)),
 Method(Tracker, 'get_success_time_last', 't.success_time_last', min_version=(0, 8,
                                                                             9)),
 Method(Tracker, 'get_success_time_next', 't.success_time_next', min_version=(0, 8,
                                                                             9)),
 Method(Tracker, 'can_scrape', 't.can_scrape', min_version=(0, 9, 1), boolean=True),
 Method(Tracker, 'get_failed_counter', 't.failed_counter', min_version=(0, 8, 9)),
 Method(Tracker, 'get_scrape_counter', 't.scrape_counter', min_version=(0, 8, 9)),
 Method(Tracker, 'get_success_counter', 't.success_counter', min_version=(0, 8, 9)),
 Method(Tracker, 'is_usable', 't.is_usable', min_version=(0, 9, 1), boolean=True),
 Method(Tracker, 'is_busy', 't.is_busy', min_version=(0, 9, 1), boolean=True),
 Method(Tracker, 'is_extra_tracker', 't.is_extra_tracker', min_version=(0, 9, 1), boolean=True),
 Method(Tracker, 'get_latest_sum_peers', 't.latest_sum_peers', min_version=(0, 9, 0)),
 Method(Tracker, 'get_latest_new_peers', 't.latest_new_peers', min_version=(0, 9, 0)),
 Method(Tracker, 'set_enabled', 't.set_enabled')]