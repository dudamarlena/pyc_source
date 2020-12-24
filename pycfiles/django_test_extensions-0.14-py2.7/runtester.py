# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/management/commands/runtester.py
# Compiled at: 2009-10-24 11:46:38
from django.core.management.base import BaseCommand
from django.utils import autoreload
import os, sys, time
INPROGRESS_FILE = 'testing.inprogress'

def get_test_command():
    """
    Return an instance of the Command class to use.

    This method can be patched in to run a test command other than the on in
    core Django.  For example, to make a runtester for South:

    from django.core.management.commands import runtester
    from django.core.management.commands.runtester import Command

    def get_test_command():
        from south.management.commands.test import Command as TestCommand
        return TestCommand()

    runtester.get_test_command = get_test_command
    """
    from test_extensions.management.commands.test import Command as TestCommand
    return TestCommand()


def my_reloader_thread():
    """
    Wait for a test run to complete before exiting.
    """
    while autoreload.RUN_RELOADER:
        if autoreload.code_changed():
            while os.path.exists(INPROGRESS_FILE):
                time.sleep(1)

            sys.exit(3)
        time.sleep(1)


autoreload.reloader_thread = my_reloader_thread

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = 'Starts a command that tests upon saving files.'
    args = '[optional apps to test]'
    requires_model_validation = False

    def handle(self, *args, **options):
        if os.path.exists(INPROGRESS_FILE):
            os.remove(INPROGRESS_FILE)

        def inner_run():
            try:
                open(INPROGRESS_FILE, 'wb').close()
                test_command = get_test_command()
                test_command.handle(*args, **options)
            finally:
                if os.path.exists(INPROGRESS_FILE):
                    os.remove(INPROGRESS_FILE)

        autoreload.main(inner_run)