# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/connectrum/constants.py
# Compiled at: 2016-06-12 00:15:26
# Size of source mod 2**32: 1159 bytes
ELECTRUM_VERSION = '2.6.4'
PROTOCOL_VERSION = '0.10'
PROTOCOL_CODES = dict(t='TCP (plaintext)', h='HTTP (plaintext)', s='SSL', g='Websocket')
DEFAULT_PORTS = {'t':50001, 
 's':50002,  'h':8081,  'g':8082}
BOOTSTRAP_SERVERS = {'erbium1.sytes.net':{'t':50001, 
  's':50002}, 
 'ecdsa.net':{'t':50001, 
  's':110}, 
 'electrum0.electricnewyear.net':{'t':50001, 
  's':50002}, 
 'VPS.hsmiths.com':{'t':50001, 
  's':50002}, 
 'ELECTRUM.jdubya.info':{'t':50001, 
  's':50002}, 
 'electrum.no-ip.org':{'t':50001, 
  's':50002,  'g':443}, 
 'us.electrum.be':DEFAULT_PORTS, 
 'bitcoins.sk':{'t':50001, 
  's':50002}, 
 'electrum.petrkr.net':{'t':50001, 
  's':50002}, 
 'electrum.dragonzone.net':DEFAULT_PORTS, 
 'Electrum.hsmiths.com':{'t':8080, 
  's':995}, 
 'electrum3.hachre.de':{'t':50001, 
  's':50002}, 
 'elec.luggs.co':{'t':80, 
  's':443}, 
 'btc.smsys.me':{'t':110, 
  's':995}, 
 'electrum.online':{'t':50001, 
  's':50002}}