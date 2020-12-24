# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/errol/config_parser.py
# Compiled at: 2020-05-09 16:25:55
# Size of source mod 2**32: 1678 bytes
import configparser

def read_config(filename='example.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    section = 'XMPP'
    pubsub_enable = config.getboolean(section, 'pubsub_enable')
    muc_enable = config.getboolean(section, 'muc_enable')
    pubsub_server = None
    node = None
    room = None
    if pubsub_enable:
        pubsub_server = config.get(section, 'pubsub')
        node = config.get(section, 'node')
    if muc_enable:
        room = config.get(section, 'room')
    jid = config.get(section, 'jid')
    password = config.get(section, 'password')
    ressource_receiver = config.get(section, 'ressource_receiver')
    ressource_sender = config.get(section, 'ressource_sender')
    nick_sender = config.get(section, 'nick_sender')
    nick_receiver = config.get(section, 'nick_receiver')
    receiver = config.get(section, 'receiver')
    presence_file = config.get(section, 'presence_file')
    conf = {'xmpp': {'pubsub_server':pubsub_server,  'node':node,  'room':room,  'jid':jid, 
              'password':password,  'ressource_receiver':ressource_receiver,  'ressource_sender':ressource_sender, 
              'nick_sender':nick_sender,  'nick_receiver':nick_receiver, 
              'receiver':receiver,  'presence_file':presence_file,  'pubsub_enable':pubsub_enable, 
              'muc_enable':muc_enable}}
    return conf


if __name__ == '__main__':
    conf = read_config('../config.example.ini')
    print(conf)