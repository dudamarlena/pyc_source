# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/stack.py
# Compiled at: 2018-01-05 13:50:32
import os, json, urlparse, boto3, subprocess, shutil, jmespath, sys, time, imp, datetime as dt
from botocore.exceptions import ClientError
from sets import Set
from yac.lib.file import FileError, file_in_registry, get_file_contents, localize_file, get_dump_path
from yac.lib.file import FileError, file_in_registry, get_file_contents, localize_file, get_dump_path
from yac.lib.file import dump_file_contents
from yac.lib.template import apply_templates_in_file, apply_templates_in_dir
from yac.lib.paths import get_config_path
from yac.lib.intrinsic import apply_fxn
from yac.lib.variables import get_variable, set_variable
from yac.lib.naming import get_stack_name
from yac.lib.file import get_localized_script_path
UPDATING = 'Updating'
BUILDING = 'Building'
STACK_STATES = [
 'CREATE_IN_PROGRESS', 'CREATE_FAILED', 'CREATE_COMPLETE', 'ROLLBACK_IN_PROGRESS',
 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE', 'DELETE_IN_PROGRESS', 'DELETE_FAILED',
 'DELETE_COMPLETE', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS', 'UPDATE_ROLLBACK_FAILED',
 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE']
CREATE_IN_PROGRESS_STATE = 'CREATE_IN_PROGRESS'
NEWLY_CREATED_STATE = 'CREATE_COMPLETE'
UPDATABLE_STATES = [
 'CREATE_COMPLETE', 'UPDATE_COMPLETE']
UNKNOWN_STATE = 'unknown'
NON_EXISTANT = 'non-existant'
NEWLY_CREATED_STATE = 'CREATE_COMPLETE'
UPDATE_COMPLETE_STATE = 'UPDATE_COMPLETE'
UPDATE_COMPLETE_STATES = ['UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
UPDATE_IN_PROGRESS_STATE = 'UPDATE_IN_PROGRESS'
UPDATABLE_STATES = [
 'CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
UNKNOWN_STATE = 'unknown'
MAX_TEMPLATE_LEN = 51200

def cost_stack(template_string='', stack_params=None, template_staging_path=None):
    cost_response = ''
    cost_error = ''
    client = boto3.client('cloudformation')
    try:
        if len(template_string) > MAX_TEMPLATE_LEN and template_staging_path:
            template_url = upload_template_to_s3(template_string, template_staging_path)
            response = client.estimate_template_cost(TemplateURL=template_url, Parameters=stack_params)
            cost_response = str(response['Url'])
        elif len(template_string) > MAX_TEMPLATE_LEN and not template_staging_path:
            cost_error = "Cost can't be calculated because the template string exceeds Amazon's character limit." + "\nTo resolve, specify an S3 path to stage the template using the 'template-staging-s3-path' parameter."
        else:
            response = client.estimate_template_cost(TemplateBody=template_string, Parameters=stack_params)
            cost_response = str(response['Url'])
    except ClientError as e:
        cost_error = 'Stack costing failed: %s' % str(e)

    return (cost_response, cost_error)


def create_stack(stack_name, template_string='', stack_params=[], template_staging_path=None, stack_tags=[]):
    create_response = ''
    create_error = ''
    client = boto3.client('cloudformation')
    try:
        if len(template_string) > MAX_TEMPLATE_LEN and template_staging_path:
            template_url = upload_template_to_s3(template_string, template_staging_path)
            response = client.create_stack(StackName=stack_name, TemplateURL=template_url, Parameters=stack_params, Tags=stack_tags, Capabilities=[
             'CAPABILITY_IAM'])
            create_response = str(response['StackId'])
        elif len(template_string) > MAX_TEMPLATE_LEN and not template_staging_path:
            create_error = "Cost can't be calculated because the template string exceeds Amazon's character limit." + "\nTo resolve, specify an S3 path to stage the template using the 'template-staging-s3-path' parameter."
        else:
            response = client.create_stack(StackName=stack_name, TemplateBody=template_string, Parameters=stack_params, Tags=stack_tags, Capabilities=[
             'CAPABILITY_IAM'])
            create_response = str(response['StackId'])
    except ClientError as e:
        create_error = 'Stack creation failed: %s' % str(e)

    return (create_response, create_error)


def update_stack(stack_name, template_string='', stack_params=[], stack_tags=[]):
    update_response = ''
    update_error = ''
    client = boto3.client('cloudformation')
    try:
        if len(template_string) > MAX_TEMPLATE_LEN and template_staging_path:
            template_url = upload_template_to_s3(template_string, template_staging_path)
            response = client.update_stack(StackName=stack_name, TemplateURL=template_url, Parameters=stack_params, Capabilities=[
             'CAPABILITY_IAM'])
            update_response = str(response['StackId'])
        elif len(template_string) > MAX_TEMPLATE_LEN and not template_staging_path:
            create_error = "Cost can't be calculated because the template string exceeds Amazon's character limit." + "\nTo resolve, specify an S3 path to stage the template using the 'template-staging-s3-path' parameter."
        else:
            response = client.update_stack(StackName=stack_name, TemplateBody=template_string, Parameters=stack_params, Capabilities=[
             'CAPABILITY_IAM'])
            update_response = str(response['StackId'])
    except ClientError as e:
        if 'No updates are to be performed' not in str(e):
            update_error = 'Stack creation failed: %s' % str(e)

    return (
     update_response, update_error)


def upload_template_to_s3(template_string, template_staging_path):
    file_path = dump_file_contents(template_string, 'staging', 'cf.json')
    cp_file_to_s3(file_path, 's3://%s' % template_staging_path)
    return 'https://s3.amazonaws.com/%s' % template_staging_path


def get_stack_state(stack_name):
    client = boto3.client('cloudformation')
    if stack_exists(stack_name):
        response = client.describe_stacks(StackName=stack_name)
        states = jmespath.search('Stacks[*].StackStatus', response)
        if len(states) == 1:
            state = states[0]
        else:
            state = UNKNOWN
    else:
        state = NON_EXISTANT
    return state


def get_stack_templates(service_descriptor, service_parameters):
    service_template = {}
    dynamic_resources = {}
    resources_fxn = get_variable(service_descriptor, 'resource-function')
    if resources_fxn:
        dynamic_resources = run_resources_fxn(resources_fxn, service_parameters)
    if 'stack-template' in service_descriptor:
        service_template_with_refs = service_descriptor['stack-template']
        service_template_with_refs['Resources'].update(dynamic_resources)
        service_template = apply_fxn(service_template_with_refs, service_parameters)
    return service_template


def get_stackdef_from_file(template_path, service_parmeters={}):
    stack_definitions = {}
    stack_defs_str = get_file_contents(template_path)
    if stack_defs_str:
        stack_definitions = json.loads(stack_defs_str)
        stack_definitions = apply_fxn(stack_definitions, service_parmeters)
    return stack_definitions


def stack_exists(stack_name):
    client = boto3.client('cloudformation')
    try:
        response = client.describe_stacks(StackName=stack_name)
        stack_count = len(response['Stacks'])
        return stack_count > 0
    except:
        return False


def deploy_stack_files(service_descriptor, service_parmeters, servicefile_path):
    files_for_boot = get_variable(service_descriptor, 'deploy-for-boot', [], 'files')
    _load_files(files_for_boot, service_parmeters, servicefile_path)
    dirs_for_boot = get_variable(service_descriptor, 'deploy-for-boot', [], 'directories')
    _load_dirs(dirs_for_boot, service_parmeters)


def _load_files(files, service_parmeters, servicefile_path):
    servicefile_path = get_variable(service_parmeters, 'servicefile-path')
    for this_ifile in files:
        if 'file-params' in this_ifile:
            service_parmeters.update(this_ifile['file-params'])
        this_file = apply_fxn(this_ifile, service_parmeters)
        localized_file = localize_file(this_file['src'], servicefile_path)
        rendered_file_path = get_dump_path(get_variable(service_parmeters, 'service-name', 'unknown'))
        if os.path.exists(localized_file):
            rendered_file = apply_templates_in_file(localized_file, service_parmeters, rendered_file_path)
            if is_s3_destination(this_file['dest']) and rendered_file:
                cp_file_to_s3(rendered_file, this_file['dest'])
            else:
                if not os.path.exists(os.path.dirname(this_file['dest'])):
                    os.makedirs(os.path.dirname(this_file['dest']))
                shutil.copy(rendered_file, this_file['dest'])
        else:
            raise FileError('%s file deploy was not performed. Source file is missing' % localized_file)


def _load_files_new(files, service_parmeters):
    servicefile_path = get_variable(service_parmeters, 'servicefile-path')
    for this_ifile in files:
        this_file = apply_fxn(this_ifile, service_parmeters)
        source_path = os.path.join(servicefile_path, this_file['src'])
        rendered_file_path = os.path.join(servicefile_path, 'tmp')
        if os.path.exists(source_path):
            rendered_file = apply_templates_in_file(source_path, service_parmeters, rendered_file_path)
            if is_s3_destination(this_file['dest']) and rendered_file:
                cp_file_to_s3(rendered_file, this_file['dest'])
            else:
                if not os.path.exists(os.path.dirname(this_file['dest'])):
                    os.makedirs(os.path.dirname(this_file['dest']))
                shutil.copy(rendered_file, this_file['dest'])
        else:
            raise FileError('%s file deploy was not performed. Source file is missing' % source_path)


def _load_dirs(directories, service_parmeters):
    servicefile_path = get_variable(service_parmeters, 'servicefile-path', '')
    for this_idir in directories:
        this_dir = apply_fxn(this_idir, service_parmeters)
        source_path = os.path.join(servicefile_path, this_dir['src'])
        rendered_dir_path = os.path.join(servicefile_path, 'tmp', this_dir['src'])
        if os.path.exists(source_path):
            apply_templates_in_dir(source_path, service_parmeters, rendered_dir_path)
            if is_s3_destination(this_dir['dest']):
                sync_dir_to_s3(rendered_dir_path, this_dir['dest'])
            else:
                if os.path.exists(this_dir['dest']):
                    shutil.rmtree(this_dir['dest'])
                shutil.copytree(rendered_dir_path, this_dir['dest'])
        else:
            raise FileError('%s directory deploy was not performed. Source dir is missing' % source_path)


def is_s3_destination(destination):
    s3_destination = False
    url_parts = urlparse.urlparse(destination)
    if url_parts and url_parts.scheme and url_parts.scheme == 's3':
        s3_destination = True
    return s3_destination


def cp_file_to_s3(source_file, destination_s3_url):
    if os.path.exists(source_file):
        aws_cmd = 'aws s3 cp %s %s' % (source_file, destination_s3_url)
        try:
            subprocess.check_output(aws_cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            raise FileError('Error copying file to s3 destination: %s' % e)

    else:
        raise FileError('Source file %s does not exist' % source_file)


def sync_dir_to_s3(source_dir, destination_s3_url):
    if os.path.exists(source_dir):
        aws_cmd = 'aws s3 sync %s %s %s' % (source_dir, destination_s3_url, '--delete')
        try:
            subprocess.check_output(aws_cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            raise FileError('Error copying directory to s3 destination: %s' % e)

    else:
        raise FileError('Source directory %s does not exist' % source_dir)


def get_running_ec2s(stack_name, name_search_string=''):
    filters = [{'Name': 'tag:aws:cloudformation:stack-name', 'Values': [stack_name]}]
    if name_search_string:
        filters.append({'Name': 'tag:Name', 'Values': [name_search_string]})
    client = boto3.client('ec2')
    reservations = client.describe_instances(Filters=filters)
    ips = jmespath.search("Reservations[?Instances[?State.Name=='running']].Instances[*]", reservations)
    ip_str_list = []
    for ip in ips:
        if len(ip) == 1:
            ip_str_list.extend(ip)

    return ip_str_list


def get_ec2_ips(stack_name, name_search_string='', publicIP=False):
    filters = [{'Name': 'tag:aws:cloudformation:stack-name', 'Values': [stack_name]}]
    if name_search_string:
        filters.append({'Name': 'tag:Name', 'Values': [name_search_string]})
    client = boto3.client('ec2')
    instances = client.describe_instances(Filters=filters)
    if publicIP:
        ips = jmespath.search("Reservations[?Instances[?State.Name=='running']].Instances[*].PublicIpAddress", instances)
    else:
        ips = jmespath.search("Reservations[?Instances[?State.Name=='running']].Instances[*].PrivateIpAddress", instances)
    ip_str_list = []
    for ip in ips:
        if len(ip) == 1:
            ip_str_list.extend(ip)

    return ip_str_list


def get_ec2_sgs(stack_name, name_search_string=''):
    filters = [{'Name': 'tag:aws:cloudformation:stack-name', 'Values': [stack_name]}]
    if name_search_string:
        filters.append({'Name': 'tag:Name', 'Values': [name_search_string]})
    client = boto3.client('ec2')
    sgs = client.describe_security_groups(Filters=filters)
    return sgs['SecurityGroups']


def get_rds_endpoints(stack_name):
    endpoints = []
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)
    rds_id = ''
    if 'StackResources' in resources:
        for resource in resources['StackResources']:
            if resource['ResourceType'] == 'AWS::RDS::DBInstance':
                rds_id = resource['PhysicalResourceId']

    if rds_id:
        client = boto3.client('rds')
        instances = client.describe_db_instances(DBInstanceIdentifier=rds_id)
        endpoints = jmespath.search('DBInstances[*].{Address: Endpoint.Address, Port: Endpoint.Port, Status: DBInstanceStatus}', instances)
    return endpoints


def get_ecs_service(stack_name, name_search_string):
    to_ret = {}
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)
    service_id = ''
    cluster_name = ''
    if 'StackResources' in resources:
        for resource in resources['StackResources']:
            if resource['ResourceType'] == 'AWS::ECS::Service':
                if name_search_string in resource['PhysicalResourceId']:
                    service_id = resource['PhysicalResourceId']
            if resource['ResourceType'] == 'AWS::ECS::Cluster':
                cluster_name = resource['PhysicalResourceId']

    if service_id and cluster_name:
        client = boto3.client('ecs')
        services = client.describe_services(cluster=cluster_name, services=[
         service_id])
        for service in services['services']:
            if name_search_string in service['serviceName']:
                to_ret = service
                break

    return to_ret


def get_stack_elbs(stack_name, name_search_string):
    to_ret = {}
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)
    elb_id = ''
    if 'StackResources' in resources:
        for resource in resources['StackResources']:
            if resource['ResourceType'] == 'AWS::ElasticLoadBalancing::LoadBalancer':
                if name_search_string in resource['PhysicalResourceId']:
                    elb_id = resource['PhysicalResourceId']
                    break

    if elb_id:
        client = boto3.client('elb')
        elbs = client.describe_load_balancers(LoadBalancerNames=[elb_id])
        for elb in elbs['LoadBalancerDescriptions']:
            if name_search_string in elb['LoadBalancerName']:
                to_ret = elb
                break

    return to_ret


def get_ami_name(ami_id):
    ec2 = boto3.resource('ec2')
    image = ec2.Image(ami_id)
    return image.name


def get_rds_instance_ids(stack_name):
    instances_ids = []
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)
    rds_id = ''
    if 'StackResources' in resources:
        for resource in resources['StackResources']:
            if resource['ResourceType'] == 'AWS::RDS::DBInstance':
                rds_id = resource['PhysicalResourceId']

    if rds_id:
        client = boto3.client('rds')
        instances = client.describe_db_instances(DBInstanceIdentifier=rds_id)
        instances_ids = jmespath.search('DBInstances[*].DBInstanceIdentifier', instances)
    return instances_ids


def get_cache_endpoint(stack_name):
    endpoint = {}
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)
    cache_id = ''
    if 'StackResources' in resources:
        for resource in resources['StackResources']:
            if resource['ResourceType'] == 'AWS::ElastiCache::ReplicationGroup':
                cache_id = resource['PhysicalResourceId']

    if cache_id:
        client = boto3.client('elasticache')
        response = client.describe_replication_groups(ReplicationGroupId=cache_id)
        if 'ReplicationGroups' in response and len(response['ReplicationGroups']) > 0:
            this_rep_group = response['ReplicationGroups'][0]
            for node in this_rep_group['NodeGroups']:
                if 'PrimaryEndpoint' in node:
                    endpoint = node['PrimaryEndpoint']

    return endpoint


