# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/default_config.py
# Compiled at: 2015-04-25 16:48:21
from __future__ import absolute_import, unicode_literals
config = {b'sources': {b'/var/log/*.log': {b'handler': b'pipes.to-web'}, b'/var/log/*/*.log': {b'handler': b'pipes.to-web'}, b'/var/log/syslog': b'pipes.to-web'}, 
   b'pipes': {b'default': b'logdog.roles.pipes.Pipe', 
              b'to-web': [
                        b'watch processors.stripper',
                        b'watch connectors.zmq-tunnel@sender',
                        b'view connectors.zmq-tunnel@receiver',
                        b'view viewers.webui'], 
              b'experiment-x001': {b'cls': b'logdog.roles.pipes.Pipe', 
                                   b'*': [
                                        b'watch processors.stripper',
                                        {b'forwarders.broadcast': [
                                                                   b'watch viewers.console',
                                                                   {b'pipes.default': [{b'watch connectors.zmq-tunnel@sender': {b'connect': b'tcp://localhost:7789'}}, {b'view connectors.zmq-tunnel@receiver': {b'bind': b'tcp://*:7789'}},
                                                                                       {b'view forwarders.round-robin': [
                                                                                                                         b'view viewers.webui',
                                                                                                                         b'view viewers.null']}]}]}]}}, 
   b'options': {b'sources': {b'default_handler': b'pipes.to-web', 
                             b'default_watcher': b'pollers.file-watcher', 
                             b'index_file': b'~/.config/logdog/sources-index.idx'}}, 
   b'pollers': {b'file-watcher': {b'cls': b'logdog.roles.pollers.FileWatcher', 
                                  b'namespaces': [
                                                b'watch']}}, 
   b'collectors': {}, b'processors': {b'stripper': {b'cls': b'logdog.roles.processors.Stripper'}}, b'parsers': {b'regex': {b'cls': b'logdog.roles.parsers.Regex', b'regex': b''}}, b'formatters': {b'formatter': {b'cls': b'logdog.roles.formatters.Formatter'}}, b'forwarders': {b'broadcast': b'logdog.roles.forwarders.Broadcast', 
                   b'round-robin': b'logdog.roles.forwarders.RoundRobin'}, 
   b'connectors': {b'zmq-tunnel': {b'cls': b'logdog.roles.connectors.ZMQTunnel', 
                                   b'@sender': {b'socket': b'PUSH', b'connect': [b'tcp://localhost:45457']}, b'@receiver': {b'socket': b'PULL', b'bind': [b'tcp://*:45457']}}}, 
   b'viewers': {b'default': b'logdog.roles.viewers.Null', 
                b'webui': {b'cls': b'logdog.roles.viewers.WebUI', 
                           b'port': 8888, 
                           b'debug': True}, 
                b'console': {b'cls': b'logdog.roles.viewers.Console', 
                             b'redirect_to': b'stdout'}, 
                b'null': b'logdog.roles.viewers.Null'}, 
   b'utils': {b'policies': {b'growing-sleep': {b'cls': b'logdog.core.policies.DefaultSleepPolicy'}, 
                            b'mostly-greedy': {b'cls': b'logdog.core.policies.GreedyPolicy'}}}}