# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seqplot/seqplot_main.py
# Compiled at: 2014-10-06 08:37:44
import sys, os, getopt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from seqplot.seqplot_helpers import Alignment
from seqplot.seqplot_helpers import Colorizer
from seqplot.seqplot_helpers import WrongInputException

def main():
    """Main"""
    aln_file = None
    boxwidth = 1
    boxheight = 1
    colorscheme = 'default'
    outfile = None
    fontpath = None
    show_names = False
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:F:o:x:y:c:sh', [
         'fasta=',
         'font_file',
         'outifle',
         'boxwidth=',
         'boxheight=',
         'colorscheme=',
         'show_names',
         'help'])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ('-f', '--fasta'):
            aln_file = a
        elif o in ('-h', '--help'):
            usage()
        elif o in ('-o', '--outfile'):
            outfile = a
            if not outfile.endswith('.png'):
                outfile += '.png'
        elif o in ('-x', '--boxwidth'):
            boxwidth = int(a)
        elif o in ('-y', '--boxheight'):
            boxheight = int(a)
        elif o in ('-c', '--colorscheme'):
            colorscheme = a
        elif o in ('-F', '--font_file'):
            fontpath = a
        elif o in ('-s', '--show_names'):
            show_names = True
        else:
            print o
            assert False, 'unhandled option'

    if not aln_file:
        usage()
    colorschemes = ['default', 'maeditor', 'cinema', 'lesk', 'clustal', 'aacid', 'dna']
    if colorscheme not in colorschemes:
        sys.stderr.write(('No such colorscheme: {}\navailable: {}\n falling back to default').format(colorscheme, (',').join(colorschemes)))
        colorscheme = 'default'
    draw(aln_file=aln_file, outfile=outfile, colorscheme=colorscheme, boxwidth=boxwidth, boxheight=boxheight, show_names=show_names, fontpath=fontpath)
    return


def draw(aln_file, outfile, colorscheme, boxwidth, boxheight, show_names=False, fontpath=None):
    width = 800
    height = 600
    boxwidth = boxwidth
    boxheight = boxheight
    offset = 0
    font = None
    al = Alignment(name=aln_file, fasta=aln_file)
    names = [ m.name for m in al.members ]
    if show_names:
        if fontpath:
            font_searchpath = fontpath
        else:
            font_searchpath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data' + os.sep + 'FreeMono.ttf'
        try:
            font = ImageFont.truetype(font_searchpath, boxheight)
            offset = font.getsize(max(names, key=len))[0]
            sys.stdout.write(('Found font in {}\n').format(str(font_searchpath)))
        except IOError as e:
            sys.stderr.write(str(e))
            sys.stderr.write(('could not find font in {}\nPlease provide a font path with the -F option\n').format(str(font_searchpath)))
            show_names = False
            offset = 0

    height = len(al.members) * boxheight
    width = len(al.members[0].sequence) * boxwidth + offset
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    yd = None
    for y, member in enumerate(al.members):
        y *= boxheight
        for x, xs in enumerate(member.sequence):
            x *= boxwidth
            try:
                color = Colorizer.color(char=xs, colorscheme=colorscheme)
            except WrongInputException as e:
                sys.stderr.write('Error! ' + str(e) + ('{} does not work with colorscheme {}.\nNo output produced.\n').format(al.name, colorscheme))
                sys.exit(1)

            for i in xrange(0, boxwidth):
                xd = x + i + offset
                for j in xrange(0, boxheight):
                    yd = y + j
                    draw.point((xd, yd), fill=color)

        if show_names:
            draw.text((0, yd - boxheight), member.name, font=font, fill=(0, 0, 0))

    if not outfile:
        img.save(aln_file + '.png', 'png')
    else:
        img.save(outfile, 'png')
    return


def usage():
    print '\n    ######################################\n    # seqPlot.py\n    ######################################\n    usage:\n        seqPlot.py -f multifasta alignment\n    options:\n         -f, --fasta=FILE    multifasta alignment (eg. "align.fas")\n\n       [ -o, --outfile=STR   output file (png) ]\n       [ -c, --colorscheme=STR STR in ("default", "clustal", "lesk",\n                                       "cinema", "maeditor") ]\n       [ -x, --boxwidth=INT draw INT pixels per residue (x direction) ]\n       [ -y, --boxheight=INT draw INT pixels per residue (y direction) ]\n\n    adding identifiers:\n       [ -s, --show_names    also draw sequence ids ]\n       [ -F, --font_file=FONT path to truetype font (monospace fonts recommended) ]\n    '
    sys.exit(2)


if __name__ == '__main__':
    main()