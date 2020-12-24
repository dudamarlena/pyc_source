# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/procblock/mainfunctions.py
# Compiled at: 2010-10-14 21:59:54
"""
mainfunctions

main() related functions for procblock
"""
import sys, os, getopt, time, logging, processing, daemon as daemonize, procyaml
from unidist.log import log
from unidist import sharedlock
from unidist import sharedstate

class OptionsAndArgsFailure(Exception):
    """A problem in the options and args."""
    pass


def Usage_GetArgNames(usage):
    args = []
    if 'args' in usage:
        for arg in usage['args']:
            name = arg['name']
            required = arg.get('required', False)
            remaining = arg.get('remaining', False)
            if remaining:
                name = '[%s1 %s2 ...]' % (name, name)
            elif 'default' in arg and not required:
                name = '[%s]' % name
            args.append(name)

    return args


def GetProgramName():
    return os.path.basename(sys.argv[0])


def PrintUsage(block, error=None):
    """Print out any __usage information in this block.
  
  Returns: string or None, string if __usage information found
  """
    if '__usage' not in block:
        return
    else:
        usage = block['__usage']
        output = ''
        if 'name' in usage:
            output += 'Name: %s\n' % usage['name']
        if 'author' in usage:
            output += 'Author: %s\n' % usage['author']
        if 'website' in usage:
            output += 'Website: %s\n' % usage['website']
        if output:
            output += '\n'
        program_name = GetProgramName()
        args = Usage_GetArgNames(usage)
        if error:
            output += '  error: %s\n\n' % error
        output += 'usage: %s <options> %s\n\n' % (GetProgramName(), (' ').join(args))
        if args:
            output += 'Args:\n'
            for arg in usage['args']:
                name = arg['name']
                info = arg.get('info', '*NO INFO*')
                required = arg.get('required', False)
                default = arg.get('default', None)
                remaining = arg.get('remaining', False)
                text = ''
                if default:
                    text += 'Default=%s ' % default
                if required:
                    text += 'Required '
                if remaining:
                    text += '<Takes 0 or more args> '
                if text:
                    text = '   (%s)' % text.strip()
                output += '  %-30s %-40s%s\n' % (name, info, text)

            output += '\n'
        if 'options' in usage:
            output += 'Options:\n'
            for name in usage['options']:
                arg = usage['options'][name]
                info = arg.get('info', '*NO INFO*')
                type = arg.get('type', 'flag')
                default = arg.get('default', None)
                letter = arg.get('letter', None)
                text = ''
                if default:
                    text += 'Default=%s ' % default
                if type != 'flag':
                    name_arg = '--%s <value>' % name
                else:
                    name_arg = '--%s' % name
                    text += '<Flag> '
                if letter:
                    name_arg = '-%s, %s' % (letter, name_arg)
                if text:
                    text = '   (%s)' % text.strip()
                output += '  %-30s %-40s%s\n' % (name_arg, info, text)

        return output


def PrintStartup(usage):
    output = ''
    if not usage:
        return 'No usage.'
    if 'name' in usage:
        output += 'Name: %s\n' % usage['name']
    if 'author' in usage:
        output += 'Author: %s\n' % usage['author']
    if 'info' in usage:
        output += 'Info: %s\n' % usage['info']
    if 'website' in usage:
        output += 'Website: %s\n' % usage['website']
    return output


def ProcessOptionsAndArgs_NoUsageBlock(block, starting_arg=2):
    """Returns a dictionary with all options and args processed.
  
  All options are put into their own keywords.  All args are put into _args.
  """
    data = {'args': []}
    args = sys.argv[starting_arg:]
    initial_options = True
    option_name = None
    for arg in args:
        if initial_options:
            if option_name == None:
                if arg.startswith('--'):
                    option_name = arg[2:]
                elif arg.startswith('-'):
                    option_name = arg[1:]
                else:
                    initial_options = False
            else:
                data[option_name] = arg
                option_name = None
        if not initial_options:
            data['args'].append(arg)

    if option_name != None:
        raise Exception('Option missing value: %s' % option_name)
    return data


