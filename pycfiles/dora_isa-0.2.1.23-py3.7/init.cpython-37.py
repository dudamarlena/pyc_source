# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dora/template/cp/score/init.py
# Compiled at: 2020-01-16 10:25:08
# Size of source mod 2**32: 1202 bytes
import sys, datetime, os, json, code_score
if __name__ == '__main__':
    try:
        data = os.environ.get('DORA_DATA', '/data')
        result_model = code_score.score(sys.argv[1:])
        timestamp = datetime.datetime.now()
        with open(os.path.join(data + '/', 'output/', 'result-' + timestamp.strftime('%m-%d-%Y-%H:%M:%S') + '.json'), 'wb') as (file):
            result = dict()
            result['statusCode'] = 'success'
            result['result'] = result_model
            file.write(json.dumps(result).encode('utf8'))
            print('Please check your path result output for more details: ' + str(file))
    except Exception as e:
        try:
            data = os.environ.get('DORA_DATA', '/data')
            error = str(e)
            timestamp = datetime.datetime.now()
            with open(os.path.join(data + '/', 'error/', 'error-' + timestamp.strftime('%m-%d-%Y-%H:%M:%S') + '.json'), 'wb') as (file):
                result = dict()
                result['statusCode'] = 'error'
                result['result'] = error
                file.write(json.dumps(result).encode('utf8'))
                print('Please check your path error output for more details: ' + str(file))
            print('Error: ' + str(e))
        finally:
            e = None
            del e