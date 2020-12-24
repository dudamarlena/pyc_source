# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/siddon/parse_templates.py
# Compiled at: 2011-01-11 11:47:19
import os, numpy as np
names = ('C_siddon', )
c_siddon_template = 'siddon' + os.sep + 'C_siddon.c.template'
templates = (
 c_siddon_template,)
ctypes = {'float': 'float32', 'double': 'float64'}
obstacles = {'none': None, 'sun': 'sun'}
pjs = {'pj': 'pj', 'bpj': 'bpj', 'pjt': 'pjt', 'bpjt': 'bpjt'}
string_dict = {'f': '%f', 'd': '%d'}
siddon_dict_list = []
for ctype in ctypes:
    for obstacle in obstacles:
        for pj in pjs:
            tmp_dict = {}
            tmp_dict['ctype'] = ctype
            tmp_dict['obstacle'] = obstacle
            tmp_dict['pj'] = pj
            siddon_dict_list.append(tmp_dict)

del tmp_dict
del ctype
del obstacle

def generate_sources():
    for replace_dict in siddon_dict_list:
        replace_dict['suffix'] = get_suffix(replace_dict)
        for template in templates:
            parse_template(template, replace_dict)


def parse_template(filename, values=None):
    f = open(filename, 'r')
    txt = f.read()
    f.close()
    if values is not None:
        values.update(string_dict)
        txt = txt % values
    out_filename = set_filename(filename, values)
    if os.path.isfile(out_filename):
        os.remove(out_filename)
    f_out = open(out_filename, 'w')
    f_out.write(txt)
    return


def set_filename(filename, values):
    filename_list = filename.split(os.extsep)[:-1]
    filename_list[(-2)] += values['suffix']
    return ('.').join(filename_list)


def reverse_dict(in_dict):
    out_dict = dict()
    for k in in_dict:
        out_dict[in_dict[k]] = k

    return out_dict


ctypes_inv = reverse_dict(ctypes)
obstacles_inv = reverse_dict(obstacles)

def get_suffix(values):
    return '_' + ('_').join(values.values())


def get_suffix_str(values):
    return '_' + ('_').join([ '%(' + key + ')s' for key in values ])


suffix_str = get_suffix_str(siddon_dict_list[0])
if __name__ == '__main__':
    generate_sources()