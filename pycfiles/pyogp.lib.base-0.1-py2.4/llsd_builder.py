# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/llsd_builder.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
from template import MsgData, MsgBlockData, MsgVariableData

class LLSDMessageBuilder(object):
    __module__ = __name__

    def __init__(self):
        self.current_template = None
        self.current_msg = None
        self.current_block = None
        self.cur_msg_name = ''
        self.cur_block_name = ''
        self.has_been_built = False
        return

    def is_built(self):
        return self.has_been_built

    def build_message(self):
        """ this does not serialize it for this type of builder. The message
            will be put in standard Python form and will need to be formatted
            based on who the target is (xml? something else?) """
        msg = {}
        for block in self.current_msg.blocks:
            block_list = self.current_msg.blocks[block]
            for block_data in block_list:
                if block_data.name not in msg:
                    msg[block_data.name] = []
                block = {}
                msg[block_data.name].append(block)
                for variable in block_data.vars.values():
                    block[variable.name] = variable.data

        self.has_been_built = True
        return (msg, len(msg))

    def new_message(self, message_name):
        self.has_been_built = False
        self.current_msg = MsgData(message_name)
        self.cur_msg_name = message_name

    def next_block(self, block_name):
        self.has_been_built = False
        block = MsgBlockData(block_name)
        self.current_msg.add_block(block)
        self.current_block = block
        self.cur_block_name = block_name

    def add_data(self, var_name, data, data_type):
        self.has_been_built = False
        var = MsgVariableData(var_name, data)
        self.current_block.add_variable(var)