# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scythe/convert/scythe_ensembl2grp.py
# Compiled at: 2014-06-13 06:15:07
import sys, getopt

def usage():
    print('\n    usage: scythe_ensembl2grp.py -f FILE1,FILE2 -o OUT.grp\n\n    -f, --files=STR     list of ensembl tsv files (eg sA.tsv,sB.tsv,sC.tsv)\n    -o, --output=FILE   output file\n    -h, --help          prints this\n\n    ')
    sys.exit(2)


def main():
    outfile = None
    infiles = None
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:ho:l:', ['files=', 'help', 'output='])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-f', '--files'):
            infiles = a
        elif o in ('-h', '--help'):
            usage()
        elif o in ('-o', '--output'):
            outfile = a
        elif not False:
            raise AssertionError('unhandled option')

    if not infiles:
        usage()
    if not outfile:
        outfile = 'out.grp'
    infiles = infiles.split(',')
    readTsvFiles(infiles, outfile)
    return


def readTsvFiles(listoftsv, outfile):
    print(outfile)
    if listoftsv is None:
        return -1
    else:
        ortho = dict()
        seen = set()
        done = set()
        res = ''
        for t in listoftsv:
            infile = open(t, 'r')
            for l in infile:
                l = l.strip()
                l = l.split('\t')
                seen.add(l[0])
                seen.add(l[1])
                if l[0] not in ortho:
                    ortho[l[0]] = [
                     l[1]]
                else:
                    ortho[l[0]].append(l[1])
                if l[1] not in ortho:
                    ortho[l[1]] = [
                     l[0]]
                else:
                    ortho[l[1]].append(l[0])

        cntr = 0
        for s in seen:
            notyetdone = [o for o in ortho[s] if o not in done]
            if s not in done and notyetdone:
                res += str(cntr) + '\t' + s + '\t' + '\t'.join(notyetdone)
                res += '\n'
                cntr += 1
                done.add(s)
                for d in ortho[s]:
                    done.add(s)

                continue

        out = open(outfile, 'w')
        out.write(res)
        return


if __name__ == '__main__':
    main()