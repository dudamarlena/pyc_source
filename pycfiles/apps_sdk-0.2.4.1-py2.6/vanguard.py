# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/vanguard.py
# Compiled at: 2010-07-26 17:09:43
"""
Run the actual apps sdk build tool (and parse out input).
"""
import ConfigParser, copy, distutils.fancy_getopt, logging, os, sys, apps.command, apps.config, apps.command.base, apps.command.add, apps.command.config, apps.command.generate, apps.command.localize, apps.command.package, apps.command.push, apps.command.serve, apps.command.setup, apps.command.submit, apps.command.update

class Options(dict):

    def __getattr__(self, k):
        return self.get(k, None)

    def __setattr__(self, k, v):
        self[k] = v


class Vanguard(object):
    global_options = [
     ('verbose', 'v', 'run verbosely (default)', None),
     ('quiet', 'q', 'run quiety (turns verbose off)', None),
     ('help', 'h', 'show detailed help message', None),
     ('debug', 'd', 'run with debugging options enabled', None)]
    display_options = [
     ('help-commands', None, 'list all available commands', None)]
    negative_opt = {'quiet': 'verbose'}

    def __init__(self):
        self.command_options = {}
        self.options = Options()
        self.args = sys.argv[1:]
        self.ran = []

    def _command_opts(self, command):
        d = self.command_options.get(command)
        if not d:
            d = self.command_options[command] = {}
        return d

    def parse_config_files(self):
        """Parse the default config files.

        The order of resolution is:
        - project/.apps.cfg
        - $HOME/.apps.cfg
        """
        config_handler = apps.config.Config()
        self.command_options = config_handler
        for (k, v) in self._command_opts('general').iteritems():
            self.options[k] = v

    def is_display_option(self, order, parser):
        if self.options.help_commands:
            self.print_commands()
            return True
        return False

    def parse_command_line(self):
        """Parse the command line.

        Note that any options on the command line will override config file
        options.
        """
        self.commands = []
        parser = distutils.fancy_getopt.FancyGetopt(self.global_options + self.display_options)
        parser.set_negative_aliases(self.negative_opt)
        args = parser.getopt(args=self.args, object=self.options)
        order = parser.get_option_order()
        self.setup_logging()
        if self.is_display_option(order, parser):
            return
        if not args:
            logging.error('Must include a command to run.\n')
            self.print_commands()
            return
        while args:
            args = self._parse_command_opts(parser, args)
            if not args:
                return

        if self.options.help:
            self._show_help()
            return
        return True

    def get_command(self, name):
        module_name = 'apps.command.%s' % (name,)
        try:
            __import__(module_name)
            module = sys.modules[module_name]
            return getattr(module, name)
        except ImportError, UnboundLocalError:
            logging.error('The command "%s" does not exist.' % (name,))
            self.print_commands()
            sys.exit(1)

    def _parse_command_opts(self, parser, args):
        command_name = args[0]
        try:
            command = self.get_command(command_name)
        except AttributeError:
            logging.error('%s is not a valid command.' % (command_name,))
            self.print_commands()
            return
        else:
            self.commands.append(command)
            negative_opt = self.negative_opt
            if hasattr(command, 'negative_opt'):
                negative_opt = copy.copy(negative_opt)
                negative_opt.update(command.negative_opt)
            parser.set_option_table(self.global_options + command.user_options)
            parser.set_negative_aliases(negative_opt)
            (args, opts) = parser.getopt(args[1:])
            if hasattr(opts, 'help') and opts.help:
                self._command_opts(command_name)['help'] = 1
                self._show_help()
                return
            opt_dict = self._command_opts(command_name)
            for (k, v) in vars(opts).items():
                opt_dict[k] = v

        return args

    def print_commands(self):
        logging.error('Commands:')
        for command in apps.command.__all__:
            logging.error('%5s%-15s%-60s' % (
             '', command, self.get_command(command).help))

    def run_commands(self):
        for command in self.commands:
            self.run_command(command.__name__)
            logging.error('')

    def run_command(self, command_name):
        if command_name in self.ran:
            return
        command = self.get_command(command_name)
        for pre in command.pre_commands:
            self.run_command(pre)

        logging.info('running `%s` ...' % (command_name,))
        if command(self).run() == -1:
            sys.exit(1)
        self.ran.append(command_name)
        for post in command.post_commands:
            self.run_command(post)

    def setup_logging(self):
        handlers = logging.getLogger().handlers
        if len(handlers) == 1:
            handlers.pop()
        logging.basicConfig(format='%(message)s')
        logger = logging.getLogger()
        if self.options.debug:
            logger.setLevel(logging.DEBUG)
        elif self.options.verbose == 0:
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.INFO)

    def _show_help(self):
        logging.error('Global options:')
        self._print_help(self.global_options + self.display_options)
        for command in self.commands:
            if len(command.user_options) == 0:
                continue
            logging.error("Options for '%s' command:" % (
             command.__name__,))
            self._print_help(command.user_options)

        logging.error('')
        logging.error('usage: apps [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ... ]')
        logging.error('   or: apps --help [cmd1 cmd2 ...]')

    def _print_help(self, options):
        for opt in options:
            logging.error('  %-18s%-60s' % (
             '--%s %s' % (opt[0], '(-%s)' % (opt[1],) if opt[1] else ''),
             opt[2]))

        logging.error('')


