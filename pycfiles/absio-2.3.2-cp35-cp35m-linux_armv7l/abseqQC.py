# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/abseqQC.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\n    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    \n    Author: Monther Alhamdoosh    \n    Python Version: 2.7\n    Changes log: check git commits. \n'
import sys, time, traceback, warnings
from datetime import timedelta
from abseqPy.IgMultiRepertoire.IgMultiRepertoire import IgMultiRepertoire
from abseqPy.argsParser import parseArgs
from abseqPy.config import VERSION
from abseqPy.utilities import PriorityPath
from abseqPy.logger import formattedTitle
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
__version__ = VERSION

def main():
    startTimeStr = time.strftime('%Y-%m-%d %H:%M:%S')
    startTime = time.time()
    try:
        try:
            with PriorityPath():
                argsVals = parseArgs()
                with IgMultiRepertoire(argsVals) as (igRepertoire):
                    print formattedTitle(argsVals.task, argsVals.yaml is not None)
                    igRepertoire.start()
                print 'The analysis started at ' + startTimeStr
                print ('The analysis took {}').format(timedelta(seconds=int(round(time.time() - startTime))))
                print 'AbSeqPy version ' + VERSION
        except Exception as e:
            print 'Unexpected error: ' + str(e)
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60

    finally:
        pass

    return