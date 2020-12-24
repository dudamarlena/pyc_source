# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/config/version.py
# Compiled at: 2019-06-22 23:02:15
# Size of source mod 2**32: 1809 bytes
VERSION_ID = '0.1.6'
AUTHOR = 'RMT'
EMAIL = 'd.rong@outlook.com'
COMMAND_LONG = [
 'version', 'help', 'subscribe-add=', 'subscribe-update', 'config-v2ray=', 'config-subscribe=',
 'config-servers=', 'autoconfig', 'subscribe-update', 'list', 'start=', 'config-file=', 'port=',
 'servers-export=', 'daemon', 'stop', 'v2ray-update', 'ping']
COMMAND_SHORT = 'vhs:lf:d'
HELP_INFO = "\n    --help[-h]                                            print help message\n    --version[-v]                                         show current version of shadowray\n    --subscribe-add '<name>,<url>'                        add subscribe\n    --subscribe-update                                    update subscribe\n    --config-v2ray <path>                                 setup the path of v2ray binary\n    --config-subscribe <path>                             setup the path of subscribe file\n    --config-servers <path>                               setup the path of servers file\n    --autoconfig                                          setup basic setting automatically\n    --subscribe-update [--port <number>]                  update subscribe\n    --list[-l]                                            show all servers\n    --start[-s] <index> [-d|--daemon]                     start v2ray,the '-d or --daemon argument used to run v2ray as a daemon'\n    --config-file[-f] <path>                              run v2ray use the config file that provided by yourself\n    --servers-export <index>:<path>                       export the config of specified index\n    --stop                                                stop v2ray\n    --v2ray-update                                        update v2ray core to latest\n    --ping                                                ping server\n    "