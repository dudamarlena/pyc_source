# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\cmdline.py
# Compiled at: 2020-02-05 20:03:04
# Size of source mod 2**32: 9120 bytes
import cmd2, sys
from winstrument.winstrument import Winstrument
from colorama import Fore, Back, Style
from cmd2 import with_argument_list
import winstrument.utils as utils

class FridaCmd(cmd2.Cmd):
    prompt = '> '

    def __init__(self, app):
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        shortcuts.update({'exit':'quit',  'q':'quit',  'use':'load'})
        self._target = 'C:\\Windows\\System32\\Notepad.exe'
        self._app = app
        cmd2.Cmd.__init__(self, shortcuts=shortcuts)

    @with_argument_list
    def do_list(self, arg):
        """
        usage: list
        Show a list of all available and loaded modules.
        """
        available = self._app.get_available_modules()
        loaded = self._app.get_loaded_modules()
        print('Loaded Modules:')
        for module in loaded:
            if module in available:
                available.remove(module)
            print(module)

        print('Available Modules:')
        for module in available:
            print(module)

    @with_argument_list
    def do_unload(self, arg):
        """
        usage: unload [modulenmae]
        Unload the speicfied loaded module, so it will no longer be used to instrument the target
        """
        self._app.unload_module(arg[0])

    def pexcept(self, errmsg, end='\n', apply_style=True):
        if self.debug:
            if sys.exc_info() != (None, None, None):
                import traceback
                traceback.print_exc()
        elif isinstance(errmsg, Exception):
            err = f"{Fore.RED}EXCEPTION of type {type(errmsg)} occurred with message: {errmsg}{Style.RESET_ALL}"
        else:
            err = f"{Fore.RED}{errmsg}"
        if not self.debug:
            if 'debug' in self.settable:
                err += f'\n{Fore.YELLOW}For more complete error output, use "config debug true" {Style.RESET_ALL}'
        self.perror(err, end=end, apply_style=False)

    @with_argument_list
    def do_load(self, arg):
        """
        usage: load [modulename]
        Load the selected module to be instrument, if it exists
        """
        self._app.load_module(arg[0])

    def _get_formatter_list(self):
        formatter_list = utils.get_formatters()
        output = []
        for formatter in formatter_list:
            output.append(formatter.name)

        return '\n'.join(output)

    @with_argument_list
    def do_info(self, args):
        """usage: info [modulename]
        Displays info about modules.
        """
        if len(args) > 1:
            self.perror('usage: info [modulename]')
            return
            if len(args) == 0:
                metadata = self._app.metadata
                for modname in metadata.keys():
                    print(modname)
                    print(metadata[modname]['description'])
                    print()

        else:
            modulename = args[0]
            if modulename.lower() not in self._app.get_available_modules():
                self.perror(f"invalid module {args[0]}")
                return
            try:
                description = self._app.metadata[modulename.lower()]['description']
                self.poutput(description)
            except (KeyError, AttributeError):
                self.perror(f"No description for module {modulename}")

    @with_argument_list
    def do_show(self, arg):
        """usage: show [modulename [format]]
        Shows the output from modulename in the specified format
        Run without arguments to view available formats
        """
        if len(arg) > 2:
            self.perror('usage: show [modulename [format]]')
        if len(arg) < 1:
            info = f"Available formatters:\n{self._get_formatter_list()}"
            self.poutput(info)
            return
        if len(arg) == 1:
            self.print_format(arg[0], sys.stdout)
            return
        if len(arg) == 2:
            self.print_format(arg[0], sys.stdout, arg[1])

    def print_format(self, modulename, outfile, formatter=None):
        if formatter is not None:
            try:
                style = utils.get_formatter(formatter)
            except ValueError:
                print(f"Invalid format\nAvailable formatters:\n{self._get_formatter_list()}")
                return
            else:
                self._app.print_saved_output(modulename, style, output=outfile)
        else:
            self._app.print_saved_output(modulename, output=outfile)

    @with_argument_list
    def do_export(self, args):
        """
        usage: export <modulename> <filename> [format]
        Exports the stored output of module <modulename> to the file stored in filename in the given format
        """
        if len(args) < 1:
            self.perror('usage: export <modulename> <filename> [format]')
            info = f"Available formatters:\n{self._get_formatter_list()}"
            self.poutput(info)
            return
        if len(args) != 2:
            if len(args) != 3:
                self.perror('usage: export <modulename> <filename> [format]')
                return
        with open(args[1], 'w+') as (outfile):
            if len(args) == 2:
                self.print_format(args[0], outfile)
            else:
                if len(args) == 3:
                    self.print_format(args[0], outfile, args[2])

    @with_argument_list
    def do_exportall(self, args):
        """
        usage: exportall <filename> [format]
        Export stored output from all modules into the specified file
        Optionally specify the preferred format to output.
        """
        if len(args) < 1:
            self.perror('usage: export <modulename> <filename> [json|table]')
            info = f"Available formatters:\n{self._get_formatter_list()}"
            self.poutput(info)
            return
        if len(args) != 1:
            if len(args) != 2:
                self.perror('usage: exportall <filename> [format]')
                return
        with open(args[0], 'w+') as (outfile):
            if len(args) == 1:
                self._app.export_all(outfile)
                return
            try:
                style = utils.get_formatter(args[1])
            except ValueError:
                print(f"Invalid Formatter\nAvailable formatters:\n{self._get_formatter_list()}")

            self._app.export_all(outfile, formatter=style)

    def do_config(self, args):
        super().do_set(args)

    @with_argument_list
    def do_set--- This code section failed: ---

 L. 208         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'args'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_CONST               0
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    74  'to 74'

 L. 209        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _app
               16  LOAD_ATTR                settings_controller
               18  LOAD_METHOD              get_module_settings
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _app
               24  LOAD_ATTR                CORE_MODNAME
               26  CALL_METHOD_1         1  '1 positional argument'
               28  STORE_FAST               'settings'

 L. 210        30  SETUP_LOOP          180  'to 180'
               32  LOAD_FAST                'settings'
               34  LOAD_METHOD              items
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  GET_ITER         
               40  FOR_ITER             70  'to 70'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'key'
               46  STORE_FAST               'value'

 L. 211        48  LOAD_FAST                'self'
               50  LOAD_METHOD              poutput
               52  LOAD_FAST                'key'
               54  FORMAT_VALUE          0  ''
               56  LOAD_STR                 '='
               58  LOAD_FAST                'value'
               60  FORMAT_VALUE          0  ''
               62  BUILD_STRING_3        3 
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          
               68  JUMP_BACK            40  'to 40'
               70  POP_BLOCK        
               72  JUMP_FORWARD        180  'to 180'
             74_0  COME_FROM            10  '10'

 L. 212        74  LOAD_GLOBAL              len
               76  LOAD_FAST                'args'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  LOAD_CONST               1
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   136  'to 136'

 L. 213        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _app
               90  LOAD_ATTR                settings_controller
               92  LOAD_METHOD              get_setting
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _app
               98  LOAD_ATTR                CORE_MODNAME
              100  LOAD_FAST                'args'
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  CALL_METHOD_2         2  '2 positional arguments'
              108  STORE_FAST               'value'

 L. 214       110  LOAD_FAST                'self'
              112  LOAD_METHOD              poutput
              114  LOAD_FAST                'args'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  FORMAT_VALUE          0  ''
              122  LOAD_STR                 '='
              124  LOAD_FAST                'value'
              126  FORMAT_VALUE          0  ''
              128  BUILD_STRING_3        3 
              130  CALL_METHOD_1         1  '1 positional argument'
              132  POP_TOP          
              134  JUMP_FORWARD        180  'to 180'
            136_0  COME_FROM            84  '84'

 L. 215       136  LOAD_GLOBAL              len
              138  LOAD_FAST                'args'
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  LOAD_CONST               2
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   180  'to 180'

 L. 216       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _app
              152  LOAD_ATTR                settings_controller
              154  LOAD_METHOD              set_setting
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _app
              160  LOAD_ATTR                CORE_MODNAME
              162  LOAD_FAST                'args'
              164  LOAD_CONST               0
              166  BINARY_SUBSCR    
              168  LOAD_FAST                'args'
              170  LOAD_CONST               1
              172  BINARY_SUBSCR    
              174  CALL_METHOD_3         3  '3 positional arguments'
              176  POP_TOP          
              178  JUMP_FORWARD        180  'to 180'
            180_0  COME_FROM           178  '178'
            180_1  COME_FROM           146  '146'
            180_2  COME_FROM           134  '134'
            180_3  COME_FROM            72  '72'
            180_4  COME_FROM_LOOP       30  '30'

Parse error at or near `COME_FROM' instruction at offset 180_3

    @with_argument_list
    def do_run(self, arg):
        """
        usage: run
        Spawn and instrument the targer pocess
        """
        target = self._app.settings_controller.get_setting(self._app.CORE_MODNAME, 'target')
        args = self._app.settings_controller.get_setting(self._app.CORE_MODNAME, 'args')
        if target != '':
            self._app.run(target, args)
        else:
            print('Error: must specify target first')

    def do_quit(self, arg):
        """
        Usage: quit
        Save settings and (optionally) output, and quit the app.
        """
        self._app.quit()
        return True


def main():
    app = Winstrument()
    cmd = FridaCmd(app)
    sys.exit(cmd.cmdloop())


if __name__ == '__main__':
    main()