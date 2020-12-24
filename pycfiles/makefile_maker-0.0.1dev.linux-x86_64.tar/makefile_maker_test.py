# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/douglas/python_envs/makefile_maker/lib/python2.6/site-packages/makefile_maker/makefile_maker_test.py
# Compiled at: 2010-05-27 22:59:54
import unittest
from os import remove
from should_dsl import *
from makefile_maker import MakefileMaker

class MakefileMakerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_cria_arquivo_makefile_fonte_existente(self):
        open('foo.c', 'wb')
        maker = MakefileMaker('foo.c')
        arquivo = open('Makefile')
        arquivo | should_be.kind_of | file
        remove('foo.c')
        remove('Makefile')

    def test_cria_arquivo_makefile_fonte_inexistente(self):
        maker = MakefileMaker('naoexiste.c')
        open('Makefile') | should_be.kind_of | file
        open('naoexiste.c') | should_be.kind_of | file
        remove('naoexiste.c')
        remove('Makefile')

    def test_verifica_conteudo_makefile(self):
        maker = MakefileMaker('bar.c')
        conteudo = [
         'all: compila\r\n',
         '\r\n',
         'compila: bar.c\r\n',
         '\tgcc bar.c -o bar\r\n',
         '\r\n',
         'clean:\r\n',
         '\trm -rf bar\r\n']
        open('Makefile').readlines() | should_be.equal_to | conteudo
        remove('bar.c')
        remove('Makefile')