# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chathuranga/Documents/Repository/Python_Projects/opsworks-cli/modules/deploy.py
# Compiled at: 2019-07-19 06:31:12
import boto3, prettytable, modules.common_functions

def test_output_summary(region, stack, layer, app, custom_json=None):
    table = prettytable.PrettyTable()
    table.field_names = ['Region', 'StackID', 'LayerID', 'ApplicationID', 'CustomJSON']
    table.add_row([str(region), str(stack), str(layer), str(app), str(custom_json)])
    print table.get_string(title='Test Input Summary')


def deploy_with_layer(region, stack, layer, app, custom_json=None):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'deploy_with_layer sub function'
        test_output_summary(region, stack, layer, app, custom_json)
    else:
        try:
            custom_json
        except NameError:
            custom_json = str({})

        if custom_json is None:
            custom_json = str({})
        client = boto3.client('opsworks', region_name=region)
        run_recipes = client.create_deployment(StackId=stack, AppId=app, LayerIds=[
         layer], Command={'Name': 'deploy'}, Comment='automated deploy job', CustomJson=custom_json)
        get_intance_count = client.describe_instances(LayerId=layer)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_recipes['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)
    return


def deploy_without_layer(region, stack, app, custom_json=None):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'deploy_without_layer sub function'
        test_output_summary(region, stack, app, custom_json)
    else:
        try:
            custom_json
        except NameError:
            custom_json = str({})

        if custom_json is None:
            custom_json = str({})
        client = boto3.client('opsworks', region_name=region)
        run_recipes = client.create_deployment(StackId=stack, AppId=app, Command={'Name': 'deploy'}, Comment='automated deploy job', CustomJson=custom_json)
        get_intance_count = client.describe_instances(StackId=stack)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_recipes['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)
    return


def deploy(region, stack, app, layer=None, custom_json=None):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'deploy main function'
        test_output_summary(region, stack, layer, app, custom_json)
    else:
        modules.common_functions.get_names(stack, layer, region, 'deploy')
        if layer is None:
            deploy_without_layer(region, stack, app, custom_json)
        else:
            deploy_with_layer(region, stack, layer, app, custom_json)
    return