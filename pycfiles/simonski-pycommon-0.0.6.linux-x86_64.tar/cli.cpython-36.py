# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simon/.virtualenvs/pyscratch/lib/python3.6/site-packages/common/cli.py
# Compiled at: 2020-03-09 05:24:05
# Size of source mod 2**32: 5700 bytes
import os, sys, time, socket, struct, sys, uuid

class CLIMissingKeyError(BaseException):

    def __init__(self, *args, **kwargs):
        super(CLIMissingKeyError, self).__init__(args, kwargs)


class CLI:

    def __init__(self, argv=sys.argv):
        self.argv = argv

    def get_command(self) -> str:
        if len(self.argv) > 1:
            return self.argv[1]
        else:
            return

    @staticmethod
    def read(prompt):
        return input(prompt)

    def index_of(self, key) -> int:
        index = 0
        while index < len(self.argv):
            if self.argv[index] == key:
                return index
            index += 1

        return -1

    def contains(self, key) -> bool:
        return self.index_of(key) > -1

    def get_or_die(self, key, error_message=None) -> str:
        v = self.get_or_default(key, None)
        if v is None:
            if error_message is None:
                print("Error, '" + key + "' is required.")
            else:
                print(error_message)
            sys.exit(1)
        else:
            return v

    def get_or_raise(self, key: str, error_message: str=None) -> str:
        """
        Requires a key/value or prints the error and raises a CLIMissingKeyError
        :param key:
        :param error_message:
        :return:
        """
        v = self.get_or_default(key, None)
        if v is None:
            if error_message is None:
                print("Error, '" + key + "' is required.")
            else:
                print(error_message)
            raise CLIMissingKeyError(error_message)
        else:
            return v

    def get_or_default(self, key, default_value) -> str:
        index = self.index_of(key)
        if index == -1:
            return default_value
        else:
            if index + 1 < len(self.argv):
                return self.argv[(index + 1)]
            return default_value

    def get_existing_filename_or_die(self, key) -> str:
        """
        returns the filename specified by the key, or dies
        """
        filename = self.get_or_default(key, None)
        if filename is None:
            print("Error, '" + key + "' is required.")
            sys.exit(1)
        else:
            if not os.path.isfile(filename):
                print("'" + str(filename) + "' is not a file.")
                sys.exit(1)
            else:
                return filename


class Application:
    __doc__ = '\n\n    An example app would be\n\n    class App(Application):\n        def __init__(self)\n            self.__init__(prompt="foo")\n\n        def on_command(self, args):\n            print("command")\n\n        def help_command(self, args):\n            return "I am the help"\n\n    app.process()\n    or\n\n    '

    def __init__(self, prompt=None):
        self.QUIT = False
        if prompt is None:
            self.prompt = '> '
        else:
            self.prompt = prompt

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_prompt(self):
        return self.prompt

    @staticmethod
    def get_command_from_user_input(user_input):
        if len(user_input) > 1:
            command = user_input[1]
            remainder = user_input[2:]
        else:
            command = None
            remainder = None
        return (
         command, remainder)

    def get_func_or_none(self, fn_name):
        try:
            attr = getattr(self, fn_name)
            return attr
        except Exception as e:
            return

    def process_interactive(self):
        quit = False
        while not self.QUIT:
            user_input = CLI.read(prompt=(self.get_prompt()))
            self.process(user_input)

    def process_line(self, user_input=None):
        command, remainder = self.get_command_from_user_input(user_input)
        if command is None:
            return self.on_usage()
        fn_name = 'on_' + command.lower().replace('-', '_')
        try:
            attr = self.get_func_or_none(fn_name)
            if attr is None:
                print("I don't know how to %s" % command)
                return False
            try:
                return attr(command, remainder)
            except Exception as e:
                print("Problem calling function '" + fn_name + "'")
                print(e)
                return False

        except Exception:
            print('Exception')

    def on_q(self, command=None, user_input=None):
        self.on_quit(user_input)

    def on_quit(self, command=None, user_input=None):
        self.QUIT = True

    def on_usage(self):
        print("Usage: TODO, implement 'on_usage' in your subclass.")
        return False

    def main(self):
        args = sys.argv
        if len(args) == 0:
            self.process_interactive()
        else:
            self.process_line(sys.argv)


class DemoApplication(Application):

    def __init__(self, prompt):
        super(DemoApplication, self).__init__(prompt=prompt)

    def on_anything(self, command: str, user_input: str):
        print('anything!')


if __name__ == '__main__':
    c = CLI()
    prompt = c.get_or_default('-prompt', '> ')
    app = DemoApplication(prompt)
    app.main()