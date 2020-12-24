# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/scripts/convert.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
import os, argparse, sys, textwrap
from spreadsheetconverter import Converter, YamlConfig

def main(argv=sys.argv, quiet=False):
    command = ConvertCommand(argv, quiet)
    return command.run()


class ConvertCommand(object):
    description = b'    指定yamlで変換を実行します\n    '
    parser = argparse.ArgumentParser(description=textwrap.dedent(description))
    parser.add_argument(b'config', nargs=b'+', help=b'convert target yaml paths')
    parser.add_argument(b'--search_path', nargs=b'+', help=b'file search paths')
    parser.add_argument(b'--yaml_search_path', nargs=b'+', help=b'yaml file search paths')
    parser.add_argument(b'--yaml_search_recursive', type=bool, help=b'yaml file search recursive')
    parser.add_argument(b'--xls_search_path', nargs=b'+', help=b'xls file search paths')
    parser.add_argument(b'--xls_search_recursive', type=bool, help=b'xls file search recursive')
    parser.add_argument(b'--json_base_path', help=b'json file out path')
    parser.add_argument(b'--timezone', help=b'default timezone')

    def __init__(self, argv, quiet=False):
        self.quiet = quiet
        self.args = self.parser.parse_args(argv[1:])

    def out(self, msg):
        if not self.quiet:
            print msg

    def run(self, shell=None):
        if not self.args:
            self.out(b'Requires a config file argument')
            return 2
        else:
            print self.args
            if self.args.search_path:
                os.environ.setdefault(b'SSC_SEARCH_PATH', (b':').join(self.args.search_path))
            if self.args.yaml_search_path:
                os.environ.setdefault(b'SSC_YAML_SEARCH_PATH', (b':').join(self.args.yaml_search_path))
            if self.args.yaml_search_recursive is not None:
                os.environ.setdefault(b'SSC_YAML_SEARCH_RECURSIVE', b'1' if self.args.yaml_search_recursive else b'0')
            if self.args.xls_search_path:
                os.environ.setdefault(b'SSC_XLS_SEARCH_PATH', (b':').join(self.args.xls_search_path))
            if self.args.xls_search_recursive is not None:
                os.environ.setdefault(b'SSC_XLS_SEARCH_RECURSIVE', b'1' if self.args.xls_search_recursive else b'0')
            if self.args.json_base_path:
                os.environ.setdefault(b'SSC_JSON_BASE_PATH', self.args.json_base_path)
            if self.args.timezone:
                os.environ.setdefault(b'SSC_TIMEZONE', self.args.timezone)
            for config in self.args.config:
                converter = Converter(YamlConfig.get_config(config))
                converter.run()

            return


if __name__ == b'__main__':
    sys.exit(main() or 0)