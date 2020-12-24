# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/start_converter.py
# Compiled at: 2015-10-23 11:42:36
# Size of source mod 2**32: 363 bytes
import online_monitor.utils as utils
from online_monitor.converter.converter_manager import ConverterManager

def main():
    args = utils.parse_arguments()
    utils.setup_logging(args.log)
    cm = ConverterManager(args.config_file)
    cm.start()


if __name__ == '__main__':
    main()