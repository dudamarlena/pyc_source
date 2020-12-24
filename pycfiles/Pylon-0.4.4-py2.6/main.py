# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\main.py
# Compiled at: 2010-12-26 13:36:33
""" Defines the entry point for Pylon.
"""
import os, sys, logging, optparse
from pylon.io import MATPOWERReader, PSSEReader, MATPOWERWriter, ReSTWriter, PickleReader, PickleWriter
from pylon import DCPF, NewtonPF, FastDecoupledPF, OPF, UDOPF
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger('pylon')

def read_case(input, format=None):
    """ Returns a case object from the given input file object. The data
    format may be optionally specified.
    """
    format_map = {'matpower': MATPOWERReader, 'psse': PSSEReader, 
       'pickle': PickleReader}
    if format_map.has_key(format):
        reader_klass = format_map[format]
        reader = reader_klass()
        case = reader.read(input)
    else:
        for reader_klass in format_map.values():
            reader = reader_klass()
            try:
                case = reader.read(input)
                if case is not None:
                    break
            except:
                pass

        else:
            case = None

        return case


def detect_data_file(input, file_name=''):
    """ Detects the format of a network data file according to the
        file extension and the header.
    """
    (_, ext) = os.path.splitext(file_name)
    if ext == '.m':
        line = input.readline()
        if line.startswith('function'):
            type = 'matpower'
            logger.info('Recognised MATPOWER data file.')
        elif line.startswith('Bus.con' or line.startswith('%')):
            type = 'psat'
            logger.info('Recognised PSAT data file.')
        else:
            type = 'unrecognised'
        input.seek(0)
    elif ext == '.raw' or ext == '.psse':
        type = 'psse'
        logger.info('Recognised PSS/E data file.')
    elif ext == '.pkl' or ext == '.pickle':
        type = 'pickle'
        logger.info('Recognised pickled case.')
    else:
        type = None
    return type


def main():
    """ Parses the command line and call Pylon with the correct data.
    """
    parser = optparse.OptionParser(usage='usage: pylon [options] input_file', version='%prog 0.4.2')
    parser.add_option('-o', '--output', dest='output', metavar='FILE', help='Write the solution report to FILE.')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Print more information.')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False, help='Print debug information.')
    parser.add_option('-t', '--input-type', dest='type', metavar='TYPE', default='any', help='The argument following the -t is used to indicate the format type of the input data file. The types which are currently supported include: matpower, psse [default: %default] If not specified Pylon will try to determine the type according to the file name extension and the file header.')
    parser.add_option('-s', '--solver', dest='solver', metavar='SOLVER', default='acpf', help="The argument following the -s is used toindicate the type of routine to use in solving. The types which are currently supported are: 'dcpf', 'acpf', 'dcopf', 'acopf', 'udopf' and 'none' [default: %default].")
    parser.add_option('-a', '--algorithm', action='store_true', metavar='ALGORITHM', dest='algorithm', default='newton', help="Indicates the algorithm type to be used for AC power flow. The types which are currently supported are: 'newton' and 'fdpf' [default: %default].")
    parser.add_option('-T', '--output-type', dest='output_type', metavar='OUTPUT_TYPE', default='rst', help='Indicates the output format type.  The type swhich are currently supported include: rst, matpower, csv, excel and none [default: %default].')
    (options, args) = parser.parse_args()
    if options.verbose:
        logger.setLevel(logging.INFO)
    elif options.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    if options.output:
        if options.output == '-':
            outfile = sys.stdout
            logger.setLevel(logging.CRITICAL)
        else:
            outfile = open(options.output, 'wb')
    else:
        outfile = sys.stdout
    if len(args) > 1:
        parser.print_help()
        sys.exit(1)
    elif len(args) == 0 or args[0] == '-':
        filename = ''
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        else:
            infile = sys.stdin
    else:
        filename = args[0]
        infile = open(filename, 'rb')
    if options.type == 'any':
        type = detect_data_file(infile, filename)
    else:
        type = options.type
    case = read_case(infile, type)
    if case is not None:
        if options.solver == 'dcpf':
            solver = DCPF(case)
        elif options.solver == 'acpf':
            if options.algorithm == 'newton':
                solver = NewtonPF(case)
            elif options.algorithm == 'fdpf':
                solver = FastDecoupledPF(case)
            else:
                logger.critical('Invalid algorithm [%s].' % options.algorithm)
                sys.exit(1)
        elif options.solver == 'dcopf':
            solver = OPF(case, True)
        elif options.solver == 'acopf':
            solver = OPF(case, False)
        elif options.solver == 'udopf':
            solver = UDOPF(case)
        elif options.solver == 'none':
            solver = None
        else:
            logger.critical('Invalid solver [%s].' % options.solver)
            solver = None
        if options.output_type == 'matpower':
            writer = MATPOWERWriter(case)
        elif options.output_type == 'rst':
            writer = ReSTWriter(case)
        elif options.output_type == 'csv':
            from pylon.io.excel import CSVWriter
            writer = CSVWriter(case)
        elif options.output_type == 'excel':
            from pylon.io.excel import ExcelWriter
            writer = ExcelWriter(case)
        elif options.output_type == 'pickle':
            writer = PickleWriter(case)
        else:
            logger.critical('Invalid output type [%s].' % options.output_type)
            sys.exit(1)
        if solver is not None:
            solver.solve()
        if options.output_type != 'none':
            writer.write(outfile)
    else:
        logger.critical('Unable to read case data.')
    if len(args) == 1:
        infile.close()
    if options.output and not options.output == '-':
        outfile.close()
    return


if __name__ == '__main__':
    main()