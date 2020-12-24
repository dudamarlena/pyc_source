# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/config_gen.py
# Compiled at: 2020-03-03 07:34:32
from __future__ import print_function, unicode_literals
import os, sys, configobj
if sys.version_info < (3, 0, 0):
    input = raw_input

class ConfigGenerator:
    """class for config generation"""

    def get_tools(self):
        """Lets the user enter the tools he want to use"""
        tools = (b'flake8,pylint,vulture,pyroma,isort,yapf,black,safety,dodgy,pytest,pypi').split(b',')
        print((b'Available tools: {0}').format((b',').join(tools)))
        answer = ask_list(b'What tools would you like to use?', [
         b'flake8', b'pytest'])
        if any(tool not in tools for tool in answer):
            print(b'Invalid answer, retry.')
            self.get_tools()
        return answer

    def flake8(self):
        """Configuring flake8"""
        pass

    def pylint(self):
        """Configuring pylint, will do nothing"""
        pass

    def vulture(self):
        """Configuring vulture"""
        pass

    def pyroma(self):
        """Configuring pyroma"""
        pass

    def isort(self):
        """Configuring isort"""
        pass

    def yapf(self):
        """Configuring yapf"""
        pass

    def safety(self):
        """Configuring safety"""
        pass

    def dodgy(self):
        """Configuring dodgy"""
        pass

    def pytest(self):
        """Configuring pytest"""
        pass

    def pypi(self):
        """Configuring pypi"""
        pass

    def main(self):
        """The main function for generating the config file"""
        path = ask_path(b'where should the config be stored?', b'.snekrc')
        conf = configobj.ConfigObj()
        tools = self.get_tools()
        for tool in tools:
            conf[tool] = getattr(self, tool)()

        conf.filename = path
        conf.write()
        print(b'Written config file!')
        if b'pylint' in tools:
            print(b'Please also run `pylint --generate-rcfile` to complete setup')


def ask_bool(question, default=True):
    """Asks a question yes no style"""
    default_q = b'Y/n' if default else b'y/N'
    answer = input((b'{0} [{1}]: ').format(question, default_q))
    lower = answer.lower()
    if not lower:
        return default
    return lower == b'y'


def ask_int(question, default=None):
    """Asks for a number in a question"""
    default_q = (b' [default: {0}]: ').format(default) if default is not None else b''
    answer = input((b'{0} [{1}]: ').format(question, default_q))
    if not answer:
        if default is None:
            print(b'No default set, try again.')
            return ask_int(question, default)
        return default
    if any(x not in b'1234567890' for x in answer):
        print(b'Please enter only numbers (0-9).')
        return ask_int(question, default)
    else:
        return int(answer)


def ask_path(question, default=None):
    """Asks for a path"""
    default_q = (b' [default: {0}]: ').format(default) if default is not None else b''
    answer = input((b'{0} [{1}]: ').format(question, default_q))
    if answer == b'':
        return default
    else:
        if os.path.isdir(answer):
            return answer
        print((b'No such directory: {answer}, please try again').format(answer=answer))
        return ask_path(question, default)


def ask_list(question, default=None):
    """Asks for a comma seperated list of strings"""
    default_q = (b' [default: {0}]: ').format((b',').join(default)) if default is not None else b''
    answer = input((b'{0} [{1}]: ').format(question, default_q))
    if answer == b'':
        return default
    else:
        return [ ans.strip() for ans in answer.split(b',') ]


def ask_str(question, default=None):
    """Asks for a simple string"""
    default_q = (b' [default: {0}]: ').format(default) if default is not None else b''
    answer = input((b'{0} [{1}]: ').format(question, default_q))
    if answer == b'':
        return default
    else:
        return answer


def generate():
    generator = ConfigGenerator()
    generator.main()