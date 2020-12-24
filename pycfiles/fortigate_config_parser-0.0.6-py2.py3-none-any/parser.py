# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/acidjunk/GIT/fortigate-config-parser/fortigate_parser/parser.py
# Compiled at: 2016-11-24 17:13:50


class ParserException(Exception):
    pass


class Parser(object):
    """
    The base class for all parsers. It's main function is to save parts of th econfig in a Object Oriented way. The
    goal of this design is to make sure users of the classes can use dot notation when the have loaded one or more
    config files.

    An example
    ----------
    with open('fortinet.conf') as f:
        config = f.read()
    fortigate = ConfigParser(config)
    fortigate.parse()
    # from here on you can use the dot notation
    zone_list = fortigate.global_section.
    zone_list = fortigate.vdom_sections['TEST_VDOM'].system_zone_section

    Implements functionality like return a splitted 
 string of the parsed config and various helper functions like:
    - ability to store unparsed config
    - ability to return the stored config in a Fortinet compliant way
    - ability to return config as a list, splitted by 

    - some easy metrics
    
    This makes it very easy to define Parser childs that 'sort of work' without really parsing the config.
    Writing more specialised classes, that really parse config, can be delegated to classes that we are interested in.
    This ensures a useful, and testable, parser at the start of the project which can gradually refined and enriched
    during the project.

    When self.parsed is set to True; the parser will return parsed content instead of the unhandled stored config file
    content.

    """
    parsed = False

    def __init__(self, config):
        self.config = config

    def parse(self):
        pass

    def unparse(self):
        if self.parsed:
            return self.config
        raise NotImplementedError

    def config_lines(self):
        return self.config.split('\n')

    def number_of_config_lines(self):
        return len(self.config_lines())


class ConfigParser(Parser):
    header = None
    global_section = None
    vdom_sections = {}

    def parse(self):
        config = self.config
        self.header = self.config_lines()[:4]
        print ('Found Header {0}').format(self.header)
        start = config.find('config global')
        end = config.find('end\n\nend\n') + 10
        self.global_section = GlobalSection(config[start:end])
        excluded_words = [
         'config', 'vdom', 'edit', 'next', 'end', '']
        global_vdoms = set(config[config.find('config vdom'):config.find('end')].replace('\n', ' ').split(' '))
        vdom_list = [ l for l in global_vdoms if l not in excluded_words ]
        for vdom in vdom_list:
            start = config.find(('config vdom\nedit {0}').format(vdom))
            end = config.find('\nend\nend\n', start) + 10
            print config[start:end]
            self.vdom_sections[vdom] = VDOMSection(config[start:end])

        print ('Found VDOMS {0}').format(vdom_list)
        self.parsed = True

    def init_subsections(self):
        pass


class GlobalSection(Parser):
    system_global_section = None
    system_accprofile_section = None
    system_np6_section = None
    system_replacemsg_section = None
    system_snmp_community = None


class VDOMSection(Parser):
    name = None
    system_settings_section = None
    system_zone_section = None

    def parse(self):
        config = self.config
        self.name = self.config_lines()[1].split(' ')[1]
        start = config.find('config system settings')
        end = config.find('end\n', start) + 4
        self.system_settings_section = SystemSettingsSection(config=config[start:end])
        start = config.find('config system zone')
        end = config.find('end\n', start) + 4
        print config[start:end]
        self.system_zone_section = SystemZoneSection(config=config[start:end])
        self.parsed = True


class SystemGlobalSection(Parser):
    pass


class SystemAccprofileSection(Parser):
    pass


class SystemSettingsSection(Parser):
    pass


class SystemZoneSection(Parser):
    zones = {}

    def parse(self):
        config_lines = self.config_lines()[1:-2]
        if not len(config_lines) % 3 == 0:
            raise ParserException
        for i in range(0, len(config_lines)):
            if i % 3 == 0:
                key = config_lines[i].replace('    edit "', '')[:-1]
                self.zones[key] = config_lines[(i + 1)].strip()

        self.parsed = True