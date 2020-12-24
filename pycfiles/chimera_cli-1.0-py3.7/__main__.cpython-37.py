# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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