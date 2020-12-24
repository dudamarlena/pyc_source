# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/template_dict.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from msgtypes import MsgFrequency
from data import msg_tmpl, msg_details
from template_parser import MessageTemplateParser
from data_packer import DataPacker
from msgtypes import MsgType, EndianType
from pyogp.lib.base import exc

class TemplateDictionary(object):
    """the dictionary with all known templates"""
    __module__ = __name__

    def __init__(self, template_list=None, message_template=None):
        if template_list == None:
            if message_template == None:
                parser = MessageTemplateParser(msg_tmpl)
            else:
                parser = MessageTemplateParser(message_template)
            template_list = parser.message_templates
            template_dict = TemplateDictionary(template_list)
            self.template_list = template_list
        self.message_templates = {}
        self.message_dict = {}
        self.build_dictionaries(template_list)
        self.build_message_ids()
        return

    def get_template_list(self):
        names = []
        for i in self.template_list:
            names.append(i.name)

        return names

    def build_dictionaries(self, template_list):
        for template in template_list:
            self.message_templates[template.name] = template
            frequency_str = ''
            if template.frequency == MsgFrequency.FIXED_FREQUENCY_MESSAGE:
                frequency_str = 'Fixed'
            elif template.frequency == MsgFrequency.LOW_FREQUENCY_MESSAGE:
                frequency_str = 'Low'
            elif template.frequency == MsgFrequency.MEDIUM_FREQUENCY_MESSAGE:
                frequency_str = 'Medium'
            elif template.frequency == MsgFrequency.HIGH_FREQUENCY_MESSAGE:
                frequency_str = 'High'
            self.message_dict[(frequency_str, template.msg_num)] = template

    def build_message_ids(self):
        packer = DataPacker()
        for template in self.message_templates.values():
            frequency = template.frequency
            if frequency == MsgFrequency.FIXED_FREQUENCY_MESSAGE:
                template.msg_num_hex = b'\xff\xff\xff' + packer.pack_data(template.msg_num, MsgType.MVT_U8)
            elif frequency == MsgFrequency.LOW_FREQUENCY_MESSAGE:
                template.msg_num_hex = b'\xff\xff' + packer.pack_data(template.msg_num, MsgType.MVT_U16, EndianType.BIG)
            elif frequency == MsgFrequency.MEDIUM_FREQUENCY_MESSAGE:
                template.msg_num_hex = b'\xff' + packer.pack_data(template.msg_num, MsgType.MVT_U8, EndianType.BIG)
            elif frequency == MsgFrequency.HIGH_FREQUENCY_MESSAGE:
                template.msg_num_hex = packer.pack_data(template.msg_num, MsgType.MVT_U8, EndianType.BIG)

    def get_template(self, template_name):
        if template_name in self.message_templates:
            return self.message_templates[template_name]
        return

    def get_template_by_pair(self, frequency, num):
        if (
         frequency, num) in self.message_dict:
            return self.message_dict[(frequency, num)]
        return

    def __getitem__(self, i):
        return self.get_template(i)