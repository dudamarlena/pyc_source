# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /data/code/pracmln/python3/pracmln/utils/latexmath2png.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 5894 bytes
from dnutils import logs
from pracmln.utils import locs
import os, tempfile
from PIL import Image
import base64
logger = logs.getlogger(__name__, logs.DEBUG)
default_packages = [
 'amsmath',
 'amsthm',
 'amssymb',
 'bm']

def __build_preamble(packages, declarations):
    preamble = '\\documentclass{article}\n'
    for p in packages:
        preamble += '\\usepackage{{{}}}\n'.format(p)

    for d in declarations:
        preamble += '{}\n'.format(d)

    preamble += '\\pagestyle{empty}\n\\begin{document}\n'
    return preamble


def __write_output(infile, outdir, workdir='.', filename='', size=1, svg=True):
    try:
        latexcmd = 'latex -halt-on-error -output-directory {} {} >/dev/null'.format(workdir, infile)
        rc = os.system(latexcmd)
        if rc != 0:
            raise Exception('latex error')
        dvifile = infile.replace('.tex', '.dvi')
        outfilename = os.path.join(outdir, filename)
        if svg:
            dvicmd = 'dvisvgm -v 0 -o {}.svg --no-fonts {}'.format(outfilename, dvifile)
        else:
            dvicmd = 'dvipng -q* -T tight -x {} -z 9 -bg Transparent -o {}.png {} >/dev/null'.format(size * 1000, outfilename, dvifile)
        rc = os.system(dvicmd)
        if rc != 0:
            raise Exception('{} error'.format('dvisvgm error' if svg else 'dvipng'))
    finally:
        basefile = infile.replace('.tex', '')
        tempext = ['.aux', '.dvi', '.log']
        for te in tempext:
            tempfile = basefile + te
            if os.path.exists(tempfile):
                os.remove(tempfile)


def math2png(content, outdir, packages=default_packages, declarations=[], filename='', size=1, svg=True):
    """
    Generate png images from $$...$$ style math environment equations.

    Parameters:
        content      - A string containing latex math environment formulas
        outdir       - Output directory for PNG images
        packages     - Optional list of packages to include in the LaTeX preamble
        declarations - Optional list of declarations to add to the LaTeX preamble
        filename     - Optional filename for output files
        size         - Scale factor for output
    """
    outfilename = '/tmp/default.tex'
    workdir = tempfile.gettempdir()
    fd, texfile = tempfile.mkstemp('.tex', 'eq', workdir, True)
    try:
        try:
            content = content.replace('$', '\\$')
            fileContent = '{}$${}$$\n\\end{{document}}'.format(__build_preamble(packages, declarations), content)
            with os.fdopen(fd, 'w+') as (f):
                f.write(fileContent)
            __write_output(texfile, outdir, workdir=workdir, filename=filename, size=size, svg=svg)
            outfilename = os.path.join(outdir, '{}.{}'.format(filename, 'svg' if svg else 'png'))
        except:
            logger.error('Unable to create image. A reason you encounter this error might be that you are either missing latex packages for generating .dvi files or {} for generating the {} image from the .dvi file.'.format('dvisvgm' if svg else 'dvipng', 'svg' if svg else 'png'))
            outfilename = os.path.join(locs.etc, 'default.{}'.format('svg' if svg else 'png'))

    finally:
        return

    if svg:
        with open(outfilename, 'r') as (outfile):
            filecontent = outfile.read()
            ratio = 1
    else:
        im = Image.open(outfilename)
        width, height = im.size
        ratio = float(width) / float(height)
        png = open(outfilename)
        filecontent = base64.b64encode(png.read())
    if os.path.exists(texfile):
        if locs.etc not in outfilename:
            os.remove(texfile)
    if os.path.exists(outfilename):
        if locs.etc not in outfilename:
            os.remove(outfilename)
    return (
     filecontent, ratio)