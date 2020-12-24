# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/experiment.py
# Compiled at: 2017-04-23 10:30:41
from cloudmesh_client.common.Shell import Shell

class Experiment(object):

    @classmethod
    def rm(cls, cluster, id=None, format=None):
        data = {'CLUSTER': cluster, 
           'ID': id}
        result = None
        if id is not None:
            try:
                result = Shell.ssh(cluster, ('rm -rf experiment/{ID}').format(**data))
            except Exception as e:
                pass

        else:
            try:
                result = Shell.ssh(cluster, 'rm -rf experiment/*').split('\n')
            except Exception as e:
                pass

        return result

    @classmethod
    def list(cls, cluster, id=None, format=None):
        data = {'CLUSTER': cluster, 
           'ID': id}
        result = None
        if id is not None:
            try:
                result = Shell.ssh(cluster, ('ls experiment/{ID}').format(**data))
                result = result.split('\n')
            except Exception as e:
                result = None

        else:
            try:
                result = Shell.ssh(cluster, 'ls experiment').split('\n')
                ids = sorted([ int(i) for i in result ])
                if format not in (None, 'txt'):
                    result = ids
            except Exception as e:
                result = None

        return result

    @classmethod
    def output(cls, cluster, id=None, format=None):
        data = {'CLUSTER': cluster, 
           'ID': id}
        result = None
        if id is None:
            ids = list(cluster)
        else:
            ids = [
             id]
        result = []
        for i in ids:
            try:
                result.append(Shell.ssh(cluster, ('cat experiment/{}/*.out').format(i)))
            except:
                result.append('')

        return result