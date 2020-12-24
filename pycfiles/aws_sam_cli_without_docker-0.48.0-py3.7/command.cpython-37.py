# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/publish/command.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 5498 bytes
"""CLI command for "publish" command."""
import json, logging, click, boto3
from serverlessrepo.publish import CREATE_APPLICATION
from samcli.cli.main import pass_context, common_options as cli_framework_options, aws_creds_options
from samcli.commands._utils.options import template_common_option
from samcli.commands._utils.template import get_template_data, TemplateFailedParsingException, TemplateNotFoundException
from samcli.lib.telemetry.metrics import track_command
from samcli.cli.cli_config_file import configuration_option, TomlProvider
LOG = logging.getLogger(__name__)
SAM_PUBLISH_DOC = 'https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-template-publishing-applications.html'
SAM_PACKAGE_DOC = 'https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-package.html'
HELP_TEXT = "\nUse this command to publish a packaged AWS SAM template to\nthe AWS Serverless Application Repository to share within your team,\nacross your organization, or with the community at large.\n\n\x08\nThis command expects the template's Metadata section to contain an\nAWS::ServerlessRepo::Application section with application metadata\nfor publishing. For more details on this metadata section, see\n{}\n\x08\nExamples\n--------\nTo publish an application\n$ sam publish -t packaged.yaml --region <region>\n".format(SAM_PUBLISH_DOC)
SHORT_HELP = 'Publish a packaged AWS SAM template to the AWS Serverless Application Repository.'
SERVERLESSREPO_CONSOLE_URL = 'https://console.aws.amazon.com/serverlessrepo/home?region={}#/published-applications/{}'
SEMANTIC_VERSION_HELP = 'Optional. The value provided here overrides SemanticVersion in the template metadata.'
SEMANTIC_VERSION = 'SemanticVersion'

@click.command('publish', help=HELP_TEXT, short_help=SHORT_HELP)
@configuration_option(provider=TomlProvider(section='parameters'))
@template_common_option
@click.option('--semantic-version', help=SEMANTIC_VERSION_HELP)
@aws_creds_options
@cli_framework_options
@pass_context
@track_command
def cli(ctx, template_file, semantic_version):
    do_cli(ctx, template_file, semantic_version)


def do_cli(ctx, template, semantic_version):
    """Publish the application based on command line inputs."""
    from serverlessrepo import publish_application
    from serverlessrepo.parser import METADATA, SERVERLESS_REPO_APPLICATION
    from serverlessrepo.exceptions import ServerlessRepoError, InvalidS3UriError
    from samcli.commands.exceptions import UserException
    try:
        template_data = get_template_data(template)
    except (TemplateFailedParsingException, TemplateNotFoundException) as ex:
        try:
            click.secho('Publish Failed', fg='red')
            raise ex
        finally:
            ex = None
            del ex

    if semantic_version:
        if SERVERLESS_REPO_APPLICATION in template_data.get(METADATA, {}):
            template_data.get(METADATA).get(SERVERLESS_REPO_APPLICATION)[SEMANTIC_VERSION] = semantic_version
    try:
        publish_output = publish_application(template_data)
        click.secho('Publish Succeeded', fg='green')
        click.secho(_gen_success_message(publish_output))
    except InvalidS3UriError as ex:
        try:
            click.secho('Publish Failed', fg='red')
            raise UserException(('Your SAM template contains invalid S3 URIs. Please make sure that you have uploaded application artifacts to S3 by packaging the template. See more details in {}'.format(SAM_PACKAGE_DOC)),
              wrapped_from=(ex.__class__.__name__))
        finally:
            ex = None
            del ex

    except ServerlessRepoError as ex:
        try:
            click.secho('Publish Failed', fg='red')
            LOG.debug('Failed to publish application to serverlessrepo', exc_info=True)
            error_msg = '{}\nPlease follow the instructions in {}'.format(str(ex), SAM_PUBLISH_DOC)
            raise UserException(error_msg, wrapped_from=(ex.__class__.__name__))
        finally:
            ex = None
            del ex

    application_id = publish_output.get('application_id')
    _print_console_link(ctx.region, application_id)


def _gen_success_message(publish_output):
    """
    Generate detailed success message for published applications.

    Parameters
    ----------
    publish_output : dict
        Output from serverlessrepo publish_application

    Returns
    -------
    str
        Detailed success message
    """
    application_id = publish_output.get('application_id')
    details = json.dumps((publish_output.get('details')), indent=2)
    if CREATE_APPLICATION in publish_output.get('actions'):
        return 'Created new application with the following metadata:\n{}'.format(details)
    return 'The following metadata of application "{}" has been updated:\n{}'.format(application_id, details)


def _print_console_link(region, application_id):
    """
    Print link for the application in AWS Serverless Application Repository console.

    Parameters
    ----------
    region : str
        AWS region name
    application_id : str
        The Amazon Resource Name (ARN) of the application

    """
    if not region:
        region = boto3.Session().region_name
    console_link = SERVERLESSREPO_CONSOLE_URL.format(region, application_id.replace('/', '~'))
    msg = 'Click the link below to view your application in AWS console:\n{}'.format(console_link)
    click.secho(msg, fg='yellow')