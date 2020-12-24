# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maziyar/Desktop/Work/JohnSnowLabs/spark-nlp/python/build/lib/sparknlp/util.py
# Compiled at: 2020-03-20 15:04:11
# Size of source mod 2**32: 314 bytes
import sparknlp.internal as _internal

def get_config_path():
    return _internal._ConfigLoaderGetter().apply()


class CoNLLGenerator:

    @staticmethod
    def exportConllFiles(spark, files_path, pipeline, output_path):
        _internal._CoNLLGeneratorExport(spark, files_path, pipeline, output_path).apply()