# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/processor/pipeline.py
# Compiled at: 2019-08-18 21:39:21
import ctypes, re, os
from ..processor.operations import *
from ..processor.dependencies import find_dependencies
from ..ctypedescs import *
from ..messages import *

def process(data, options):
    status_message('Processing description list.')
    find_dependencies(data, options)
    automatically_typedef_structs(data, options)
    remove_NULL(data, options)
    remove_descriptions_in_system_headers(data, options)
    filter_by_regexes_exclude(data, options)
    filter_by_regexes_include(data, options)
    remove_macros(data, options)
    if options.output_language == 'python':
        fix_conflicting_names(data, options)
    find_source_libraries(data, options)
    calculate_final_inclusion(data, options)
    print_errors_encountered(data, options)
    calculate_final_inclusion(data, options)


def calculate_final_inclusion(data, opts):
    """calculate_final_inclusion() calculates which descriptions will be included in the
    output library.

    An object with include_rule="never" is never included.
    An object with include_rule="yes" is included if its requirements can be
        included.
    An object with include_rule="if_needed" is included if an object to be
        included requires it and if its requirements can be included.
    """

    def can_include_desc(desc):
        if desc.can_include == None:
            if desc.include_rule == 'no':
                desc.can_include = False
            elif desc.include_rule == 'yes' or desc.include_rule == 'if_needed':
                desc.can_include = True
                for req in desc.requirements:
                    if not can_include_desc(req):
                        desc.can_include = False

        return desc.can_include

    def do_include_desc(desc):
        if desc.included:
            return
        desc.included = True
        for req in desc.requirements:
            do_include_desc(req)

    for desc in data.all:
        desc.can_include = None
        desc.included = False

    for desc in data.all:
        if desc.include_rule == 'yes':
            if can_include_desc(desc):
                do_include_desc(desc)

    return


def print_errors_encountered(data, opts):
    for desc in data.all:
        if desc.included or opts.show_all_errors:
            if opts.show_long_errors or len(desc.errors) + len(desc.warnings) <= 2:
                for error, cls in desc.errors:
                    if isinstance(desc, MacroDescription):
                        if opts.show_macro_warnings:
                            warning_message(error, cls)
                    else:
                        error_message(error, cls)

                for warning, cls in desc.warnings:
                    warning_message(warning, cls)

            elif desc.errors:
                error1, cls1 = desc.errors[0]
                error_message(error1, cls1)
                numerrs = len(desc.errors) - 1
                numwarns = len(desc.warnings)
                if numwarns:
                    error_message('%d more errors and %d more warnings for %s' % (
                     numerrs, numwarns, desc.casual_name()))
                else:
                    error_message('%d more errors for %s ' % (numerrs, desc.casual_name()))
            else:
                warning1, cls1 = desc.warnings[0]
                warning_message(warning1, cls1)
                warning_message('%d more errors for %s' % (len(desc.warnings) - 1, desc.casual_name()))
        if desc.errors:
            desc.include_rule = 'never'