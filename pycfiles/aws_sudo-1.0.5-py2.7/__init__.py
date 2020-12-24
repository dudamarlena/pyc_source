# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/aws_sudo/__init__.py
# Compiled at: 2017-08-31 11:29:41
from __future__ import print_function
import argparse, boto3, botocore, os, sys, aws_sudo.CommandParser
from six.moves import configparser

def sudo(cmd_args):
    profile_config = read_config(cmd_args.profile)
    credentials = {}
    profile_config['session_timeout'] = cmd_args.session_timeout
    profile_config['mfa_code'] = cmd_args.mfa_code
    credentials = get_credentials(profile_config)
    if cmd_args.mode is 'in_place':
        update_credentials(cmd_args.profile, credentials)
    elif cmd_args.mode is 'export':
        print_exports(credentials)
    elif cmd_args.mode is 'proxy':
        proxy_command(cmd_args.command, cmd_args.command_args, credentials)


def read_config(profile):
    """This reads our config files automatically, and combines config and
    credentials files for us"""
    profiles = botocore.session.get_session().full_config.get('profiles', {})
    if profile not in profiles:
        print("Profile '%s' does not exist in the config file." % profile)
        quit(2)
    profiles[profile]['profile_name'] = profile
    return profiles[profile]


def print_exports(credentials):
    print('export', end=' ')
    print('AWS_ACCESS_KEY_ID=' + credentials['AccessKeyId'], end=' ')
    print('AWS_SECRET_ACCESS_KEY=' + credentials['SecretAccessKey'], end=' ')
    print('AWS_SESSION_TOKEN=' + credentials['SessionToken'], end=' ')
    print('AWS_SECURITY_TOKEN=' + credentials['SessionToken'], end='')


def update_credentials(profile, credentials):
    credentials_file = os.path.expanduser('~/.aws/credentials')
    config = configparser.ConfigParser()
    config.read(credentials_file)
    if not config.has_section(profile):
        config.add_section(profile)
    config.set(profile, 'aws_access_key_id', credentials['AccessKeyId'])
    config.set(profile, 'aws_secret_access_key', credentials['SecretAccessKey'])
    config.set(profile, 'aws_session_token', credentials['SessionToken'])
    config.set(profile, 'aws_security_token', credentials['SessionToken'])
    with open(credentials_file, 'w') as (credentials_file):
        config.write(credentials_file)
    print('# Aws credentials file got updated with temporary access for profile %s' % profile)


def proxy_command(command, command_args, credentials):
    os.unsetenv('AWS_DEFAULT_PROFILE')
    os.unsetenv('AWS_PROFILE')
    os.unsetenv('AWS_ACCESS_KEY_ID')
    os.unsetenv('AWS_SECRET_ACCESS_KEY')
    os.unsetenv('AWS_SESSION_TOKEN')
    os.unsetenv('AWS_SECURITY_TOKEN')
    os.putenv('AWS_ACCESS_KEY_ID', credentials['AccessKeyId'])
    os.putenv('AWS_SECRET_ACCESS_KEY', credentials['SecretAccessKey'])
    os.putenv('AWS_SESSION_TOKEN', credentials['SessionToken'])
    os.putenv('AWS_SECURITY_TOKEN', credentials['SessionToken'])
    command_status = os.system(command + ' ' + (' ').join(command_args))
    exit(os.WEXITSTATUS(command_status))


def get_credentials(profile_config):
    if 'role_arn' in profile_config:
        session = get_session(profile_config)
        return assume_role(session, profile_config)
    else:
        if 'mfa_serial' in profile_config:
            session = get_session(profile_config)
            return login_with_mfa(session, profile_config)
        if 'source_profile' in profile_config or 'aws_access_key_id' not in profile_config:
            session = get_session(profile_config)
            credentials = session.get_credentials().get_frozen_credentials()
            return {'AccessKeyId': credentials.access_key, 
               'SecretAccessKey': credentials.secret_key, 
               'SessionToken': str(credentials.token)}
        return {'AccessKeyId': profile_config['aws_access_key_id'], 
           'SecretAccessKey': profile_config['aws_secret_access_key'], 
           'SessionToken': ''}


def get_session(profile_config):
    session_profile = profile_config['profile_name']
    if 'source_profile' in profile_config:
        session_profile = profile_config['source_profile']
    if 'region' in profile_config:
        os.putenv('AWS_DEFAULT_REGION', profile_config['region'])
        os.putenv('AWS_REGION', profile_config['region'])
    session = boto3.Session(profile_name=session_profile)
    return session


def login_with_mfa(session, profile_config):
    sts_client = session.client('sts')
    credentials = sts_client.get_session_token(DurationSeconds=profile_config['session_timeout'], SerialNumber=profile_config['mfa_serial'], TokenCode=profile_config['mfa_code'])
    return credentials['Credentials']


def assume_role(session, profile_config):
    role_arn = profile_config['role_arn']
    sts_client = session.client('sts')
    if 'mfa_serial' in profile_config:
        if profile_config['mfa_code'] is None:
            profile_config['mfa_code'] = raw_input('Enter MFA token: ')
        assumedRoleObject = sts_client.assume_role(RoleArn=role_arn, RoleSessionName='AssumeRoleSession', DurationSeconds=profile_config['session_timeout'], SerialNumber=profile_config['mfa_serial'], TokenCode=profile_config['mfa_code'])
    else:
        assumedRoleObject = sts_client.assume_role(RoleArn=role_arn, RoleSessionName='AssumeRoleSession', DurationSeconds=profile_config['session_timeout'])
    return assumedRoleObject['Credentials']


def main():
    sudo(CommandParser.CommandParser().get_arguments())