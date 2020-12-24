# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lpabon/git/golang/porx/src/github.com/libopenstorage/openstorage-sdk-clients/sdk/python/build/lib/python3.6/site-packages/pycparser/ply/ygen.py
# Compiled at: 2017-02-02 23:11:34
# Size of source mod 2**32: 2251 bytes
import os.path, shutil

def get_source_range(lines, tag):
    srclines = enumerate(lines)
    start_tag = '#--! %s-start' % tag
    end_tag = '#--! %s-end' % tag
    for start_index, line in srclines:
        if line.strip().startswith(start_tag):
            break

    for end_index, line in srclines:
        if line.strip().endswith(end_tag):
            break

    return (
     start_index + 1, end_index)


def filter_section(lines, tag):
    filtered_lines = []
    include = True
    tag_text = '#--! %s' % tag
    for line in lines:
        if line.strip().startswith(tag_text):
            include = not include
        else:
            if include:
                filtered_lines.append(line)

    return filtered_lines


def main():
    dirname = os.path.dirname(__file__)
    shutil.copy2(os.path.join(dirname, 'yacc.py'), os.path.join(dirname, 'yacc.py.bak'))
    with open(os.path.join(dirname, 'yacc.py'), 'r') as (f):
        lines = f.readlines()
    parse_start, parse_end = get_source_range(lines, 'parsedebug')
    parseopt_start, parseopt_end = get_source_range(lines, 'parseopt')
    parseopt_notrack_start, parseopt_notrack_end = get_source_range(lines, 'parseopt-notrack')
    orig_lines = lines[parse_start:parse_end]
    parseopt_lines = filter_section(orig_lines, 'DEBUG')
    parseopt_notrack_lines = filter_section(parseopt_lines, 'TRACKING')
    lines[parseopt_notrack_start:parseopt_notrack_end] = parseopt_notrack_lines
    lines[parseopt_start:parseopt_end] = parseopt_lines
    lines = [line.rstrip() + '\n' for line in lines]
    with open(os.path.join(dirname, 'yacc.py'), 'w') as (f):
        f.writelines(lines)
    print('Updated yacc.py')


if __name__ == '__main__':
    main()