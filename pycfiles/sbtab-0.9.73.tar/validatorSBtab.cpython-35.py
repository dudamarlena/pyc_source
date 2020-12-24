# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/timo/Desktop/projects/SBtab/pypi_installer/sbtab/validatorSBtab.py
# Compiled at: 2018-10-25 03:40:01
# Size of source mod 2**32: 14710 bytes
"""
SBtab Validator
===============

Python script that validates SBtab files

See specification for further information.
"""
try:
    from . import SBtab
    from . import misc
except:
    import SBtab, misc

import re, collections, sys, os

class SBtabError(Exception):
    __doc__ = '\n    Base class for errors in the SBtab validation class.\n    '

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ValidateTable:
    __doc__ = '\n    Validates SBtab file and SBtab object.\n    '

    def __init__(self, sbtab, def_table=None):
        """
        Initialises validator and starts check for file and table format.

        Parameters
        ----------
        table: SBtab object
            SBtab data file as SBtab object
        sbtab_name: str
            File path of the SBtab data file
        def_table: SBtab object
            SBtab definition table as SBtab object
        """
        self.warnings = []
        self.sbtab = sbtab
        self.filename = sbtab.filename
        self.read_definition(def_table)
        self.allowed_table_types = list(set([row[2] for row in self.definitions[2:][0]]))
        self.allowed_columns = {}
        for table_type in self.allowed_table_types:
            self.allowed_columns[table_type] = [row[0] for row in self.definitions[2:][0] if row[2] == table_type]

        self.check_general_format()
        self.column2format = {}
        defs = self.definitions[2]
        for row in defs:
            if row[2] == self.sbtab.table_type:
                self.column2format[row[0]] = row[3]

        columns = []
        for element in self.sbtab.columns:
            if element == '':
                pass
            else:
                columns.append(element)

        self.sbtab.columns = columns
        self.check_table_content()

    def read_definition(self, def_table):
        """
        read the required definition file; either it is provided by the user
        or the default definition file is read in; otherwise program exit
        """
        if def_table:
            try:
                self.sbtab_def = def_table
                self.definitions = self.sbtab_def.create_list()
            except:
                print('Definition file could not be loaded, so the validationcould not be started. Please provide definition fileas argument')
                sys.exit()

        try:
            path_ = os.path.join(os.path.dirname(__file__), '../definition_table/definitions.tsv')
            def_file = open(path_, 'r')
            def_table = def_file.read()
            self.sbtab_def = SBtab.SBtabTable(def_table, 'definitions.tsv')
            self.definitions = self.sbtab_def.create_list()
            def_file.close()
        except:
            print('Definition file could not be loaded, so the validation\n                could not be started. Please provide definition file\n                as argument')
            sys.exit()

    def check_general_format(self):
        """
        Validates format of SBtab file, checks file format and header row.
        """
        header = self.sbtab.header_row
        quotes = [
         '"', 'â\x80\x9d', 'â\x80\x98', 'â\x80\x99',
         'â\x80\x9b', 'â\x80\x9c', 'â\x80\x9f',
         'â\x80²', 'â\x80³', 'â\x80´',
         'â\x80µ', 'â\x80¶', 'â\x80·']
        for quote in quotes:
            try:
                header = header.replace(quote, "'")
            except:
                pass

        if not header.startswith('!!'):
            self.warnings.append('Error: The header row of the table does not\n                                 start with "!!SBtab". This file cannot be v\n                                 alidated.')
        if not re.search("TableType='([^']*)'", header):
            self.warnings.append('Error: The attribute TableType is not defin\n                                 ed in the SBtab table; This file cannot be\n                                 validated.')
        if not re.search("TableName='([^']*)'", header):
            self.warnings.append('Warning: The (optional) attribute TableName\n                                 is not defined in the SBtab table.')
        for column in self.sbtab.columns:
            if not column.startswith('!') and column != '':
                self.warnings.append('Warning: Column %s does not start with\n                an exclamation mark. It will not be processed.' % column)

        if len(self.sbtab.value_rows) < 1:
            self.warnings.append('Warning: Column %s does not start with\n            an exclamation mark. It will not be processed.' % column)
        for vr in self.sbtab.value_rows:
            if len(vr) != len(self.sbtab.columns):
                self.warnings.append('Warning: The length of row %s does notcorrespond to the amount of columns,which is %s.' % (
                 vr, len(self.sbtab.columns)))

    def check_table_content(self):
        """
        Validates the mandatory format of the SBtab in accordance to the
        TableType attribute.
        """
        if self.sbtab.table_type not in self.allowed_table_types:
            self.warnings.append('Warning: The SBtab file has an invalid TableType in its header: %s. Thus, the validity of its columns cannot be checked' % self.sbtab.table_type)
            return
        unique = []
        for row in self.sbtab.value_rows:
            try:
                identifier = row[self.sbtab.columns_dict['!ID']]
            except:
                break

            if identifier not in unique:
                unique.append(identifier)
            else:
                warning = 'Warning: There is an identifier that is not unique. Please change that: %s' % identifier
                self.warnings.append(warning)
            try:
                int(identifier[0])
                self.warnings.append('Warning: There is an identifier that starts with a digit; this is not permitted for the SBML conversion:%s' % identifier)
            except:
                pass

        if self.sbtab.table_type == 'Reaction' and '!ReactionFormula' not in self.sbtab.columns_dict:
            ident = False
            for it in self.sbtab.columns_dict:
                if it.startswith('!Identifier'):
                    ident = True
                    break

            if not ident:
                warning = 'Error: A Reaction SBtab needs at least a column !ReactionFormula or an !Identifier column tobe characterised.'
                self.warnings.append(warning)
        if self.sbtab.table_type == 'Quantity' and '!Unit' not in self.sbtab.columns_dict:
            warning = 'Error: A Quantity SBtab requires the column "Unit". Please add this column to the SBtab file.'
            self.warnings.append(warning)
        for column in self.sbtab.columns:
            if column.replace('!', '') not in self.allowed_columns[self.sbtab.table_type] and 'Identifiers:' not in column and 'ID:urn.' not in column:
                self.warnings.append('Warning: The SBtab file has an unknown column: %s.\nPlease use only supported column types!' % column)

        for row in self.sbtab.value_rows:
            if '!ID' in self.sbtab.columns_dict and (str(row[self.sbtab.columns_dict['!ID']]).startswith('+') or str(row[self.sbtab.columns_dict['!ID']]).startswith('-')):
                self.warnings.append('Warning: An identifier for a data row must not begin with "+" or "-": \n%s' % row)
            if '!ReactionFormula' in self.sbtab.columns_dict and '<=>' not in row[self.sbtab.columns_dict['!ReactionFormula']]:
                warning = 'There is a sum formula that does not adhere to the sum formula syntax from the SBtab specification: %s' % str(row[self.sbtab.columns_dict['!ReactionFormula']])
                self.warnings.append(warning)
            for i, entry in enumerate(row):
                if entry == '':
                    pass
                else:
                    if self.sbtab.columns[i][1:].startswith('Identifier'):
                        req_format = 'string'
                    else:
                        try:
                            req_format = self.column2format[self.sbtab.columns[i][1:]]
                        except:
                            continue

                if req_format == 'Boolean':
                    if entry != 'True' and entry != 'False' and entry != 'TRUE' and entry != 'FALSE' and entry != '0' and entry != '1':
                        warning = 'Warning: The column %s holds a value that does not conform with the assigned column format %s: %s' % (
                         self.sbtab.columns[i][1:],
                         req_format, entry)
                        self.warnings.append(warning)
                elif req_format == 'float':
                    try:
                        float(entry)
                    except:
                        warning = 'Warning: The column %s holds a value that does not conform with the assigned column format %s: %s' % (
                         self.sbtab.columns[i][1:],
                         req_format, entry)
                        self.warnings.append(warning)

                elif req_format == '{+,-,0}' and entry != '+' and entry != '-' and entry != '0':
                    warning = 'Warning: The column %s holds a value that does not conform with the assigned column format %s: %s' % (
                     self.sbtab.columns[i][1:],
                     req_format, entry)
                    self.warnings.append(warning)

        for column in collections.Counter(self.sbtab.columns).items():
            if column[1] > 1:
                self.warnings.append('Warning: There was a duplicate column i\n                                     n this SBtab file. Please remove it:\n                                     %s' % str(column[0]))

    def return_output(self):
        """
        Returns the warnings from the validation process.
        """
        return self.warnings


