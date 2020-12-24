# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/env/tmplt_env2str_envrc.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 1558 bytes
import logging, os, sys
from future.utils import lfilter, lmap
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool
from foxylib.tools.string.string_tool import str2strip

def main():
    logger = FoxylibLogger.func_level2logger(main, logging.DEBUG)
    from foxylib.tools.file.file_tool import FileTool
    l = lfilter(bool, map(str2strip, sys.stdin))
    logger.debug({'l': l})
    h_env = dict(os.environ)
    filepath_list = lmap(lambda s: Jinja2Tool.tmplt_str2str((s.split(maxsplit=1)[1]), data=h_env), l)
    str_tmplt = '\n'.join([Jinja2Tool.tmplt_file2str(fp, h_env) for fp in filepath_list if not fp.endswith('.yaml') if fp.endswith('.yml')])
    envname_list = lfilter(bool, [h_env.get('ENV'), '_DEFAULT_'])
    kv_list = EnvTool.yaml_str2kv_list(str_tmplt, envname_list)
    str_export = '\n'.join(['export {0}="{1}"'.format(k, v_yaml) for k, v_yaml in kv_list])
    print(str_export)


if __name__ == '__main__':
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    main()