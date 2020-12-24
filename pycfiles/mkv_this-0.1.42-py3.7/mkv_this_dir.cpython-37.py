# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mkv_this/mkv_this_dir.py
# Compiled at: 2020-04-25 22:37:44
# Size of source mod 2**32: 7130 bytes
"""
    mkv-this-dir: input a directory (+ optional url), output markovified text based on all its text files.

    Copyright (C) 2020 martianhiatus@riseup.net.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os, sys, argparse
from .functions import URL, convert_html, read, mkbtext, mkbnewline, writesentence, writeshortsentence

def parse_the_args():
    parser = argparse.ArgumentParser(prog='mkv-this-dir', description='markovify all text files in a director and output the results to a text file.', epilog='may you find many prophetic énoncés in your virtual bird guts! Here, this is not at all the becomings that are connected... so if you want to edit it like a bot yourself, it is trivial.')
    parser.add_argument('indir',
      help='the directory to extract the text of all text files from, with path.')
    parser.add_argument('outfile', nargs='?', default='./mkv-dir-output.txt', help='the file to save to, with path. if the file is used more than once, subsequent literature will be appended to the file after a star. defaults to ./mkv-dir-output.txt.')
    parser.add_argument('-s',
      '--state-size', help='the number of preceeding words the probability of the next word depends on. defaults to 2, 1 makes it more random, 3 less so.', type=int, default=2)
    parser.add_argument('-n',
      '--sentences', help="the number of 'sentences' to output. defaults to 5. NB: if your text has no initial caps, a 'sentence' will be a paragraph.", type=int, default=5)
    parser.add_argument('-l',
      '--length', help='set maximum number of characters per sentence.', type=int)
    parser.add_argument('-o', '--overlap', help='the amount of overlap allowed between original text and the output, expressed as a radio between 0 and 1. lower values make it more random. defaults to 0.5', type=float, default=0.5)
    parser.add_argument('-C', '--combine-URL', help='provide a URL to be combined with the input dir')
    parser.add_argument('-w', '--weight', help='specify the weight to be given to the second text provided with --combine. defaults to 1, and the weight of the initial text is also 1. setting this to 1.5 will place 50 percent more weight on the second text. setting it to 0.5 will place less.', type=float, default=1)
    parser.add_argument('-f', '--well-formed', help="enforce 'well_formed', doscard sentences with []{}()'' from the markov model. use if output is filthy.",
      action='store_true')
    parser.add_argument('--newline',
      help='sentences in input file end with newlines rather than with full stops.', action='store_true')
    return parser.parse_args()


args = parse_the_args()

def main():
    matches = []
    if os.path.isdir(args.indir) is True:
        for root, dirnames, filenames in os.walk(args.indir):
            for filename in filenames:
                if filename.endswith(('.txt', '.org', '.md')):
                    matches.append(os.path.join(root, filename))

        print(': text files fetched and combined')
    else:
        print(': error: please enter a valid directory')
        sys.exit()
    batchfile = os.path.dirname(args.indir) + os.path.sep + 'batchfile.txt'
    with open(batchfile, 'w') as (outfile):
        for fname in matches:
            try:
                with open(fname, encoding='utf-8') as (infile):
                    outfile.write(infile.read())
            except UnicodeDecodeError:
                with open(fname, encoding='latin-1') as (infile):
                    outfile.write(infile.read())

        outfile.close()
    text = read(batchfile)
    if args.combine_URL:
        html = URL(args.combine_URL)
        ctext = convert_html(html)
        if args.newline:
            text_model = mkbnewline(text, args.state_size, args.well_formed)
            ctext_model = mkbnewline(ctext, args.state_size, args.well_formed)
        else:
            text_model = mkbtext(text, args.state_size, args.well_formed)
            ctext_model = mkbtext(ctext, args.state_size, args.well_formed)
        combo_model = markovify.combine([
         text_model, ctext_model], [1, args.weight])
        if args.length:
            writeshortsentence(combo_model, args.sentences, args.outfile, args.overlap, args.length)
        else:
            writesentence(combo_model, args.sentences, args.outfile, args.overlap, args.length)
    else:
        if args.newline:
            text_model = mkbnewline(text, args.state_size, args.well_formed)
        else:
            text_model = mkbtext(text, args.state_size, args.well_formed)
        if args.length:
            writeshortsentence(text_model, args.sentences, args.outfile, args.overlap, args.length)
        else:
            writesentence(text_model, args.sentences, args.outfile, args.overlap, args.length)
    os.unlink(batchfile)
    print('\n:                :\n')
    for key, value in vars(args).items():
        print(': ' + key.ljust(15, ' ') + ':  ' + str(value).ljust(10))

    if os.path.isfile(args.outfile):
        print('\n:  literary genius has been written to the file ' + args.outfile + '. thanks for playing!\n\n: Here, this is not at all the becomings that are connected... so if you want to edit it like a bot yourself, it is trivial. Yes, although your very smile suggests that this Armenian enclave is not at all the becomings that are connected...')
    else:
        print(': mkv-this ran but did NOT create an output file as requested. this is a very regrettable and dangerous situation. contact the package maintainer asap. soz!')
    sys.exit()


if __name__ == '__main__':
    main()