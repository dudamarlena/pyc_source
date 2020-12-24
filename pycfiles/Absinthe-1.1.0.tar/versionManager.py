# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/versionManager.py
# Compiled at: 2019-04-23 02:08:32
import argparse, os, numpy, pandas, Bio, datetime
from subprocess import check_output, CalledProcessError
from abseqPy.config import VERSION

def writeParams(args, outDir):
    """
    Writes the parameters used for analysis into analysis.params

    :param args: argparse.Namespace or dict type
            argparse namespace object, or a dict

    :param outDir: string
            output directory where analysis.params reside

    :return: string
            the filename that was produced in outDir
    """
    if isinstance(args, argparse.Namespace):
        args = vars(args)
    elif isinstance(args, dict):
        pass
    else:
        raise Exception(('Unsupported parameter type {}, expecting argparse.Namespace or dict').format(type(args)))
    filename = os.path.join(outDir, 'analysis.params')
    with open(filename, 'w') as (out):
        out.write('AbSeqPy version: ' + VERSION + '\n')
        out.write('IMGT version - IMGT database directory last modified time : ' + _getIMGTDate(args['database']) + '\n')
        merger = args.get('merger', None)
        if merger:
            out.write(('{} version: ').format(merger) + _getSoftwareVersion(merger) + '\n')
        out.write('IgBLAST version: ' + _getSoftwareVersion('igblast') + '\n')
        out.write('pandas version: ' + str(pandas.__version__) + '\n')
        out.write('numpy version: ' + str(numpy.__version__) + '\n')
        out.write('biopy version: ' + str(Bio.__version__) + '\n')
        out.write('FastQC version: ' + _getSoftwareVersion('fastqc') + '\n')
        out.write('Clustalo version: ' + _getSoftwareVersion('clustalo') + '\n')
        out.write('Executed AbSeqPy with the following parameters:\n')
        for key, val in args.items():
            out.write(('Parameter: {:17}\tValue: {:>20}\n').format(key, os.path.expandvars(str(val))))

    return os.path.basename(filename)


def _getSoftwareVersion(prog):
    """
    taken as-is from setup.py (flash version modification)
    :param prog: program name. Possible values: igblast, clustalo, fastqc, gs, leehom, flash
    :return:
    """
    try:
        if prog == 'igblast':
            retval = check_output(['igblastn', '-version']).split('\n')[1].strip().split()[2].rstrip(',')
            try:
                return retval.decode()
            except AttributeError:
                return retval

        else:
            if prog == 'clustalo' or prog == 'fastqc' or prog == 'gs':
                retval = check_output([prog, '--version'])
                try:
                    retval = retval.decode().strip()
                except AttributeError:
                    retval = retval.strip()

                if prog == 'fastqc':
                    retval = retval.split()[(-1)].strip().lstrip('v')
                return str(retval)
            if prog == 'leehom':
                check_output(['which', 'leeHomMulti'])
                return '-'
            if prog == 'flash':
                retval = check_output(['flash', '--version'])
                try:
                    retval = retval.decode()
                except AttributeError:
                    retval = retval

                return retval.split('\n')[0].split()[(-1)].lstrip('v')
    except (CalledProcessError, OSError):
        return 'Not found'


def _getIMGTDate(fname):
    fname = os.path.abspath(os.path.expandvars(fname))
    if os.path.exists(fname):
        return str(datetime.datetime.fromtimestamp(os.path.getmtime(fname)).replace(microsecond=0))
    return '-'