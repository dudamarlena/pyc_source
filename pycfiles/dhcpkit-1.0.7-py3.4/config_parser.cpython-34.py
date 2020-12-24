# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/config_parser.py
# Compiled at: 2017-06-23 16:45:53
# Size of source mod 2**32: 4115 bytes
"""
Configuration file definition and parsing
"""
import inspect, logging, os, ZConfig.info
from ZConfig import SchemaResourceError
from ZConfig.loader import ConfigLoader, SchemaLoader
from ZConfig.schema import BaseParser
from dhcpkit.ipv6.server.config_elements import MainConfig
from dhcpkit.ipv6.server.extension_registry import server_extension_registry
logger = logging.getLogger(__name__)

def get_config_loader() -> ConfigLoader:
    """
    Get the config loader with all extensions

    :return: The fully extended config loader
    """
    schema_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config_schema.xml'))
    if 'schema' not in BaseParser._allowed_parents['example']:
        BaseParser._allowed_parents['example'].append('schema')
        ZConfig.info.SchemaType.example = None
        ZConfig.info.oldCreateDerivedSchema = ZConfig.info.createDerivedSchema

        def patchedCreateDerivedSchema(base: ZConfig.info.SchemaType) -> ZConfig.info.SchemaType:
            """
            Also copy the example section.

            :param base: The original
            :return: The copy
            """
            new = ZConfig.info.oldCreateDerivedSchema(base)
            new.example = base.example
            return new

        ZConfig.info.createDerivedSchema = patchedCreateDerivedSchema
    if 'sectiontype' not in BaseParser._allowed_parents['example']:
        BaseParser._allowed_parents['example'].append('sectiontype')
        ZConfig.info.SectionType.example = None
    if 'section' not in BaseParser._allowed_parents['example']:
        BaseParser._allowed_parents['example'].append('section')
        ZConfig.info.SectionInfo.example = None
    if 'multisection' not in BaseParser._allowed_parents['example']:
        BaseParser._allowed_parents['example'].append('multisection')
        ZConfig.info.SectionInfo.example = None
    schema_loader = SchemaLoader()
    schema = schema_loader.loadURL(url=schema_filename)
    config_loader = ConfigLoader(schema=schema)
    for extension_name, extension in server_extension_registry.items():
        if inspect.ismodule(extension) and hasattr(extension, '__path__'):
            try:
                config_loader.importSchemaComponent(extension.__name__)
                logger.debug('Configuration extension {} loaded'.format(extension_name))
            except SchemaResourceError:
                pass

            continue

    return config_loader


def load_config(config_filename: str) -> MainConfig:
    """
    Load the given configuration file.

    :param config_filename: The configuration file
    :return: The parsed config
    """
    logger.debug('Loading configuration file {}'.format(config_filename))
    config_loader = get_config_loader()
    config_filename = os.path.realpath(config_filename)
    config, handlers = config_loader.loadURL(config_filename)
    return config