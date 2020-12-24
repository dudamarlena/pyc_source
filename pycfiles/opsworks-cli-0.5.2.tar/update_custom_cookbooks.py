# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chathuranga/Documents/Repository/Python_Projects/opsworks-cli/modules/update_custom_cookbooks.py
# Compiled at: 2019-07-19 06:31:12
import boto3, prettytable, modules.common_functions

def test_output_summary(region, stack, layer):
    table = prettytable.PrettyTable()
    table.field_names = ['Region', 'StackID', 'LayerID']
    table.add_row([str(region), str(stack), str(layer)])
    print table.get_string(title='Test Input Summary')


def update_custom_cookbooks_with_layer(region, stack, layer):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'update_custom_cookbooks_with_layer sub function testing'
        test_output_summary(region, stack, layer)
    else:
        client = boto3.client('opsworks', region_name=region)
        run_update_custom_cookbooks = client.create_deployment(StackId=stack, LayerIds=[
         layer], Command={'Name': 'update_custom_cookbooks'}, Comment='automated update_custom_cookbooks job')
        get_intance_count = client.describe_instances(LayerId=layer)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_update_custom_cookbooks['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)


def update_custom_cookbooks_without_layer(region, stack):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'update_custom_cookbooks_without_layer sub function testing'
        layer = None
        test_output_summary(region, stack, layer)
    else:
        client = boto3.client('opsworks', region_name=region)
        run_update_custom_cookbooks = client.create_deployment(StackId=stack, Command={'Name': 'update_custom_cookbooks'}, Comment='automated update_custom_cookbooks job')
        get_intance_count = client.describe_instances(StackId=stack)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_update_custom_cookbooks['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)
    return


def update_custom_cookbooks(region, stack, layer):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'update_custom_cookbooks main function testing'
        test_output_summary(region, stack, layer)
    else:
        modules.common_functions.get_names(stack, layer, region, 'update_custom_cookbooks')
        if layer is None:
            update_custom_cookbooks_without_layer(region, stack)
        else:
            update_custom_cookbooks_with_layer(region, stack, layer)
    return