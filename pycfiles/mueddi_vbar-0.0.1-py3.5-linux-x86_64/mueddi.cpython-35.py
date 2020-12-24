# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mueddit/mueddi.py
# Compiled at: 2019-04-19 02:32:55
# Size of source mod 2**32: 2564 bytes
"""MUlti-word EDit DIstance package interface.

Also contains main function for command-line use.
"""
from mueddit.dawg import make_dawg
from mueddit.leven import Facade
import argparse, logging

class Iterator:
    __doc__ = 'Standard iterator interface.\n\n    Initialized by the checked (possibly mis-spelled) word, the\n    maximum allowed number of edit operations and a finite automaton\n    constructed from a dictionary of correct words; instances of this\n    class produce a subset of the dictionary within the specified\n    distance from the checked word.\n    '
    log = logging.getLogger('mueddi')

    def __init__(self, seen, n, dawg):
        assert dawg
        self.dawg = dawg
        self.facade = Facade(seen, n)

    def __iter__(self):
        queue = [
         (
          '', self.dawg.root, self.facade.initial_state())]
        while len(queue):
            v, q, m = queue.pop(0)
            self.log.info('pop "%s",, %s' % (v, m))
            if q.final and self.facade.is_final(m):
                yield v
            for x in q.keys():
                mp = self.facade.delta(m, x)
                if mp:
                    v1 = v + x
                    q1 = q.get_child(x)
                    assert q1
                    self.log.info('push "%s",, %s' % (v1, mp))
                    queue.append((v1, q1, mp))


def main():
    parser = argparse.ArgumentParser(description='MUlti-word EDit DIstance')
    parser.add_argument('--log', '-l', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='logging level')
    parser.add_argument('--seen', '-s', required=True, help='seen word')
    parser.add_argument('--tolerance', '-t', required=True, type=int, help='max allowed number of edits')
    parser.add_argument('dict_word', nargs='+', help='dictionary words')
    args = parser.parse_args()
    log_level = args.log if args.log else 'WARNING'
    logging.basicConfig(format='%(name)s:%(message)s', level=getattr(logging, log_level))
    seen = args.seen
    if not seen:
        raise Exception('seen word must not be empty')
    n = args.tolerance
    if n <= 0:
        raise Exception('max allowed number of edits must be positive')
    words = set(args.dict_word)
    if len(words) != len(args.dict_word):
        raise Exception('duplicate dictionary words')
    dawg = make_dawg(words)
    it = Iterator(seen, n, dawg)
    for found in it:
        print(found)


if __name__ == '__main__':
    main()