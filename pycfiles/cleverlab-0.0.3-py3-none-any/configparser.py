# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/lib/configparser.py
# Compiled at: 2006-08-02 05:57:51
import os, ConfigParser
from harold.lib import config_expression

class HaroldConfigParser(ConfigParser.SafeConfigParser):
    """ Parser type for reading Clever Harold application .ini files

    There isn't much here yet, but it's where we'll build out template
    string handling and expression handling.
    """
    __module__ = __name__

    def as_dict(self):
        sections = [
         ConfigParser.DEFAULTSECT] + self.sections()
        config = {}
        for section in sections:
            normname = str.join(':', [ s.strip() for s in section.split(':') ])
            config[normname] = items = {}
            entries = dict(self.items(section))
            for (key, value) in entries.items():
                entries[key] = config_expression(value)

            items.update(entries)

        return config

    @classmethod
    def parse_file(cls, filename, defaults=None):
        if defaults is None:
            defaults = {}
        defaults['here'] = os.path.dirname(os.path.abspath(filename))
        defaults['__file__'] = os.path.abspath(filename)
        parser = cls(defaults=defaults)
        parser.read(filename)
        return parser.as_dict()


config_dict = HaroldConfigParser.parse_file