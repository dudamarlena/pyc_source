# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpers/b2_wrapper.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 1435 bytes
from subprocess import run, check_output
import os, json

class B2:

    def __init__(self):
        pass

    def main(self):
        print('main')

    def install(self):
        command = '\n        git clone https://github.com/Backblaze/B2_Command_Line_Tool.git\n        cd B2_Command_Line_Tool\n        python setup.py build\n        python setup.py install\n        b2 authorize-account\n        '
        run(command, shell=True)

    def upload(self, source, dest):
        command = 'b2 upload-file mendelmd {} {}'.format(source, dest)
        output = check_output(command, shell=True).decode('utf-8')
        output = output.splitlines()
        print(output)
        results = ''.join(output[2:])
        print('results', results)
        results = json.loads(results)
        results[output[0].split(':', 1)[0]] = output[0].split(':', 1)[1:]
        results[output[1].split(':', 1)[0]] = output[1].split(':', 1)[1:]
        return results

    def download(self, bucket, file):
        basename = os.path.basename(file)
        command = 'b2 download-file-by-name mendelmd {} {}'.format(file, file)
        run(command, shell=True)