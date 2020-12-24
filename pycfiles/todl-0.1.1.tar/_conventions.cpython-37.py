# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/utils/flags/_conventions.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1818 bytes
"""Central location for shared argparse convention definitions."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys, codecs, functools
from absl import app as absl_app
from absl import flags
_help_wrap = functools.partial((flags.text_wrap), length=80, indent='', firstline_indent='\n')

def _stdout_utf8():
    try:
        codecs.lookup('utf-8')
    except LookupError:
        return False
    else:
        return sys.stdout.encoding == 'UTF-8'


if _stdout_utf8():
    help_wrap = _help_wrap
else:

    def help_wrap(text, *args, **kwargs):
        return _help_wrap(text, *args, **kwargs).replace('\ufeff', '')


absl_app.HelpshortFlag.SHORT_NAME = 'h'