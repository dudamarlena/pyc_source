# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioUtil/readfq.py
# Compiled at: 2016-06-05 23:22:42
# Size of source mod 2**32: 1634 bytes


def readfq(fp):
    last = None
    while 1:
        if not last:
            for l in fp:
                if l[0] in '>@':
                    last = l[:-1]
                    break

        if not last:
            break
        name, seqs, last = last[1:].partition(' ')[0], [], None
        for l in fp:
            if l[0] in '@+>':
                last = l[:-1]
                break
            seqs.append(l[:-1])

        if not last or last[0] != '+':
            yield (
             name, ''.join(seqs), None)
            if not last:
                break
        else:
            seq, leng, seqs = ''.join(seqs), 0, []
            for l in fp:
                seqs.append(l[:-1])
                leng += len(l) - 1
                if leng >= len(seq):
                    last = None
                    yield (name, seq, ''.join(seqs))
                    break

            if last:
                yield (
                 name, seq, None)
                break


if __name__ == '__main__':
    import sys
    n, slen, qlen = (0, 0, 0)
    for name, seq, qual in readfq(sys.stdin):
        n += 1
        slen += len(seq)
        qlen += qual and len(qual) or 0

    print(n, '\t', slen, '\t', qlen)