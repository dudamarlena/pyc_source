# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/cli/summarycombine.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 1552 bytes
from pesummary.core.command_line import command_line
from pesummary.gw.command_line import insert_gwspecific_option_group, add_dynamic_PSD_to_namespace, add_dynamic_calibration_to_namespace
from pesummary.utils import functions
__doc__ = 'This executable is used to combine multiple result files into a\nsingle PESummary metafile'

def main(args=None):
    """Top level interface for `summarycombine`
    """
    parser = command_line()
    insert_gwspecific_option_group(parser)
    opts, unknown = parser.parse_known_args(args=args)
    add_dynamic_PSD_to_namespace(opts)
    add_dynamic_calibration_to_namespace(opts)
    func = functions(opts)
    args = func['input'](opts)
    func['MetaFile'](args)


if __name__ == '__main__':
    main()