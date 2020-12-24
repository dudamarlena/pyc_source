# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/json/yaml_tool.py
# Compiled at: 2020-02-07 15:07:37
# Size of source mod 2**32: 820 bytes
import yaml
from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class YAMLTool:

    @classmethod
    def filepath2j(cls, filepath, loader=None):
        logger = FoxylibLogger.func2logger(cls.filepath2j)
        utf8 = FileTool.filepath2utf8(filepath)
        if loader is None:
            loader = yaml.SafeLoader
        j = yaml.load(utf8, Loader=loader)
        return j

    @classmethod
    def j_yaml2h_reversed(cls, j_yaml):
        h = merge_dicts([{v: k} for k, l in j_yaml.items() for v in l],
          vwrite=vwrite_no_duplicate_key)
        return h