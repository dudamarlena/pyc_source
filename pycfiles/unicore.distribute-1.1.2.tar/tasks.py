# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.distribute/unicore/distribute/tasks.py
# Compiled at: 2016-05-07 05:25:40
from pyramid_celery import celery_app as app
from elasticgit import EG
from unicore.content.models import Page, Category, Localisation

@app.task(ignore_result=True)
def fastforward(repo_path, index_prefix, es={}):
    workspace = EG.workspace(repo_path, index_prefix=index_prefix, es=es)
    workspace.fast_forward()
    workspace.reindex(Page)
    workspace.reindex(Category)
    workspace.reindex(Localisation)