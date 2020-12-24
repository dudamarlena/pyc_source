# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_no_nest_name_space_collision.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2089 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages

class CoCoNoNestNameSpaceCollision(CoCo):
    __doc__ = '\n    This coco tests that no functions are defined which collide with the nest namespace, which are:\n      "update",\n      "calibrate",\n      "handle",\n      "connect_sender",\n      "check_connection",\n      "get_status",\n      "set_status",\n      "init_state_",\n      "init_buffers_"\n    Allowed:\n        function fun(...)\n    Not allowed:    \n        function handle(...) <- collision\n    '
    nest_name_space = ['update', 'calibrate', 'handle', 'connect_sender', 'check_connection', 'get_status',
     'set_status', 'init_state_', 'init_buffers_']

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        for func in node.get_functions():
            if func.get_name() in cls.nest_name_space:
                code, message = Messages.get_nest_collision(func.get_name())
                Logger.log_message(error_position=func.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)