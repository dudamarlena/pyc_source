# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/newtex/newtexrc/fabfile.py
# Compiled at: 2014-12-16 18:53:34
import glob, os, shutil
from fabric.api import task

@task(default=True)
def copy():
    master_bib = '$master_bib'
    dest = 'bib/$master_bib_name'
    shutil.copyfile(master_bib, dest)
    print ('Copied {0}').format(master_bib)


@task
def help():
    print 'Commands:\n\n    copy            copy bib file to refs [default]\n    clean           remove latex intermediate files'


@task
def clean():
    globs = [
     '*.aux',
     '*.bak',
     '*.bbl',
     '*.blg',
     '*.dvi',
     '*.fgx',
     '*.log',
     '*.out',
     '*.pdf',
     '*.synctex.gz',
     '*.sav',
     '*.spl',
     '*.tbx',
     '*.vdx',
     '*.fdb_latexmk',
     '*.fls',
     '*.mp',
     '*.top',
     '*.tui',
     '*.pyc']
    to_remove = []
    for glob_pattern in globs:
        to_remove.extend(glob.glob(glob_pattern))

    for filename in to_remove:
        os.remove(filename)

    print 'Removed aux / compiled files'