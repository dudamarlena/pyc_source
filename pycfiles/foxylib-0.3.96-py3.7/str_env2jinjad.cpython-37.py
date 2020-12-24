# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/jinja2/str_env2jinjad.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 554 bytes
import logging, os, sys
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool

def main():
    logger = FoxylibLogger.func_level2logger(main, logging.DEBUG)
    str_in = sys.stdin.read()
    h_env = dict(os.environ)
    str_out = Jinja2Tool.tmplt_str2str(str_in, h_env)
    logger.debug({'str_in':str_in,  'str_out':str_out})
    print(str_out)


if __name__ == '__main__':
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    main()