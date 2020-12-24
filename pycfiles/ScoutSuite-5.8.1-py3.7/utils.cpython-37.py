# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/utils.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1975 bytes
from __future__ import print_function
formatted_service_name = {'acm':'ACM', 
 'cloudformation':'CloudFormation', 
 'cloudtrail':'CloudTrail', 
 'cloudwatch':'CloudWatch', 
 'credentials':'Credentials', 
 'config':'Config', 
 'directconnect':'Direct Connect', 
 'dynamodb':'DynamoDB', 
 'elbv2':'ELBv2', 
 'elasticache':'ElastiCache', 
 'lambda':'Lambda', 
 'awslambda':'Lambda', 
 'redshift':'RedShift', 
 'route53':'Route53', 
 'secretsmanager':'Secrets Manager', 
 'storageaccounts':'Storage Accounts', 
 'sqldatabase':'SQL Database', 
 'securitycenter':'Security Center', 
 'keyvault':'Key Vault', 
 'appgateway':'Application Gateway', 
 'rediscache':'Redis Cache', 
 'network':'Network', 
 'appservice':'App Services', 
 'loadbalancer':'Load Balancer', 
 'virtualmachines':'Virtual Machines', 
 'cloudstorage':'Cloud Storage', 
 'cloudsql':'Cloud SQL', 
 'stackdriverlogging':'Stackdriver Logging', 
 'stackdrivermonitoring':'Stackdriver Monitoring', 
 'computeengine':'Compute Engine', 
 'kubernetesengine':'Kubernetes Engine', 
 'cloudresourcemanager':'Cloud Resource Manager', 
 'actiontrail':'ActionTrail', 
 'identity':'Identity', 
 'objectstorage':'Object Storage'}

def manage_dictionary(dictionary, key, init, callback=None):
    """
    :param dictionary:
    :param key:
    :param init:
    :param callback:
    :return:
    """
    if not isinstance(dictionary, dict):
        raise TypeError()
    if str(key) in dictionary:
        return dictionary
    dictionary[str(key)] = init
    manage_dictionary(dictionary, key, init)
    if callback:
        callback(dictionary[key])
    return dictionary


def format_service_name(service):
    """

    :param service:
    :return:
    """
    if service in formatted_service_name:
        return formatted_service_name[service]
    return service.upper()