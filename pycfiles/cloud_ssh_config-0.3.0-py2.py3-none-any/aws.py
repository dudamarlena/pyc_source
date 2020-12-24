# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/silver/Projects/Public/cloud_ssh_config/cloud_ssh_config/cloud/aws.py
# Compiled at: 2018-10-24 05:58:08
import boto3

class cloud:

    def get_hosts(self):
        client = boto3.client('ec2')
        instances = client.describe_instances(Filters=[
         {'Name': 'tag:Name', 
            'Values': [
                     '*']},
         {'Name': 'instance-state-name', 
            'Values': [
                     'running']}], MaxResults=100)
        del client
        hosts = {}
        for host in instances['Reservations']:
            if 'PublicIpAddress' in host['Instances'][0]:
                for tag in host['Instances'][0]['Tags']:
                    if tag['Key'] == 'Name':
                        hosts.update({tag['Value']: host['Instances'][0]['PublicIpAddress']})

        return hosts