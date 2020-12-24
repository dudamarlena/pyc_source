# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/amundsen_common/log/action_log_model.py
# Compiled at: 2020-02-13 16:36:56
# Size of source mod 2**32: 1325 bytes
from typing import Any, Optional

class ActionLogParams(object):
    """ActionLogParams"""

    def __init__(self, *, command: str, start_epoch_ms: int, end_epoch_ms: Optional[int]=0, user: str, host_name: str, pos_args_json: str, keyword_args_json: str, output: Any=None, error: Optional[Exception]=None) -> None:
        self.command = command
        self.start_epoch_ms = start_epoch_ms
        self.end_epoch_ms = end_epoch_ms
        self.user = user
        self.host_name = host_name
        self.pos_args_json = pos_args_json
        self.keyword_args_json = keyword_args_json
        self.output = output
        self.error = error

    def __repr__(self) -> str:
        return 'ActionLogParams(command={!r}, start_epoch_ms={!r}, end_epoch_ms={!r}, user={!r}, host_name={!r}, pos_args_json={!r}, keyword_args_json={!r}, output={!r}, error={!r})'.format(self.command, self.start_epoch_ms, self.end_epoch_ms, self.user, self.host_name, self.pos_args_json, self.keyword_args_json, self.output, self.error)