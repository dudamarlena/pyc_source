# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloth/utils.py
# Compiled at: 2013-02-24 06:07:50
import re, os, boto.ec2
from fabric.api import env
REGION = os.environ.get('AWS_EC2_REGION')

def ec2_instances():
    """Use the EC2 API to get a list of all machines"""
    region = boto.ec2.get_region(REGION)
    reservations = region.connect().get_all_instances()
    instances = []
    for reservation in reservations:
        instances += reservation.instances

    return instances


def ip(node):
    if node.ip_address:
        return node.ip_address
    else:
        return node.private_ip_address


def instances(exp='.*'):
    """Filter list of machines matching an expression"""
    expression = re.compile(exp)
    instances = []
    for node in ec2_instances():
        if node.tags and ip(node):
            try:
                if expression.match(node.tags.get('Name')):
                    instances.append(node)
            except TypeError:
                pass

    return instances


def use(node):
    """Set the fabric environment for the specifed node"""
    try:
        role = node.tags.get('Name').split('-')[1]
        env.roledefs[role] += [ip(node)]
    except IndexError:
        pass

    env.nodes += [node]
    env.hosts += [ip(node)]