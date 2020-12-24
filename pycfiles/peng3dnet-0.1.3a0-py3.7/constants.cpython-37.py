# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/constants.py
# Compiled at: 2020-04-07 16:41:35
# Size of source mod 2**32: 7127 bytes
"""
This module is designed to be imported via ``from peng3dnet.constants import *`` without any side-effects.
"""
__all__ = [
 'MAX_PACKETLENGTH',
 'STRUCT_FORMAT_LENGTH32', 'STRUCT_FORMAT_HEADER',
 'STATE_INIT',
 'STATE_HANDSHAKE_WAIT1', 'STATE_HANDSHAKE_WAIT2',
 'STATE_WAITTYPE', 'STATE_HELLOWAIT',
 'STATE_LOGGEDIN',
 'STATE_ACTIVE', 'STATE_CLOSED',
 'MODE_NOTSET', 'MODE_CLOSED',
 'MODE_PING', 'MODE_PLAY', 'MODE_CHAT',
 'CONNTYPE_NOTSET', 'CONNTYPE_CLASSIC', 'CONNTYPE_PING',
 'FLAG_COMPRESSED', 'FLAG_ENCRYPTED_AES',
 'SIDE_CLIENT', 'SIDE_SERVER',
 'SSLSEC_NONE', 'SSLSEC_WRAPPED', 'SSLSEC_ENCRYPTED',
 'SSLSEC_SERVERAUTH', 'SSLSEC_BOTHAUTH',
 'DEFAULT_CONFIG']
MAX_PACKETLENGTH = 4294967295
STRUCT_FORMAT_LENGTH32 = '!I'
STRUCT_FORMAT_HEADER = '!IH'
STATE_INIT = 0
STATE_HANDSHAKE_WAIT1 = 1
STATE_HANDSHAKE_WAIT2 = 2
STATE_WAITTYPE = 3
STATE_HELLOWAIT = 4
STATE_ACTIVE = 64
STATE_LOGGEDIN = 65
STATE_CLOSED = 128
MODE_NOTSET = 0
MODE_CLOSED = 1
MODE_PING = 2
MODE_PLAY = 3
MODE_CHAT = 4
CONNTYPE_NOTSET = '_notset'
CONNTYPE_CLASSIC = 'classic'
CONNTYPE_PING = 'ping'
FLAG_COMPRESSED = 1
FLAG_ENCRYPTED_AES = 2
SIDE_CLIENT = 0
SIDE_SERVER = 1
SSLSEC_NONE = 0
SSLSEC_WRAPPED = 1
SSLSEC_ENCRYPTED = 2
SSLSEC_SERVERAUTH = 3
SSLSEC_BOTHAUTH = 4
DEFAULT_CONFIG = {'net.server.addr':None, 
 'net.server.addr.host':'0.0.0.0', 
 'net.server.addr.port':8080, 
 'net.client.addr':None, 
 'net.client.addr.host':'localhost', 
 'net.client.addr.port':8080, 
 'net.compress.enabled':True, 
 'net.compress.threshold':8192, 
 'net.compress.level':6, 
 'net.encrypt.enabled':False, 
 'net.ssl.enabled':False, 
 'net.ssl.force':True, 
 'net.ssl.cafile':None, 
 'net.ssl.server.force_verify':True, 
 'net.ssl.server.certfile':None, 
 'net.ssl.server.keyfile':None, 
 'net.ssl.client.check_hostname':False, 
 'net.ssl.client.force_verify':False, 
 'net.events.enable':'auto', 
 'net.debug.print.recv':False, 
 'net.debug.print.send':False, 
 'net.debug.print.connect':False, 
 'net.debug.print.close':False, 
 'net.registry.autosync':True, 
 'net.registry.missingpacketaction':'closeconnection'}