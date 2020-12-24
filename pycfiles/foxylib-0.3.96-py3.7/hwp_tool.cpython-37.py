# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/software/haansoft/hwp/hwp_tool.py
# Compiled at: 2020-01-28 20:07:19
# Size of source mod 2**32: 2457 bytes
import logging, sys
from contextlib import closing
from functools import lru_cache
from io import BytesIO
from tempfile import NamedTemporaryFile
from hwp5.dataio import ParseError
from hwp5.errors import InvalidHwp5FileError
from hwp5.hwp5txt import TextTransform
from hwp5.utils import make_open_dest_file
from hwp5.xmlmodel import Hwp5File
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.version.version_tool import VersionTool

class HWPTool:

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def _text_transform(cls):
        return TextTransform()

    @classmethod
    def bytes2text(cls, bytes):
        with NamedTemporaryFile() as (f):
            f.write(bytes)
            return cls.filepath2text(f.name)

    @classmethod
    def filepath2text(cls, filepath_hwp):
        logger = FoxylibLogger.func_level2logger(cls.filepath2text, logging.DEBUG)
        tt = cls._text_transform()
        try:
            with closing(Hwp5File(filepath_hwp)) as (hwp5file):
                with BytesIO() as (bytes_io):
                    tt.transform_hwp5_to_text(hwp5file, bytes_io)
                    bytes_io.seek(0)
                    bytes = bytes_io.read()
                    return bytes.decode('UTF-8')
        except ParseError as e:
            try:
                e.print_to_logger(logger)
                raise
            finally:
                e = None
                del e

        except InvalidHwp5FileError as e:
            try:
                logger.error('%s', e)
                raise
            finally:
                e = None
                del e

    @classmethod
    @VersionTool.inactive(reason='Unnecessary because cls.filepath2text works')
    def filepath2textfile(cls, filepath_hwp, filepath_text):
        logger = FoxylibLogger.func_level2logger(cls.filepath2textfile, logging.DEBUG)
        text_transform = TextTransform()
        open_dest = make_open_dest_file(filepath_text)
        transform = text_transform.transform_hwp5_to_text
        try:
            with closing(Hwp5File(filepath_hwp)) as (hwp5file):
                with open_dest() as (dest):
                    transform(hwp5file, dest)
        except ParseError as e:
            try:
                e.print_to_logger(logger)
            finally:
                e = None
                del e

        except InvalidHwp5FileError as e:
            try:
                logger.error('%s', e)
                sys.exit(1)
            finally:
                e = None
                del e