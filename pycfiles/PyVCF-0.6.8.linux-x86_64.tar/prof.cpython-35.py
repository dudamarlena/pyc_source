# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/vcf/test/prof.py
# Compiled at: 2016-03-18 12:18:33
# Size of source mod 2**32: 712 bytes
import vcf, cProfile, timeit, pstats, sys

def parse_1kg():
    for line in vcf.Reader(filename='vcf/test/1kg.vcf.gz'):
        pass


if len(sys.argv) == 1:
    sys.argv.append(None)
if sys.argv[1] == 'profile':
    cProfile.run('parse_1kg()', '1kg.prof')
    p = pstats.Stats('1kg.prof')
    p.strip_dirs().sort_stats('time').print_stats()
else:
    if sys.argv[1] == 'time':
        n = 1
        t = timeit.timeit('parse_1kg()', 'from __main__ import parse_1kg', number=n)
        print(t / n)
    elif sys.argv[1] == 'stat':
        import statprof
        statprof.start()
        try:
            parse_1kg()
        finally:
            statprof.stop()
            statprof.display()

    else:
        print('prof.py profile/time')