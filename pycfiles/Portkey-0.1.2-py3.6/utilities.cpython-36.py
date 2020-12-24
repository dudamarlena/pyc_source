# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/portkey/utilities.py
# Compiled at: 2018-03-28 07:49:26
# Size of source mod 2**32: 1178 bytes
import json
id2handlerInfo = {}

class JSONSerializable:

    def __str__(self):
        return jsonify(self)

    def __repr__(self):
        return jsonify(self, indent=4)


class EventHandlerInfo(JSONSerializable):

    def __init__(self):
        self.selector = None
        self.event = None
        self.uiData = None
        self.handler = None
        self._handler = None
        self.filter_selector = None
        self.stop_propagation = False
        self.throttle = False


def get_handler_info(func) -> EventHandlerInfo:
    function_id = id(func)
    handler_info = id2handlerInfo.get(function_id)
    if handler_info is None:
        handler_info = EventHandlerInfo()
        id2handlerInfo[function_id] = handler_info
    return handler_info


def jsonify(obj, **kwargs) -> str:
    return (json.dumps)(obj, default=lambda o: {k:v for k, v in o.__dict__.items() if not k.startswith('_') if not k.startswith('_')}, separators=(',', ':'), **kwargs)


class UIData:

    def __init__(self, data):
        self._data = data

    def __getattr__(self, item):
        return self._data[item]

    def __repr__(self):
        return repr(self._data)