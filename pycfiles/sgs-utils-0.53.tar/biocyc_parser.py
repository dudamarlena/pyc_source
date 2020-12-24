# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/biocyc/biocyc_parser.py
# Compiled at: 2016-02-16 15:22:25
import sys, os, re
LINE_COMMENT = '#'
BLOCK_SEPARATOR = '\n//\n'
UNIQUE_ID = 'UNIQUE-ID'
FIELD_SEP = ' - '
LINE_BREAK = '/'
ADDITIONAL_INFO = '^'

def load_flat_file(flat_file, complementary_attributes=False):
    flat_map = {}
    with open(flat_file, 'r') as (reader):
        blocks = reader.read().replace('\r\n', '\n').split(BLOCK_SEPARATOR)
        for b in blocks:
            unique_id, attributes = parse_block(b, complementary_attributes)
            if unique_id:
                flat_map[unique_id] = attributes
            elif b != '':
                sys.stderr.write('Warning, bad structured block:\n%s\n' % b)

    return flat_map


def remove_additional_info(value_list):
    result = []
    for v in value_list:
        if isinstance(v, basestring):
            result.append(v)
        else:
            result.append(v[0])

    return result


def parse_block(block, complementary_attributes):
    attribute_map = {}
    unique_id = ''
    last_attribute = ''
    for l in block.splitlines():
        if l and not l.startswith(LINE_COMMENT):
            if l.startswith(LINE_BREAK):
                attribute = attribute_map[last_attribute]
                attribute[-1] = attribute[(-1)] + '\n' + l
            elif l.startswith(ADDITIONAL_INFO):
                if complementary_attributes:
                    attribute = attribute_map[last_attribute]
                    av = l.lstrip(ADDITIONAL_INFO).split(FIELD_SEP)
                    if isinstance(attribute[(-1)], basestring):
                        attribute[-1] = (
                         attribute[(-1)], {})
                    attribute[(-1)][1][av[0]] = av[1]
            else:
                av = l.split(FIELD_SEP)
                if av[0] == UNIQUE_ID:
                    unique_id = av[1]
                elif len(av) > 1:
                    last_attribute = av[0]
                    if last_attribute in attribute_map:
                        attribute_map[last_attribute].append(FIELD_SEP.join(av[1:]))
                    else:
                        attribute_map[last_attribute] = [
                         FIELD_SEP.join(av[1:])]
                else:
                    attribute = attribute_map[last_attribute]
                    sys.stderr.write('Warning: Malformed bloc %s for %s attribute: missing breakline\n' % (unique_id, last_attribute))
                    attribute[-1] = attribute[(-1)] + '\n' + l

    return (
     unique_id, attribute_map)


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument('flatfile', help='Biocyc .dat flatfile')
    args = parser.parse_args(argv)
    for k, v in load_flat_file(args.flatfile, True).iteritems():
        print k, v


if __name__ == '__main__':
    main(sys.argv[1:])