class ValidateDocument:
    __doc__ = '\n    Validates SBtabDocument object\n    '

    def __init__(self, sbtab_doc, def_table=None):
        """
        Initialises validator and starts check for file and table format.

        Parameters
        ----------
        sbtab_doc:
            SBtabDocument object
        """
        self.sbtab_doc = sbtab_doc
        self.sbtab_def = def_table

    def validate_document(self):
        """
        validate SBtabDocument
        """
        warnings = []
        for sbtab in self.sbtab_doc.sbtabs:
            warnings_s = [
             'Warnings for %s:\n' % sbtab.filename]
            self.vt = ValidateTable(sbtab, self.sbtab_def)
            try:
                warnings_s.append(self.vt.return_output())
            except:
                raise SBtabError('SBtab %s cannot be validated.' % sbtab.filename)

            warnings.append(warnings_s)

        return warnings


if __name__ == '__main__':
    try:
        sys.argv[1]
    except:
        print('You have not provided input arguments. Please start the script\n               by also providing an SBtab file and the required definition f\n               ile: >python validatorSBtab.py SBtab.csv definition.tsv')
        sys.exit()

    file_name = sys.argv[1]
    sbtab_file_o = open(file_name, 'r')
    sbtab_file = sbtab_file_o.read()
    sbtab_file_o.close()
    delimiter = misc.getDelimiter(sbtab_file)
    try:
        default_def = sys.argv[2]
        def_file = open(default_def, 'r')
        def_tab = def_file.read()
        def_file.close()
    except:
        def_tab = None

    validator_output = []
    Validate_file_class = ValidateFile(sbtab_file, file_name)
    validator_output.append(Validate_file_class.return_output())
    Validate_table_class = ValidateTable(sbtab_file, file_name, def_tab)
    validator_output.append(Validate_table_class.return_output())
    warned = False
    for warning in validator_output:
        if warning != []:
            print('WARNINGS: ', warning)
            warned = True

    if not warned:
        print('The SBtab file is valid.')