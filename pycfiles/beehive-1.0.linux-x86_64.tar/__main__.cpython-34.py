# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/__main__.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 4206 bytes
import sys
from beehive import __version__
from beehive.configuration import Configuration, ConfigError
from beehive.runner import Runner
from beehive.runner_util import print_undefined_step_snippets, InvalidFileLocationError, InvalidFilenameError, FileNotFoundError
from beehive.parser import ParserError
TAG_HELP = '\nScenarios inherit tags declared on the Feature level. The simplest\nTAG_EXPRESSION is simply a tag::\n\n    --tags @dev\n\nYou may even leave off the "@" - beehive doesn\'t mind.\n\nWhen a tag in a tag expression starts with a ~, this represents boolean NOT::\n\n    --tags ~@dev\n\nA tag expression can have several tags separated by a comma, which represents\nlogical OR::\n\n    --tags @dev,@wip\n\nThe --tags option can be specified several times, and this represents logical\nAND, for instance this represents the boolean expression\n"(@foo or not @bar) and @zap"::\n\n    --tags @foo,~@bar --tags @zap.\n\nBeware that if you want to use several negative tags to exclude several tags\nyou have to use logical AND::\n\n    --tags ~@fixme --tags ~@buggy.\n'.strip()

def main(args=None):
    config = Configuration(args)
    if config.version:
        print('beehive ' + __version__)
        return 0
    if config.tags_help:
        print(TAG_HELP)
        return 0
    if config.lang_list:
        from beehive.i18n import languages
        iso_codes = languages.keys()
        iso_codes.sort()
        print('Languages available:')
        for iso_code in iso_codes:
            native = languages[iso_code]['native'][0]
            name = languages[iso_code]['name'][0]
            print('%s: %s / %s' % (iso_code, native, name))

        return 0
    if config.lang_help:
        from beehive.i18n import languages
        if config.lang_help not in languages:
            print('%s is not a recognised language: try --lang-list' % config.lang_help)
            return 1
        trans = languages[config.lang_help]
        print('Translations for %s / %s' % (trans['name'][0],
         trans['native'][0]))
        for kw in trans:
            if kw in 'name native'.split():
                continue
            print('%16s: %s' % (kw.title().replace('_', ' '),
             ', '.join(w for w in trans[kw] if w != '*')))

        return 0
    if not config.format:
        config.format = [
         config.default_format]
    elif config.format:
        if 'format' in config.defaults:
            if len(config.format) == len(config.defaults['format']):
                config.format.append(config.default_format)
    if 'help' in config.format:
        from beehive.formatter import formatters
        print('Available formatters:')
        formatters.list_formatters(sys.stdout)
        return 0
    if len(config.outputs) > len(config.format):
        print('CONFIG-ERROR: More outfiles (%d) than formatters (%d).' % (
         len(config.outputs), len(config.format)))
        return 1
    failed = True
    runner = Runner(config)
    try:
        failed = runner.run()
    except ParserError as e:
        print('ParseError: %s' % e)
    except ConfigError as e:
        print('ConfigError: %s' % e)
    except FileNotFoundError as e:
        print('FileNotFoundError: %s' % e)
    except InvalidFileLocationError as e:
        print('InvalidFileLocationError: %s' % e)
    except InvalidFilenameError as e:
        print('InvalidFilenameError: %s' % e)

    if config.show_snippets:
        if runner.undefined_steps:
            print_undefined_step_snippets(runner.undefined_steps, colored=config.color)
    return_code = 0
    if failed:
        return_code = 1
    return return_code


if __name__ == '__main__':
    sys.exit(main())