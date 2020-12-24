# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/utils/csv2xml.py
# Compiled at: 2018-08-13 08:58:37
from __future__ import print_function, unicode_literals
from io import open
import sys
reload(sys)
sys.setdefaultencoding(b'utf8')
import csv, sys
from optparse import OptionParser, OptionGroup

def replace(text, s, r):
    return r.join(text.split(s))


def openio(filename, mode, encoding, newline=None):
    if filename == b'-':
        filename = None
    if filename:
        return open(filename, mode=mode, encoding=encoding, newline=newline)
    else:
        if mode == b'r':
            return sys.stdin
        if mode == b'w':
            return sys.stdout
        raise ValueError(b'mode not recognized')
        return


def field_subst_factory(newline):
    newline_tag = (b'<{0}/>').format(newline)

    def text_replace(field):
        return replace(field, b'\n', newline_tag)

    def text_keep(field):
        return field

    if newline:
        return text_replace
    else:
        return text_keep


class Writer:

    def __init__(self, ofile, args):
        self.file = ofile
        self.args = args
        self.newline_subst = field_subst_factory(args.newline_elem)
        if args.header:
            self.fieldname = self.__fieldname_header
        elif args.flat_fields:
            self.fieldname = self.__fieldname_flat
        else:
            self.fieldname = self.__fieldname_indexed

    def write_file(self, data):
        if self.args.declaration:
            declaration = (b'<?xml version="1.0" encoding="{0}"?>').format(self.args.oencoding)
            self.write(declaration)
        self.write((b'<{0}>').format(self.args.root_elem))
        for record in data:
            self.write_record(record)

        self.write((b'</{0}>').format(self.args.root_elem))

    def write_record(self, record):
        self.write((b'{0}<{1}>').format(self.args.indent, self.args.record_elem))
        for index, field in enumerate(record):
            self.write_field(field, index)

        self.write((b'{0}</{1}>').format(self.args.indent, self.args.record_elem))

    def write_field(self, field, index):
        self.write((b'{0}{0}<{1}>{2}</{1}>').format(self.args.indent, self.fieldname(index), self.newline_subst(field)))

    def write(self, text):
        print(text, file=self.file, end=self.args.linebreak)

    def __fieldname_header(self, index):
        return self.args.header[index]

    def __fieldname_flat(self, index):
        return self.args.field_elem

    def __fieldname_indexed(self, index):
        return self.args.field_elem + str(index)


def cleanup_callback(option, opt, value, parser):
    result = replace(value, b'\\n', b'\n')
    result = replace(result, b'\\t', b'\t')
    setattr(parser.values, option.dest, result)


def parse_cmdline():
    usage = b'usage: %prog [options] IFILE'
    parser = OptionParser(usage)
    parser.set_defaults(iencoding=b'UTF-8', oencoding=b'UTF-8', delimiter=b',', doublequote=True, quotechar=b'"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=False, header=False, declaration=False, root_elem=b'root', record_elem=b'record', field_elem=b'field', flat_fields=False, indent=b'    ', linebreak=b'\n')
    parser.add_option(b'-o', b'--output-file', dest=b'ofile', help=b'save to file OFILE')
    parser.add_option(b'-c', b'--input-encoding', dest=b'iencoding', help=b'input file encoding')
    parser.add_option(b'-C', b'--output-encoding', dest=b'oencoding', help=b'output file encoding')
    igroup = OptionGroup(parser, b'CSV Dialect Options')
    igroup.add_option(b'-d', b'--delimiter', dest=b'delimiter', type=b'str', action=b'callback', callback=cleanup_callback, help=b'a one-character string used to separate fields')
    igroup.add_option(b'-b', b'--no-doublequote', action=b'store_false', dest=b'doublequote', help=b'controls how instances of quotechar appearing inside a field should be themselves be quoted')
    igroup.add_option(b'-e', b'--escapechar', help=b'the escapechar removes any special meaning from the following character')
    igroup.add_option(b'-q', b'--quotechar', help=b'A one-character string used to quote fields containing special characters')
    igroup.add_option(b'--quote-all', dest=b'quoting', action=b'store_const', const=csv.QUOTE_ALL, help=b'quote all field (READER?)')
    igroup.add_option(b'--quote-minimal', dest=b'quoting', action=b'store_const', const=csv.QUOTE_MINIMAL, help=b'quote only special characters (WRITER?)')
    igroup.add_option(b'--quote-nonnumeric', dest=b'quoting', action=b'store_const', const=csv.QUOTE_NONNUMERIC, help=b'convert all non-quoted fields to type float')
    igroup.add_option(b'--quote-none', dest=b'quoting', action=b'store_const', const=csv.QUOTE_NONE, help=b'perform no special processing of quote characters')
    igroup.add_option(b'-s', b'--skipinitialspace', action=b'store_true', help=b'if whitespace immediately following the delimiter should be ignored')
    igroup.add_option(b'-a', b'--header', action=b'store_true', help=b'read field names from file')
    ogroup = OptionGroup(parser, b'XML Dialect Options')
    ogroup.add_option(b'-x', b'--xml-declaration', dest=b'declaration', action=b'store_true', help=b'whether to output an XML declaration')
    ogroup.add_option(b'-t', b'--root-element', dest=b'root_elem', help=b'name of the root element')
    ogroup.add_option(b'-r', b'--record-element', dest=b'record_elem', help=b'name of the record-level element')
    ogroup.add_option(b'-f', b'--field-element', dest=b'field_elem', help=b'name of the field-level element')
    ogroup.add_option(b'-n', b'--newline-element', dest=b'newline_elem', help=b'name of the line break element')
    ogroup.add_option(b'-l', b'--flat-fields', action=b'store_true', help=b'disable field element numbering')
    ogroup.add_option(b'-i', b'--indent', dest=b'indent', type=b'str', action=b'callback', callback=cleanup_callback, help=b'indentation')
    ogroup.add_option(b'-k', b'--linebreak', dest=b'linebreak', type=b'str', action=b'callback', callback=cleanup_callback, help=b'line break character in output file')
    parser.add_option_group(igroup)
    parser.add_option_group(ogroup)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error(b'incorrect number of arguments')
    options.ifile = args[0]
    return options


if __name__ == b'__main__':
    args = parse_cmdline()
    csv.register_dialect(b'custom', delimiter=args.delimiter, doublequote=args.doublequote, escapechar=args.escapechar, quotechar=args.quotechar, quoting=args.quoting, skipinitialspace=args.skipinitialspace)
    with openio(args.ifile, mode=b'r', encoding=args.iencoding, newline=b'') as (ifile):
        csvreader = csv.reader(ifile, dialect=b'custom')
        if args.header:
            args.header = next(csvreader)
        with openio(args.ofile, b'w', args.oencoding) as (ofile):
            writer = Writer(ofile, args)
            writer.write_file(csvreader)