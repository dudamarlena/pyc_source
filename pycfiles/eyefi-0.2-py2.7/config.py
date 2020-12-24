# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/config.py
# Compiled at: 2012-01-03 19:27:38
import os
from configglue.inischema.glue import ini2schema
from twisted.python import usage
from pkg_resources import Requirement, resource_filename
base = resource_filename(Requirement.parse('eyefi'), 'conf/base.conf')
confs = (
 '/etc/eyefi.conf',
 os.path.expanduser('~/.eyefi.conf'),
 'eyefi.conf')

def glue_config(confs=confs, base=base):
    config_parser = ini2schema(open(base))
    config_parser.read(confs)
    return config_parser


def get_cards(config_parser):
    cards = {}
    for sec in config_parser.sections():
        if sec == '__main__':
            continue
        d = {'name': sec}
        d.update(config_parser.values('card'))
        for k, v in config_parser.items(sec):
            d[k] = config_parser.parse('card', k, v)

        if not d['active']:
            continue
        cards[d['macaddress']] = d

    return cards


def twisted_schemaconfigglue(parser, argv=None):
    """Populate an usage.Options subclass with options and defaults
    taken from a fully loaded SchemaConfigParser. After the Options
    instance has parse the options, the SchemaConfigParser is updated.
    """

    def long_name(option):
        if option.section.name == '__main__':
            return option.name
        return option.section.name + '_' + option.name

    def opt_name(option):
        return long_name(option).replace('-', '_')

    schema = parser.schema
    params = []
    for section in schema.sections():
        for option in section.options():
            params.append([long_name(option), None,
             parser.get(section.name, option.name), option.help])

    class Options(usage.Options):
        optParameters = params

        def postOptions(self):
            for section in schema.sections():
                for option in section.options():
                    value = self[opt_name(option)]
                    if parser.get(section.name, option.name) != value:
                        parser.set(section.name, option.name, value)

    return Options