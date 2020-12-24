# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/devstage/ise-python-libraries/intelligence/phishme_intelligence/core/supported_integrations.py
# Compiled at: 2019-06-06 10:09:19
# Size of source mod 2**32: 4018 bytes
from __future__ import unicode_literals, absolute_import
import os, sys
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import RawConfigParser as ConfigParser

PYTHON_MAJOR_VERSION = sys.version_info[0]

def read_manifest(manifest_file=None):
    """
    Read PhishMe Intelligence integration manifest file

    :param str manifest_file: (optional) Path to PhishMe Intelligence integration manifest; defaults to './phishme_intelligence/output/manifest.ini'
    :return: PhishMe Intelligence integration manifest
    :rtype: ConfigParser
    """
    if manifest_file is None:
        manifest_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'manifest.ini')
    elif PYTHON_MAJOR_VERSION == 3:
        manifest = ConfigParser(interpolation=None)
    else:
        manifest = ConfigParser()
    manifest.read(manifest_file)
    return manifest


def import_libraries(config):
    """
    Returns the module and package that needs to be imported, depending on whether an integration is activated.

    :param ConfigParser config: PhishMe Intelligence configuration
    :return: list of integrations used by the installation (based on 'use' being set to True in the section)
    :rtype: list of :class:`phishme_intelligence.core.supported_integrations.SupportedIntegration`
    """
    supported_integrations = read_manifest()
    activated_integrations = []
    for integration in supported_integrations.sections():
        if config.has_section(integration) and config.getboolean(integration, 'use'):
            sample = SupportedIntegration(config_name=integration, mrti_format=(supported_integrations.get(integration, 'mrti_format')),
              output_product_module=(supported_integrations.get(integration, 'output_product_module')),
              class_name=(supported_integrations.get(integration, 'class_name')))
            config.set('pm_format', sample.mrti_format, 'True')
            activated_integrations.append(sample)

    return activated_integrations


class SupportedIntegration(object):
    __doc__ = '\n    Class for holding information for each integration enabled by a PhishMe Intelligence installation\n    '

    def __init__(self, config_name, mrti_format, output_product_module, class_name):
        """
        Initialize a SupportedIntegration object

        :param str config_name: Name of integration (section name e.g. integration_mcafee_siem)
        :param str mrti_format: format of data from PhishMe Intelligence API used by integration
        :param str output_product_module: Python classpath for integration module
        :param str class_name: Name of Python class for integration
        """
        self.config_name = config_name
        self.mrti_format = mrti_format
        self.output_product_module = output_product_module
        self.class_name = class_name