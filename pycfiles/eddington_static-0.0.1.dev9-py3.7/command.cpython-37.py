# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_static/command.py
# Compiled at: 2020-05-13 12:10:19
# Size of source mod 2**32: 3336 bytes
import os, subprocess
from dataclasses import dataclass, field
from typing import List, Union

@dataclass(repr=False)
class Command:
    __doc__ = '\n    Data class representing a command to run in order to evaluate the code.\n\n    :param name: The name of the command to run.\n    :param args: A callable that gets input paths and return the arguments for the\n    command.\n    :param test_args: List of arguments to add when evaluating test directory.\n    :param check_arg: A checking argument that indicates that no formatting actions are\n    :param help: Help string\n    '
    name: str
    help: str
    args = field(default=None)
    args: Union[(List[str], None)]
    test_args = field(default=None)
    test_args: Union[(List[str], None)]
    check_arg = field(default=None)
    check_arg: Union[(str, None)]

    def execute(self, input_paths: List[str], is_format: bool=False, is_silent: bool=False, is_verbose: bool=False, is_test: bool=False) -> int:
        """
        Execute the command.

        :param input_paths: input files to check.
        :param is_format: Boolean. Indicates if formatting is required.
        :param is_silent: Boolean. Indicates to run the command without capturing
         output.
        :param is_verbose: Boolean. Run commands verbosely
        :param is_test: Boolean. Is running on test folder or file
        :return: Int. Returns the return code of the command
        """
        args = [
         
          self.name, *input_paths]
        if self.args is not None:
            args.extend(self.args)
        if is_test:
            if self.test_args is not None:
                args.extend(self.test_args)
        if not is_format:
            if self.check_arg is not None:
                args.append(self.check_arg)
        if is_verbose:
            print(f"""Running the following command: "{' '.join(args)}"""")
        return subprocess.run(args,
          env=(os.environ), check=False, capture_output=is_silent).returncode

    def __repr__(self) -> str:
        """
        Create a representation string for the command.

        :return: A representation string.
        """
        return f"{self.name} - {self.help}"


BLACK = Command(name='black', check_arg='--check', help='A code formatter for python')
FLAKE8 = Command(name='flake8',
  args=['--max-line-length=88'],
  help='Code style checker for python')
ISORT = Command(name='isort',
  args=[
 '--recursive',
 '--multi-line=3',
 '--trailing-comma',
 '--force-grid-wrap=0',
 '--use-parentheses',
 '--lines=88'],
  check_arg='--check-only',
  help='A tool for sorting and cleaning python imports')
MYPY = Command(name='mypy',
  args=[
 '--ignore-missing-imports', '--allow-untyped-calls'],
  help='Validate types using mypy')
PYLINT = Command(name='pylint',
  args=[
 '--disable=C0330,E0401'],
  test_args=[
 '--disable=C0103,C0114,C0115,C0116,E1101'],
  help='Python code linter')
PYDOCSTYLE = Command(name='pydocstyle',
  args=[
 '--ignore=D203,D212,D400,D401'],
  test_args=[
 '--ignore=D100,D101,D102'],
  help='A tool for python docstring style enforcing')
COMMANDS = [
 BLACK,
 FLAKE8,
 ISORT,
 MYPY,
 PYLINT,
 PYDOCSTYLE]