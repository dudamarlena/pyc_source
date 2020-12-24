# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/prettify.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 2547 bytes
import re
from xsrfprobe.core.colors import *

def formPrettify(response):
    """
    The main aim for this is to beautify the forms
        that will be displayed on the terminal.
    """
    highlighted = []
    response = response.splitlines()
    for newLine in response:
        line = newLine
        pattern = re.findall('(<+\\w+>)', line)
        for grp in pattern:
            starttag = ''.join(grp)
            if starttag:
                line = line.replace(starttag, color.BLUE + starttag + color.END)

        pattern = re.findall('(\\s\\w+=)', line)
        for grp in pattern:
            stu = ''.join(grp)
            if stu:
                line = line.replace(stu, color.CYAN + stu + color.END)

        pattern = re.findall('(</.*>)', line)
        for grp in pattern:
            endtag = ''.join(grp)
            if endtag:
                line = line.replace(endtag, color.CYAN + endtag + color.END)

        if line != newLine:
            highlighted.append(line)
        else:
            highlighted.append(color.GREY + newLine)

    for h in highlighted:
        print('  ' + h)


def indentPrettify(soup, indent=2):
    pretty_soup = str()
    previous_indent = 0
    for line in soup.prettify().split('\n'):
        current_indent = str(line).find('<')
        if current_indent == -1 or current_indent > previous_indent + 2:
            current_indent = previous_indent + 1
        previous_indent = current_indent
        pretty_soup += writeOut(line, current_indent, indent)

    return pretty_soup


def writeOut(line, current_indent, desired_indent):
    new_line = ''
    spaces_to_add = current_indent * desired_indent - current_indent
    if spaces_to_add > 0:
        for i in range(spaces_to_add):
            new_line += ' '

    new_line += str(line) + '\n'
    return new_line