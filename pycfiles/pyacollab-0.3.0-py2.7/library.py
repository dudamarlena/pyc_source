# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/activecollab/library.py
# Compiled at: 2011-09-27 18:53:27
import urllib
from xml.dom.minidom import parse
from activecollab.settings import API_KEY, AC_URL
from activecollab.constants import *
from activecollab.exceptions import ACCommandException

class ACRequest(object):
    """ Makes a request to your Active Collab site and executes
        commands with a given API key. The returned XML is
        then parsed and returned in usable form """

    def __init__(self, command, item_id=None, subcommand=None, sub_id=None, **kwargs):
        if command not in AC_COMMANDS:
            raise ACCommandException('Not a valid command')
        if subcommand and subcommand not in AC_SUBCOMMAND:
            raise ACCommandException('Not a valid subcommand')
        if subcommand and not item_id:
            raise ACCommandException('Subcommands require a top level id')
        self.command = command
        self.item_id = item_id
        self.sub_id = sub_id
        self.subcommand = subcommand
        self.api_key = kwargs.get('api_key', API_KEY)
        self.ac_url = kwargs.get('ac_url', AC_URL)
        self.params = urllib.urlencode(kwargs.get('params', dict()))
        self.valid_fields = AC_BASE_FIELDS
        if self.subcommand:
            try:
                self.valid_fields += AC_SUB_FIELDS[self.subcommand]
            except KeyError:
                pass

    @property
    def base_url(self):
        """ Build our base API request URL"""
        return 'http://%s/api.php?token=%s&path_info=' % (
         self.ac_url, self.api_key)

    @property
    def command_url(self):
        """ This url is the base of all executed commands """
        url = self.base_url + self.command
        if self.item_id:
            url += '/' + str(self.item_id)
        if self.subcommand:
            url += '/' + self.subcommand
        if self.sub_id:
            url += '/' + self.sub_id
        if self.params:
            return '%s&%s' % (url, self.params)
        else:
            return url

    def execute(self):
        """ Make a request for the XML and parse the response """
        try:
            raw_xml = urllib.urlopen(self.command_url)
        except:
            raise ACCommandException('Could not execute command')

        xml = parse(raw_xml)
        if self.subcommand:
            items = xml.getElementsByTagName(AC_COMMAND_ELEMENT[self.subcommand])
        else:
            items = xml.getElementsByTagName(AC_COMMAND_ELEMENT[self.command])
        output = list()
        for item in items:
            item_str = ''
            for node in item.childNodes:
                if node.localName in self.valid_fields:
                    item_str += node.childNodes[0].nodeValue + AC_FIELD_SEP

            output.append(item_str)

        return [ o.rstrip(AC_FIELD_SEP) for o in output ]