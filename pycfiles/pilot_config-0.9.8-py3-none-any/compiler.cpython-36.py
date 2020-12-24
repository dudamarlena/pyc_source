# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amd/work/pilot/pilotconfig/pilot/compiler/rust/compiler.py
# Compiled at: 2020-01-31 08:26:52
# Size of source mod 2**32: 2362 bytes
import os, sys, subprocess, json
from distutils.dir_util import copy_tree
from shutil import copyfile, move
import yaml, lazy_import
from sys import platform as _platform
Compiler = lazy_import.lazy_callable('pybars.Compiler')
os = lazy_import.lazy_module('os')
json = lazy_import.lazy_module('json')
itertools = lazy_import.lazy_module('itertools')
string = lazy_import.lazy_module('string')
re = lazy_import.lazy_module('re')
defaultdict = lazy_import.lazy_callable('collections.defaultdict')
fnmatch = lazy_import.lazy_module('fnmatch')

def init(config, model):
    pass


def program(config):
    pass


def templateparser(args, dir, model, compiler, helpers):
    for subdir, dirs, files in os.walk(dir):
        outdir = os.path.join(args.workdir, os.path.relpath(subdir, dir))
        for file in files:
            infile = os.path.join(subdir, file)
            with open(infile) as (f):
                if infile.endswith('.templ'):
                    template = compiler.compile(f.read())
                    output = template(model, helpers)
                else:
                    output = f.read()
                with open(os.path.join(outdir, os.path.splitext(os.path.basename(infile))[0]), 'w+') as (f):
                    f.write(output)


def parsetemplate(out_path, templatedata, dir):
    template_path = os.path.join(dir, 'template')
    compiler = Compiler()
    for subdir, _dirs, files in os.walk(template_path):
        outdir = os.path.join(out_path, os.path.relpath(subdir, template_path))
        for file in files:
            infile = os.path.join(subdir, file)
            with open(infile) as (f):
                if infile.endswith('.templ'):
                    template = compiler.compile(f.read())
                    output = template(templatedata)
                    with open(os.path.join(outdir, os.path.splitext(os.path.basename(infile))[0]), 'w+') as (f):
                        f.write(output)


def main(args, config, model, projectdir, compilerdir):
    parsetemplate(projectdir, model, compilerdir)
    subprocess.call(['make', '-C', args.workdir])
    return 0