# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/wordtex.py
# Compiled at: 2013-11-13 15:05:09
import sys, os
sys.path.insert(1, '..')
from cloudtb import dbe, system
import texlib
document = None

def main():
    import wp_formatting, pdb
    texlib.TexPart.FORMAT_MODULE = wp_formatting
    argv = sys.argv
    inputfile = 'tex_docs/simple.tex'
    inputfile = '/home/user/Documents/Cloudform Design/Website/Blog/Projects In the works.tex'
    inputfile = '/home/user/Documents/Cloudform Design/Website/Personal/Resume.tex'
    if len(argv) > 1:
        inputfile = argv[1]
    else:
        inputfile = os.path.join(os.getcwd(), inputfile)
    if len(argv) > 2:
        outputfile = argv[2]
    elif system.is_file_ext(inputfile, 'tex'):
        outputfile = inputfile[:-4] + '.wp.html'
    else:
        outputfile = inputfile + '.wp.html'
    document = texlib.process_document(inputfile)
    texlib.print_tex_tree(document)
    document.format()
    import bs4
    html_text = bs4.BeautifulSoup(document.get_wp_text()).prettify()
    print html_text
    with open(outputfile, 'w') as (f):
        f.write(html_text)
    print 'File output: ', outputfile


if __name__ == '__main__':
    main()