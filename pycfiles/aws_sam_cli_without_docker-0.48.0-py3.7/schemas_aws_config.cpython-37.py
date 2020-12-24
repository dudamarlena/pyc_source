# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/schemas/schemas_aws_config.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3420 bytes
""" configure Schemas client based on AWS configuration provided by user """
import os, click
from boto3 import Session
from samcli.commands.local.cli_common.user_exceptions import NotAvailableInRegion
from samcli.commands.local.cli_common.user_exceptions import ResourceNotFound

def get_aws_configuration_choice():
    """
    Allow user to select their AWS Connection configuration (profile/region)
    :return: AWS profile and region dictionary
    """
    session = Session()
    profile = session.profile_name
    region = session.region_name
    message = '\nDo you want to use the default AWS profile [%s] and region [%s]?' % (profile, region)
    choice = click.confirm(message, default=True)
    schemas_available_regions_name = [
     'us-east-1', 'us-east-2', 'us-west-2', 'eu-west-1', 'ap-northeast-1']
    if choice:
        if region not in schemas_available_regions_name:
            raise NotAvailableInRegion('EventBridge Schemas are not yet available in %s. Please select one of %s' % (
             region, schemas_available_regions_name))
    elif not choice:
        available_profiles = session.available_profiles
        profile = _get_aws_profile_choice(available_profiles)
        region = _get_aws_region_choice(schemas_available_regions_name)
    else:
        profile = None
    return {'profile':profile,  'region':region}


def _get_aws_profile_choice(available_profiles):
    if not available_profiles:
        raise ResourceNotFound('No configured AWS profile found.')
    profile_choices = list(map(str, range(1, len(available_profiles) + 1)))
    profile_choice_num = 1
    click.echo('\nWhich AWS profile do you want to use?')
    for profile in available_profiles:
        msg = str(profile_choice_num) + ' - ' + profile
        click.echo('\t' + msg)
        profile_choice_num = profile_choice_num + 1

    profile_choice = click.prompt('Profile', type=(click.Choice(profile_choices)), show_choices=False)
    return available_profiles[(int(profile_choice) - 1)]


def _get_aws_region_choice(available_regions_name):
    if not available_regions_name:
        raise ResourceNotFound('No AWS region found for AWS schemas service. This should not be possible, please raise an issue.')
    region_choices = list(map(str, range(1, len(available_regions_name) + 1)))
    region_choice_num = 1
    click.echo('\nWhich region do you want to use for your schema registry?')
    for available_region in available_regions_name:
        msg = str(region_choice_num) + ' - ' + available_region
        click.echo('\t' + msg)
        region_choice_num = region_choice_num + 1

    region_choice = click.prompt('Region', type=(click.Choice(region_choices)), show_choices=False)
    return available_regions_name[(int(region_choice) - 1)]


def get_schemas_client(profile, region):
    if profile:
        session = Session(profile_name=profile)
    else:
        session = Session()
    return session.client('schemas', region_name=region)