def get_asg_subnet_ids(asg_name):
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if response['AutoScalingGroups']:
        asg = response['AutoScalingGroups'][0]
    else:
        asg = {}
    subnet_ids = []
    if asg:
        subnet_id_str = asg['VPCZoneIdentifier']
        subnet_ids = subnet_id_str.split(',')
    return subnet_ids


def get_stack_iam_role(params):
    asg_name = get_resource_name(params, 'asg')
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if response['AutoScalingGroups']:
        asg = response['AutoScalingGroups'][0]
        launchConfigName = asg['LaunchConfigurationName']
    else:
        launchConfigName = ''
    iam_role = ''
    if launchConfigName:
        response = client.describe_launch_configurations(LaunchConfigurationNames=[launchConfigName])
        if response['LaunchConfigurations']:
            iam_role = response['LaunchConfigurations'][0]['IamInstanceProfile']
    return iam_role


def get_stack_ssh_keys(params):
    asg_name = get_resource_name(params, 'asg')
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if response['AutoScalingGroups']:
        asg = response['AutoScalingGroups'][0]
        launchConfigName = asg['LaunchConfigurationName']
    else:
        launchConfigName = ''
    ssh_key = ''
    if launchConfigName:
        response = client.describe_launch_configurations(LaunchConfigurationNames=[launchConfigName])
        if response['LaunchConfigurations']:
            ssh_key = response['LaunchConfigurations'][0]['KeyName']
    return ssh_key