def ProcessOptionsAndArgs(block, starting_arg=2):
    """Returns a dictionary with all options and args processed.
  
  NOTE(g): starting_arg=2, and not 1, because procblock will typically
      be given a procblock YAML file to process first, then options and args
      will be extracted.  Change if required.
  """
    data = {}
    if '__usage' not in block:
        log('No __usage block')
        return ProcessOptionsAndArgs_NoUsageBlock(block, starting_arg=starting_arg)
    else:
        usage = block['__usage']
        args = []
        if 'args' in usage:
            for count in range(0, len(usage['args'])):
                args.append(usage['args'][count])

        options = {}
        if 'options' in usage:
            for key in usage['options']:
                options[key] = usage['options'][key]

        getopt_options = ['help']
        getopt_short = 'h'
        for (name, option) in options.items():
            default = option.get('default', None)
            if option.get('type', 'flag') != 'flag':
                name = '%s=' % name
            getopt_options.append(name)
            if 'letter' in option:
                if option.get('type', 'flag') != 'flag':
                    getopt_short += '%s:' % option['letter']
                else:
                    getopt_short += '%s' % option['letter']

        args = sys.argv[starting_arg:]
        (post_options, post_args) = getopt.getopt(args, getopt_short, getopt_options)
        if 'options' in usage:
            for (key, option) in usage['options'].items():
                letter = option.get('letter', None)
                for (opt_name, opt_value) in post_options:
                    if opt_name in ('-h', '--help'):
                        output = PrintUsage(block)
                        print output
                        sys.exit(0)
                    if '--%s' % key == opt_name:
                        if option.get('type', 'flag') != 'flag':
                            data[key] = opt_value
                        else:
                            data[key] = True
                    elif letter and '-%s' % letter == opt_name:
                        if option.get('type', 'flag') != 'flag':
                            data[key] = opt_value
                        else:
                            data[key] = True

                if key not in data and 'default' in option:
                    data[key] = option['default']
                elif key not in data and option.get('type', 'flag') == 'flag':
                    data[key] = False

        if 'args' in usage:
            for count in range(0, len(usage['args'])):
                arg = usage['args'][count]
                name = arg['name']
                if count < len(post_args):
                    if not arg.get('remaining', False):
                        data[name] = post_args[count]
                    else:
                        data[name] = post_args[count:]
                        break
                elif arg.get('required', False):
                    error = 'Required argument missing: Arg count %s: Name: %s' % (count, arg.get('name', '*UNKNOWN NAME*'))
                    raise OptionsAndArgsFailure(error)
                elif 'default' in arg:
                    data[name] = arg.get('default', None)
                elif arg.get('remaining', False):
                    data[name] = []

        return data


class ProcessAndLoopDaemon(daemonize.Daemon):
    """Daemonized version of this command.  Use in production.  Default."""

    def __init__(self, usage, block, data, state, chain_output):
        self.usage = usage
        self.block = block
        self.data = data
        self.state = state
        self.chain_output = chain_output
        daemonize.Daemon(self, pidfile)

    def run(self):
        log('ProcessAndLoopDaemon')
        sharedlock.Acquire('__running')
        try:
            output = processing.Process(self.block, self.data, self.state, self.chain_output)
            print 'Output:'
            import pprint
            pprint.pprint(output)
        except Exception, e:
            log(e, logging.ERROR)
            raise e


def ProcessAndLoop(usage, block, input_data, request_state, pipe_data):
    """Process the block, and loop while it is executing RunThreads.
  
  Handles daemonization as well.
  """
    sharedlock.Acquire('__running')
    if usage and 'load state' in usage:
        for (bucket, save_path) in usage['load state'].items():
            if '%s' not in save_path and os.path.isfile(save_path):
                imported_data = procyaml.ImportYaml(save_path)
            else:
                imported_data = None
            sharedstate.ImportSave(bucket, save_path, imported_data=imported_data)
            sharedstate.RegisterDefaultSave(bucket, save_path)

    if usage and usage.get('daemon', False):
        pidfile = usage.get('pidfile', 'procblock.pid')
        stdout = 'procblock.out'
        try:
            raise Exception('Have to sub-class Daemon class, so we can pass in the proper arguments to have it run processing.Process()')
            log('Daemonizing: pidfile: %s' % pidfile)
            daemon = daemonize.Daemon(pidfile)
            log('Daemonizing: Starting: (CWD: %s)' % os.path.abspath('.'))
            daemon.start()
        except Exception, e:
            log(e, logging.ERROR)
            raise e

    elif usage and usage.get('longrunning', False):
        log('Long Running Process: Starting...  (CWD: %s)' % os.path.abspath('.'))
        output = processing.Process(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None)
        import pprint
        pprint.pprint(output)
        try:
            while sharedlock.IsLocked('__running'):
                time.sleep(0.1)

        except KeyboardInterrupt, e:
            log('ProcessAndLoop: Keyboard Interrupt: Releasing lock: __running')
            sharedlock.Release('__running')

    else:
        log('ProcessAndLoop: Running once...  (CWD: %s)' % os.path.abspath('.'))
        try:
            output = processing.Process(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None)
            import pprint
            pprint.pprint(output)
        finally:
            sharedlock.Release('__running')

    log('Quitting...')
    return