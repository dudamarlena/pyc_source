# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lucas/Programmation/Python/AlwaysCorrectCorrectnessCompiler/accc/dnacompiler/dnacompiler.py
# Compiled at: 2015-03-06 11:02:13
# Size of source mod 2**32: 1811 bytes
from accc.compiler import Compiler

class DNACompiler(Compiler):
    """DNACompiler"""

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