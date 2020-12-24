# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/cli/context.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 6657 bytes
"""
Context information passed to each CLI command
"""
import logging, uuid, boto3, botocore, botocore.session
from botocore import credentials
import click
from samcli.commands.exceptions import CredentialsError

class Context:
    __doc__ = "\n    Top level context object for the CLI. Exposes common functionality required by a CLI, including logging,\n    environment config parsing, debug logging etc.\n\n    This object is passed by Click to every command that adds the proper annotation.\n    Read this for more details on Click Context - http://click.pocoo.org/5/commands/#nested-handling-and-contexts\n    Each command gets its own context object, but linked to both parent and child command's context, like a Linked List.\n\n    This class itself does not rely on how Click works. It is just a plain old Python class that holds common\n    properties used by every CLI command.\n    "

    def __init__(self):
        """
        Initialize the context with default values
        """
        self._debug = False
        self._aws_region = None
        self._aws_profile = None
        self._session_id = str(uuid.uuid4())

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        """
        Turn on debug logging if necessary.

        :param value: Value of debug flag
        """
        self._debug = value
        if self._debug:
            logging.getLogger('samcli').setLevel(logging.DEBUG)
            logging.getLogger('aws_lambda_builders').setLevel(logging.DEBUG)

    @property
    def region(self):
        return self._aws_region

    @region.setter
    def region(self, value):
        """
        Set AWS region
        """
        self._aws_region = value
        self._refresh_session()

    @property
    def profile(self):
        return self._aws_profile

    @profile.setter
    def profile(self, value):
        """
        Set AWS profile for credential resolution
        """
        self._aws_profile = value
        self._refresh_session()

    @property
    def session_id(self):
        """
        Returns the ID of this command session. This is a randomly generated UUIDv4 which will not change until the
        command terminates.
        """
        return self._session_id

    @property
    def command_path(self):
        """
        Returns the full path of the command as invoked ex: "sam local generate-event s3 put". Wrapper to
        https://click.palletsprojects.com/en/7.x/api/#click.Context.command_path

        Returns
        -------
        str
            Full path of the command invoked
        """
        click_core_ctx = click.get_current_context()
        if click_core_ctx:
            return click_core_ctx.command_path

    @staticmethod
    def get_current_context():
        """
        Get the current Context object from Click's context stacks. This method is safe to run within the
        actual command's handler that has a ``@pass_context`` annotation. Outside of the handler, you run
        the risk of creating a new Context object which is entirely different from the Context object used by your
        command.
         .. code:
            @pass_context
            def my_command_handler(ctx):
                 # You will get the right context from within the command handler. This will also work from any
                # downstream method invoked as part of the handler.
                 this_context = Context.get_current_context()
                assert ctx == this_context
         Returns
        -------
        samcli.cli.context.Context
            Instance of this object, if we are running in a Click command. None otherwise.
        """
        click_core_ctx = click.get_current_context()
        if click_core_ctx:
            return click_core_ctx.find_object(Context) or click_core_ctx.ensure_object(Context)

    def _refresh_session(self):
        """
        Update boto3's default session by creating a new session based on values set in the context. Some properties of
        the Boto3's session object are read-only. Therefore when Click parses new AWS session related properties (like
        region & profile), it will call this method to create a new session with latest values for these properties.
        """
        try:
            botocore_session = botocore.session.get_session()
            boto3.setup_default_session(botocore_session=botocore_session,
              region_name=(self._aws_region),
              profile_name=(self._aws_profile))
            botocore_session.get_component('credential_provider').get_provider('assume-role').cache = credentials.JSONFileCache()
        except botocore.exceptions.ProfileNotFound as ex:
            try:
                raise CredentialsError(str(ex))
            finally:
                ex = None
                del ex


def get_cmd_names(cmd_name, ctx):
    """
    Given the click core context, return a list representing all the subcommands passed to the CLI

    Parameters
    ----------
    cmd_name : name of current command

    ctx : click.Context

    Returns
    -------
    list(str)
        List containing subcommand names. Ex: ["local", "start-api"]

    """
    if not ctx:
        return []
    if ctx:
        if not getattr(ctx, 'parent', None):
            return [
             ctx.info_name]
    _parent = ctx.parent
    _cmd_names = []
    if cmd_name != ctx.info_name:
        _cmd_names = [
         cmd_name]
    _cmd_names.append(ctx.info_name)
    while _parent.parent:
        info_name = _parent.info_name
        _cmd_names.append(info_name)
        _parent = _parent.parent

    _cmd_names.reverse()
    return _cmd_names