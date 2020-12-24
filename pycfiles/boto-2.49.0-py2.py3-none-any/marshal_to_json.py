# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/helpers/marshal_to_json.py
# Compiled at: 2012-08-15 05:42:57
__doc__ = "\nScript that loads in MetaDict and DataDict and saves them out in json format.\nIf botnee_config.META_DICT_TYPE (and DATA) are both 'marshal', this will\ntranslate the files from marshal to json format.\n"
import os
from botnee import botnee_config
from botnee.process.meta_dict import MetaDict
from botnee.process.data_dict import DataDict
INPUT_FORMAT = 'marshal'
OUTPUT_FORMAT = 'json'
botnee_config.DATA_DICT_STORE_TYPE = INPUT_FORMAT
botnee_config.META_DICT_STORE_TYPE = INPUT_FORMAT
md = MetaDict()
md.format = OUTPUT_FORMAT
md.filename = os.path.join(botnee_config.DATA_DIRECTORY, OUTPUT_FORMAT, 'meta_dict' + botnee_config.SUFFIX) + '.dat'
md.flush()
dd = DataDict()
dd.format = OUTPUT_FORMAT
dd.filename = os.path.join(botnee_config.DATA_DIRECTORY, OUTPUT_FORMAT, 'data_dict' + botnee_config.SUFFIX) + '.dat'
dd.flush()