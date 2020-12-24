# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cgee/dev/xsiftx/xsiftx/sifters/__init__.py
# Compiled at: 2014-05-02 21:59:20
"""
Place whatever executable you like in here and it will be
added to the list of sifters for use in the command.

The expectations of sifters are that the first line output
is the filename to use, and everything else on stdout is
the file to upload to the dashboard.

You can write to stderr without consequence if neccessary,
and returning anything but 0 will cause the upload to be
aborted. Command is run with the following arguments:
<sifter> edx_venv_path edx_platform_path course_id [extra_arg, extra_arg,....]
"""