# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/commands/debug.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 7275 bytes
from __future__ import absolute_import
import locale, logging, os, sys, pip._vendor
from pip._vendor import pkg_resources
from pip._vendor.certifi import where
from pip import __file__ as pip_location
from pip._internal.cli import cmdoptions
from pip._internal.cli.base_command import Command
from pip._internal.cli.cmdoptions import make_target_python
from pip._internal.cli.status_codes import SUCCESS
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import get_pip_version
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from types import ModuleType
    from typing import Any, List, Optional, Dict
    from optparse import Values
logger = logging.getLogger(__name__)

def show_value(name, value):
    logger.info('{}: {}'.format(name, value))


def show_sys_implementation():
    logger.info('sys.implementation:')
    if hasattr(sys, 'implementation'):
        implementation = sys.implementation
        implementation_name = implementation.name
    else:
        implementation_name = ''
    with indent_log():
        show_value('name', implementation_name)


def create_vendor_txt_map():
    vendor_txt_path = os.path.join(os.path.dirname(pip_location), '_vendor', 'vendor.txt')
    with open(vendor_txt_path) as (f):
        lines = [line.strip().split(' ', 1)[0] for line in f.readlines() if '==' in line]
    return dict((line.split('==', 1) for line in lines))


def get_module_from_module_name(module_name):
    module_name = module_name.lower()
    if module_name == 'setuptools':
        module_name = 'pkg_resources'
    __import__(('pip._vendor.{}'.format(module_name)),
      (globals()),
      (locals()),
      level=0)
    return getattr(pip._vendor, module_name)


def get_vendor_version_from_module(module_name):
    module = get_module_from_module_name(module_name)
    version = getattr(module, '__version__', None)
    if not version:
        pkg_set = pkg_resources.WorkingSet([
         os.path.dirname(getattr(module, '__file__'))])
        package = pkg_set.find(pkg_resources.Requirement.parse(module_name))
        version = getattr(package, 'version', None)
    return version


def show_actual_vendor_versions(vendor_txt_versions):
    for module_name, expected_version in vendor_txt_versions.items():
        extra_message = ''
        actual_version = get_vendor_version_from_module(module_name)
        if not actual_version:
            extra_message = ' (Unable to locate actual module version, using vendor.txt specified version)'
            actual_version = expected_version
        else:
            if actual_version != expected_version:
                extra_message = ' (CONFLICT: vendor.txt suggests version should be {})'.format(expected_version)
        logger.info('{name}=={actual}{extra}'.format(name=module_name,
          actual=actual_version,
          extra=extra_message))


def show_vendor_versions():
    logger.info('vendored library versions:')
    vendor_txt_versions = create_vendor_txt_map()
    with indent_log():
        show_actual_vendor_versions(vendor_txt_versions)


def show_tags(options):
    tag_limit = 10
    target_python = make_target_python(options)
    tags = target_python.get_tags()
    formatted_target = target_python.format_given()
    suffix = ''
    if formatted_target:
        suffix = ' (target: {})'.format(formatted_target)
    msg = 'Compatible tags: {}{}'.format(len(tags), suffix)
    logger.info(msg)
    if options.verbose < 1 and len(tags) > tag_limit:
        tags_limited = True
        tags = tags[:tag_limit]
    else:
        tags_limited = False
    with indent_log():
        for tag in tags:
            logger.info(str(tag))

        if tags_limited:
            msg = '...\n[First {tag_limit} tags shown. Pass --verbose to show all.]'.format(tag_limit=tag_limit)
            logger.info(msg)


def ca_bundle_info(config):
    levels = set()
    for key, value in config.items():
        levels.add(key.split('.')[0])

    if not levels:
        return 'Not specified'
    else:
        levels_that_override_global = [
         'install', 'wheel', 'download']
        global_overriding_level = [level for level in levels if level in levels_that_override_global]
        return global_overriding_level or 'global'
    if 'global' in levels:
        levels.remove('global')
    return ', '.join(levels)


class DebugCommand(Command):
    __doc__ = '\n    Display debug information.\n    '
    usage = '\n      %prog <options>'
    ignore_require_venv = True

    def __init__(self, *args, **kw):
        (super(DebugCommand, self).__init__)(*args, **kw)
        cmd_opts = self.cmd_opts
        cmdoptions.add_target_python_options(cmd_opts)
        self.parser.insert_option_group(0, cmd_opts)
        self.parser.config.load()

    def run(self, options, args):
        logger.warning('This command is only meant for debugging. Do not use this with automation for parsing and getting these details, since the output and options of this command may change without notice.')
        show_value('pip version', get_pip_version())
        show_value('sys.version', sys.version)
        show_value('sys.executable', sys.executable)
        show_value('sys.getdefaultencoding', sys.getdefaultencoding())
        show_value('sys.getfilesystemencoding', sys.getfilesystemencoding())
        show_value('locale.getpreferredencoding', locale.getpreferredencoding())
        show_value('sys.platform', sys.platform)
        show_sys_implementation()
        show_value("'cert' config value", ca_bundle_info(self.parser.config))
        show_value('REQUESTS_CA_BUNDLE', os.environ.get('REQUESTS_CA_BUNDLE'))
        show_value('CURL_CA_BUNDLE', os.environ.get('CURL_CA_BUNDLE'))
        show_value('pip._vendor.certifi.where()', where())
        show_value('pip._vendor.DEBUNDLED', pip._vendor.DEBUNDLED)
        show_vendor_versions()
        show_tags(options)
        return SUCCESS