# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ddp\getpar.py
# Compiled at: 2015-04-09 20:49:55
import ddp.inc as inc, os

def get_ddpostprocess():
    tpl_path = inc.get_tpl_path('ddpostprocess')
    tpl_content = open(tpl_path, 'r').read()
    par_path = os.path.join(inc.get_project_path(), 'ddpostprocess.par')
    open(par_path, 'w').write(tpl_content)
    print 'ddpostprocess.par write successfully...'


def get_ddscat_fromfile():
    tpl_path = inc.get_tpl_path('ddscat_fromfile')
    tpl_content = open(tpl_path, 'r').read()
    par_path = os.path.join(inc.get_project_path(), 'ddscat.par')
    open(par_path, 'w').write(tpl_content)
    print 'ddscat.par from file write successfully...'


def get_ddscat_builtin():
    tpl_path = inc.get_tpl_path('ddscat_builtin')
    tpl_content = open(tpl_path, 'r').read()
    par_path = os.path.join(inc.get_project_path(), 'ddscat.par')
    open(par_path, 'w').write(tpl_content)
    print 'ddscat.par builtin write successfully...'