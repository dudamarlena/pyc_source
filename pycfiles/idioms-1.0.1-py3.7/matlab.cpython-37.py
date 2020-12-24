# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/idioms/utils/matlab.py
# Compiled at: 2019-05-09 14:32:24
# Size of source mod 2**32: 2400 bytes
import re, os
from munch import Munch
test_str = '\nNfft = 156\na_camel_cased_Arg = 1\nscientific_notation = 1e-6\ndo_matlab_lines_have_semicolons = 1;\n% here is a comment!\n% more comments\n% a comment that has an assignment statement in it\n% x = 3\nan_alias = scientific_notation;\nm\na_derived_variable = Nfft + a_camel_cased_Arg\na_reduced_array = sum(Nfft, a_camel_cased_arg, scientific_notation);\nfor x in someMatlabObject\n    result.x += x\nend\n    '
boilerplate_end = "        % and yeah that's pretty much that\n      catch ME:\n          if you_can\n              this = some_error_Reporting_stuff\n              do_some_more_things(ME)\n              goodbye()\n              "
boilerplate_start = '        try\n               % boilerplate here\n               g = R^arctan(pi)\n               for file in some_remote_glob:\n                  do_something(file)'

def extract_atomic_variables(file_contents):
    symbol_table = {}
    body = []
    patt = re.compile('\\s*([\\w_\\d]+)+\\s*=\\s*([\\d\\-e]+)[;%\\s]*')
    for line in file_contents.split('\n'):
        matches = re.match(patt, line)
        if matches:
            sandbox = {}
            try:
                exec(line.strip(), sandbox)
            except Exception as e:
                try:
                    body.append(line)
                finally:
                    e = None
                    del e

            for k, v in sandbox.items():
                if type(v) in (int, complex, float):
                    symbol_table[k] = v

        else:
            body.append(line)

    body = '\n        '.join(body)
    return Munch({'body':body,  'vars':symbol_table})


def gen_header(atoms):
    head = '%%%%%% SomeHeaderInitializationKeyword'
    tail = '%%%%%% ThisClosesTheHeader'
    header = [head]
    for k, v in atoms.items():
        header.append(f"%{k} %{v}")

    header.append(tail)
    return '\n'.join(header)


def gen_signature(filepath):
    function_name, _ = os.path.splitext(os.path.basename(filepath))
    function_name = function_name[:-3]
    return f"function {function_name}(inputFile, somethingElse, here_is_an_array_of_butts) {{"


def interpolate_sim_code(filepath='/home/kzeidler/mcc/TestSPRITE_IM.m', sim_code=test_str, boilerplate_start=boilerplate_start, boilerplate_end=boilerplate_end):
    header, extracted_code = gen_header(sim_code)
    sig = gen_signature(filepath)
    body = f"{header}\n{sig}\n{boilerplate_start}\n{extracted_code}\n{boilerplate_end}\n    "
    return body