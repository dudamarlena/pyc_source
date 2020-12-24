# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/gametex_django_print/latex.py
# Compiled at: 2013-03-08 00:20:58
from django.core.mail import mail_admins
import os, tempfile, subprocess
from django.conf import settings

def setup_texpath():
    if 'TEXINPUTS' in os.environ:
        if settings.GAMETEX_PROJECT_ROOT not in os.environ['TEXINPUTS']:
            os.environ['TEXINPUTS'] = '%s/LaTeX/:%s' % (settings.GAMETEX_PROJECT_ROOT, os.environ['TEXINPUTS'])
    else:
        os.environ['TEXINPUTS'] = '%s/LaTeX/:' % settings.GAMETEX_PROJECT_ROOT
    os.environ[settings.GAMETEX_NAME] = settings.GAMETEX_PROJECT_ROOT


def pdflatex(entities, gametexclass, owner=None, target_dir=None):
    """
    Given a list of entities and a GameTeX class, generate a PDF.

    Returns a path to a filename, or None.

    WARNING: This could be *seriously insecure* if you don't sanitize the input.
    """
    setup_texpath()
    try:
        template = '\n       \\documentclass[%(type)s]{%(class)s}\n       \\begin{document}\n\n       %(owner)s\n       %(entities)s\n\n       \\end{document}\n       '
        template %= {'type': gametexclass, 
           'class': settings.GAMETEX_NAME, 
           'owner': '\\name{%s}' % owner if owner else '', 
           'entities': ('\n').join([ '\\%s{}' % ent for ent in entities ])}
        cwd = os.getcwd()
        tempf = tempfile.mkstemp(suffix='.tex')
        os.chdir(target_dir if target_dir else os.path.dirname(tempf[1]))
        tpf = os.fdopen(tempf[0], 'w')
        tpf.write(template)
        tpf.close()
        print template
        result = subprocess.check_output('%s -halt-on-error -interaction=batchmode %s' % (settings.PDFLATEX_PATH, tempf[1]), shell=True)
        src = tempf[1].replace('.tex', '.pdf')
        tgt = ''
        if target_dir:
            tgt = os.path.join(target_dir, os.path.basename(src))
            os.rename(src, tgt)
        os.chdir(cwd)
        if target_dir:
            return tgt
        return src
    except subprocess.CalledProcessError as e:
        print e.output
        return

    return