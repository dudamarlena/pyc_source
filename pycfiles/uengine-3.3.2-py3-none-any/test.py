# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/p.vorobyov/PycharmProjects/exyaru/commands/test.py
# Compiled at: 2019-01-25 06:12:31
from commands import Command
from unittest import main
import logging

class Test(Command):
    NO_ARGPARSE = True

    def run(self):
        from app.models import User, Token, Stream
        from app import app
        from app import tests
        app.logger.level = logging.ERROR
        User._collection = 'test_users'
        Token._collection = 'test_tokens'
        Stream._collection = 'test_streams'
        argv = [
         'micro.py test'] + self.raw_args
        test_program = main(argv=argv, module=tests, exit=False)
        if test_program.result.wasSuccessful():
            return 0
        else:
            return 1