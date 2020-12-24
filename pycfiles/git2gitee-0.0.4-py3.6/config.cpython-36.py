# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/config.py
# Compiled at: 2020-05-01 01:33:11
# Size of source mod 2**32: 581 bytes
token = '16604e967d52281868a18b0300670a43'

def params(repo, username, token, import_url):
    return {'utf8':'✓', 
     'authenticity_token':token, 
     'project[name]':repo, 
     'project[namespace_path]':username, 
     'project[path]':repo, 
     'project[public]':'1', 
     'language':'0', 
     'ignore':'no', 
     'license':'no', 
     'model':'1', 
     'prod':'master', 
     'dev':'develop', 
     'feat':'feature', 
     'rel':'release', 
     'bugfix':'hotfix', 
     'project[import_url]':import_url}