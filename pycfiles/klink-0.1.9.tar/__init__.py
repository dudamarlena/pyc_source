# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/dev/python/klink/klink/__init__.py
# Compiled at: 2015-06-16 14:00:38
import os
from subprocess import call
import shutil, re

def convert_notebooks():
    """
    Converts IPython Notebooks to proper .rst files and moves static
    content to the _static directory.
    """
    convert_status = call(['ipython', 'nbconvert', '--to', 'rst', '*.ipynb'])
    if convert_status != 0:
        raise SystemError('Conversion failed! Status was %s' % convert_status)
    notebooks = [ x for x in os.listdir('.') if '.ipynb' in x and os.path.isfile(x)
                ]
    names = [ os.path.splitext(x)[0] for x in notebooks ]
    for i in range(len(notebooks)):
        name = names[i]
        notebook = notebooks[i]
        print 'processing %s (%s)' % (name, notebook)
        sdir = '%s_files' % name
        statics = os.listdir(sdir)
        statics = [ os.path.join(sdir, x) for x in statics ]
        [ shutil.copy(x, '_static/') for x in statics ]
        shutil.rmtree(sdir)
        rst_file = '%s.rst' % name
        print 'REsT file is %s' % rst_file
        data = None
        with open(rst_file, 'r') as (f):
            data = f.read()
        if data is not None:
            with open(rst_file, 'w') as (f):
                data = re.sub('%s' % sdir, '_static', data)
                f.write(data)
        lines = None
        with open(rst_file, 'r') as (f):
            lines = f.readlines()
        if lines is not None:
            n = len(lines)
            i = 0
            rawWatch = False
            while i < n:
                line = lines[i]
                if 'image::' in line:
                    lines.insert(i + 1, '    :class: pynb\n')
                    n += 1
                elif 'parsed-literal::' in line:
                    lines.insert(i + 1, '    :class: pynb-result\n')
                    n += 1
                elif 'raw:: html' in line:
                    rawWatch = True
                if rawWatch:
                    if '<div' in line:
                        line = line.replace('<div', '<div class="pynb-result"')
                        lines[i] = line
                        rawWatch = False
                i += 1

            with open(rst_file, 'w') as (f):
                f.writelines(lines)

    return


def get_html_theme_path():
    """Returns list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir


VERSION = (0, 1, 9)
__version__ = ('.').join(str(v) for v in VERSION)
__version_full__ = __version__