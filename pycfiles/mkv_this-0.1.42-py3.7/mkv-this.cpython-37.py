# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mkv-this/mkv-this.py
# Compiled at: 2020-04-17 16:37:49
# Size of source mod 2**32: 4156 bytes
"""
    mkv-this: input text, output markovified text.
    Copyright (C) 2020 mousebot@riseup.net.

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
import markovify, sys, argparse
parser = argparse.ArgumentParser()
parser.add_argument('infile', help='the text file to process, with path. NB: file cannot be empty.')
parser.add_argument('outfile', nargs='?', default='./mkv-output.txt', help='the file to save to, with path. if the file is used more than once, subsequent literature will be appended to the file after a star. defaults to ./mkv-output.txt.')
parser.add_argument('-s', '--statesize', help='the number of preceeding words the probability of the next word depends on. defaults to 2, 1 makes it more random, 3 less so.', type=int, default=2)
parser.add_argument('-n', '--sentences', help="the number of 'sentences' to output. defaults to 5.", type=int, default=5)
parser.add_argument('-c', '--combine', help='provide an another input text file with path to be combined with the first.')
parser.add_argument('-l', '--length', help='set maximum number of characters per sentence.', type=int)
args = parser.parse_args()
if args.combine:
    with open(args.infile) as (f):
        text = f.read()
    with open(args.combine) as (cf):
        ctext = cf.read()
    text_model = markovify.Text(text, state_size=(args.statesize))
    ctext_model = markovify.Text(ctext, state_size=(args.statesize))
    combo_model = markovify.combine([text_model, ctext_model])
    for i in range(args.sentences):
        output = open(args.outfile, 'a')
        if args.length:
            output.write(str(combo_model.make_short_sentence((args.length),
              tries=500, max_overlap_ratio=20)) + '\n \n')
        else:
            output.write(str(combo_model.make_sentence(tries=500,
              max_overlap_ratio=20)) + '\n \n')

    output.write(str(' \n \n * \n \n'))
    output.close()
else:
    with open(args.infile) as (f):
        text = f.read()
    text_model = markovify.Text(text, state_size=(args.statesize))
    for i in range(args.sentences):
        output = open(args.outfile, 'a')
        if args.length:
            output.write(str(text_model.make_short_sentence((args.length),
              tries=500, max_overlap_ratio=20)) + '\n \n')
        else:
            output.write(str(text_model.make_sentence(tries=500,
              max_overlap_ratio=20)) + '\n \n')

    output.write(str(' \n \n * \n \n'))
    output.close()
print('\n:  literary genius has been written to the file ' + args.outfile + '. thanks for playing!')
sys.exit()