def run--- This code section failed: ---

 L. 219         0  LOAD_GLOBAL           0  'Vanguard'
                3  CALL_FUNCTION_0       0  None
                6  STORE_FAST            0  'handler'

 L. 220         9  LOAD_FAST             0  'handler'
               12  LOAD_ATTR             1  'parse_config_files'
               15  CALL_FUNCTION_0       0  None
               18  POP_TOP          

 L. 221        19  LOAD_FAST             0  'handler'
               22  LOAD_ATTR             2  'parse_command_line'
               25  CALL_FUNCTION_0       0  None
               28  POP_TOP          

 L. 222        29  LOAD_FAST             0  'handler'
               32  LOAD_ATTR             3  'options'
               35  LOAD_ATTR             4  'help'
               38  UNARY_NOT        
               39  JUMP_IF_FALSE        87  'to 129'
             42_0  THEN                     130
               42  POP_TOP          

 L. 223        43  LOAD_GLOBAL           5  'len'
               46  LOAD_GLOBAL           6  'filter'
               49  LOAD_LAMBDA              '<code_object <lambda>>'
               52  MAKE_FUNCTION_0       0  None

 L. 224        55  BUILD_LIST_0          0 
               58  DUP_TOP          
               59  STORE_FAST            1  '_[1]'

 L. 225        62  LOAD_FAST             0  'handler'
               65  LOAD_ATTR             7  'command_options'
               68  LOAD_ATTR             8  'values'
               71  CALL_FUNCTION_0       0  None
               74  GET_ITER         
               75  FOR_ITER             19  'to 97'
               78  STORE_FAST            2  'x'
               81  LOAD_FAST             1  '_[1]'
               84  LOAD_FAST             2  'x'
               87  LOAD_ATTR             9  'keys'
               90  CALL_FUNCTION_0       0  None
               93  LIST_APPEND      
               94  JUMP_BACK            75  'to 75'
               97  DELETE_FAST           1  '_[1]'
              100  CALL_FUNCTION_2       2  None
              103  CALL_FUNCTION_1       1  None
              106  LOAD_CONST               0
              109  COMPARE_OP            2  ==
              112  JUMP_IF_FALSE        14  'to 129'
              115  POP_TOP          

 L. 227       116  LOAD_FAST             0  'handler'
              119  LOAD_ATTR            10  'run_commands'
              122  CALL_FUNCTION_0       0  None
              125  POP_TOP          
              126  JUMP_FORWARD          1  'to 130'
            129_0  COME_FROM           112  '112'
            129_1  COME_FROM            39  '39'
              129  POP_TOP          
            130_0  COME_FROM           126  '126'

Parse error at or near `POP_TOP' instruction at offset 129


if __name__ == '__main__':
    run()