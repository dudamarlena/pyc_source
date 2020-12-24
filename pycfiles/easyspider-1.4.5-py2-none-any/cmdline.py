# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/core/cmdline.py
# Compiled at: 2017-10-01 02:36:17
"""
    copy from scrapy
"""
import sys, optparse, easyspider
from scrapy.cmdline import _run_command
from scrapy.cmdline import _print_header
from scrapy.cmdline import _run_print_help
from scrapy.cmdline import _pop_command_name
from scrapy.cmdline import _get_commands_dict
from scrapy.cmdline import _print_unknown_command
from scrapy.cmdline import _get_commands_from_module
from scrapy.cmdline import _get_commands_from_entry_points
from scrapy.settings.deprecated import check_deprecated_settings
from scrapy.utils.project import inside_project, get_project_settings
from easycrawler import easyCrawlerProcess

def _print_header(settings, inproject):
    if inproject:
        print 'easyspider %s - project: %s\n' % (easyspider.__version__,
         settings['BOT_NAME'])
    else:
        print 'easyspider %s - no active project\n' % easyspider.__version__


def _get_commands_dict(settings, inproject):
    cmds = _get_commands_from_module('easyspider.commands', inproject)
    cmds.update(_get_commands_from_entry_points(inproject))
    cmds_module = settings['COMMANDS_MODULE']
    if cmds_module:
        cmds.update(_get_commands_from_module(cmds_module, inproject))
    return cmds


def _print_commands(settings, inproject):
    _print_header(settings, inproject)
    print 'Usage:'
    print '  easyspider <command> [options] [args]\n'
    print 'Available commands:'
    cmds = _get_commands_dict(settings, inproject)
    for cmdname, cmdclass in sorted(cmds.items()):
        print '  %-13s %s' % (cmdname, cmdclass.short_desc())

    if not inproject:
        print
        print '  [ more ]      More commands available when run from project directory'
    print
    print 'Use "easyspider <command> -h" to see more info about a command'


def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv
    if settings is None and 'scrapy.conf' in sys.modules:
        from scrapy import conf
        if hasattr(conf, 'settings'):
            settings = conf.settings
    if settings is None:
        print 'settings is None \n\n\n'
        settings = get_project_settings()
    check_deprecated_settings(settings)
    import warnings
    from scrapy.exceptions import ScrapyDeprecationWarning
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', ScrapyDeprecationWarning)
        from scrapy import conf
        conf.settings = settings
    inproject = inside_project()
    cmds = _get_commands_dict(settings, inproject)
    cmdname = _pop_command_name(argv)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), conflict_handler='resolve')
    if not cmdname:
        _print_commands(settings, inproject)
        sys.exit(0)
    elif cmdname not in cmds:
        _print_unknown_command(settings, cmdname, inproject)
        sys.exit(2)
    cmd = cmds[cmdname]
    parser.usage = 'scrapy %s %s' % (cmdname, cmd.syntax())
    parser.description = cmd.long_desc()
    settings.setdict(cmd.default_settings, priority='command')
    cmd.settings = settings
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    _run_print_help(parser, cmd.process_options, args, opts)
    cmd.crawler_process = easyCrawlerProcess(settings)
    _run_print_help(parser, _run_command, cmd, args, opts)
    sys.exit(cmd.exitcode)
    return


if __name__ == '__main__':
    execute()