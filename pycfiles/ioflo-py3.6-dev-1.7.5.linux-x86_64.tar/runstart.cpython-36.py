# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/app/test/runstart.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 1345 bytes
"""
Runs alls the example FloScripts

"""
import sys, os, ioflo.app.run
PLAN_DIR_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'plan')

def getPlanFiles(planDirPath=PLAN_DIR_PATH):
    planFiles = []
    for fname in os.listdir(os.path.abspath(planDirPath)):
        root, ext = os.path.splitext(fname)
        if not ext != '.flo':
            if root.startswith('__'):
                pass
            else:
                planFiles.append(os.path.abspath(os.path.join(planDirPath, fname)))

    return planFiles


def test():
    """ Execute run.start """
    plans = getPlanFiles()
    filepath = '../plan/continuation.flo'
    opts = dict(gandolf='grey', saruman='white')
    metas = [('opts', '.testmeta.opts', dict(value=opts))]
    ioflo.app.run.start(name='teststart',
      period=0.125,
      stamp=0.0,
      real=False,
      filepath=filepath,
      behaviors=None,
      username='',
      password='',
      mode=None,
      houses=None,
      metas=metas,
      verbose=4)


if __name__ == '__main__':
    test()