# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nemo/Scrivania/gitlab/phys2bids/phys2bids/heuristics/heur.py
# Compiled at: 2019-11-29 18:36:44
# Size of source mod 2**32: 2132 bytes
import sys, fnmatch

def heur(physinfo, name, task='', acq='', direct='', rec='', run=''):
    if physinfo == 'origfilename1':
        task = 'newname1'
    else:
        if physinfo == 'origfilename2':
            task = 'newname2'
            run = 'runnum'
        else:
            if physinfo == 'BH4':
                task = 'breathhold'
            else:
                if fnmatch.fnmatchcase(physinfo, 'MOTOR?'):
                    task = 'motor'
                else:
                    if fnmatch.fnmatchcase(physinfo, 'LOCALIZER?'):
                        task = 'pinel'
                    else:
                        if fnmatch.fnmatchcase(physinfo, 'SIMON?'):
                            task = 'simon'
                        else:
                            if physinfo == 'RS1':
                                task = 'rest'
                                run = '01'
                            else:
                                if physinfo == 'RS2':
                                    task = 'rest'
                                    run = '02'
                                else:
                                    if physinfo == 'RS3':
                                        task = 'rest'
                                        run = '03'
                                    else:
                                        if physinfo == 'RS4':
                                            task = 'rest'
                                            run = '04'
                                        else:
                                            raise Warning(f"The heuristic {__file__} could not deal with {physinfo}")
                    if not task:
                        raise KeyError('No "task" attribute found')
                    name = name + '_task-' + task
                    if acq:
                        name = name + '_acq-' + acq
                if direct:
                    name = name + '_dir-' + direct
            if rec:
                name = name + '_rec-' + rec
        if run:
            name = name + '_run-' + run
    return name