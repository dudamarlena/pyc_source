# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/langserver/base.py
# Compiled at: 2019-07-30 12:11:49
# Size of source mod 2**32: 1477 bytes
from typing import Dict
from enum import IntEnum
from code.document import Document
import logging
logger = logging.getLogger(__name__)
logger.propagate = True

class LSPErrCode(IntEnum):
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    serverErrorStart = -32099
    serverErrorEnd = -32000
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001
    RequestCancelled = -32800
    ContentModified = -32801


class JSONRPC2Error(Exception):

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data


class ServerError(Exception):

    def __init__(self, server_error_message, json_rpc_error):
        self.server_error_message = server_error_message
        self.json_rpc_error = json_rpc_error


class CWLLangServerBase:

    def __init__(self, conn, config):
        self.conn = conn
        self.running = True
        self.root_path = None
        self.fs = None
        self.all_symbols = None
        self.workspace = None
        self.streaming = True
        self.open_documents = {}
        self.initialization_request_received = False
        self.client_capabilities = {}
        self.config = config