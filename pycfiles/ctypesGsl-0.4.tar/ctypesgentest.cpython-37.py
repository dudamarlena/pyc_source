# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/test/ctypesgentest.py
# Compiled at: 2019-09-02 10:47:47
# Size of source mod 2**32: 2667 bytes
import os, sys, io, optparse, glob, json
try:
    from importlib import reload as reload_module
except:
    reload_module = reload

sys.path.append('.')
sys.path.append('..')
import ctypesgen
redirect_stdout = True

def test(header, **more_options):
    if not isinstance(header, str):
        raise AssertionError
    else:
        with open('temp.h', 'w') as (f):
            f.write(header)
        options = ctypesgen.options.get_default_options()
        options.headers = ['temp.h']
        for opt, val in more_options.items():
            setattr(options, opt, val)

        if redirect_stdout:
            sys.stdout = io.StringIO()
        else:
            descriptions = ctypesgen.parser.parse(options.headers, options)
            ctypesgen.processor.process(descriptions, options)
            printer = None
            if options.output_language.startswith('py'):
                ctypesgen.printer_python.WrapperPrinter('temp.py', options, descriptions)
                module = __import__('temp')
                reload_module(module)
                retval = module
            elif options.output_language == 'json':
                ctypesgen.ctypedescs.last_tagnum = 0
                ctypesgen.printer_json.WrapperPrinter('temp.json', options, descriptions)
                with open('temp.json') as (f):
                    JSON = json.load(f)
                retval = JSON
            else:
                raise RuntimeError('No such output language `' + options.output_language + "'")
        if redirect_stdout:
            output = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = sys.__stdout__
        else:
            output = ''
    return (retval, output)


def cleanup(filepattern='temp.*'):
    fnames = glob.glob(filepattern)
    for fname in fnames:
        os.unlink(fname)