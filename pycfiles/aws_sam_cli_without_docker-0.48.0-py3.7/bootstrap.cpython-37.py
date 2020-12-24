# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/bootstrap/bootstrap.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 6226 bytes
"""
Bootstrap's user's development environment by creating cloud resources required by SAM CLI
"""
import json, logging, boto3, click
from botocore.config import Config
from botocore.exceptions import ClientError, BotoCoreError, NoRegionError, NoCredentialsError
from samcli.commands.bootstrap.exceptions import ManagedStackError
from samcli import __version__
from samcli.cli.global_config import GlobalConfig
from samcli.commands.exceptions import UserException, CredentialsError, RegionError
SAM_CLI_STACK_NAME = 'aws-sam-cli-managed-default'
LOG = logging.getLogger(__name__)

def manage_stack(profile, region):
    try:
        cloudformation_client = boto3.client('cloudformation', config=Config(region_name=(region if region else None)))
    except NoCredentialsError:
        raise CredentialsError('Error Setting Up Managed Stack Client: Unable to resolve credentials for the AWS SDK for Python client. Please see their documentation for options to pass in credentials: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html')
    except NoRegionError:
        raise RegionError('Error Setting Up Managed Stack Client: Unable to resolve a region. Please provide a region via the --region parameter or by the AWS_REGION environment variable.')

    return _create_or_get_stack(cloudformation_client)


def _create_or_get_stack(cloudformation_client):
    try:
        stack = None
        try:
            ds_resp = cloudformation_client.describe_stacks(StackName=SAM_CLI_STACK_NAME)
            stacks = ds_resp['Stacks']
            stack = stacks[0]
            click.echo('\n\tLooking for resources needed for deployment: Found!')
        except ClientError:
            click.echo('\n\tLooking for resources needed for deployment: Not found.')
            stack = _create_stack(cloudformation_client)

        tags = stack['Tags']
        try:
            sam_cli_tag = next((t for t in tags if t['Key'] == 'ManagedStackSource'))
            if not sam_cli_tag['Value'] == 'AwsSamCli':
                msg = 'Stack ' + SAM_CLI_STACK_NAME + ' ManagedStackSource tag shows ' + sam_cli_tag['Value'] + ' which does not match the AWS SAM CLI generated tag value of AwsSamCli. Failing as the stack was likely not created by the AWS SAM CLI.'
                raise UserException(msg)
        except StopIteration:
            msg = 'Stack  ' + SAM_CLI_STACK_NAME + ' exists, but the ManagedStackSource tag is missing. Failing as the stack was likely not created by the AWS SAM CLI.'
            raise UserException(msg)

        outputs = stack['Outputs']
        try:
            bucket_name = next((o for o in outputs if o['OutputKey'] == 'SourceBucket'))['OutputValue']
        except StopIteration:
            msg = 'Stack ' + SAM_CLI_STACK_NAME + ' exists, but is missing the managed source bucket key. Failing as this stack was likely not created by the AWS SAM CLI.'
            raise UserException(msg)

        return bucket_name
    except (ClientError, BotoCoreError) as ex:
        try:
            LOG.debug('Failed to create managed resources', exc_info=ex)
            raise ManagedStackError(str(ex))
        finally:
            ex = None
            del ex


def _create_stack(cloudformation_client):
    click.echo('\tCreating the required resources...')
    change_set_name = 'InitialCreation'
    change_set_resp = cloudformation_client.create_change_set(StackName=SAM_CLI_STACK_NAME,
      TemplateBody=(_get_stack_template()),
      Tags=[
     {'Key':'ManagedStackSource', 
      'Value':'AwsSamCli'}],
      ChangeSetType='CREATE',
      ChangeSetName=change_set_name)
    stack_id = change_set_resp['StackId']
    change_waiter = cloudformation_client.get_waiter('change_set_create_complete')
    change_waiter.wait(ChangeSetName=change_set_name,
      StackName=SAM_CLI_STACK_NAME,
      WaiterConfig={'Delay':15,  'MaxAttempts':60})
    cloudformation_client.execute_change_set(ChangeSetName=change_set_name, StackName=SAM_CLI_STACK_NAME)
    stack_waiter = cloudformation_client.get_waiter('stack_create_complete')
    stack_waiter.wait(StackName=stack_id, WaiterConfig={'Delay':15,  'MaxAttempts':60})
    ds_resp = cloudformation_client.describe_stacks(StackName=SAM_CLI_STACK_NAME)
    stacks = ds_resp['Stacks']
    click.echo('\tSuccessfully created!')
    return stacks[0]


def _get_stack_template():
    gc = GlobalConfig()
    info = {'version':__version__,  'installationId':gc.installation_id if gc.installation_id else 'unknown'}
    template = '\n    AWSTemplateFormatVersion : \'2010-09-09\'\n    Transform: AWS::Serverless-2016-10-31\n    Description: Managed Stack for AWS SAM CLI\n\n    Metadata:\n        SamCliInfo: {info}\n\n    Resources:\n      SamCliSourceBucket:\n        Type: AWS::S3::Bucket\n        Properties:\n          VersioningConfiguration:\n            Status: Enabled\n          Tags:\n            - Key: ManagedStackSource\n              Value: AwsSamCli\n\n      SamCliSourceBucketBucketPolicy:\n        Type: AWS::S3::BucketPolicy\n        Properties:\n          Bucket: !Ref SamCliSourceBucket\n          PolicyDocument:\n            Statement:\n              -\n                Action:\n                  - "s3:GetObject"\n                Effect: "Allow"\n                Resource:\n                  Fn::Join:\n                    - ""\n                    -\n                      - "arn:"\n                      - !Ref AWS::Partition\n                      - ":s3:::"\n                      - !Ref SamCliSourceBucket\n                      - "/*"\n                Principal:\n                  Service: serverlessrepo.amazonaws.com\n\n    Outputs:\n      SourceBucket:\n        Value: !Ref SamCliSourceBucket\n    '
    return template.format(info=(json.dumps(info)))