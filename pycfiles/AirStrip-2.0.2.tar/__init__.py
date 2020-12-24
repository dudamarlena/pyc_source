# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmp/dev/projects/jsboot/airstrip.js/airstrip/__init__.py
# Compiled at: 2013-04-26 20:49:54
__title__ = 'airstrip'
__version__ = '2.0.2'
__build__ = 5120
__author__ = 'WebItUp'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 WebItUp'
import sys, logging, os, traceback, pkg_resources
from optparse import OptionParser
import puke
try:
    sys.path.insert(1, os.getcwd())
except:
    pass

def run():
    """ Main routine which should be called on startup """
    parser = OptionParser()
    parser.add_option('-v', '--version', action='store_true', dest='version', help='get version')
    options, args = parser.parse_args()
    consoleCfg = logging.StreamHandler()
    consoleCfg.setFormatter(logging.Formatter(' %(message)s', '%H:%M:%S'))
    logging.getLogger().addHandler(consoleCfg)
    logging.getLogger().setLevel(logging.DEBUG)
    if options.version:
        print 'AirStrip %s' % __version__
        sys.exit(0)
    if os.path.isfile('.pukeignore'):
        try:
            f = open('.pukeignore', 'r')
            for line in f:
                puke.FileList.addGlobalExclude(line.strip())

        except Exception as e:
            print 'Puke ignore error : %s' % e

    pukefiles = [
     'pukefile', 'pukeFile', 'pukefile', 'pukefile.py', 'pukeFile.py', 'pukefile.py']
    working_dir = os.path.dirname(os.path.realpath(__file__))
    script = None
    for name in pukefiles:
        if os.path.isfile(os.path.join(working_dir, name)):
            script = os.path.join(working_dir, name)

    retval = execfile(script)
    try:
        args = args.strip()
    except:
        pass

    if not args:
        if puke.hasDefault():
            puke.executeTask('default')
        else:
            logging.error('No tasks to execute. Please choose from: ')
            puke.printTasks()
            sys.exit(1)
    else:
        name = args.pop(0)
        puke.executeTask(name.strip(), *args)
    return


def gettraceback(level=0):
    trace = ''
    exception = ''
    exc_list = traceback.format_exception_only(sys.exc_type, sys.exc_value)
    reverse = -1 - level
    for entry in exc_list:
        exception += entry

    tb_list = traceback.format_tb(sys.exc_info()[2])
    for entry in tb_list[reverse]:
        trace += entry

    return trace


def main():
    try:
        run()
    except Exception as error:
        print 'ERROR %s \n %s \n' % (error, gettraceback())
        sys.exit(1)
    except KeyboardInterrupt:
        print 'Build interrupted!\n'
        sys.exit(2)

    sys.exit(0)