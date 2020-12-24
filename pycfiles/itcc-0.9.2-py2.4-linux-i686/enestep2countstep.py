# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/enestep2countstep.py
# Compiled at: 2008-04-20 13:19:45


def enestep2countstep(ifile, enes, ofile, gm=None):
    data = []
    for line in ifile:
        words = line.split()
        assert len(words) == 2
        data.append((float(words[0]), int(words[1])))

    data.sort(cmp=lambda x, y: cmp(x[1], y[1]))
    ofile.write('#')
    for ene in enes:
        ofile.write(' %s' % ene)

    ofile.write('\n')
    count = [
     0] * len(enes)
    if gm is None:
        gm = min([ x[0] for x in data ])
    for (ene, step) in data:
        for (idx, ene_ref) in enumerate(enes):
            if 0 <= ene - gm <= ene_ref:
                count[idx] += 1

        ofile.write('%s %s\n' % (step, (' ').join([ str(x) for x in count ])))

    return


def main():
    import sys, getopt
    (opts, args) = getopt.getopt(sys.argv[1:], 'b:', ['base='])
    base = None
    for (o, a) in opts:
        if o in ('-b', '--base'):
            base = float(a)

    if len(args) < 2:
        import os.path
        sys.stderr.write('usage: %s [-b BASE] <ifname|-> ene...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
    enes = [ float(x) for x in args[1:] ]
    enestep2countstep(ifile, enes, sys.stdout, base)
    return


if __name__ == '__main__':
    main()