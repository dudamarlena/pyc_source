# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pandoc_include.py
# Compiled at: 2020-04-29 23:52:11
# Size of source mod 2**32: 4659 bytes
"""
Panflute filter to allow file includes

Each include statement has its own line and has the syntax:

    !include ../somefolder/somefile

    !include-header ./header.yaml

Or

    $include ../somefolder/somefile

    $include-header ./header.yaml

Each include statement must be in its own paragraph. That is, in its own line
and separated by blank lines.

If no extension was given, ".md" is assumed.
"""
import os, panflute as pf, yaml, json
from collections import OrderedDict

def is_include_line(elem):
    if len(elem.content) < 3:
        return 0
        if not all((isinstance(x, (pf.Str, pf.Space)) for x in elem.content)):
            return 0
    elif elem.content[0].text != '!include':
        if elem.content[0].text != '$include':
            if elem.content[0].text != '!include-header' and elem.content[0].text != '$include-header':
                return 0
    if type(elem.content[1]) != pf.Space:
        return 0
    if elem.content[0].text == '!include' or elem.content[0].text == '$include':
        return 1
    return 2


def get_filename(elem, includeType):
    fn = pf.stringify(elem, newlines=False).split(maxsplit=1)[1]
    if not os.path.splitext(fn)[1]:
        if includeType == 1:
            fn += '.md'
        else:
            fn += '.yaml'
    return fn


entryEnter = False
options = None
temp_filename = '.temp.pandoc-include'

def action(elem, doc):
    global entryEnter
    global options
    if isinstance(elem, pf.Para):
        includeType = is_include_line(elem)
        if includeType == 0:
            return
        if options is None:
            try:
                with open(temp_filename, 'r') as (f):
                    options = json.load(f)
            except:
                options = {}

        pandoc_options = doc.get_metadata('pandoc-options')
        if not pandoc_options:
            if 'pandoc-options' in options:
                pandoc_options = options['pandoc-options']
            else:
                pandoc_options = [
                 '--filter=pandoc-include']
        else:
            for i in range(len(pandoc_options)):
                pandoc_options[i] = pandoc_options[i].replace('–', '--')

            options['pandoc-options'] = pandoc_options
        entry = doc.get_metadata('include-entry')
        if not entryEnter:
            if entry:
                os.chdir(entry)
                entryEnter = True
        fn = get_filename(elem, includeType)
        if not os.path.isfile(fn):
            raise ValueError('Included file not found: ' + '%r %r %r' % (fn, entry, os.getcwd()))
        with open(fn, encoding='utf-8') as (f):
            raw = f.read()
        cur_path = os.getcwd()
        target = os.path.dirname(fn)
        if not target:
            target = '.'
        os.chdir(target)
        with open(temp_filename, 'w+') as (f):
            json.dump(options, f)
        new_elems = None
        new_metadata = None
        if includeType == 1:
            new_elems = pf.convert_text(raw,
              extra_args=pandoc_options)
            new_metadata = pf.convert_text(raw, standalone=True, extra_args=pandoc_options).get_metadata()
        else:
            new_metadata = yaml.load(raw)
            new_metadata = OrderedDict(new_metadata)
        for key in new_metadata:
            if key not in doc.get_metadata():
                doc.metadata[key] = new_metadata[key]

        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        os.chdir(cur_path)
        return new_elems


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()