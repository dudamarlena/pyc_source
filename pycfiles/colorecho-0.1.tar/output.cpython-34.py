# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vagrant/.virtualenvs/temp3/lib/python3.4/site-packages/colordiffs/output.py
# Compiled at: 2015-06-21 18:46:03
# Size of source mod 2**32: 937 bytes
from .formats import green_bg, red_bg, discreet

def output_diff_chunk(dc, colorized_a, colorized_b):
    results = [
     discreet(dc.diff_line)]
    for instr in dc.output_instructions:
        if instr[0] == ' ':
            results.append(' ' + dc.a_hunk.get_current_line(colorized_a))
            dc.b_hunk.get_current_line(colorized_b)
        if instr[0] == '-':
            results.append(red_bg('-') + dc.a_hunk.get_current_line(colorized_a))
        if instr[0] == '+':
            results.append(green_bg('+') + dc.b_hunk.get_current_line(colorized_b))
            continue

    return results


def output(diff, colorized_a, colorized_b):
    print(discreet(diff.header))
    print(discreet(diff.index))
    if diff.line_a:
        print(discreet(diff.line_a))
    if diff.line_b:
        print(discreet(diff.line_b))
    for dc in diff.dcs:
        for o in output_diff_chunk(dc, colorized_a, colorized_b):
            print(o)