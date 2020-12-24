# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucas/Programmation/Python/AlwaysCorrectCorrectnessCompiler/accc/dnacompiler/dnacompiler.py
# Compiled at: 2015-03-06 11:02:13
# Size of source mod 2**32: 1811 bytes
from accc.compiler import Compiler

class DNACompiler(Compiler):
    __doc__ = "\n    Compiler specialized in DNA: vocabulary is 'ATGC'.\n    "

    def __init__(self, target_language_spec, comparables, predicats, actions, operators):
        """"""
        super().__init__('ATGC', target_language_spec, comparables, predicats, actions, operators)


if __name__ == '__main__':
    import random, time
    from accc.langspec import python as python_spec

    def mutated(dna, mutation_rate=0.1):
        new_dna = ''
        for nuc in dna:
            if random.random() < mutation_rate:
                new_dna += random.choice(dc.alphabet)
            else:
                new_dna += nuc

        return new_dna


    dc = DNACompiler(python_spec, ('temperature', ), ('haveNeighbors', ), ('die', 'duplicate'), ('>',
                                                                                                 '==',
                                                                                                 '<'))
    dna = ''.join(random.choice(dc.alphabet) for _ in range(40))
    while True:
        print(dna)
        mdna = mutated(dna)
        print(''.join([' ' if n == m else '!' for n, m in zip(dna, mdna)]))
        print(dc.compile(mdna))
        print(dc.header(dna), dc.structure(dna), dc.values(dna), sep='|', end='\n------------\n\n\n\n')
        time.sleep(0.4)