# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/douglas/python_envs/makefile_maker/lib/python2.6/site-packages/makefile_maker/makefile_maker.py
# Compiled at: 2010-05-27 22:51:45
from sys import argv
from optparse import OptionParser

class MakefileMaker(object):

    def __init__(self, nome_do_arquivo):
        self.nome_do_arquivo = nome_do_arquivo
        self.destino = nome_do_arquivo[:-2]
        if not self._existe(nome_do_arquivo):
            open(nome_do_arquivo, 'wb').close()
        self._cria_makefile()

    def _existe(self, arquivo):
        try:
            f = open(arquivo)
        except:
            return False

        return True

    def _cria_makefile(self):
        conteudo = [
         'all: compila\r\n',
         'compila: %s' % self.nome_do_arquivo,
         '\tgcc %s -o %s\r\n' % (self.nome_do_arquivo, self.destino),
         'clean:',
         '\trm -rf %s\r\n' % self.destino]
        conteudo = ('\r\n').join(conteudo)
        makefile = open('Makefile', 'wb')
        makefile.write(conteudo)
        makefile.close()


if __name__ == '__main__':
    if argv[1] and '.c' in argv[1]:
        MakefileMaker(argv[1])
    else:
        print 'Nome do arquivo mal formado (faltando extensao c).'
        Exception('Faltando um argumento.')