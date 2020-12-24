# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/llsd_builder.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
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
        return (
         msg, len(msg))

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