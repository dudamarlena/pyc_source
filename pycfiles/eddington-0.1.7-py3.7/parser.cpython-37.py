# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/arguments/parser.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 6607 bytes
from argparse import ArgumentParser
from pathlib import Path
from eddington import __version__
import eddington.consts as ct
from eddington.arguments.general_functionalities import argument_string
from eddington.arguments.validation import validate_arguments

class LabUtilParser:
    _LabUtilParser__parser = None

    @classmethod
    def parse_and_validate(cls, argv=None):
        args = cls.parser().parse_args(argv)
        validate_arguments(args)
        return args

    @classmethod
    def print_help(cls):
        cls.parser().print_help()

    @classmethod
    def parser(cls):
        if cls._LabUtilParser__parser is None:
            cls._LabUtilParser__parser = cls._LabUtilParser__build_parser()
        return cls._LabUtilParser__parser

    @classmethod
    def clear_parser(cls):
        cls._LabUtilParser__parser = None

    @classmethod
    def __build_parser(cls):
        parser = ArgumentParser(description='Fit data to function according to theoretical model.')
        parser.add_argument('--version', action='version', version=__version__)
        parser.add_argument('func',
          type=str,
          nargs='*',
          help='\n            Model function to fit.\n            Enter "list" to list out fitting options.\n            Enter "syntax" and functions names to print the functions syntax.\n            ')
        parser.add_argument('-c',
          '--costumed', type=str, nargs='?', help='Costumed fitting function')
        parser.add_argument('--a0',
          type=float, nargs='+', help='Initial guess of parameters')
        parser.add_argument((argument_string(ct.OUTPUT_DIR)),
          type=Path,
          help='Output directory for plots and report')
        parser.add_argument('--x-column',
          type=str,
          default=(ct.DEFAULT_X_COLUMN),
          help='Column name or index of X values.\n            Default is column number %(default)s.\n            ')
        parser.add_argument('--xerr-column',
          type=str, help='Column name or index of X error values')
        parser.add_argument('--y-column',
          type=str, help='Column name or index of Y values')
        parser.add_argument('--yerr-column',
          type=str, help='Column name or index of Y error values')
        data_source_group = parser.add_mutually_exclusive_group()
        data_source_group.add_argument('--csv-data',
          type=str,
          help='CSV file from which to take the data to be fitted.')
        data_source_group.add_argument('--excel-data',
          nargs=2,
          type=str,
          help='Excel file from which to take the data to be fitted.')
        data_source_group.add_argument('--random-data',
          default=False,
          action='store_true',
          help='Generate random data for the fit function')
        plot_group = parser.add_argument_group(title='Plot',
          description='Arguments for plotting the data and fitting')
        plot_group.add_argument((ct.NO_PLOT),
          dest=(ct.PLOT),
          default=True,
          action='store_false',
          help='Do not show fitting plots.')
        plot_group.add_argument((argument_string(ct.TITLE)),
          nargs='?', type=str, help='Plot title')
        plot_group.add_argument((argument_string(ct.RESIDUALS_TITLE)),
          nargs='?',
          type=str,
          help='Residuals plot title')
        plot_group.add_argument((argument_string(ct.XLABEL)),
          nargs='?',
          type=str,
          help='\n            Label for the x coordinate.\n            If not given, will take x header in data file.\n            ')
        plot_group.add_argument((argument_string(ct.YLABEL)),
          nargs='?',
          type=str,
          help='\n            Label for the y coordinate.\n            If not given, will take y header in data file.\n            ')
        plot_group.add_argument('--plot-data',
          default=False,
          action='store_true',
          help='Add plot data points without fitting result')
        plot_group.add_argument('--grid',
          default=False,
          action='store_true',
          help='\n            Label for the y coordinate.\n            If not given, will take y header in data file.\n            ')
        random_data_group = parser.add_argument_group(title='Random Data',
          description='Arguments for data randomization')
        random_data_group.add_argument('--actual-a',
          nargs='*',
          type=float,
          help='Actual value of a. If not given, chosen randomly')
        random_data_group.add_argument('--min-coeff',
          nargs='+',
          type=float,
          default=(ct.DEFAULT_MIN_COEFF),
          help='Minimum coefficient for parameter. Default is %(default)s.')
        random_data_group.add_argument('--max-coeff',
          nargs='+',
          type=float,
          default=(ct.DEFAULT_MAX_COEFF),
          help='Maximum coefficient for parameter. Default is %(default)s.')
        random_data_group.add_argument('--measurements',
          nargs='?',
          type=int,
          default=(ct.DEFAULT_MEASUREMENTS),
          help='How many measurements to produce. Default is %(default)s.')
        random_data_group.add_argument('--xmin',
          nargs='?',
          type=float,
          default=(ct.DEFAULT_XMIN),
          help='Minimum x value. Default is %(default)s.')
        random_data_group.add_argument('--xmax',
          nargs='?',
          type=float,
          default=(ct.DEFAULT_XMAX),
          help='Maximum x value. Default is %(default)s.')
        random_data_group.add_argument('--xsigma',
          nargs='?',
          type=float,
          default=(ct.DEFAULT_XSIGMA),
          help='Standard derivation of x errors. Default is %(default)s.')
        random_data_group.add_argument('--ysigma',
          nargs='?',
          type=float,
          default=(ct.DEFAULT_YSIGMA),
          help='Standard derivation of y errors. Default is %(default)s.')
        return parser