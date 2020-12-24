# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpers/scw_wrapper.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 2651 bytes
from subprocess import run, check_output
import subprocess
from time import sleep

class SCW:

    def __init__(self):
        pass

    def main(self):
        print('main')

    def install():
        command = '\n\t\tsudo apt-get update\n\t\tsudo apt-get -y upgrade\n\t\twget https://storage.googleapis.com/golang/go1.9.2.linux-amd64.tar.gz\n\t\tsudo tar -xvf go1.9.2.linux-amd64.tar.gz\n\t\tsudo mv go /usr/local\n\t\texport GOROOT=/usr/local/go\n\n\t\texport GOPATH=$HOME/go\n\n\t\texport PATH=$GOPATH/bin:$GOROOT/bin:$PATH\n\t\t'
        run(command, shell=True)

    def launch(self, worker_type=None):
        result = {}
        command = 'scw --region=ams1 create --name="mendelmd_worker" ubuntu-xenial'
        output = run(command, shell=True, stdout=(subprocess.PIPE)).stdout.decode('utf-8').strip()
        short_id = output.split('-')[0]
        result['id'] = short_id
        command = 'scw --region=ams1 start {}'.format(short_id)
        output = run(command, shell=True, stdout=(subprocess.PIPE)).stdout.decode('utf-8').strip()
        flag = True
        while flag:
            command = 'scw --region=ams1 ps -a'
            output = run(command, shell=True, stdout=(subprocess.PIPE)).stdout.decode('utf-8').splitlines()
            for line in output:
                row = line.split()
                if row[0] == short_id:
                    if row[5] == 'running':
                        ip = row[6]
                        result['ip'] = ip
                        flag = False
                    else:
                        print('Waiting {} to start'.format(short_id))
                        sleep(30)

        command = 'ssh-keygen -f ~/.ssh/known_hosts -R {}'.format(ip)
        print(command)
        output = run(command, shell=True, stdout=(subprocess.PIPE)).stdout.decode('utf-8')
        print(output)
        return result

    def terminate(self, id):
        command = 'scw --region=ams1 stop -t {}'.format(id)
        output = run(command, shell=True, stdout=(subprocess.PIPE)).stdout.decode('utf-8').splitlines()