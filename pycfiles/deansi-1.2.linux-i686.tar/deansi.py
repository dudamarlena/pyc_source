# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/deansi.py
# Compiled at: 2016-01-08 08:24:39
"""
Copyright 2012 David Garcia Garzon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
__doc__ = "This module provides functions to convert terminal output including\nansi terminal codes to stylable html.\n\nThe main entry point are 'deansi(input)' which performs the conversion\non an input string and 'styleSheet' which provides a minimal style sheet.\nYou can overwrite stylesheets by placing new rules after this minimal one.\n"
import re
try:
    from html import escape as _htmlescape
    htmlescape = lambda s: _htmlescape(s, quote=False)
except ImportError:
    from cgi import escape as htmlescape

try:
    xrange
except NameError:
    xrange = range

colorCodes = {0: 'black', 
   1: 'red', 
   2: 'green', 
   3: 'yellow', 
   4: 'blue', 
   5: 'magenta', 
   6: 'cyan', 
   7: 'white'}
attribCodes = {1: 'bright', 
   2: 'faint', 
   3: 'italic', 
   4: 'underscore', 
   5: 'blink', 
   7: 'reverse', 
   8: 'hide', 
   9: 'strike'}
variations = [
 ('black', 'black', 'gray'),
 ('red', 'darkred', 'red'),
 ('green', 'darkgreen', 'green'),
 ('yellow', 'orange', 'yellow'),
 ('blue', 'darkblue', 'blue'),
 ('magenta', 'purple', 'magenta'),
 ('cyan', 'darkcyan', 'cyan'),
 ('white', 'lightgray', 'white')]

def styleSheet(brightColors=True):
    """        Returns a minimal css stylesheet so that deansi output 
        could be displayed properly in a browser.
        You can append more rules to modify this default
        stylesheet.

        brightColors: set it to False to use the same color
                when bright attribute is set and when not.
        """
    simpleColors = [ '.ansi_%s { color: %s; }' % (normal, normal) for normal, pale, bright in variations
                   ]
    paleColors = [ '.ansi_%s { color: %s; }' % (normal, pale) for normal, pale, bright in variations
                 ]
    lightColors = [ '.ansi_bright.ansi_%s { color: %s; }' % (normal, bright) for normal, pale, bright in variations
                  ]
    bgcolors = [ '.ansi_bg%s { background-color: %s; }' % (normal, normal) for normal, pale, bright in variations
               ]
    attributes = [
     '.ansi_bright { font-weight: bold; }',
     '.ansi_faint { opacity: .5; }',
     '.ansi_italic { font-style: italic; }',
     '.ansi_underscore { text-decoration: underline; }',
     '.ansi_blink { text-decoration: blink; }',
     '.ansi_reverse { border: 1pt solid; }',
     '.ansi_hide { opacity: 0; }',
     '.ansi_strike { text-decoration: line-through; }']
    return ('\n').join([
     '.ansi_terminal { white-space: pre; font-family: monospace; }'] + (paleColors + lightColors if brightColors else simpleColors) + bgcolors + attributes)


def ansiAttributes(block):
    """Given a sequence "[XX;XX;XXmMy Text", where XX are ansi 
        attribute codes, returns a tuple with the list of extracted
        ansi codes and the remaining text 'My Text'"""
    attributeRe = re.compile('^[[](\\d+(?:;\\d+)*)?m')
    match = attributeRe.match(block)
    if not match:
        return ([], block)
    else:
        if match.group(1) is None:
            return ([0], block[2:])
        return ([ int(code) for code in match.group(1).split(';') ], block[match.end(1) + 1:])


def ansiState(code, attribs, fg, bg):
    """Keeps track of the ansi attribute state given a new code"""
    if code == 0:
        return (set(), None, None)
    else:
        if code == 39:
            return (attribs, None, bg)
        if code == 49:
            return (attribs, fg, None)
        if code in xrange(30, 38):
            return (attribs, colorCodes[(code - 30)], bg)
        if code in xrange(40, 48):
            return (attribs, fg, colorCodes[(code - 40)])
        if code in attribCodes:
            attribs.add(attribCodes[code])
        if code in xrange(21, 30) and code - 20 in attribCodes:
            toRemove = attribCodes[(code - 20)]
            if toRemove in attribs:
                attribs.remove(toRemove)
        return (
         attribs, fg, bg)


def stateToClasses(attribs, fg, bg):
    """Returns css class names given a given ansi attribute state"""
    return (' ').join([ 'ansi_' + attrib for attrib in sorted(attribs) ] + (['ansi_' + fg] if fg else []) + (['ansi_bg' + bg] if bg else []))


def deansi(text):
    text = htmlescape(text)
    blocks = text.split('\x1b')
    state = (set(), None, None)
    ansiBlocks = blocks[:1]
    for block in blocks[1:]:
        attributeCodes, plain = ansiAttributes(block)
        for code in attributeCodes:
            state = ansiState(code, *state)

        classes = stateToClasses(*state)
        ansiBlocks.append("<span class='%s'>" % classes + plain + '</span>' if classes else plain)

    text = ('').join(ansiBlocks)
    return text


if __name__ == '__main__':
    import sys, argparse
    parser = argparse.ArgumentParser(description='Converts coloured console output into equivalent HTML')
    parser.add_argument('-s', '--style', metavar='FILE', help='use FILE as stylesheet')
    parser.add_argument('-t', '--template', metavar='FILE', help='use FILE as html template')
    parser.add_argument('--dark', action='store_true', help='use the dark background style')
    parser.add_argument('input', metavar='INPUT_FILE', nargs='?', help='the console input to convert (default stdin)')
    parser.add_argument('output', metavar='OUTPUT_FILE', nargs='?', help='the file where to drop the html output (default stdout)')
    args = parser.parse_args()
    default_template = "<style>\n%s\n</style>\n<div class='ansi_terminal'>%s</div>\n"
    with open(args.input) if args.input else sys.stdin as (inputFile):
        deansied = deansi(inputFile.read())
    if args.template:
        with open(args.template) as (templateFile):
            template = templateFile.read()
    else:
        template = default_template
    if args.style:
        with open(args.style) as (styleFile):
            style = styleFile.read()
    else:
        style = styleSheet()
    if args.dark:
        style += '\n.ansi_terminal { background-color: #222; color: #cfc; }'
    with open(args.output) if args.output else sys.stdout as (outputFile):
        outputFile.write(template % (
         style,
         deansied))
    sys.exit(0)