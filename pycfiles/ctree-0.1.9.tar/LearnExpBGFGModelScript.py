# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/LearnExpBGFGModelScript.py
# Compiled at: 2013-10-30 23:00:08
from params import params
params.interactive = False
import ExpBGFGModel, re, os, os.path, ParseExpDirs, sys, matplotlib.pyplot as plt
mode = 'show'
protocol = '20121212_non_olympiad_heberlein'
expdirs_in = '/groups/branson/bransonlab/projects/olympiad/FlyBowlCtrax/%s/LearnCtraxParams/expdirs.txt' % protocol
mindatestr = ''
maxdatestr = ''
linename = '.*'
rig = ''
plate = ''
bowl = ''
notstarted = False
print '*** PROTOCOL %s ***\n' % protocol
resdir = '/groups/branson/bransonlab/projects/olympiad/FlyBowlCtrax/%s/LearnCtraxParams' % protocol
paramsdir = '/groups/branson/bransonlab/projects/olympiad/FlyBowlCtrax/%s' % protocol
paramsFileStr = 'ExpBGFGModelParams.txt'
movieFileStr = 'movie.ufmf'
annFileStr = 'movie.ufmf.ann'
expdirsFileStr = 'expdirs.txt'
outputFileStr = 'ExpBGFGModelResults.pickle'
matFileStr = 'ExpBGFGModelResults.mat'
expdirsFileName = os.path.join(resdir, expdirsFileStr)
paramsFileName = os.path.join(paramsdir, paramsFileStr)
outputFileName = os.path.join(resdir, outputFileStr)
matFileName = os.path.join(resdir, matFileStr)
if expdirs_in == '':
    expdirs, expdir_reads, expdir_writes, experiments = ParseExpDirs.getExpDirs(protocol=protocol, mindatestr=mindatestr, maxdatestr=maxdatestr, linename=linename, rig=rig, plate=plate, bowl=bowl, notstarted=notstarted, subreadfiles=[
     movieFileStr, annFileStr])
else:
    fid = open(expdirs_in, 'r')
    expdirs = []
    experiments = []
    for expdir in fid:
        expdir = expdir.strip()
        if expdir == '':
            continue
        expdirs.append(expdir)
        exp, success = ParseExpDirs.parseExpDir(expdir)
        experiments.append(exp)

    expdir_reads = expdirs
    expdir_writes = expdirs
    fid.close()
if mode == 'learn':
    print 'expdirs = ' + str(expdirs)
    fid = open(expdirsFileName, 'w')
    for expdir in expdir_reads:
        fid.write('%s\n' % expdir)

    fid.close()
    print 'execute the following command:'
    print 'python ExpBGFGModel.py' + ' -f ' + expdirsFileName + ' -p ' + paramsFileName + ' -m ' + movieFileStr + ' -a ' + annFileStr + ' -o ' + outputFileName + ' --mat ' + matFileName
elif mode == 'show':
    model = ExpBGFGModel.ExpBGFGModel(picklefile=outputFileName)
    model.show()
    for i in range(len(expdirs)):
        moviename = os.path.join(expdir_reads[i], movieFileStr)
        print moviename
        model.showtest(moviename=moviename)
        savename = os.path.join(resdir, 'ExpBGFGModel_SampleFrames_%s.png' % os.path.basename(expdirs[i]))
        plt.savefig(savename, format='png')

elif mode == 'change':
    model = ExpBGFGModel.ExpBGFGModel(picklefile=outputFileName)