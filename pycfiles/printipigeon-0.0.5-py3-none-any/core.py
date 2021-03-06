# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\printio\core.py
# Compiled at: 2012-08-24 13:21:20
__doc__ = '\n\nPretty-up your data for print or display.\n\n'
import re, math
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

class PrettyValue(object):
    """Pretty up a value by converting to string.

    Examples:
    >>> pv = PrettyValue('+10.2f')
    >>> pv.format('23.4567')
    '+    23.46'

    >>> pv = PrettyValue('^10s', fill='*')
    >>> pv.format('Center')
    '**Center**'
    """

    def __init__(self, rawtext=None, fill=None, align=None, width=None):
        """
        :param rawtext: (optional) type of value to format.
            * 's': string
            * 'i': integer
            * 'f': float
            * '%': percent
        :param fill: (optional) character to fill leftover space.
        :param align: (optional) align the value in the total space.
            * left: left-align value (default for strings).
            * center: center-align value.
            * right: right-align value.
            * rightpad: right-align numeric values with padding
                after sign (default for numbers).
        :param width: (optional) length of formatted string.
        """
        self.aligns = {}
        self.aligns['<'] = ('left', '<')
        self.aligns['^'] = ('center', '^')
        self.aligns['>'] = ('right', '>')
        self.aligns['='] = ('rightpad', '=')
        self.aligns['left'] = self.aligns['<']
        self.aligns['center'] = self.aligns['^']
        self.aligns['right'] = self.aligns['>']
        self.aligns['rightpad'] = self.aligns['=']
        self.validsigns = ('+', '-', ' ')
        self.validstrings = ('s', '')
        self.validints = ('d', 'i')
        self.validfloats = ('f', '%')
        self.validnums = []
        self.validnums.extend(self.validints)
        self.validnums.extend(self.validfloats)
        self.knowntypes = []
        self.knowntypes.extend(self.validstrings)
        self.knowntypes.extend(self.validnums)
        _text = "\n                 ([<^>=]{1})?   #0 or 1 align specifier\n                 ([\\s+-]{1})?   #0 or 1 sign specifier\n                 (\\s+)?         #0 or 1 spaces that shouldn't be there.\n                 (\\d+)?         #0 or 1 width specifier\n                 (\\.+\\d+)?      #decimal and precision specifier\n                 (.+)?$         #what's left\n                "
        self.regex = re.compile(_text, re.VERBOSE)
        self.setoptions(rawtext, fill=fill, align=align, width=width)

    def setoptions(self, rawtext=None, fill=None, align=None, width=None):
        """Set the formatting options for the values passed.

        :param rawtext: (optional) type of value to format.
            * 's': string
            * 'i': integer
            * 'f': float
            * '%': percent
        :param fill: (optional) character to fill leftover space.
        :param align: (optional) align the value in the total space.
            * left: left-align value (default for strings).
            * center: center-align value.
            * right: right-align value.
            * rightpad: right-align numeric values with padding
                after sign (default for numbers).
        :param width: (optional) length of formatted string.
        """
        self.maxwidth = 0
        self.set_fill(fill)
        options = self.parse_rawtype(rawtext)
        self.set_atype(options['atype'])
        if align:
            self.set_align(align)
        else:
            self.set_align(options['align'])
        self.set_sign(options['sign'])
        if width:
            self.set_width(width)
        else:
            self.set_width(options['width'])
        self.set_precision(options['precision'])

    def parse_rawtype(self, rawtype=None):
        """Returns the various format specifiers parsed from the
        string, rawtype.

        :param rawtext: (optional) type of value to format.
            * 's': string
            * 'i': integer
            * 'f': float
            * '%': percent
        :rtype: dictionary of format specifiers.
        """
        results = {}
        results['atype'] = None
        results['align'] = None
        results['sign'] = None
        results['width'] = None
        results['precision'] = None
        if not rawtype:
            return results
        else:
            rawtype = rawtype.rstrip()
            match = self.regex.search(rawtype)
            if not match:
                return results
            groups = match.groups()
            bar = 0
            results['align'] = groups[bar]
            bar += 1
            results['sign'] = groups[bar]
            bar += 2
            if groups[bar]:
                results['width'] = int(groups[bar])
            bar += 1
            if groups[bar]:
                results['precision'] = int(groups[bar].lstrip('.'))
            bar += 1
            if groups[bar]:
                results['atype'] = groups[bar].strip()
            return results

    def set_atype(self, atype=None):
        """
        :param atype: (optional) type of value to format.
            * 's': string
            * 'i': integer
            * 'f': float
            * '%': percent
        """
        self.atype = ''
        self._atype = ''
        self.typesummary = ''
        if atype:
            self.atype = atype
            self._atype = atype
            if atype == 'i':
                self._atype = 'd'
        if self.atype in self.validstrings:
            self.typesummary = 'str'
            return
        else:
            if self.atype in self.validints:
                self.typesummary = 'int'
                return
            if self.atype in self.validfloats:
                self.typesummary = 'float'
                return
            self.typesummary = 'unknown'
            if len(self.atype) <= 1:
                msg = "invalid atype: '%s'" % self.atype
                raise ValueError(msg)
            return

    def set_align(self, align=None):
        """Sets the alignment options for the formatted value.

        :param align: (optional) align the value in the total space.
            * left or <: left-align value (default for strings).
            * center or ^: center-align value.
            * right or >: right-align value (default for numbers).
            * rightpad or =: right-align number with padding after sign.
        """
        self.align = ''
        if not align:
            if self.atype in self.validnums:
                self.align = '='
            else:
                self.align = '<'
            return
        else:
            if align not in self.aligns:
                msg = "invalid align:'%s', atype:'%s'" % (align, self.atype)
                raise ValueError(msg)
            (_alignment, _align) = self.aligns[align]
            if _align == '=' and self.atype not in self.validnums:
                msg = 'invalid align for non-numeric types: '
                msg = "%s align:'%s', atype:'%s'" % (msg, align, self.atype)
                raise ValueError(msg)
            self.align = _align
            return

    def set_fill(self, fill=None):
        """Specify how to fill the remaining space in the string.

        :param fill: (optional) fill character for the leftover space.
        """
        self.fill = ''
        if fill or fill == 0 or fill == ' ':
            self.fill = str(fill)

    def set_sign(self, sign=None):
        """Specify how to sign the numeric value in the string.

        :param sign: (optional) show the sign of the field.
            * '+': show '+' if positive number and '-' if negative.
            * '-': only show '-' for negative numbers.
            * ' ': show ' ' for positive numbers, '-' if negative.
        """
        self.sign = ''
        if not sign:
            if self.atype in self.validnums:
                self.sign = '-'
            return
        else:
            if self.atype not in self.validnums:
                msg = 'sign invalid for non-numeric types: '
                msg = "%s sign:'%s', atype:'%s'" % (msg, sign, self.atype)
                raise ValueError(msg)
            if sign not in self.validsigns:
                msg = 'sign invalid specifier: '
                msg = "%s sign:'%s', atype:'%s'" % (msg, sign, self.atype)
                raise ValueError(msg)
            self.sign = sign
            return

    def set_width(self, width=None):
        """Specify the length of the formatted string.

        :param width: (optional) size of the destination string.
        """
        self.width = ''
        if width:
            self.width = int(width)

    def set_precision(self, precision=None):
        """Specify how many decimal points to show.

        :param precision: (optional) how many digits to the right of the
            decimal place to show.
                * default is 4.
        """
        self.precision = ''
        if not precision:
            if self.atype in self.validfloats:
                self.precision = 4
            return
        else:
            if self.atype not in self.validfloats:
                msg = 'precision invalid for non-float types, '
                msg = "%s precision:'%s'" % (msg, precision)
                msg = "%s, atype:'%s'" % (msg, self.atype)
                raise ValueError(msg)
            try:
                self.precision = int(precision)
            except ValueError:
                msg = 'invalid precision specifier, '
                msg = "%s precision:'%s'" % (msg, precision)
                msg = "%s, atype:'%s'" % (msg, self.atype)
                raise ValueError(msg)

            return

    def format(self, value):
        """Returns a formatted string based on the format specifiers.

        :param value: value to format.
        :rtype: pretty formatted string.
        """
        newvalue = value
        newatype = self._atype
        newprecision = ''
        newsign = self.sign
        newalign = self.align
        if self.typesummary == 'str':
            newvalue = str(value)
        elif self.typesummary == 'int':
            newvalue = int(value)
        elif self.typesummary == 'float':
            newvalue = float(value)
            if math.isnan(newvalue):
                newvalue = ('{0!r}').format(newvalue)
                newatype = 's'
                newsign = ''
                if newalign == '=':
                    newalign = '>'
            elif math.isinf(newvalue):
                newvalue = ('{0!r}').format(newvalue)
                newatype = 's'
                asign = ''
                beg_idx = 0
                if newsign == '+':
                    asign = '+'
                newsign = ''
                if newvalue[0] in ('+', '-'):
                    asign = newvalue[0]
                    beg_idx = 1
                newvalue = newvalue[beg_idx:]
                if newalign == '=':
                    newalign = '>'
                    if len(newvalue) < self.width:
                        specs = '{0:>%s%s}' % (self.width - 1, newatype)
                    else:
                        specs = '{0:>%s%s}' % (self.width, newatype)
                    newvalue = ('').join((asign, specs.format(newvalue)))
                else:
                    newvalue = ('').join((asign, newvalue))
            elif self.precision:
                newprecision = '.%s' % self.precision
        elif self.typesummary == 'unknown':
            formatspecs = '{0:%s}' % (newatype,)
            newvalue = formatspecs.format(newvalue)
            newatype = 's'
        formatspecs = '{%s:%s%s%s%s%s%s}' % (0,
         self.fill,
         newalign,
         newsign,
         self.width,
         newprecision,
         newatype)
        result = formatspecs.format(newvalue)
        newwidth = len(result)
        if newwidth > self.maxwidth:
            self.maxwidth = newwidth
        return result


