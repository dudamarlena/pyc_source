# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chathuranga/Documents/Repository/Python_Projects/opsworks-cli/modules/setup.py
# Compiled at: 2019-07-19 06:31:12
import boto3, prettytable, modules.common_functions

def test_output_summary(region, stack, layer):
    table = prettytable.PrettyTable()
    table.field_names = ['Region', 'StackID', 'LayerID']
    table.add_row([str(region), str(stack), str(layer)])
    print table.get_string(title='Test Input Summary')


def setup_with_layer(region, stack, layer):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'setup_with_layer sub function testing'
        test_output_summary(region, stack, layer)
    else:
        client = boto3.client('opsworks', region_name=region)
        run_setup = client.create_deployment(StackId=stack, LayerIds=[
         layer], Command={'Name': 'setup'}, Comment='automated setup job with layer id')
        get_intance_count = client.describe_instances(LayerId=layer)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_setup['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)


def setup_without_layer(region, stack):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'setup_without_layer sub function testing'
        layer = None
        test_output_summary(region, stack, layer)
    else:
        client = boto3.client('opsworks', region_name=region)
        run_setup = client.create_deployment(StackId=stack, Command={'Name': 'setup'}, Comment='automated setup job with stack id')
        get_intance_count = client.describe_instances(StackId=stack)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_setup['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)
    return


def setup(region, stack, layer=None):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'setup main function testing'
        test_output_summary(region, stack, layer)
    else:
        modules.common_functions.get_names(stack, layer, region, 'setup')
        if layer is None:
            setup_without_layer(region, stack)
        else:
            setup_with_layer(region, stack, layer)
    return