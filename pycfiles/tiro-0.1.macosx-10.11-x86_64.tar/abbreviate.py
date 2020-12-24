# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/tiro/abbreviate.py
# Compiled at: 2016-03-06 22:27:13
import collections, re, sys
from os import path
import yaml
from tiro.regnets import Regnet, Parser
from tiro.rules_generator import Generator
__all__ = [
 'AbbreviationRegister']
Abbreviation = collections.namedtuple('Abbreviation', 'name, pattern, codepoint')

class AbbreviationRegister(object):
    """
    This object contains sequences of glyph transformations which it can run on
    text objects.
    """
    CONTROL_CHARS_START = 57344
    CONTROL_CHARS_END = 63743

    def __init__(self, abbreviations, encoding='uni_rep'):
        self.abb_sequences = []
        self.lookup_table = {}
        self.legend = {}
        self.pool = range(self.CONTROL_CHARS_START, self.CONTROL_CHARS_END)
        for i, abbreviation in zip(self.pool, abbreviations):
            codepoint = chr(i)
            regnet = Regnet(abbreviation['pattern'])
            name = abbreviation['name']
            self.add_to_sequences(name, regnet, codepoint)
            value = abbreviation.get(encoding, name)
            self.lookup_table[codepoint] = value
            self.legend[name] = value

    def __getitem__(self, char):
        if self.CONTROL_CHARS_START <= ord(char) < self.CONTROL_CHARS_END:
            return self.lookup_table[char]
        else:
            return char

    def add_to_sequences(self, section, regnet_object, serial):
        """
        Given the makings of an abbreviation, create a new object
        and add it to the sequences list.
        """
        precedence = regnet_object.prec
        while len(self.abb_sequences) < precedence + 1:
            self.abb_sequences.append([])

        self.abb_sequences[precedence].append(Abbreviation(section, regnet_object.pattern, serial))

    def abbreviate_text(self, text):
        """
        Runs each sequence of transforms in the order they were loaded into the
        controller.
        """
        for sequence in self.abb_sequences:
            for abbreviation in sequence:
                text = re.sub(abbreviation.pattern, abbreviation.codepoint, text)

        return text

    def generate_legend(self):
        return ('\n').join(('{}: {}').format(value, key) for key, value in self.legend.items())

    def decode(self, text):
        return ('').join(self[char] for char in text)


if __name__ == '__main__':
    dir_name = path.dirname(__file__)
    tna_filename = path.join(dir_name, 'config', 'tna.yml')
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate', help='Analyze a text for frequency and generate abbreviations on the fly.', action='store_true')
    parser.add_argument('--ruleset', help='The ruleset to use. Uses The New Abbreviations if none is supplied.', default=tna_filename)
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'))
    parser.add_argument('-t', '--text', nargs='+', help='\tThe text to operate on.')
    parser.add_argument('-r', '--render', help="Render method. Accepts 'unicode' or 'base'.", default='unicode')
    parser.add_argument('-l', '--legend', help='Print a legend at the top of the text.', action='store_true')
    args = parser.parse_args()
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip('\r\n')
    elif args.infile:
        text = args.infile.read()
    elif args.text:
        text = (' ').join(args.text)
    else:
        exit("No input received. Run 'python3 abbreviate.py -h' for more information.")
    encoding = args.render
    if args.generate:
        ruleset = Generator(text).generate_rules()
    else:
        with open(args.ruleset, 'r') as (f):
            ruleset = yaml.safe_load(f)
    parser = Parser(ruleset, encoding)
    abba = AbbreviationRegister(parser.abbreviations, encoding=encoding)
    if args.legend:
        legend = abba.generate_legend()
        print legend
    abbreviated = abba.abbreviate_text(text)
    print abba.decode(abbreviated)