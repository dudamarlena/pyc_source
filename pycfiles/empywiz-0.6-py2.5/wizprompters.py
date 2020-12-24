# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\empywiz\wizprompters.py
# Compiled at: 2006-10-06 10:24:39
UseDefaultValue = object()

class IntPrompter:
    """ Demo prompter

    Ask for an integer with a certain range of legal values.
    """

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def prompt(self, varname):
        while 1:
            i = raw_input('give an int (min=%s, max=%s) for %s: ' % (
             self.min, self.max, varname))
            try:
                val = int(i)
            except ValueError:
                print 'You should enter a legal integer!'

            if (self.min == None or val >= self.min) and (self.max == None or val <= self.max):
                return val
            print 'The integer should be in specified range!'

        return

    def __repr__(self):
        return '<int prompter>'


class ListPrompter:
    """ ask for a list of strings"""

    def prompt(self, varname):
        print "Entering an array '%s'; end by entering '.' on the line alone" % varname
        l = []
        i = 0
        while 1:
            s = raw_input('%s[ %s ] := ' % (varname, i))
            if not s:
                continue
            if s == '.':
                return l
            l.append(s)
            i += 1

        return l

    def __repr__(self):
        return '<list prompter>'


class DefaultPrompter:

    def prompt(self, varname):
        choice = raw_input('%s: ' % varname)
        if choice == '-':
            return UseDefaultValue
        return choice


once = None