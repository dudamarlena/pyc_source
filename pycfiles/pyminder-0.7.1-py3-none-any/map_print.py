# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyMind/map_print.py
# Compiled at: 2013-06-11 17:50:10
__doc__ = '\nCopyright 2012 Alexey Kravets  <mr.kayrick@gmail.com>\n\nThis file is part of PyMind.\n\nPyMind is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nPyMind is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with PyMind.  If not, see <http://www.gnu.org/licenses/>.\n'
import curses

def suppored_icons(icon):
    if icon.startswith('priority_'):
        return '(' + icon[len('priority_'):].lstrip('0') + ')'
    else:
        if icon.startswith('task_'):
            return '[' + str(25 * (int(icon[len('task_'):]) - 1)).rjust(3) + '%]'
        else:
            return

        return


def get_prefix(idea):
    result = ''
    for icon in idea.icons:
        item = suppored_icons(icon)
        if item != None:
            result += item

    if result != '':
        result += ' '
    return result


def get_str(idea, offset, num):
    prefix = get_prefix(idea)
    result = '  ' * offset + prefix + idea.title
    if len(idea.ideas) > 0 and idea.closed == 'true':
        result += ' [+]'
    return result


def print_idea(idea, offset, num):
    print get_str(idea, offset, num)
    if idea.closed == 'true':
        return
    for index, item in enumerate(idea.ideas):
        print_idea(item, offset + 1, index + 1)


def print_map(data):
    print_idea(data.ideas[0], 0, 1)


def print_idea_curses(idea, offset, num, stdsrc, current):
    line = get_str(idea, offset, num) + '\n'
    if idea == current:
        stdsrc.addstr(line, curses.A_BOLD)
    else:
        stdsrc.addstr(line)
    if idea.closed == 'true':
        return
    for index, item in enumerate(idea.ideas):
        print_idea_curses(item, offset + 1, index + 1, stdsrc, current)


def print_curses(data, stdsrc, current):
    print_idea_curses(data.ideas[0], 0, 1, stdsrc, current)