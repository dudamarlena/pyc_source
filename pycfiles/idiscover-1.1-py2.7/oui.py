# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/idiscover/oui.py
# Compiled at: 2014-05-26 11:27:58
import re
from pkg_resources import resource_filename

def get_oui_path():
    """
    Return the OUI file path.
    """
    return resource_filename(__name__, 'data/oui.txt')


class OUI(object):
    """ The OUI database
    """
    __shared_state = {}
    oui_file = get_oui_path()
    hex_manuf_pattern = re.compile('\\s+(?P<hex>\\S+)\\s+(\\(hex\\)|\\(base 16\\))\\s+(?P<manuf>.*)')

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.__parse_oui_file()

    def __parse_oui_file(self):
        if not hasattr(self, '__oui_db'):
            self.__oui_db = {}
            with open(self.oui_file) as (f):
                lines = f.readlines()
                for line in lines:
                    match = self.hex_manuf_pattern.match(line)
                    if match:
                        self.__oui_db[match.group('hex')] = match.group('manuf')

    def find_manuf(self, oui):
        return self.__oui_db.get(oui, None)


if __name__ == '__main__':
    oui = OUI()
    print oui.find_manuf('0080E5')
    print oui.find_manuf('00B04A')
    print oui.find_manuf('281878')