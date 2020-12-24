# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maya/exp_runner/maya_utils.py
# Compiled at: 2019-06-13 05:22:46
# Size of source mod 2**32: 2213 bytes
import csv, os, psutil, json, datetime, time
from subprocess import call, check_output
import random, string
from .batch_command import BatchCommand

def run_batch(args):
    if args.debug != True:
        try:
            bc = BatchCommand(command=(args.command), source_dir=(args.source_dir), target_dir=(args.target_dir))
            print(bc.run())
        except:
            print('BatchCommand error')
            exit(1)

    else:
        bc = BatchCommand(command=(args.command), source_dir=(args.source_dir), target_dir=(args.target_dir))
        print(bc.run())