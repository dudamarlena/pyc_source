# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hyperlambda/main.py
# Compiled at: 2018-02-21 02:09:56
from __future__ import division, print_function, unicode_literals
import argparse, os
from shutil import copyfileobj
import sys
from tempfile import NamedTemporaryFile
import ConfigParser, json
from . import exceptions
import logging, traceback, time, base64

class StoreNameValuePair(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        parsed_conf = {}
        for pair in values[0].split(b','):
            key, value = pair.split(b'=')
            parsed_conf[key] = value

        setattr(namespace, b'tags', parsed_conf)


class ValidateNameValuePair(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        parsed_conf = None
        if b'Variables' in values and isinstance(values[b'Variables'], dict):
            parsed_conf = values
        else:
            parser.error(b'invalid environment arguments')
        setattr(namespace, b'environment', parsed_conf)
        return


class ValidateListValues(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        parsed_conf = None
        if values != None and isinstance(values, list):
            parsed_conf = values
        else:
            parser.error(b'invalid security_group_ids input type. argument should be a list')
        setattr(namespace, b'security_group_ids', parsed_conf)
        return


class ReadDataFromFile(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        parsed_conf = b''
        if values != None and os.path.isfile(values):
            with open(values) as (file):
                parsed_conf = file.read().strip()
        setattr(namespace, b'userdata', parsed_conf)
        return


def parse_args(args):
    """Parses command-line `args`"""
    from . import settings
    parser = argparse.ArgumentParser(description=b'Create  a Hyper Lambda Instance to Execute Script')
    parser.add_argument(b'-v', b'--verbose', action=b'count', default=1, help=b'explain what is being done')
    group = parser.add_argument_group(title=b' metadata arguments')
    group.add_argument(b'--function-name', default=None, required=True, help=b'Human-readable name of the function. ')
    group.add_argument(b'--description', default=b'', help=b'Description of the function. Defaults to ""')
    group.add_argument(b'--version', default=b'1.0.0', help=b'Version of the metadata. Defaults to "1.0.0"')
    group = parser.add_argument_group(title=b' warp arguments')
    group.add_argument(b'--runtime', default=b'python2.7', help=b'The runtime environment for the Lambda function you are uploading. Defaults to python2.7')
    group.add_argument(b'--role', type=str, help=b'The Amazon Resource Name (ARN) of the IAM role that Lambda assumes when it executes your function to access any other Amazon Web Services (AWS) resources ')
    group.add_argument(b'--timeout', type=int, default=180, help=b'The function execution time at which Lambda should terminate the function. The Default is 180 seconds ')
    group.add_argument(b'--handler', required=True, help=b'The function within your code that Lambda calls to begin execution. ')
    group.add_argument(b'--code', help=b'The code for the Lambda function. ')
    group.add_argument(b'--zip-file', help=b'The URL to the zip file of the code you are uploaded ')
    group.add_argument(b'--data', type=json.loads, help=b'A dictionary that you want to provide to your Lambda function as input.')
    group.add_argument(b'--environment', type=json.loads, default=None, action=ValidateNameValuePair, help=b"The parent object that contains your environment's configuration settings. ")
    group.add_argument(b'--userdata', default=b'', action=ReadDataFromFile, help=b'The location of the userdata file for the instance. eg: userdata.txt ')
    group.add_argument(b'--tags', nargs=b'*', action=StoreNameValuePair, help=b'The list of tags (key-value pairs) assigned to the new function.')
    group = parser.add_argument_group(title=b' instance arguments')
    group.add_argument(b'--instance-type', type=str, default=settings.instance_type, help=b'The type of the instance to be created')
    group.add_argument(b'--key-name', type=str, default=settings.key_name, help=b'The name of the key pair')
    group.add_argument(b'--security-group-ids', action=ValidateListValues, default=settings.security_group_ids, help=b'One or more security group ids')
    group.add_argument(b'--callback-url', type=str, help=b'Optional URL to be called after execution.')
    args = parser.parse_args(args=args)
    if args.zip_file is None and args.code is None:
        parser.error(b'must provide --zip-file or --code')
    return args


class HyperLambda(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description=b'Create  a Hyper Lambda Instance to Execute Script', usage=b'hyperlambda <command> [<args>]\n            The most commonly used hyperlambda commands are:\n            configure     Configure the settings\n            invoke_function      create and execute lambda function\n            ')
        parser.add_argument(b'command', help=b'Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print(b'Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def configure(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        VALUES_TO_PROMPT_CREDENTIAL = [
         ('aws_access_key_id', 'AWS Access Key ID'),
         ('aws_secret_access_key', 'AWS Secret Access Key'),
         ('region', 'Default region name')]
        VALUES_TO_PROMPT_INSTANCE = [
         ('security_group_ids', 'Security Group Ids<list>'),
         ('key_name', 'key Name'),
         ('volume_size', 'Volume Size(GiB)'),
         ('instance_type', 'Instance Type'),
         ('spot_price', 'Spot Price')]
        configfile_name = b'config.ini'
        if not os.path.isfile(os.path.join(BASE_DIR, b'data', configfile_name)):
            cfgfile = open(os.path.join(BASE_DIR, b'data', configfile_name), b'w')
            Config = ConfigParser.ConfigParser()
            Config.add_section(b'aws_credentials')
            for itm in VALUES_TO_PROMPT_CREDENTIAL:
                Config.set(b'aws_credentials', itm[0], raw_input(itm[1] + b': '))

            Config.add_section(b'instance_settings')
            for itm in VALUES_TO_PROMPT_INSTANCE:
                Config.set(b'instance_settings', itm[0], raw_input(itm[1] + b': '))

            Config.write(cfgfile)
            cfgfile.close()

    def invoke_function(self, use_logging=True):
        args = parse_args(sys.argv[2:])
        if use_logging:
            configure_logging(args)
        from .helper import warp_lambda
        lambda_object = warp_lambda(**vars(args))
        try:
            created = lambda_object.create_instance()
            if created:
                time.sleep(60)
                exec_status = lambda_object.execute_lambda()
            else:
                raise exceptions.NoInstanceCreated(message=lambda_object.message)
            lambda_object.thread_terminate_timeout_instance.cancel()
            return exec_status
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 1


def configure_logging(args):
    if not args.verbose:
        return
    if args.verbose == 1:
        level = logging.INFO
        fmt = b'[%(asctime)s] [%(levelname)s] : %(message)s'
    else:
        level = logging.DEBUG
        fmt = b'[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)s] : %(message)s'
    logging.basicConfig(level=level, format=fmt, datefmt=b'%Y-%m-%d %H:%M:%S')


if __name__ == b'__main__' and __package__ is None:
    HyperLambda()