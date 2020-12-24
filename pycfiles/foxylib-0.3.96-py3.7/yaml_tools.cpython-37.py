# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/json/yaml_tools.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 386 bytes
import yaml
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.logger_tools import FoxylibLogger

class YAMLToolkit:

    @classmethod
    def filepath2j(cls, filepath):
        logger = FoxylibLogger.func2logger(cls.filepath2j)
        utf8 = FileTool.filepath2utf8(filepath)
        j = yaml.load(utf8)
        return j