def get_stack_ssl_cert(params):
    ielb_name = get_resource_name(params, 'i-elb')
    eelb_name = get_resource_name(params, 'e-elb')
    client = boto3.client('elb')
    response = client.describe_load_balancers(LoadBalancerNames=[ielb_name, eelb_name])
    if response['LoadBalancerDescriptions']:
        elb = response['LoadBalancerDescriptions'][0]
    else:
        elb = {}
    ssl_cert = ''
    if elb:
        ssl_certs = jmespath.search('[*].Listener.SSLCertificateId', elb['ListenerDescriptions'])
        if ssl_certs and len(ssl_certs) == 1:
            ssl_cert = ssl_cert[0]
    return ssl_cert


def stack_has_external_access(params):
    external_access = False
    eelb_name = get_resource_name(params, 'e-elb')
    client = boto3.client('elb')
    response = client.describe_load_balancers(LoadBalancerNames=[eelb_name])
    if response['LoadBalancerDescriptions']:
        elb = response['LoadBalancerDescriptions'][0]
    else:
        elb = {}
    if elb:
        external_access = True
    return external_access


def get_stack_vpc(params):
    stack_name = get_stack_name(params)
    vpc_id = ''
    if stack_name:
        cloudformation = boto3.client('cloudformation')
        try:
            stack = cloudformation.describe_stacks(StackName=stack_name)
            stack_id = stack['Stacks'][0]['StackId']
            filters = [{'Name': 'tag:aws:cloudformation:stack-id', 'Values': [stack_id]}]
            client = boto3.client('ec2')
            reservations = client.describe_instances(Filters=filters)
            intances = jmespath.search('Reservations[*].Instances', reservations)
            if len(intances) >= 1:
                vpc_id = intances[0][0]['VpcId']
                vpcs = client.describe_vpcs(VpcIds=[vpc_id])
                if 'Vpcs' in vpcs and len(vpcs['Vpcs']) == 1:
                    vpc = vpcs['Vpcs'][0]
                    vpc_id = vpc['VpcId']
        except ClientError as e:
            print 'existing stack not found'

        return vpc_id


