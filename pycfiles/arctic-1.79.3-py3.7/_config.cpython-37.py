# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/_config.py
# Compiled at: 2019-12-06 10:13:42
# Size of source mod 2**32: 4743 bytes
import logging, os, pymongo
from enum import Enum
logger = logging.getLogger(__name__)
STRICT_WRITE_HANDLER_MATCH = bool(os.environ.get('STRICT_WRITE_HANDLER_MATCH'))
CHECK_CORRUPTION_ON_APPEND = bool(os.environ.get('CHECK_CORRUPTION_ON_APPEND'))
ARCTIC_AUTO_EXPAND_CHUNK_SIZE = bool(os.environ.get('ARCTIC_AUTO_EXPAND_CHUNK_SIZE'))
MAX_DOCUMENT_SIZE = int(pymongo.common.MAX_BSON_SIZE * 0.8)
FAST_CHECK_DF_SERIALIZABLE = bool(os.environ.get('FAST_CHECK_DF_SERIALIZABLE'))

class FwPointersCfg(Enum):
    ENABLED = 0
    DISABLED = 1
    HYBRID = 2


FW_POINTERS_REFS_KEY = 'SEGMENT_SHAS'
FW_POINTERS_CONFIG_KEY = 'FW_POINTERS_CONFIG'
ARCTIC_FORWARD_POINTERS_RECONCILE = False
ARCTIC_FORWARD_POINTERS_CFG = FwPointersCfg.DISABLED
ENABLE_PARALLEL = not os.environ.get('DISABLE_PARALLEL')
LZ4_HIGH_COMPRESSION = bool(os.environ.get('LZ4_HIGH_COMPRESSION'))
LZ4_WORKERS = os.environ.get('LZ4_WORKERS', 2)
LZ4_N_PARALLEL = os.environ.get('LZ4_N_PARALLEL', 16)
LZ4_MINSZ_PARALLEL = os.environ.get('LZ4_MINSZ_PARALLEL', 524288.0)
BENCHMARK_MODE = False
ARCTIC_ASYNC_NWORKERS = os.environ.get('ARCTIC_ASYNC_NWORKERS', 4)
FORCE_BYTES_TO_UNICODE = bool(os.environ.get('FORCE_BYTES_TO_UNICODE'))
ENABLE_CACHE = not bool(os.environ.get('ARCTIC_DISABLE_CACHE'))
SKIP_BSON_ENCODE_PICKLE_STORE = bool(os.environ.get('SKIP_BSON_ENCODE_PICKLE_STORE'))
MAX_BSON_ENCODE = os.environ.get('MAX_BSON_ENCODE', 262144)