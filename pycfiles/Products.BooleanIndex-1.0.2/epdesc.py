# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/epdesc.py
# Compiled at: 2012-02-27 07:41:53


class MetaEntryPointDescription(object):
    description = '\n    This is an entry point that describes other entry points.\n    '


class CreateTemplateDescription(object):
    description = '\n    Entry point for creating the file layout for a new project\n    from a template.\n    '


class PasterCommandDescription(object):
    description = '\n    Entry point that adds a command to the ``paster`` script\n    to a project that has specifically enabled the command.\n    '


class GlobalPasterCommandDescription(object):
    description = '\n    Entry point that adds a command to the ``paster`` script\n    globally.\n    '


class AppInstallDescription(object):
    description = '\n    This defines a runner that can install the application given a\n    configuration file.\n    '


class ConsoleScriptsDescription(object):
    description = '\n    When a package is installed, any entry point listed here will be\n    turned into a command-line script.\n    '


class DistutilsCommandsDescription(object):
    description = '\n    This will add a new command when running\n    ``python setup.py entry-point-name`` if the\n    package uses setuptools.\n    '


class SetupKeywordsDescription(object):
    description = "\n    This adds a new keyword to setup.py's setup() function, and a\n    validator to validate the value.\n    "


class EggInfoWriters(object):
    description = '\n    This adds a new writer that creates files in the PkgName.egg-info/\n    directory.\n    '