def get_elb_subnet_ids(load_balancer_name):
    client = boto3.client('elb')
    response = client.describe_load_balancers(LoadBalancerNames=[load_balancer_name])
    if response['LoadBalancerDescriptions']:
        elb = response['LoadBalancerDescriptions'][0]
    else:
        elb = {}
    subnet_ids = []
    if elb:
        subnet_ids = elb['Subnets']
    return subnet_ids


def get_stack_param_value(stack_name, stack_param_name):
    client = boto3.client('cloudformation')
    response = client.describe_stacks(StackName=stack_name)
    if response['Stacks']:
        stack = response['Stacks'][0]
    else:
        stack = {}
    value = ''
    if stack and 'Parameters' in stack:
        for param in stack['Parameters']:
            if param['ParameterKey'] == stack_param_name:
                value = param['ParameterValue']

    return value


def get_stack_tag_value(service_params, stack_tag_name):
    stack_name = get_stack_name(service_params)
    client = boto3.client('cloudformation')
    response = client.describe_stacks(StackName=stack_name)
    if response['Stacks']:
        stack = response['Stacks'][0]
    else:
        stack = {}
    value = ''
    if stack and 'Tags' in stack:
        for param in stack['Tags']:
            if param['Key'] == stack_tag_name:
                value = param['Value']

    return value


