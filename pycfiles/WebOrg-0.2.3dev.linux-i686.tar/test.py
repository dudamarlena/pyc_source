# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/lib/test.py
# Compiled at: 2011-07-12 22:16:02
import client, json
print client.entry_index()
print client.entry_update('88bf8c57-5bd6-4d45-b2a2-44c3fa4d3b6c', json.dumps({'category': 'play.org', 'scheduled': None, 'parent': 'root', 'state': 'TODO', 'deadline': None, 'heading': '三国杀（修改）'}))
print client.entry_new('88bf8c57-5bd6-4d45-b2a2-44c3fa4d3b6c')
print client.entry_create('88bf8c57-5bd6-4d45-b2a2-44c3fa4d3b6c', json.dumps({'heading': '三国杀杀杀', 'state': None, 'parent': '88bf8c57-5bd6-4d45-b2a2-44c3fa4d3b6c', 'category': 'play.org', 'scheduled': None, 'deadline': None}))
print client.entry_delete('c859cf52-1029-463b-a01a-903045c15491')
print client.entry_show('88bf8c57-5bd6-4d45-b2a2-44c3fa4d3b6c')