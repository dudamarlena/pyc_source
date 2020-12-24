# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/hpc/provider/slurm/squeue.py
# Compiled at: 2017-04-23 10:30:41
import json
from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider

class Squeue(object):

    @staticmethod
    def squeue_to_json(input_str):
        d = {}
        for i, line in enumerate(input_str.splitlines()):
            if not line.startswith('Warning:') and not line.__contains__('NODELIST(REASON)'):
                d[i] = {}
                d[i]['jobid'], d[i]['partition'], d[i]['name'], d[i]['user'], d[i]['st'], d[i]['time'], d[i]['nodes'], d[i]['nodelist(reason)'] = line.split()

        json_str = json.dumps(d, indent=4, separators=(',', ': '))
        assert isinstance(json_str, str)
        return json.loads(json_str)

    @staticmethod
    def get(user=None, name=None):
        squeue_json = Squeue.read_squeue()
        assert isinstance(squeue_json, str)
        json_obj = json.loads(squeue_json)
        d = {}
        for i, key in enumerate(json_obj.keys()):
            if user and name:
                if user == json_obj[key]['user'] and name == json_obj[key]['name']:
                    d[i] = json_obj[key]
            elif user:
                if user == json_obj[key]['user']:
                    d[i] = json_obj[key]
            elif name:
                if name == json_obj[key]['name']:
                    d[i] = json_obj[key]
            else:
                d[i] = json_obj[key]

        return json.dumps(d, indent=4, separators=(',', ': '))

    @staticmethod
    def read_squeue():
        name = None
        provider = BatchProvider(name)
        return provider.read_squeue(format='json')


if __name__ == '__main__':
    print Squeue.read_squeue()
    print Squeue.get(name='NGBW-JOB', user='cipres')