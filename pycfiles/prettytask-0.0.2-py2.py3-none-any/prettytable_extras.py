# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/prettytable_extras.py
# Compiled at: 2014-06-18 17:24:20
__version__ = '0.1.0'
import os
from prettytable import PrettyTable as PrettyTableCore, ALL, FRAME

def get_terminal_size():
    """Returns terminal width and height"""

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
            dim = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return

        return dim

    dim = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not dim:
        try:
            file_descriptor = os.open(os.ctermid(), os.O_RDONLY)
            dim = ioctl_GWINSZ(file_descriptor)
            os.close(file_descriptor)
        except:
            pass

    if not dim:
        dim = (
         os.environ.get('LINES', 25), os.environ.get('COLUMNS', 80))
    return (
     int(dim[1]), int(dim[0]))


COLOR_STYLES = {'bold': [
          '\x1b[1m', '\x1b[22m'], 
   'italic': [
            '\x1b[3m', '\x1b[23m'], 
   'underline': [
               '\x1b[4m', '\x1b[24m'], 
   'inverse': [
             '\x1b[7m', '\x1b[27m'], 
   'white': [
           '\x1b[37m', '\x1b[39m'], 
   'grey': [
          '\x1b[90m', '\x1b[39m'], 
   'black': [
           '\x1b[30m', '\x1b[39m'], 
   'blue': [
          '\x1b[34m', '\x1b[39m'], 
   'cyan': [
          '\x1b[36m', '\x1b[39m'], 
   'green': [
           '\x1b[32m', '\x1b[39m'], 
   'magenta': [
             '\x1b[35m', '\x1b[39m'], 
   'red': [
         '\x1b[31m', '\x1b[39m'], 
   'yellow': [
            '\x1b[33m', '\x1b[39m']}

def colorify(text, colors):
    """Prefix and suffix text to render terminal color"""
    for color in colors:
        style = COLOR_STYLES[color]
        text = ('{}{}{}').format(style[0], text, style[1])

    return text


class PrettyTable(PrettyTableCore):

    def __init__(self, field_names=None, **kwargs):
        new_options = ['auto_width', 'header_color']
        super(PrettyTable, self).__init__(field_names, **kwargs)
        for option in new_options:
            if option in kwargs:
                self._validate_new_option(option, kwargs[option])
            else:
                kwargs[option] = None

        self._auto_width = kwargs['auto_width'] or False
        self._header_color = kwargs['header_color'] and kwargs['header_color'].split(',') or None
        self._options.extend(new_options)
        return

    def _validate_new_option(self, option, val):
        """Same as _validate_option for prettytable_extra specific options"""
        if option in 'auto_width':
            self._validate_true_or_false(option, val)
        elif option in 'header_color':
            self._validate_color(option, val)
        else:
            raise Exception(('Unrecognised option: {}!').format(option))

    def _validate_color(self, option, val):
        available_colors = COLOR_STYLES.keys()
        if val:
            for color in val.split(','):
                try:
                    assert color in available_colors
                except AssertionError:
                    raise Exception(('Invalide color, use {} or None!').format((', ').join(available_colors)))

    def _optimize_widths(self, options=None, max_width=None, term_width=None, border_width=None):
        """Update widths to match the current terminal size

        Arguments:

        options - dictionary of options settings."""
        if not options:
            options = self._get_options()
        (lpad, rpad) = self._get_padding_widths(options)
        if not border_width:
            border_width = len(self._widths) * (1 + lpad + rpad) + 1
        if not term_width:
            (term_width, term_height) = get_terminal_size()
        if max_width:
            for (i, width) in enumerate(self._widths):
                self._widths[i] = min(width, max_width)

        while term_width < border_width + sum(self._widths):
            extra_width = border_width + sum(self._widths) - term_width
            greatest_width = max(self._widths)
            for (i, width) in enumerate(self._widths):
                if width == greatest_width:
                    if self._widths[i] / 2 + 1 > extra_width:
                        self._widths[i] -= extra_width
                    else:
                        self._widths[i] = int(width / 2)
                    break

    def _stringify_header(self, options):
        bits = []
        (lpad, rpad) = self._get_padding_widths(options)
        if options['border']:
            if options['hrules'] in (ALL, FRAME):
                bits.append(self._hrule)
                bits.append('\n')
            if options['vrules'] in (ALL, FRAME):
                bits.append(options['vertical_char'])
            else:
                bits.append(' ')
        if not self._field_names:
            if options['vrules'] in (ALL, FRAME):
                bits.append(options['vertical_char'])
            else:
                bits.append(' ')
        for (field, width) in zip(self._field_names, self._widths):
            if options['fields'] and field not in options['fields']:
                continue
            if self._header_style == 'cap':
                fieldname = field.capitalize()
            elif self._header_style == 'title':
                fieldname = field.title()
            elif self._header_style == 'upper':
                fieldname = field.upper()
            elif self._header_style == 'lower':
                fieldname = field.lower()
            else:
                fieldname = field
            if options['header_color']:
                fieldname = colorify(fieldname, options['header_color'])
            bits.append(' ' * lpad + self._justify(fieldname, width, self._align[field]) + ' ' * rpad)
            if options['border']:
                if options['vrules'] == ALL:
                    bits.append(options['vertical_char'])
                else:
                    bits.append(' ')

        if options['border'] and options['vrules'] == FRAME:
            bits.pop()
            bits.append(options['vertical_char'])
        if options['border'] and options['hrules'] is not None:
            bits.append('\n')
            bits.append(self._hrule)
        return ('').join(bits)

    def get_string(self, **kwargs):
        options = self._get_options(kwargs)
        lines = []
        if self.rowcount == 0 and (not options['print_empty'] or not options['border']):
            return ''
        rows = self._get_rows(options)
        formatted_rows = self._format_rows(rows, options)
        self._compute_widths(formatted_rows, options)
        if options.get('auto_width', False):
            self._optimize_widths(options)
        self._hrule = self._stringify_hrule(options)
        if options['header']:
            lines.append(self._stringify_header(options))
        elif options['border'] and options['hrules'] in (ALL, FRAME):
            lines.append(self._hrule)
        for row in formatted_rows:
            lines.append(self._stringify_row(row, options))

        if options['border'] and options['hrules'] == FRAME:
            lines.append(self._hrule)
        return self._unicode('\n').join(lines)


def main():
    x = PrettyTable(['City name', 'Area', 'Population', 'Annual Rainfall'], auto_width=True, border=True, header_color='yellow,bold', left_padding_width=3, right_padding_width=3)
    x.sortby = 'Population'
    x.reversesort = True
    x.int_format['Area'] = '04d'
    x.float_format = '6.1f'
    x.align['City name'] = 'l'
    x.add_row(['Adelaide', 1295, 1158259, 600.5])
    x.add_row(['Brisbane', 5905, 1857594, 1146.4])
    x.add_row(['Darwin', 112, 120900, 1714.7])
    x.add_row(['Hobart', 1357, 205556, 619.5])
    x.add_row(['Sydney', 2058, 4336374, 1214.8])
    x.add_row(['Melbourne City', 1566, 3806092, 646.9])
    x.add_row(['Perth', 5386, 1554769, 869.4])
    print x


if __name__ == '__main__':
    main()