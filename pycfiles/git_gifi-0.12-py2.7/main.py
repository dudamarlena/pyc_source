# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gifi/main.py
# Compiled at: 2017-06-13 11:17:47
import sys, logging
from utils import git_utils
from command import Command, AggregatedCommand, UnknownCommandException, CommandException
import epic, feature, pkg_resources, queue, git_hub, slack
logging.basicConfig(filename='/tmp/gifi.log', level=logging.DEBUG)
command = AggregatedCommand('gifi', 'Git and github enhancements to git.', [
 epic.command,
 feature.command,
 queue.command,
 git_hub.command,
 slack.command,
 Command('version', 'Show version number.', lambda : pkg_resources.require('git-gifi')[0].version)])

class HelpGenerator(object):

    def __init__(self, main):
        self.main = main

    def __call__(self):
        help = str(self.main)
        help += '\nUsage:\n\t%s command [command arguments]\n\nCommands:\n' % self.main.name
        for command in self.main.nested_commands():
            help += str(command)
            if len(command.nested_commands()) != 0:
                help += ' See below subcommands:\n'
                for subcommand in command.nested_commands():
                    help += '\t%s\n' % str(subcommand)

            else:
                help += '\n'

        return help


command.add_command(Command('help', 'Display this window.', HelpGenerator(command)))

class AliasesInstaller(object):

    def __init__(self, main):
        self.main = main

    def __call__(self, config_level='global'):
        repo = git_utils.get_repo()
        config_writer = repo.config_writer(config_level)
        for command in self.main.nested_commands():
            if len(command.nested_commands()) != 0:
                for subcommand in command.nested_commands():
                    alias = '%s-%s' % (command.name, subcommand.name)
                    value = '"!%s %s %s"' % (sys.argv[0], command.name, subcommand.name)
                    config_writer.set_value('alias', alias, value)

        config_writer.release()


command.add_command(Command('install', 'Install gifi as a bunch of git aliases.', AliasesInstaller(command)))

def main():
    args = list(sys.argv)
    args.pop(0)
    _main(args)


def _main(args):
    if len(args) == 0:
        args.append('help')
    try:
        result = command(*args)
        if result is not None:
            print result
    except UnknownCommandException:
        print "Wrong command, try 'help'."
    except CommandException as e:
        print 'ERROR: %s' % e

    return