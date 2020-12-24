# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sesame/utils.py
# Compiled at: 2017-01-16 18:33:42
# Size of source mod 2**32: 844 bytes
import requests, boto3

def get_external_ip():
    SERVICE_URLS = [
     'http://checkip.amazonaws.com/']
    for url in SERVICE_URLS:
        response = requests.get(url)
        return response.text.strip()


def get_sg_id_from_name(sg_name):
    ec2 = boto3.client('ec2')
    groups = ec2.describe_security_groups(Filters=[
     {'Name': 'group-name', 
      'Values': [sg_name]}]).get('SecurityGroups', [])
    if len(groups) > 1:
        raise Exception('More than one SecurityGroup found with name: %s' % sg_name)
    elif len(groups) == 0:
        raise Exception('No SecurityGroups found with name: %s' % sg_name)
    return groups[0].get('GroupId')


def get_all_sgs():
    ec2 = boto3.resource('ec2')
    return ec2.security_groups.all()