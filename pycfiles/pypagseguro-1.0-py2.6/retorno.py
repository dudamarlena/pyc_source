# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pypagseguro/retorno.py
# Compiled at: 2011-01-06 19:06:57
import urllib, time, re

def gravaLog(log, arquivo, mensagem):
    u"""
    Método auxiliar que grava as informações de log em um arquivo.
    
    Esse método é usado pelo método retorno

    Recebe os seguintes parâmetros:
    - log       True|False
    - arquivo   String
    - mensagem  String
  """
    if log:
        try:
            f = open(arquivo, 'a')
            f.write('%s - %s\n' % (time.ctime(), mensagem))
        except:
            print 'LOG FAIL'


def retorno(inputs, token, fn, log=True, logfile='/tmp/pagseguro.log'):
    u"""
    Método que faz a validação junto ao pagseguro para os posts recebidos
    Voce deve executá-lo, no método POST de sua aplicação passando os seguintes
    parâmetros:

    - inputs  - um dicionário com os posts recebidos
    - token   - seu token configurado no pagseguro
    - fn      - um método que será executádo caso a validação seja verdadeira
    - log     - (True|False) Define se você quer que o método grave um log com as transações
    - logfile - String('/tmp/pagseguro.log') Onde deverá gravar o log
  """
    data = {}
    for (name, value) in inputs.iteritems():
        data[name] = value

    data['Comando'] = 'validar'
    data['Token'] = token
    gravaLog(log, logfile, '---\nRecebendo o POST (verificar junto ao pagseguro): %s\n----' % data)
    params = urllib.urlencode(data)
    ret = urllib.urlopen('https://pagseguro.uol.com.br/Security/NPI/Default.aspx', params)
    ret = ret.read()
    produtos = {}
    s = re.compile('_\\d+$')
    for (k, v) in data.iteritems():
        if s.search(k):
            produtos[k] = v

    for (k, v) in produtos.iteritems():
        del data[k]

    prod = []
    i = 0
    while True:
        i += 1
        try:
            prod.append({'id': produtos[('ProdID_' + str(i))], 
               'valor': produtos[('ProdValor_' + str(i))], 
               'descricao': produtos[('ProdDescricao_' + str(i))], 
               'quantidade': produtos[('ProdQuantidade_' + str(i))], 
               'extras': produtos[('ProdExtras_' + str(i))], 
               'frete': produtos[('ProdFrete_' + str(i))]})
        except:
            break

    data['produtos'] = prod
    if ret == 'VERIFICADO':
        gravaLog(log, logfile, 'Dados verificados junto ao pagseguro com sussesso! Executando a funcao. %s' % data)
        fn(data)
    else:
        gravaLog(log, logfile, 'Dados inválidos: %s - Resposta %s' % (data, ret))