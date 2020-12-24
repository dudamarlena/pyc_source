# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lib/chimera_cli/__main__.py
# Compiled at: 2019-12-26 07:55:18
# Size of source mod 2**32: 307 bytes
from lib.chimera_cli.parsing import main_parser
from lib.chimera_cli.api import chimera_rest_api
from lib.chimera_cli.yaml_config import configuration_files
if __name__ == '__main__':
    config = main_parser.parse_args()
    if config.subcommand == 'deploy':
        files = configuration_files()