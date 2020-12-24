# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/pc.py
# Compiled at: 2014-07-07 15:44:50
from parameter.empty import Empty
from parameter.flag import Flag
from parameter.float import Float
from parameter.genomictagoption import GenomicTagOption
from parameter.int import Int
from parameter.label import Label
from parameter.option import Option
from parameter.fileinput import FileInput
from parameter.fileoutput import FileOutput
from parameter.fileoutputformat import FileOutputFormat
from parameter.string import String
from exceptions import AuthorParameterSpecificationError, ParameterValidationError
import argparse, warnings

class DefaultList(list):

    def __copy__(self):
        return []


class ParameterCollection(object):

    def __init__(self, desc, vers='1.0.0', argv=[]):
        self.params = []
        self.argv = argv
        self.cur_group = None
        self.argparser = argparse.ArgumentParser(description=desc)
        self.argparser.add_argument('--version', action='version', version='%(prog)s ' + str(vers))
        self.argparser.add_argument('-v', '--verbose', action='count', help='Produce more verbose output')
        return

    def validate(self):
        issue_count = 0
        for item in self.params:
            if not item.validate(self.parsed_args[item.name]):
                issue_count += 1

        return issue_count == 0

    def push_param(self, param):
        self._push(param)

    def push_params(self, params):
        for p in params:
            self.push_param(p)

    def _push(self, param):
        p = self._coerce_param(param)
        if p is not None:
            param_extracted = self.convert_params(p)
            argument_flags = param_extracted[0]
            extended_options = param_extracted[1]
            if self.get_current_group() is not None:
                self.get_current_group().add_argument(*argument_flags, **extended_options)
            else:
                self.argparser.add_argument(*argument_flags, **extended_options)
            self.params.append(p)
        return

    def convert_params(self, parameter_subclass_object):
        positional_args = []
        if parameter_subclass_object.short is not None:
            positional_args.append('-' + parameter_subclass_object.short)
        if parameter_subclass_object.name is not None:
            positional_args.append('--' + parameter_subclass_object.name)
        extended_args = self.sanitise_attrs(parameter_subclass_object)
        return [
         positional_args, extended_args]

    def sanitise_attrs(self, parameter_subclass_object):
        clean_attr = {}
        attr = parameter_subclass_object.get_all_keys()
        for key in attr:
            if key == 'action':
                if attr[key] in ('store', 'store_const', 'count', 'version', 'help'):
                    clean_attr[key] = attr[key]
            elif key in ('const', 'default', 'version'):
                clean_attr[key] = attr[key]

        if parameter_subclass_object.multiple:
            clean_attr['action'] = 'append'
        else:
            clean_attr['action'] = 'store'
        obj_type = type(parameter_subclass_object).__name__
        if obj_type == 'Option':
            try:
                clean_attr['choices'] = attr['options']
            except:
                raise AuthorParameterSpecificationError("Author failed to specify 'options' for an Option type parameter")

        elif obj_type == 'GenomicTagOption':
            clean_attr['choices'] = attr['options']
        elif obj_type == 'Int':
            clean_attr['type'] = int
        elif obj_type == 'Float':
            clean_attr['type'] = float
        elif obj_type == 'File':
            clean_attr['type'] = file
        elif obj_type == 'FileInput':
            clean_attr['type'] = argparse.FileType('r')
        elif obj_type == 'FileOutput':
            clean_attr['type'] = str
        elif obj_type == 'Flag':
            clean_attr['action'] = 'store_const'
            clean_attr['const'] = True
        elif obj_type == 'String':
            clean_attr['type'] = str
        elif obj_type == 'FileOutputFormat':
            clean_attr['type'] = str
        else:
            warnings.warn("I don't know how to handle a type of '%s'" % (
             type(parameter_subclass_object),), UserWarning)
        if parameter_subclass_object.description is not None:
            help_text = parameter_subclass_object.description
        if parameter_subclass_object.default is not None:
            if parameter_subclass_object.multiple and not isinstance(parameter_subclass_object.default, list):
                raise AuthorParameterSpecificationError('Author declared a multiple attribute, then provided a default value as a scalar, not a list')
            if parameter_subclass_object.multiple:
                clean_attr['default'] = DefaultList(parameter_subclass_object.default)
            else:
                clean_attr['default'] = parameter_subclass_object.default
            help_text += ' (Default: %(default)s)'
        if isinstance(parameter_subclass_object, Option):
            help_text += ' (Options: '
            pso_options = parameter_subclass_object.child_params['options']
            help_text += (', ').join(map(lambda key: '%s [%s]' % (
             pso_options[key], key), pso_options))
        if parameter_subclass_object.required:
            help_text += ' [Required]'
        clean_attr['help'] = help_text
        if parameter_subclass_object.hidden:
            clean_attr['help'] = argparse.SUPPRESS
        if 'action' not in clean_attr.keys() or 'action' in clean_attr.keys() and clean_attr['action'] != 'version' and clean_attr['action'] != 'count' and clean_attr['action'] != 'store_const':
            clean_attr['nargs'] = '?'
        return clean_attr

    def parse_short_name(self, name):
        try:
            return name[name.index('|') + 1:]
        except:
            return

        return

    def parse_long_name(self, name):
        try:
            return name[0:name.index('|')]
        except:
            return name

    def _coerce0(self, parts=[]):
        p = Empty()
        return p

    def _coerce1(self, parts=[]):
        p = Label(label=parts[0])
        self.add_group(parts[0])
        return p

    def _coerce2(self, parts=[]):
        p = Flag(name=self.parse_long_name(parts[0]), short=self.parse_short_name(parts[0]), multiple=False, description=parts[1])
        return p

    def _coerce3(self, parts=[]):
        attr = {'name': self.parse_long_name(parts[0]), 'short': self.parse_short_name(parts[0]), 
           'multiple': False, 'description': parts[1]}
        set_attr = parts[2]
        for opt in ('default options required hidden implies multiple _show_in_galaxy _galaxy_specific _cheetah_var data_format default_format file_format').split(' '):
            if opt in set_attr:
                attr[opt] = set_attr[opt]

        if 'validate' in set_attr:
            validate = set_attr['validate']
            if validate == 'Flag':
                return Flag(**attr)
            if validate == 'Float':
                for opt in ['min', 'max']:
                    if opt in set_attr:
                        attr[opt] = set_attr[opt]

                return Float(**attr)
            if validate == 'Int':
                for opt in ['min', 'max']:
                    if opt in set_attr:
                        attr[opt] = set_attr[opt]

                return Int(**attr)
            if validate == 'Option':
                for opt in ['options']:
                    if opt in set_attr:
                        attr[opt] = set_attr[opt]

                return Option(**attr)
            if validate == 'String':
                return String(**attr)
            if validate == 'File/Input':
                return FileInput(**attr)
            if validate == 'File/Output':
                return FileOutput(**attr)
            if validate == 'Genomic/Tag':
                return GenomicTagOption(**attr)
            if validate == 'File/OutputFormat':
                return FileOutputFormat(**attr)
            raise ParameterValidationError('Error validating parameter type: ' + validate)
        else:
            return Flag(**attr)

    def _coerce_param(self, param=[]):
        if len(param) == 0:
            return
        else:
            if len(param) == 1:
                self._coerce1(param)
                return
            if len(param) == 2:
                return self._coerce2(param)
            if len(param) == 3:
                return self._coerce3(param)
            return

    def get_by_name(self, name):
        for item in self.params:
            if item.name == name:
                return item

        return

    def getarg(self, argv_override=None):
        if argv_override is not None:
            args = self.argparser.parse_args(argv_override)
        else:
            args = self.argparser.parse_args(self.argv[1:])
        self.parsed_args = vars(args)
        return self.parsed_args

    def get_current_group(self):
        return self.cur_group

    def add_group(self, name):
        self.cur_group = self.argparser.add_argument_group(name)