# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/validate/validate.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2870 bytes
"""
CLI Command for Validating a SAM Template
"""
import os, boto3
from botocore.exceptions import NoCredentialsError
import click
from samcli.cli.main import pass_context, common_options as cli_framework_options, aws_creds_options
from samcli.commands._utils.options import template_option_without_build
from samcli.lib.telemetry.metrics import track_command
from samcli.cli.cli_config_file import configuration_option, TomlProvider

@click.command('validate', short_help='Validate an AWS SAM template.')
@configuration_option(provider=TomlProvider(section='parameters'))
@template_option_without_build
@aws_creds_options
@cli_framework_options
@pass_context
@track_command
def cli(ctx, template_file):
    do_cli(ctx, template_file)


def do_cli(ctx, template):
    """
    Implementation of the ``cli`` method, just separated out for unit testing purposes
    """
    from samtranslator.translator.managed_policy_translator import ManagedPolicyLoader
    from samcli.commands.exceptions import UserException
    from samcli.commands.local.cli_common.user_exceptions import InvalidSamTemplateException
    from lib.exceptions import InvalidSamDocumentException
    from lib.sam_template_validator import SamTemplateValidator
    sam_template = _read_sam_file(template)
    iam_client = boto3.client('iam')
    validator = SamTemplateValidator(sam_template, ManagedPolicyLoader(iam_client))
    try:
        validator.is_valid()
    except InvalidSamDocumentException as e:
        try:
            click.secho(("Template provided at '{}' was invalid SAM Template.".format(template)), bg='red')
            raise InvalidSamTemplateException(str(e))
        finally:
            e = None
            del e

    except NoCredentialsError as e:
        try:
            raise UserException('AWS Credentials are required. Please configure your credentials.',
              wrapped_from=(e.__class__.__name__))
        finally:
            e = None
            del e

    click.secho(('{} is a valid SAM Template'.format(template)), fg='green')


def _read_sam_file(template):
    """
        Reads the file (json and yaml supported) provided and returns the dictionary representation of the file.

        :param str template: Path to the template file
        :return dict: Dictionary representing the SAM Template
        :raises: SamTemplateNotFoundException when the template file does not exist
    """
    from samcli.commands.local.cli_common.user_exceptions import SamTemplateNotFoundException
    from samcli.yamlhelper import yaml_parse
    if not os.path.exists(template):
        click.secho('SAM Template Not Found', bg='red')
        raise SamTemplateNotFoundException('Template at {} is not found'.format(template))
    with click.open_file(template, 'r', encoding='utf-8') as (sam_template):
        sam_template = yaml_parse(sam_template.read())
    return sam_template