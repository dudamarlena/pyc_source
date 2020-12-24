# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vizqespkg/vizqes_main.py
# Compiled at: 2015-02-08 11:07:25
import sys, os, getopt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from vizqespkg.vizqes_helpers import Alignment
from vizqespkg.vizqes_helpers import Colorizer
from vizqespkg.vizqes_helpers import WrongInputException

def main():
    """Main"""
    aln_file = None
    boxwidth = 1
    boxheight = 1
    colorscheme = 'default'
    outfile = None
    fontpath = None
    show_names = False
    show_grouping = False
    out_format = 'png'
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:F:o:x:y:c:sgh', [
         'fasta=',
         'font_file',
         'outfile',
         'boxwidth=',
         'boxheight=',
         'colorscheme=',
         'show_names',
         'show_grouping',
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
            if outfile.endswith('.eps'):
                out_format = 'eps'
            elif outfile.endswith('.jpg') or outfile.endswith('.jpeg'):
                out_format = 'jpeg'
            elif not outfile.endswith('.png'):
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
        elif o in ('-g', '--show_grouping'):
            show_grouping = True
        else:
            print o
            assert False, 'unhandled option'

    if not aln_file:
        usage()
    colorschemes = ['default', 'maeditor', 'cinema', 'lesk', 'clustal', 'aacid', 'dna']
    if colorscheme not in colorschemes:
        sys.stderr.write(('No such colorscheme: {}\navailable: {}\n falling back to default').format(colorscheme, (',').join(colorschemes)))
        colorscheme = 'default'
    if show_grouping:
        draw_feat(aln_file=aln_file, outfile=outfile, colorscheme=None, boxwidth=boxwidth, boxheight=boxheight, show_names=show_names, fontpath=fontpath, out_format=out_format)
    else:
        draw(aln_file=aln_file, outfile=outfile, colorscheme=colorscheme, boxwidth=boxwidth, boxheight=boxheight, show_names=show_names, fontpath=fontpath, out_format=out_format)
    return


def draw(aln_file, outfile, colorscheme, boxwidth, boxheight, show_names=False, fontpath=None, out_format='png'):
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

            for i in range(0, boxwidth):
                xd = x + i + offset
                for j in range(0, boxheight):
                    yd = y + j
                    draw.point((xd, yd), fill=color)

        if show_names:
            draw.text((0, yd - boxheight), member.name, font=font, fill=(0, 0, 0))

    if not outfile:
        print 'Wrote ' + aln_file + '.png'
        img.save(aln_file + '.png', 'png')
    else:
        print 'Wrote ' + outfile
        img.save(outfile, out_format)
    return


def draw_feat(aln_file, outfile, colorscheme, boxwidth, boxheight, show_names=False, fontpath=None, out_format='png'):
    boxwidth = boxwidth
    boxheight = boxheight
    offset = 0
    font = None
    al = Alignment(name=aln_file, fasta=aln_file)
    al.calc_numbers()
    names = [ m.name for m in al.members ]
    width = len(al.members[0].sequence) * boxwidth + offset
    height = len(al.members) * boxheight
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

    else:
        height = 1 * boxheight
        al.members = [al.members[0]]
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    yd = None
    for y, member in enumerate(al.members):
        y *= boxheight
        for x, xs in enumerate(member.sequence):
            try:
                if x in al.gap_pos:
                    color = Colorizer.color(char='gap', colorscheme='feature')
                if x in al.match_gap_pos:
                    color = Colorizer.color(char='gap_match', colorscheme='feature')
                if x in al.match_pos:
                    color = Colorizer.color(char='match', colorscheme='feature')
                if x in al.mismatch_pos:
                    color = Colorizer.color(char='mismatch', colorscheme='feature')
            except WrongInputException as e:
                sys.stderr.write('Error! ' + str(e) + ('{} does not work with colorscheme {}.\nNo output produced.\n').format(al.name, colorscheme))
                sys.exit(1)

            x *= boxwidth
            for i in range(0, boxwidth):
                xd = x + i + offset
                for j in range(0, boxheight):
                    yd = y + j
                    draw.point((xd, yd), fill=color)

        if show_names:
            draw.text((0, yd - boxheight), member.name, font=font, fill=(0, 0, 0))

    if not outfile:
        print 'Wrote ' + aln_file + '.png'
        img.save(aln_file + '.png', 'png')
    else:
        print 'Wrote ' + outfile
        img.save(outfile, out_format)
    return


def usage():
    print '\n    ######################################\n    # vizqes\n    ######################################\n    usage:\n        vizqes -f multifasta alignment\n    options:\n         -f, --fasta=FILE    multifasta alignment (eg. "align.fas")\n\n       [ -o, --outfile=STR   output file (png, eps, jpg) ]\n       [ -c, --colorscheme=STR STR in ("default", "clustal", "lesk",\n                                       "cinema", "maeditor", "dna",\n                                       "aacid") ]\n       [ -x, --boxwidth=INT draw INT pixels per residue (x direction) ]\n       [ -y, --boxheight=INT draw INT pixels per residue (y direction) ]\n\n    adding identifiers:\n       [ -s, --show_names     also draw sequence ids ]\n       [ -g, --show_grouping] draw colors for match, mismatch, gap, and gapped matches\n                              (ignores colorscheme) ]\n       [ -F, --font_file=FONT path to truetype font (monospace fonts recommended) ]\n    '
    sys.exit(2)


if __name__ == '__main__':
    main()