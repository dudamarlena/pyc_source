# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/main.py
# Compiled at: 2017-08-01 11:05:34
import argparse, atexit, boto3, cmd, json, os, readline, shlex, subprocess, sys, traceback, yaml, Config
from AwsProcessor import AwsProcessor
from AwsProcessorFactoryImpl import AwsProcessorFactoryImpl
from CommandArgumentParser import CommandArgumentParser
from botocore.exceptions import ClientError
from fnmatch import fnmatch
from pprint import pprint
from stdplus import *
mappedKeys = {'SecretAccessKey': 'AWS_SECRET_ACCESS_KEY', 'SessionToken': 'AWS_SECURITY_TOKEN', 'AccessKeyId': 'AWS_ACCESS_KEY_ID'}
from SilentException import SilentException
from SlashException import SlashException
from AwsAutoScalingGroup import AwsAutoScalingGroup
from AwsStack import AwsStack
from AwsRoot import AwsRoot
histfile = os.path.join(os.path.expanduser('~'), '.nephele', 'history')

def main():
    try:
        argv = sys.argv
        Config.loadConfig()
        parser = CommandArgumentParser(argv[0])
        parser.add_argument('-p', '--profile', dest='profile', default=defaultifyDict(Config.config, 'profile', 'default'), help='select nephele profile')
        parser.add_argument('-m', '--mfa', dest='mfa', help='provide mfa code')
        parser.add_argument('-c', '--continue', dest='continue', action='store_true', default=False, help='continue after executing `command`')
        parser.add_argument(dest='command', nargs=argparse.REMAINDER)
        args = vars(parser.parse_args(argv[1:]))
        command = args['command']
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
        except IOError:
            pass

        atexit.register(readline.write_history_file, histfile)
        atexit.register(AwsProcessor.killBackgroundTasks)
        AwsProcessor.processorFactory = AwsProcessorFactoryImpl()
        awsConfigFilename = os.path.expanduser('~/.aws/config')
        if not os.path.exists(awsConfigFilename):
            print 'ERROR: aws cli has not been configured.'
            pid = fexecvp(['aws', 'configure'])
            os.waitpid(pid, 0)
        command_prompt = AwsRoot()
        command_prompt.onecmd(('profile -v {}').format(args['profile']))
        if None != args['mfa']:
            command_prompt.onecmd(('mfa {}').format(args['mfa']))
        cmdloop = True
        if command:
            command_prompt.onecmd((' ').join(command))
            cmdloop = args['continue']
        else:
            command_prompt.onecmd('stacks --summary')
        if cmdloop:
            command_prompt.cmdloop()
    except SystemExit as e:
        print 'exiting...'
    except SilentException:
        pass

    return


if __name__ == '__main__':
    main()