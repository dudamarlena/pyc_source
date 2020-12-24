# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arpa2/quickder_tools/asn1literate.py
# Compiled at: 2020-03-04 06:22:47
# Size of source mod 2**32: 1699 bytes
import sys

def main():
    if len(sys.argv) not in (2, 3):
        sys.stderr.write('Usage: %s literalfile.asn [literalfile.md]\n' % sys.argv[0])
        sys.exit(1)
    else:
        infile = sys.argv[1]
        if len(sys.argv) > 2:
            otfile = sys.argv[2]
        else:
            if infile[-5:] == '.asn1':
                otfile = infile[:-5] + '.md'
            else:
                otfile = infile = '.md'
    inf = open(infile, 'r')
    otf = open(otfile, 'w')
    mode = 'md'
    for ln in inf.readlines():
        if ln == '\n' or ln == '--\n':
            otf.write('\n')
        elif ln[:3] == '-- ':
            if mode != 'md':
                mode = 'md'
                otf.write('\n')
            otf.write(ln[3:])
        else:
            if mode != 'asn1':
                mode = 'asn1'
                otf.write('\n')
            otf.write('    ' + ln)

    inf.close()


if __name__ == '__main__':
    main()