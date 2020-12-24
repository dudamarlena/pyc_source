# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/pickle_converter/main.py
# Compiled at: 2013-02-21 05:29:50
import argparse, pickle, json, base64

def main():
    parser = argparse.ArgumentParser(description='Pickle - JSON converter')
    parser.add_argument('command', choices=['decode', 'encode'], help='what operation to perform (choices: %(choices)s)', metavar='command')
    parser.add_argument('-f', '--file', help='input/output pickle file depending on the command')
    parser.add_argument('-i', '--input', help='input base64 encoded JSON')
    args = parser.parse_args()
    if args.command == 'decode':
        working_file = open(args.file, 'r')
        data = pickle.load(working_file)
        working_file.close()
        print json.dumps(data, separators=(',', ':'))
    if args.command == 'encode':
        data = json.loads(base64.b64decode(args.input))
        working_file = open(args.file, 'w')
        pickle.dump(data, working_file, 1)
        working_file.close()


if __name__ == '__main__':
    main()