# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/config_handler.py
# Compiled at: 2015-08-07 10:15:35
import ConfigParser, os.path, re

class Parser(object):

    def __init__(self, file_object='file', filename=None):
        self.parser = ConfigParser.RawConfigParser()
        if file_object == 'file' and filename != None:
            if self.config_exists(filename) != True:
                print 'Creating config file at %s' % filename
                newf = open(filename, 'a')
                newf.close()
            assert self.config_exists(filename), 'ERROR: Could not find the configuration file.'
            self.parser.read(filename)
        if file_object == 'fp':
            self.parser.readfp(filename)
        return

    def get_setting(self, section, option):
        if self.has_section(section) == True and option in self.options(section):
            if self.parser.get(section, option) != '':
                return self.parser.get(section, option)
            else:
                return

        else:
            return
        return

    def sections(self):
        return self.parser.sections()

    def section_search(self, string):
        pattern = re.compile(string)
        matches = []
        for i in self.sections():
            if pattern.search(i) != None:
                matches.append(i)

        return matches

    def options(self, section):
        if self.has_section(section) == True:
            return self.parser.options(section)
        else:
            return
            return

    def has_section(self, section):
        return self.parser.has_section(section)

    def config_exists(self, file_loc):
        if os.path.exists(file_loc):
            return True
        else:
            return False