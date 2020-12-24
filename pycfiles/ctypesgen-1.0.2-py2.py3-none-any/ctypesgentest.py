# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/test/ctypesgentest.py
# Compiled at: 2019-09-02 10:47:47
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
    assert isinstance(header, str)
    with open('temp.h', 'w') as (f):
        f.write(header)
    options = ctypesgen.options.get_default_options()
    options.headers = ['temp.h']
    for opt, val in more_options.items():
        setattr(options, opt, val)

    if redirect_stdout:
        sys.stdout = io.StringIO()
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