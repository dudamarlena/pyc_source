# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/argdb/train_arc.py
# Compiled at: 2019-06-05 13:08:57
import cPickle, train_deepARG, make_XY, process_blast, sys, os
path = sys.argv[1]
version = sys.argv[2]
os.system('mkdir -p ' + path + '/' + version)
alignments1 = process_blast.make_alignments_json(path + '/database/' + version + '/train_reads.tsv', iden=30, eval=1, len=25, BitScore=True)
data = make_XY.make_xy2(alignments1)
deepL = train_deepARG.main(data)
cPickle.dump(deepL['parameters'], open(path + '/model/' + version + '/metadata_SS.pkl', 'w'))
deepL['clf'].save_params_to(path + '/model/' + version + '/model_SS.pkl')