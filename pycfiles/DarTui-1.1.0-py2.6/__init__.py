# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dartui/__init__.py
# Compiled at: 2012-04-16 18:25:37
import sys, common, config, actions
__version__ = '1.1.0'
__author__ = 'Chris Lucas'
__contact__ = 'chris@chrisjlucas.com'
__license__ = 'MIT'
common.__version__ = __version__

def run(conf_dir, http_ip, http_port):
    common.conf = config.ConfigDir(conf_dir)
    if common.conf.get_rt() is not None:
        print 'Filling torrent cache. May take some time.'
        actions.get_torrents_and_update_cache()
        common.recent_torrent_dests = actions.get_recent_torrent_dests()
        print 'Caching complete, starting server.'
    import http
    http.run_server(http_ip, http_port)
    return