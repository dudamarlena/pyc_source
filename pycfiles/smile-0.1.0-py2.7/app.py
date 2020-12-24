# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smile/app.py
# Compiled at: 2018-01-18 22:47:05
"""Generic entry point script. Idea from tensorflow."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
from absl import flags as absl_flags
from smile import flags

def run(main=None, argv=None):
    """Runs the program with an optional 'main' function and 'argv' list."""
    flags_obj = flags.FLAGS
    absl_flags_obj = absl_flags.FLAGS
    args = argv[1:] if argv else None
    flags_passthrough = flags_obj._parse_flags(args=args)
    if absl_flags_obj['verbosity'].using_default_value:
        absl_flags_obj.verbosity = 0
    main = main or sys.modules['__main__'].main
    sys.exit(main(sys.argv[:1] + flags_passthrough))
    return