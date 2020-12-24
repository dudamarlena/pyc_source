# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/parse/configfile.py
# Compiled at: 2019-04-23 22:11:57
# Size of source mod 2**32: 2217 bytes
import os
from configparser import ConfigParser
from pocsuite3.lib.core.data import logger, cmd_line_options, conf
from pocsuite3.lib.core.enums import OPTION_TYPE
from pocsuite3.lib.core.exception import PocsuiteFilePathException, PocsuiteMissingMandatoryOptionException, PocsuiteValueException
from pocsuite3.lib.core.optiondict import optDict

def config_file_parser(configFile):
    """
    Parse configuration file and save settings into the configuration
    advanced dictionary.
    """
    debugMsg = 'parsing configuration file'
    logger.debug(debugMsg)
    if not os.path.isfile(configFile):
        raise PocsuiteFilePathException("file '{}' don't exist".format(configFile))
    config = ConfigParser()
    config.read(configFile)
    if not config.has_section('Target'):
        errMsg = "missing a mandatory section 'Target' in the configuration file"
        raise PocsuiteMissingMandatoryOptionException(errMsg)
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        if options:
            for option in options:
                datatype = 'string'
                try:
                    datatype = optDict[section][option]
                except KeyError:
                    pass

                try:
                    if datatype == OPTION_TYPE.BOOLEAN:
                        value = config.getboolean(section, option) if config.get(section, option) else False
                    else:
                        if datatype == OPTION_TYPE.INTEGER:
                            value = config.getint(section, option) if config.get(section, option) else 0
                        else:
                            if datatype == OPTION_TYPE.FLOAT:
                                value = config.getfloat(section, option) if config.get(section, option) else 0.0
                            else:
                                value = config.get(section, option)
                except ValueError as ex:
                    try:
                        errMsg = 'error occurred while processing the option '
                        errMsg += "'%s' in provided configuration file ('%s')" % (option, ex)
                        raise PocsuiteValueException(errMsg)
                    finally:
                        ex = None
                        del ex

                if value:
                    conf[option] = value