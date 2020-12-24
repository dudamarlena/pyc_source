# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/file_translate/translate.py
# Compiled at: 2016-02-04 11:11:18
import argparse, json, os, re

def convert(config_file, input_file, output_file):
    with open(config_file, 'r') as (content_file):
        config = json.load(content_file)
    with open(input_file, 'r') as (content_file):
        content = content_file.read()
    for translation in config['translations']:
        search = translation['search'].encode()
        replace = translation['replace'].encode()
        content = re.sub(search, replace, content)

    with open(output_file, 'w') as (content_file):
        content_file.write(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Configuration file', default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json'))
    parser.add_argument('-i', '--input', help='Input file', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)
    args = parser.parse_args()
    convert(args.config, args.input, args.output)


if __name__ == '__main__':
    main()