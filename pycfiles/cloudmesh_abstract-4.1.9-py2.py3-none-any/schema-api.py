# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/ENV2/lib/python2.7/site-packages/resources/experimental/schema-api.py
# Compiled at: 2017-04-12 13:00:41
from __future__ import print_function
from ruamel import yaml
import os
from os.path import splitext, exists
import glob
from cloudmesh.common.Shell import Shell
import json
from cloudmesh.common.util import writefile

class ConvertSpec(object):

    def __init__(self, infile, outfile, indent=2):
        if '.yml' in infile and '.json' in outfile:
            element = yaml.safe_load(open(infile))
            print('... writing to', outfile)
            writefile(outfile, json.dumps(element, indent=indent))
        else:
            print('conversion not yet supported')


class YmlToSpec(object):

    def __init__(self, infile, outfile=None, kind='yml'):
        self.execute(infile, outfile)

    def execute(self, infile, outfile):
        yfile = infile
        base, _ = splitext(yfile)
        texfile = base + '.tex'
        if exists(texfile):
            description = Shell.execute('pandoc', ['--to', 'rst', '--wrap', 'none', texfile])
        else:
            description = 'FIXME'
        example = yaml.safe_load(open(yfile))
        assert len(example) == 1, example

        def typeit(value):
            if isinstance(value, str) or isinstance(value, unicode):
                return 'string'
            if isinstance(value, int):
                return 'int'
            if isinstance(value, float):
                return 'float'
            if isinstance(value, bool):
                return 'bool'
            if isinstance(value, list):
                assert len(value) > 0
                subtype = typeit(value[0])
                return 'list of %s' % subtype
            if isinstance(value, dict):
                return 'dict'
            raise NotImplementedError(type(value), value)

        name = example.keys()[0]
        definition = dict()
        definition[name] = dict()
        for attr, value in example[name].iteritems():
            definition[name][attr] = {'type': typeit(value)}

        definition[name]['__description'] = str(description)
        definition[name]['__example'] = example[name]
        result = yaml.dump(definition, default_flow_style=False)
        with open(outfile, 'w') as (fd):
            fd.write(result)


class SpecToTex(object):

    def __init__(self, infile, dirout):
        if not os.path.exists(dirout):
            os.makedirs(dirout)
        name = os.path.basename(infile)
        initial = os.path.join(dirout, name)
        base, _ = os.path.splitext(initial)
        description_file = base + '.tex'
        example_file = base + '-example.yml'
        simple_file = base + '-simple.yml'
        spec_file = initial
        spec = yaml.safe_load(open(infile))
        assert len(spec) == 1, spec
        name = spec.keys()[0]
        description = spec[name]['__description']
        example = yaml.dump(spec[name]['__example'], default_flow_style=False, indent=4)

        def flatten(spec):
            flat = dict()
            for k, v in spec.iteritems():
                if k.startswith('__'):
                    continue
                typ = v['type']
                flat[k] = typ

            return flat

        flat = {name: flatten(spec[name])}
        flat = yaml.dump(flat, default_flow_style=False, indent=4)
        spec_str = yaml.dump(spec, default_flow_style=False, indent=4)
        for path, string in [(description_file, description), (example_file, example),
         (
          simple_file, flat), (spec_file, spec_str)]:
            print('   Writing', path)
            with open(path, 'w') as (fd):
                fd.write(string)