def stop_service_blocking(stack_name, name_search_string):
    ecs_service = get_ecs_service(stack_name, name_search_string)
    if ecs_service and ecs_service['runningCount'] == 1:
        print 'Stopping the %s service ...' % ecs_service['serviceName']
        client = boto3.client('ecs')
        client.update_service(cluster=ecs_service['clusterArn'], service=ecs_service['serviceName'], desiredCount=0)
        timer_start = dt.datetime.now()
        while ecs_service['runningCount'] != 0:
            now = dt.datetime.now()
            elapsed_secs = (now - timer_start).seconds
            sys.stdout.write('\r')
            msg = 'After %s seconds, the service is still running ...' % elapsed_secs
            sys.stdout.write(msg)
            sys.stdout.flush()
            time.sleep(5)
            ecs_service = get_ecs_service(stack_name, name_search_string)

        print ''


def start_service(stack_name, name_search_string):
    ecs_service = get_ecs_service(stack_name, name_search_string)
    if ecs_service and ecs_service['runningCount'] == 0:
        client = boto3.client('ecs')
        client.update_service(cluster=ecs_service['clusterArn'], service=ecs_service['serviceName'], desiredCount=1)


def run_resources_fxn(script_rel_path, service_parameters):
    stack_resources = {}
    script_path = get_localized_script_path(script_rel_path, service_parameters)
    if not script_path or not os.path.exists(script_path):
        print 'resources fxn %s executable does not exist' % script_path
    else:
        module_name = 'yac.lib.customizations'
        script_module = imp.load_source(module_name, script_path)
        stack_resources = script_module.get_resources(service_parameters)
    return stack_resources