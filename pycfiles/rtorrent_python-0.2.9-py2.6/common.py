# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/rtorrent/common.py
# Compiled at: 2012-04-10 18:00:40
import sys
_py3 = sys.version_info > (3, )

def bool_to_int(value):
    """Translates python booleans to RPC-safe integers"""
    if value == True:
        return '1'
    else:
        if value == False:
            return '0'
        return value


def cmd_exists(cmds_list, cmd):
    """Check if given command is in list of available commands
    
    @param cmds_list: see L{RTorrent._rpc_methods}
    @type cmds_list: list
    
    @param cmd: name of command to be checked
    @type cmd: str
    
    @return: bool
    """
    return cmd in cmds_list


def find_torrent(info_hash, torrent_list):
    """Find torrent file in given list of Torrent classes
    
    @param info_hash: info hash of torrent
    @type info_hash: str
    
    @param torrent_list: list of L{Torrent} instances (see L{RTorrent.get_torrents})
    @type torrent_list: list
    
    @return: L{Torrent} instance, or -1 if not found
    """
    for t in torrent_list:
        if t.info_hash == info_hash:
            return t

    return -1


def is_valid_port(port):
    """Check if given port is valid"""
    return 0 <= int(port) <= 65535


def convert_version_tuple_to_str(t):
    return ('.').join([ str(n) for n in t ])