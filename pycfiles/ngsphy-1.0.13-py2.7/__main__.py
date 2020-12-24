# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngsphy/__main__.py
# Compiled at: 2018-02-15 07:08:26
import argparse, datetime, logging, ngsphy, os, sys, platform, loggingformatter as lf
VERSION = 1
MIN_VERSION = 0
FIX_VERSION = 13
PROGRAM_NAME = 'ngsphy.py'
AUTHOR = 'Merly Escalona <merlyescalona@uvigo.es>'
INSTITUTION = 'University of Vigo, Spain.'
LOG_LEVEL_CHOICES = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
LINE = '--------------------------------------------------------------------------------'
ch = logging.StreamHandler()
loggerFormatter = lf.MELoggingFormatter(fmt='%(asctime)s - %(levelname)s:\t%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
ch.setFormatter(loggerFormatter)
ch.setLevel(logging.NOTSET)
APPLOGGER = logging.getLogger('ngsphy')
APPLOGGER.addHandler(ch)

def createLogFile():
    formatString = ''
    if platform.system() == 'Darwin':
        formatString = '%(asctime)s - %(levelname)s (%(module)s:%(lineno)d):\t%(message)s'
    else:
        formatString = '%(asctime)s - %(levelname)s (%(module)s|%(funcName)s:%(lineno)d):\t%(message)s'
    logging.basicConfig(filename=os.path.join(os.getcwd(), ('{0}.{1:%Y}{1:%m}{1:%d}-{1:%H}:{1:%M}:{1:%S}.log').format(PROGRAM_NAME[0:-3].upper(), datetime.datetime.now())), level=logging.DEBUG, format=formatString)


def handlingCmdArguments():
    """
        handlingCmdArguments
        --------------------

        This function configurates the ArgumentParser with the specific details of
        this programs.

        Does not take parameters.
        """
    parser = argparse.ArgumentParser(prog=('{0} (v.{1}.{2}.{3})').format(PROGRAM_NAME, VERSION, MIN_VERSION, FIX_VERSION), formatter_class=argparse.RawDescriptionHelpFormatter, description='\x1b[1m\n================================================================================\n  NGSphy\n================================================================================\n\x1b[0m\nNGSphy is a Python open-source tool for the genome-wide simulation of NGS data\n(read counts or Illumina reads) obtained from thousands of gene families evolving\nunder a common species tree, with multiple haploid and/or diploid individuals per\nspecies, where sequencing coverage (depth) heterogeneity can vary among\nindividuals and loci, including off-target loci and phylogenetic decay effects.\n\nFor more information about usage and installation please go to the README file\nor to the wiki page https://gihub.com/merlyescalona/ngsphy/wiki/\n\t\t\t', epilog=('Developed by:\n{0}\n{1}\n\nVersion:\t{2}.{3}.{4} (Under development)\n{5}\n').format(AUTHOR, INSTITUTION, VERSION, MIN_VERSION, FIX_VERSION, LINE), add_help=False)
    optionalGroup = parser.add_argument_group(('{0}Optional arguments{1}').format('\x1b[1m', '\x1b[0m'))
    optionalGroup.add_argument('-s', '--settings', metavar='<settings_file_path>', type=str, help='Path to the settings file.')
    optionalGroup.add_argument('-l', '--log', metavar='<log_level>', type=str, choices=LOG_LEVEL_CHOICES, default='INFO', help=('Specified level of log that will be shown through the standard output. Log will be stored in a separate file when level==DEBUG. Values:{0}. Default: {1}. ').format(LOG_LEVEL_CHOICES, LOG_LEVEL_CHOICES[1]))
    informationGroup = parser.add_argument_group(('{0}Information arguments{1}').format('\x1b[1m', '\x1b[0m'))
    informationGroup.add_argument('-v', '--version', action='version', version=('{0}: Version {1}.{2}.{3}').format(PROGRAM_NAME, VERSION, MIN_VERSION, FIX_VERSION), help="Show program's version number and exit")
    informationGroup.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    status = True
    message = ''
    try:
        tmpArgs = parser.parse_args()
        if tmpArgs.help:
            parser.print_help()
        if tmpArgs.log == LOG_LEVEL_CHOICES[0]:
            APPLOGGER.setLevel(logging.DEBUG)
            createLogFile()
        if tmpArgs.log == LOG_LEVEL_CHOICES[1]:
            APPLOGGER.setLevel(logging.INFO)
        if tmpArgs.log == LOG_LEVEL_CHOICES[2]:
            APPLOGGER.setLevel(logging.WARNING)
        if tmpArgs.log == LOG_LEVEL_CHOICES[3]:
            APPLOGGER.setLevel(logging.ERROR)
    except:
        message = ('{0}\n{1}\n{2}\n').format('Something happened while parsing the arguments.', 'Please verify. Exiting.', LINE)
        APPLOGGER.error(message)
        parser.print_help()
        sys.exit(-1)

    if not tmpArgs.settings and not os.path.exists(os.path.abspath(os.path.join(os.getcwd(), 'settings.txt'))):
        parser.print_help()
    return tmpArgs


def main():
    """
        main()
        --------------------

        Entry point of the NGSphy program.
        """
    try:
        cmdArgs = handlingCmdArguments()
        prog = ngsphy.NGSphy(cmdArgs)
        prog.run()
    except ngsphy.NGSphyExitException as ex:
        if ex.expression:
            APPLOGGER.info('NGSphy finished properly.')
            APPLOGGER.info(('Elapsed time (ETA):\t{0}').format(ex.time))
            APPLOGGER.info(('Ending at:\t{0}').format(datetime.datetime.now().strftime('%a, %b %d %Y. %I:%M:%S %p')))
            sys.exit()
        else:
            APPLOGGER.error(ex.message)
            APPLOGGER.error(('Elapsed time (ETA):\t{0}').format(ex.time))
            APPLOGGER.error(('Ending at:\t{0}').format(datetime.datetime.now().strftime('%a, %b %d %Y. %I:%M:%S %p')))
            sys.exit(-1)
    except KeyboardInterrupt:
        APPLOGGER.error(('{0}{1}\nProgram has been interrupted.{2}\nPlease run again for the expected outcome.\n{3}\n').format('\x1b[91m', '\x1b[1m', '\x1b[0m', LINE))
        sys.exit(-1)


if __name__ == '__main__':
    main()