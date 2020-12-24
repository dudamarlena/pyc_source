# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chathuranga/Documents/Repository/Python_Projects/opsworks-cli/modules/execute_recipes.py
# Compiled at: 2019-07-19 06:31:12
import boto3, prettytable, modules.common_functions

def test_output_summary(region, stack, layer, cookbook, custom_json):
    table = prettytable.PrettyTable()
    table.field_names = ['Region', 'StackID', 'LayerID', 'Cookbook', 'Custom_JSON']
    table.add_row([str(region), str(stack), str(layer), str(cookbook), str(custom_json)])
    print table.get_string(title='Test Input Summary')


def run_recipes_with_layer(region, stack, layer, cookbook, custom_json=None):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'run_recipes_with_layer sub function'
        test_output_summary(region, stack, layer, cookbook, custom_json)
    else:
        try:
            custom_json
        except NameError:
            custom_json = str({})

        if custom_json is None:
            custom_json = str({})
        client = boto3.client('opsworks', region_name=region)
        run_recipes = client.create_deployment(StackId=stack, Command={'Name': 'execute_recipes', 
           'Args': {'recipes': [
                              cookbook]}}, Comment='automated execute_recipes job with custom_json', CustomJson=custom_json)
        get_intance_count = client.describe_instances(LayerId=layer)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_recipes['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)
    return


def run_recipes_without_layer(region, stack, cookbook, custom_json=None):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'run_recipes_without_layer sub function'
        layer = None
        test_output_summary(region, stack, layer, cookbook, custom_json=None)
    else:
        try:
            custom_json
        except NameError:
            custom_json = str({})

        if custom_json is None:
            custom_json = str({})
        client = boto3.client('opsworks', region_name=region)
        run_recipes = client.create_deployment(StackId=stack, Command={'Name': 'execute_recipes', 
           'Args': {'recipes': [
                              cookbook]}}, Comment='automated execute_recipes job without custom_json', CustomJson=custom_json)
        get_intance_count = client.describe_instances(StackId=stack)
        all_instance_status = []
        for instancestatus in get_intance_count['Instances']:
            ec2status = instancestatus['Status']
            all_instance_status.append(ec2status)

        instances = len(all_instance_status)
        deploymentid = run_recipes['DeploymentId']
        modules.common_functions.get_status(deploymentid, region, instances)
    return


def execute_recipes(region, stack, cookbook, layer=None, custom_json=None):
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print 'execute_recipes main function testing'
        test_output_summary(region, stack, layer, cookbook, custom_json)
    else:
        modules.common_functions.get_names(stack, layer, region, 'execute_recipe')
        if layer is None:
            run_recipes_without_layer(region, stack, cookbook, custom_json)
        else:
            run_recipes_with_layer(region, stack, layer, cookbook, custom_json)
    return