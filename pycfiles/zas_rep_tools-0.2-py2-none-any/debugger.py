# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/utils/debugger.py
# Compiled at: 2018-09-30 20:51:11
import platform, sys
from kitchen.text.converters import getwriter
import inspect, re, traceback
if platform.uname()[0].lower() != 'windows':
    from blessings import Terminal
from nose.plugins.attrib import attr
from cached_property import cached_property
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
t = Terminal()
colores = {'b': 't.bold_on_bright_blue', 'r': 't.bold_on_bright_red', 'g': 't.bold_on_bright_green', 'w': 't.bold_black_on_bright_white', 'm': 't.bold_white_on_bright_magenta', 'c': 't.bold_white_on_bright_cyan', 'y': 't.bold_white_on_bright_yellow', 'b': 't.bold_white_on_bright_black'}
pattern = re.compile('\\(\\s?\\((.*?)\\).*\\).*$')

def p(context_to_print, name_to_print='DEBUGING', c='w', r=False):
    """
    Functionality: Print-Function for Debigging 
    """
    try:
        context_to_print = context_to_print.decode('utf-8')
    except:
        pass

    if platform.uname()[0].lower() != 'windows':
        if isinstance(context_to_print, tuple):
            stack = traceback.extract_stack()
            filename, lineno, function_name, code = stack[(-2)]
            var_names = pattern.search(code)
            if var_names:
                var_names = var_names.groups()[0]
                var_names = var_names.strip(' ').strip(',').strip(' ')
                var_names = var_names.split(',')
                var_names = [ var.strip(' ') for var in var_names ]
                if len(context_to_print) == len(var_names):
                    temp_elem_to_print = ''
                    for var_name, var_value in zip(var_names, context_to_print):
                        var_value = repr(var_value) if r else var_value
                        var_name = var_name if "'" not in var_name and '"' not in var_name else None
                        temp_elem_to_print += ('\n   {start}{var_name}{stop}  = {var_value}\n').format(var_name=var_name, var_value=var_value, t=t, start=t.bold_magenta, stop=t.normal)

                    if temp_elem_to_print:
                        r = False
                        context_to_print = temp_elem_to_print
                else:
                    print 'ERROR(P): No right Number of extracted val_names'
        context_to_print = repr(context_to_print) if r else context_to_print
        print ('\n\n{start} <{0}>{stop}  \n  {1}  \n   {start} </{0}>{stop}\n').format(name_to_print, context_to_print, t=t, start=eval(colores[c]), stop=t.normal)
    else:
        print "p() is not supported for 'Windows'-OS."
    return


def wipd(f):
    """
    decorator for nose attr.
    """
    return attr('wipd')(f)


def wipdn(f):
    """
    decorator for nose attr.
    """
    return attr('wipdn')(f)


def wipdl(f):
    """
    decorator for nose attr.
    """
    return attr('wipdl')(f)


def wipdo(f):
    """
    decorator for nose attr.
    """
    return attr('wipdo')(f)