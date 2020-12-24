# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sesame/sg_open.py
# Compiled at: 2017-02-09 18:51:27
# Size of source mod 2**32: 1215 bytes
from .utils import get_external_ip, get_sg_id_from_name
import boto3

def __open_one_sg(sg_name):
    sg_id = get_sg_id_from_name(sg_name)
    ec2 = boto3.resource('ec2')
    current_ip = get_external_ip()
    current_cidr = current_ip + '/32'
    security_group = ec2.SecurityGroup(sg_id)
    security_group.authorize_ingress(IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp=current_cidr)


def __open_all_sgs():
    ec2 = boto3.resource('ec2')
    print('Opening incoming port 22 on ALL Security Groups.')
    print("I hope you know what you're doing.")
    for sg in ec2.security_groups.all():
        print('Opening port 22 on SG %s' % sg.group_name)


def sg_open(sg_name=None, all_sgs=False):
    if all_sgs:
        __open_all_sgs()
    if sg_name is not None:
        __open_one_sg(sg_name)