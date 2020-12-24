# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/init/init_generator.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 630 bytes
"""
Cookiecutter-based generation logic for project templates.
"""
from samcli.commands.exceptions import UserException
from samcli.lib.init import generate_project
from samcli.lib.init.exceptions import GenerateProjectFailedError, ArbitraryProjectDownloadFailed

def do_generate(location, runtime, dependency_manager, output_dir, name, no_input, extra_context):
    try:
        generate_project(location, runtime, dependency_manager, output_dir, name, no_input, extra_context)
    except (GenerateProjectFailedError, ArbitraryProjectDownloadFailed) as e:
        try:
            raise UserException((str(e)), wrapped_from=(e.__class__.__name__))
        finally:
            e = None
            del e