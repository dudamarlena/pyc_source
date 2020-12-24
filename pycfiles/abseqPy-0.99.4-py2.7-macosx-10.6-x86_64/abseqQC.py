# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/abseqQC.py
# Compiled at: 2019-04-23 02:08:32
"""
    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    
    Author: Monther Alhamdoosh    
    Python Version: 2.7
    Changes log: check git commits. 
"""
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