class PrettyValues(object):
    """Pretty format values based on various formatting
    options.

    Usage:
    >>> lol = []
    >>> lol.append([0, 'yhoo', 23.45])
    >>> lol.append([1, 'goog', 200.4565])
    >>> lol.append([2, 't', 1.00])
    >>> pv = PrettyValues()
    >>> pv.newcol(0, 'i', cname='Bar')
    >>> pv.newcol(1, cname='Symbol')
    >>> pv.newcol(2, '+.2f', cname='Close')
    >>> print pv.text(lol)
    +-----+--------+---------+
    | Bar | Symbol | Close   |
    +-----+--------+---------+
    |   0 | yhoo   | + 23.45 |
    |   1 | goog   | +200.46 |
    |   2 | t      | +  1.00 |
    +-----+--------+---------+
    """

    def __init__(self):
        self.cols = []
        self.cformatters = {}
        self.vformatters = {}

    def newcol(self, key=None, vformat=None, vfill=None, cname=None, cformat=None, cfill=None):
        """Specify column attributes for prettying up your values.

        :param key: (optional) index of list or key of the dict to format.
        :param vformat: (optional) format specifier of the values
            for the column.
        :param vfill: (optional) fill character for the values.
        :param cname: (optional) name of the column.
        :param cformat: (optional) format specifier for the column name.
        :param cfill: (optional) fill character for the column name.
        """
        if not key:
            if self.cols:
                key = len(self.cols)
            else:
                key = 0
        if not cname:
            cname = key
        self.vformatters[(key, cname)] = PrettyValue(vformat, vfill)
        self.cformatters[(key, cname)] = PrettyValue(cformat, cfill)
        self.cols.append([key, cname])

    def text(self, values, noheader=False):
        """
        :param values: list of values to pretty format to text.
        :param noheader: if False (default) - headers returned with results.
        """
        records = self.format(values, noheader=noheader)
        if not records:
            return ''
        output = StringIO()
        dashes = '+'
        bar = 0
        headers = '|'
        for row in records[0]:
            headers = ('').join((headers, ' ', row, ' |'))
            dashes = ('').join((dashes, '-' * (len(row) + 2), '+'))

        if not noheader:
            line = ('').join((dashes, '\n'))
            output.write(line)
            line = ('').join((headers, '\n'))
            output.write(line)
            bar += 1
        details = records[bar:]
        if details:
            line = ('').join((dashes, '\n'))
            output.write(line)
            for detail in details:
                rows = '|'
                for field in detail:
                    rows = ('').join((rows, ' ', field, ' |'))

                line = ('').join((rows, '\n'))
                output.write(line)

        lines = output.getvalue()
        if lines:
            lines = ('').join((lines, dashes))
        return lines

    def format(self, values, noheader=False):
        """Return a pretty formatted list of values based on the
        format specifiers of the columns.

        :param values: list of values to pretty format.
        :param useheader: if False (default) - headers returned with results.
        """
        results = []
        sizes = {}
        if not self.cols:
            if not values:
                return results
            try:
                keys = values[0].keys()
            except AttributeError:
                keys = range(len(values[0]))
            else:
                for key in keys:
                    self.newcol(key)

        for (key, cname) in self.cols:
            sizes[key] = 0

        for row in values:
            for (key, cname) in self.cols:
                pv = self.vformatters[(key, cname)]
                try:
                    oldvalue = row[key]
                except KeyError:
                    msg = "Invalid key: '%s' row: %s" % (key, row)
                    raise KeyError(msg)

                newvalue = pv.format(oldvalue)
                if pv.maxwidth > sizes[key]:
                    sizes[key] = pv.maxwidth

        headers = []
        for (key, cname) in self.cols:
            pc = self.cformatters[(key, cname)]
            newcol = pc.format(cname)
            pv = self.vformatters[(key, cname)]
            if pv.maxwidth > pc.maxwidth:
                pc.set_width(pv.maxwidth)
                pv.set_width(pv.maxwidth)
                newcol = pc.format(cname)
            else:
                pv.set_width(pc.maxwidth)
            headers.append(newcol)

        if not noheader:
            results.append(headers)
        for row in values:
            record = []
            for (key, cname) in self.cols:
                pv = self.vformatters[(key, cname)]
                newvalue = pv.format(row[key])
                record.append(newvalue)

            results.append(record)

        return results


def _testit(verbose=None):
    import doctest
    doctest.testmod(verbose=verbose)


if __name__ == '__main__':
    _testit()