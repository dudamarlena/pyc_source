# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/short_reads_pipeline/tools/deepargClass.py
# Compiled at: 2019-06-06 15:01:54
import os, sys

def run(R, data, path_to_deeparg='/deeparg/'):
    try:
        cmd = (' ').join([
         'python ' + path_to_deeparg + 'deepARG.py',
         '--align',
         '--type nucl',
         '--reads',
         '--input', R,
         '--output', R + '.deeparg',
         '--iden', str(data['deep_arg_parameters']['identity']),
         '--prob', str(data['deep_arg_parameters']['probability']),
         '--evalue', str(data['deep_arg_parameters']['evalue'])])
        print cmd
        x = os.popen(cmd).read()
        return True
    except Exception as inst:
        print str(inst)
        return False


def dsize(path_to_deeparg):
    return {i.split()[0].split('|')[(-1)].upper():i.split() for i in open(path_to_deeparg + '/database/v2/features.gene.length')}