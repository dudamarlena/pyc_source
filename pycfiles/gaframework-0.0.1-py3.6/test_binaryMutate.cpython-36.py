# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_binaryMutate.py
# Compiled at: 2019-06-14 12:47:17
# Size of source mod 2**32: 843 bytes
from unittest import TestCase
from GaPy.binary_mutate import *

class TestBinaryMutate(TestCase):

    def test__mutate_gene(self):
        mutate = BinaryMutate(1.0)
        self.assertEqual(1.0, mutate._p == 1.0)
        gene = True
        m_gene = mutate._mutate_gene(gene)
        self.assertFalse(m_gene)
        gene = False
        m_gene = mutate._mutate_gene(gene)
        self.assertTrue(m_gene)

    def test__mutate_chromosome(self):
        mutate = BinaryMutate(1.0)
        chromosome = Chromosome()
        mutate = BinaryMutate(1.0)
        for i in range(16):
            chromosome.genes.append(True)

        mutate._mutate_chromosome(chromosome)
        self.assertEqual('0000000000000000', str(chromosome))