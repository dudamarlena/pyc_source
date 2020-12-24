# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/coco/coco.py
# Compiled at: 2016-08-16 08:07:02
# Size of source mod 2**32: 1852 bytes
import codecs, chardet, argparse
__author__ = 'buptmiao'

def getargs():
    parse = argparse.ArgumentParser(prog='CoCo')
    parse.add_argument('--version', '-v', action='version', version='%(prog)s 0.0.1')
    parse.add_argument('-i', nargs='+', help='print the encoding of the input files')
    parse.add_argument('-o', type=str, help='specify the encoding of output file, utf-8 by default')
    parse.add_argument('src', nargs='?', help='input file')
    parse.add_argument('dst', nargs='?', help='output file')
    args = parse.parse_args()
    return (
     parse, args)


def readfile(src, encoding):
    with codecs.open(src, 'r', encoding) as (f):
        return f.read()


def writefile(dst, u, encoding):
    with codecs.open(dst, 'w', encoding) as (f):
        f.write(u)


def detect(src):
    try:
        with open(src, 'rb') as (f):
            data = f.read(1024)
            return chardet.detect(data)['encoding']
    except Exception as e:
        print(e)
        raise e


def convert(src, dst, dstco):
    try:
        srcco = detect(src)
        if srcco == 'gb2312' or srcco == 'GB2312':
            srcco = 'gb18030'
        content = readfile(src, encoding=srcco)
        writefile(dst, content, encoding=dstco)
    except Exception as e:
        print(e)
        raise e


def start():
    parse, args = getargs()
    try:
        if args.i is not None:
            for file in args.i:
                print(file, detect(file))

            exit()
        src = args.src
        dst = args.dst
        if src is None or dst is None:
            parse.print_help()
            exit()
        encoding = args.o
        if encoding is None:
            encoding = 'utf-8'
        convert(src, dst, encoding)
    except Exception as e:
        parse.print_help()


if __name__ == '__main__':
    start()