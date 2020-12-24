# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/column/api/model/run_model.py
# Compiled at: 2017-08-21 17:11:27
from collections import defaultdict

def get_progress(run):
    progress = run['api_runner'].get_progress()
    if progress is None:
        return 0
    else:
        return progress


def format_response(run):
    response = defaultdict(dict)
    for item, value in run.iteritems():
        if item == 'api_runner':
            response['progress'] = get_progress(run)
        elif item == 'options':
            for sub_i, sub_v in value.iteritems():
                if sub_i == 'become_pass':
                    response[item][sub_i] = '***'
                elif sub_i == 'conn_pass':
                    response[item][sub_i] = '***'
                else:
                    response[item][sub_i] = sub_v

        else:
            response[item] = value

    return response