# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/twister/fg-twister-start.py
# Compiled at: 2012-09-06 11:03:15
"""
This program is to setup Twister on FutureGrid automatically
"""
import os, sys, time
from datetime import datetime
from fg_euca_twister_util import instance_id, get_nodes
args = sys.argv
if len(args) != 9:
    print 'Usage: python fg_euca_start_twister.py [-k user key] [-i public key file path] [-n number of instances][-t instance type]'
    sys.exit()
key_tag = '-k'
key = ''
pem_tag = '-i'
pem = ''
num_tag = '-n'
num = 1
type_tag = '-t'
instance_type = 'c1.medium'
for i in range(len(args)):
    if cmp(args[i], key_tag) == 0:
        key = args[(i + 1)]
    if cmp(args[i], pem_tag) == 0:
        pem = args[(i + 1)]
    if cmp(args[i], num_tag) == 0:
        num = args[(i + 1)]
    if cmp(args[i], type_tag) == 0:
        instance_type = args[(i + 1)]

print 'User key:', key
print 'User pem:', pem
print 'Number of nodes:', num
print 'Instance type:', instance_type
print '\n### Future Grid Euca Twister Starts...###'
print 'euca-run-instances -k ' + key + ' -n ' + num + ' ' + instance_id + ' -t ' + instance_type
os.system('euca-run-instances -k ' + key + ' -n ' + num + ' ' + instance_id + ' -t ' + instance_type)
lines = get_nodes()
num_nodes = len(lines)
if num_nodes == 0:
    print '\nNo available Twister nodes...'
    sys.exit()
print '\nGet', num_nodes, 'instances,', 'checking if they are all ready, please wait... (possibly needs several minutes)'
tstart = datetime.now()
ready = False
ready_count = 0
while not ready:
    lines = get_nodes()
    for i in range(num_nodes):
        if lines[i].find('running') != -1:
            ready_count = ready_count + 1

    if ready_count == num_nodes:
        ready = True
        break
    time.sleep(10)

tdiff = datetime.now() - tstart
print 'Time used:', tdiff.seconds, 'seconds.'
print 'Are nodes ready?', ready
lines = get_nodes()
ip_dict = {}
for i in range(num_nodes):
    items = lines[i].split('\t')
    ip_dict[items[4].strip()] = items[3].strip()

print 'Now write IP addresses to nodes file...'
home_dir = os.popen('echo $HOME').read()
home_dir = home_dir[:len(home_dir) - 1]
fp = open(home_dir + '/nodes', 'w')
for ip in ip_dict.keys():
    fp.write(ip + '\n')

fp.close()
os.system('euca-authorize -P tcp -p 22 -s 0.0.0.0/0   default')
twister_home = os.popen('ssh -i ' + pem + ' -o StrictHostKeyChecking=no root@' + ip_dict.values()[0] + " 'echo $TWISTER_HOME'").read()
twister_home = twister_home[:len(twister_home) - 1]
print 'Remote Twister Home is', twister_home
print 'Copy node file to remote...'
os.system('scp -i ' + pem + ' ' + home_dir + '/nodes root@' + ip_dict.values()[0] + ':' + twister_home + '/bin/')
print '\n### Kill potential Twister processes...###'
os.system('ssh -i ' + pem + ' root@' + ip_dict.values()[0] + " 'cd " + twister_home + "/bin/; ./kill_all_java_processes.sh root'")
print '\n### Twister Auto Configuration Starts...###'
cmd_line = 'ssh -i ' + pem + ' root@' + ip_dict.values()[0] + " 'cd " + twister_home + "/bin/; TwisterPowerMakeUp.sh'"
configuration = os.popen(cmd_line).read()
print configuration
broker_address = ''
conf_lines = configuration.split('\n')
for line in conf_lines:
    if line.find('ActiveMQ') != -1:
        for ip in ip_dict.keys():
            if line.find(ip) != -1:
                broker_address = ip_dict[ip]
                break

    if cmp(broker_address, '') != 0:
        break

print '### Notice...###'
print 'Please log in to ' + broker_address + ' and start ActiveMQ broker.'