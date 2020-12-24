# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Modelo.py
# Compiled at: 2018-01-27 08:41:24
# Size of source mod 2**32: 20192 bytes
"""
Autor                   :       Marcos Felipe da Silva Jardim
Versão atual    :       1.0
Data da versão atual    :       17-02-2017

Resumo                  : Reúne classes responsáveis pela geração de dados para um projeto. Realiza conexão
                        a bancos de dados, gera cookies, destrói cookies, etc...
------------------------------------------------------------------------------------------------------------------------------
Notas de versão:

versão 1.0  :   17-02-2017 Inclusão da classe Consulta que trabalha sobre dados retornados de uma consulta

------------------------------------------------------------------------------------------------------------------------------  

"""
import pymysql, pymssql, os, sys, re, time
from datetime import datetime
from http import cookies

def executarConsulta(consulta, usuario, senha, banco, servidor, tipo_sgbd='mysql', porta=1433):
    """ Realiza de fato a conexão, usando os parametros passados para a conexão """
    if tipo_sgbd == 'mysql':
        con = pymysql.connect(user=usuario, password=senha, database=banco, host=servidor)
    else:
        if tipo_sgbd == 'mssql':
            con = pymssql.connect(user=usuario, password=senha, database=banco, host=servidor, port=porta)
        else:
            return 'Erro, tipo de SGBD não reconhecido'
    cur = con.cursor()
    cur.execute(consulta)
    con.commit()
    cur.close()
    con.close()


try:
    praca = os.path.dirname(os.environ['REQUEST_URI']).replace('/', '')
except KeyError:
    praca = 'NADA'
    print('ERRO AO ACESSAR A BASE DE DADOS, ' + praca, file=sys.stderr)

my_usuario = 'root'
my_senha = 'marcos'
my_banco = praca
my_servidor = '172.17.0.1'
SQL = "SELECT usuario, senha, banco, servidor, porta FROM adm_mssql where praca = '%s' LIMIT 1" % praca
con = pymysql.connect(user=my_usuario, password=my_senha, database='administrador', host=my_servidor)
cur = con.cursor()
cur.execute(SQL)
ms_usuario = ''
ms_senha = ''
ms_banco = ''
ms_servidor = ''
ms_porta = ''
for reg in cur.fetchall():
    ms_usuario = reg[0]
    ms_senha = reg[1]
    ms_banco = reg[2]
    ms_servidor = reg[3]
    ms_porta = reg[4]

class Consulta:
    _Consulta__campos = ''
    _Consulta__registros = ''

    def __init__(self, consulta, usuario, senha, banco, servidor, tipo_sgbd='mysql', porta=1433):
        """Retorna um objeto consulta sendo os parametros consulta, usuario , senha, banco, servidor devem ser repassados no momento de criação do objeto. O único parâmetro opcional é  o tipo de sgbd que vem como padrão mysql
    EX: obj = Consulta('select * from teste', 'root', 'marcos', 'banco_teste', 'localhost', 'mysql')
        """
        self._Consulta__consulta = consulta
        self._Consulta__usuario = usuario
        self._Consulta__senha = senha
        self._Consulta__banco = banco
        self._Consulta__servidor = servidor
        self._Consulta__tipo_sgbd = tipo_sgbd
        self._Consulta__porta = porta
        self._Consulta__conexao()

    def __str__(self):
        return 'Consulta("%s", "%s", "%s", "%s", "%s", "%s")' % (
         self._Consulta__consulta, self._Consulta__usuario, self._Consulta__senha, self._Consulta__banco, self._Consulta__servidor, self._Consulta__tipo_sgbd)

    def __repr__(self):
        return eval('Consulta("%s", "%s", "%s", "%s", "%s", "%s")' % (
         self._Consulta__consulta, self._Consulta__usuario, self._Consulta__senha, self._Consulta__banco, self._Consulta__servidor, self._Consulta__tipo_sgbd))

    def __len__(self):
        return len(self._Consulta__campos)

    def getCampos(self):
        """ Retorna todos os campos da tabela """
        return self._Consulta__campos

    def getRegistros(self):
        """ Retorna todos os registros da consulta """
        return self._Consulta__registros

    def setConsulta(self, consulta):
        """
        self.setConsulta('select * from adm_menu')
        
        Executa uma nova consulta no banco e redefine as variaveis de instancia __registros e __campos.        Este metodo foi criado com o intuito de permitir a mudança de dados sem de fato ter de criar outro
        objeto consulta.
        OBS: Somente aceita querys de selecao (select)
        """
        self._Consulta__consulta = consulta
        self._Consulta__conexao()

    def __conexao(self):
        """ Realiza de fato a conexão, usando os parametros passados para a conexão """
        if self._Consulta__tipo_sgbd == 'mysql':
            con = pymysql.connect(user=self._Consulta__usuario, password=self._Consulta__senha, database=self._Consulta__banco, host=self._Consulta__servidor)
        else:
            if self._Consulta__tipo_sgbd == 'mssql':
                con = pymssql.connect(user=self._Consulta__usuario, password=self._Consulta__senha, database=self._Consulta__banco, host=self._Consulta__servidor, port=self._Consulta__porta)
            else:
                return 'Erro, tipo de SGBD não reconhecido'
        cur = con.cursor()
        cur.execute(self._Consulta__consulta)
        try:
            self._Consulta__campos = [str(campo) for campo, *_ in cur.description]
        except TypeError:
            self._Consulta__campos = []

        self._Consulta__registros = [reg for reg in cur.fetchall()]
        con.commit()
        cur.close()

    def selecionaCampo(self, nome):
        """
        self.selecionaCampo('nome') ou self.selecionaCampo(0) => list()
        
        Seleciona um campo baseado no nome que é informado ou no seu numero de coluna.         O nome de fato deve ser real ao nome do campo informado pelo retornno de self.getCampos() """
        if nome in self._Consulta__campos:
            index = self._Consulta__campos.index(nome)
            return [str(item[index]) for item in self._Consulta__registros]
        if isinstance(nome, int):
            if nome <= len(self._Consulta__campos) - 1:
                index = nome
                return [str(item[index]) for item in self._Consulta__registros]
            else:
                return 'O indice de coluna informado não é acessivel na consulta, verifique os campos no atributo _campos ou use um nome de coluna'
        else:
            return 'A coluna informada não foi encontrada, favor verificar o atributo _campos'

    def selecionaCampos(self, lista):
        """self.selecionaCampos(['nome','senha']) => list()
        Seleciona um ou mais campos informados pelo seu nome. Os nomes devem ser enviados         dentro de uma lista. Se não sabe quais colunas deseja capturar verifique o metodo getCampos().
        Os campos são retornados como uma tupla aninhada dentro de uma lista externa. """
        if isinstance(lista, list):
            conjunto = list()
            for item in lista:
                if isinstance(item, str) and item in self._Consulta__campos:
                    conjunto.append(self._Consulta__campos.index(item))
                else:
                    return 'Favor enviar somente nomes de colunas que existam em self.__campos'
                reg = []
                for item in self._Consulta__registros:
                    listas = []
                    for campo in conjunto:
                        listas.append(item[campo])

                    reg.append(tuple(listas))

            return reg
        else:
            return 'Por favor informe uma lista para os campos que se deseja retornar'

    def ordenaColuna(self, coluna, decrescente=True):
        """Ordena a coluna informada na ordem desejada(ordena os registros) e devolve uma copia para o
        usuario. A coluna deve existir em __campos (verificar com o metodo getCampos()).
        self.ordenaColuna('id_usuarios', False)
        """
        if coluna not in self._Consulta__campos:
            return 'Campo nao existe'
        campo_original = self._Consulta__campos[:]
        registro_original = self._Consulta__registros[:]
        campo_alterado = self._Consulta__campos[:]
        campos_ordenados = [
         campo_alterado.pop(self._Consulta__campos.index(coluna))]
        desc = [campos_ordenados.append(item) for item in campo_alterado]
        del desc
        del campo_alterado
        registros_ordenados = self.selecionaCampos(campos_ordenados)
        registros_ordenados = sorted(registros_ordenados, reverse=decrescente)
        self._Consulta__registros = registros_ordenados
        self._Consulta__campos = campos_ordenados
        registros_ordenados = self.selecionaCampos(campo_original)
        self._Consulta__campos = campo_original
        self._Consulta__registros = registro_original
        return registros_ordenados

    def procuraDados(self, dado):
        """ Retorna True se o dado a ser procurado existe em self.getRegistros(), caso contrario retorna False"""
        for reg in self.getRegistros():
            for item in reg:
                if dado == item:
                    return True

        return False


def obterCookie(nome):
    """Retorna o valor do cookie pelo nome que foi informado """
    if 'HTTP_COOKIE' in os.environ:
        cookie = os.environ['HTTP_COOKIE']
        cookies = cookie.split('; ')
        for cookie in cookies:
            cookie = cookie.split('=')
            if cookie[0] == nome:
                return cookie[1]

        return


def salvarCookie(dicio):
    """Recebe uma quantidade de cookies e salva eles desenhando no cabecalho da requisicao os mesmos"""
    c = cookies.SimpleCookie()
    for dado in dicio.keys():
        c[dado] = dicio[dado]

    return str(c.output())


class Data:
    _Data__de = ''
    _Data__ate = ''

    def __init__(self):
        self._Data__obterData()

    def __obterData(self):
        self._Data__de = obterCookie('de')
        self._Data__ate = obterCookie('ate')
        if self._Data__de == '' or self._Data__ate == '' or self._Data__de is None or self._Data__ate is None:
            dataAtual = datetime.now()
            self._Data__de = '%04d-%02d-%02d' % (dataAtual.year, dataAtual.month, dataAtual.day)
            self._Data__ate = '%04d-%02d-%02d' % (dataAtual.year, dataAtual.month, dataAtual.day)

    def getDataForm(self):
        """Obtem a data no formato tradicional"""
        return [
         self._Data__de, self._Data__ate]

    def getData(self):
        """Obtem a data no formato de acesso ao banco de dados """
        de = self._Data__de.replace('-', '')
        ate = self._Data__ate.replace('-', '')
        return [de, ate]

    def gravaData(self):
        """ Grava a data atual em um cookie no formato das datas de formulario """
        response.set_cookie('de', self._Data__de, expires=time.time() + 259200, path='/')
        response.set_cookie('ate', self._Data__ate, expires=time.time() + 259200, path='/')

    def setData(self, de, ate):
        """ Grava as variaveis de data."""
        padrao = re.compile('^[2][0][1-9][0-9]-([0][1-9]|[1][0-2])-([3][0-1]|[0][1-9]|[1-2][0-9])$')
        if padrao.match(de) and padrao.match(ate):
            self._Data__de = de
            self._Data__ate = ate
        else:
            return 'Data informada de forma incorreta'


class Usuario(Consulta, Data):
    _Usuario__id = 0
    _Usuario__nome = ''
    _Usuario__menus = list()

    def __init__(self, usuario='', senha=''):
        """ Retorna um objeto usuario recebendo como parametro inicial o ID do usuario """
        self._Usuario__dadosUsuario(usuario, senha)
        Data.__init__(self)

    def getLojas(self, com_id=False):
        """ Retorna todas as lojas que o usuario tem acesso. """
        if com_id:
            sql = 'select af.id_filial, af.filial from adm_filial af INNER JOIN adm_usuario_filial auf             ON af.id_filial = auf.id_filial INNER JOIN adm_usuario au ON au.id_usuario = auf.id_usuario             WHERE auf.id_usuario = %d ORDER BY af.id_filial' % self.getID()
        else:
            sql = 'select af.filial from adm_filial af INNER JOIN adm_usuario_filial auf             ON af.id_filial = auf.id_filial INNER JOIN adm_usuario au ON au.id_usuario = auf.id_usuario             WHERE auf.id_usuario = %d ORDER BY af.id_filial' % self.getID()
        con = pymysql.connect(user=my_usuario, password=my_senha, database=my_banco, host=my_servidor)
        cur = con.cursor()
        cur.execute(sql)
        if com_id:
            lojas = [(loja[0], loja[1]) for loja in cur.fetchall()]
        else:
            lojas = ['%s' % loja for loja in cur.fetchall()]
        cur.close()
        con.close()
        return lojas

    def getGrupos(self):
        """Retorna todos os grupos que o usuario tem acesso. Os grupos são retornados em uma matriz """
        sql = 'select ag.grupo from adm_grupo  ag INNER JOIN adm_usuario_grupo aug ON ag.id_grupo = aug.id_grupo         INNER JOIN adm_usuario au ON au.id_usuario = aug.id_usuario WHERE aug.id_usuario = %d ' % self.getID()
        con = pymysql.connect(user=my_usuario, password=my_senha, database=my_banco, host=my_servidor)
        cur = con.cursor()
        cur.execute(sql)
        grupos = ['%s' % grupo for grupo in cur.fetchall()]
        cur.close()
        con.close()
        return grupos

    def getID(self):
        """ Retorna o ID do usuario."""
        return self._Usuario__id

    def getNome(self):
        """ Retorna o nome do usuario."""
        return self._Usuario__nome

    def getMenu(self):
        """ Retorna todos os menus do usuario em forma de lista com lista aninhada. """
        return self._Usuario__menus

    def getMenuAdm(self):
        """ Retorna um dicionario com os menus já agrupados da forma que o metodo getMenuAdm da classe Pagina vai entender o fluxo de dados"""
        dados = {}
        for reg in self.getMenu():
            chave, valor = reg
            if chave in dados.keys():
                dados[chave].append(valor)
            else:
                dados[chave] = [
                 valor]

        return dados

    def __dadosUsuario(self, usuario, senha):
        """ Verifica se usuario e senha estao em branco, então ver se tem cookies. Se tiver preencher variaveis. """
        sqlMenu = 'SELECT am.familia, am.link FROM adm_usuario au INNER JOIN adm_usuario_menu aum         ON au.id_usuario = aum.id_usuario INNER JOIN adm_menu am ON aum.id_menu = am.id_menu WHERE aum.id_usuario = %d'
        if usuario == '' and senha == '':
            if obterCookie('id') is None:
                self._Usuario__id = 0
            else:
                self._Usuario__id = int(obterCookie('id'))
                self._Usuario__nome = obterCookie('nome')
            sql = 'select * from adm_usuario where id_usuario = %d' % self._Usuario__id
            Consulta.__init__(self, sql, my_usuario, my_senha, my_banco, my_servidor, 'mysql')
        else:
            sql = "SELECT id_usuario, nome FROM adm_usuario WHERE nome = '%s' AND senha = SHA('%s')" % (usuario, senha)
            Consulta.__init__(self, sql, my_usuario, my_senha, my_banco, my_servidor, 'mysql')
            dados = self.getRegistros()
            for reg in dados:
                self._Usuario__id, self._Usuario__nome = reg

        self.setConsulta(sqlMenu % self._Usuario__id)
        self._Usuario__menus = self.getRegistros()

    def atualizaSenha(self, senhaAntiga, novaSenha):
        """ Recebe a senha antiga e a senha nova do usuario, baseado nisto tenta alterar a senha conectando com e atualizando a nova."""
        sqlSenha = "SELECT senha FROM adm_usuario WHERE id_usuario = %d AND senha = SHA('%s') " % (self._Usuario__id, senhaAntiga)
        self.setConsulta(sqlSenha)
        dados = self.getRegistros()
        if len(dados) == 1:
            sqlAtualizaSenha = "UPDATE adm_usuario SET senha = SHA('%s') WHERE id_usuario = %d" % (novaSenha, self._Usuario__id)
            executarConsulta(sqlAtualizaSenha, my_usuario, my_senha, my_banco, my_servidor)
            return 'Senha Atualizada'
        else:
            return 'Erro com a senha enviada. Senha incorreta'

    def getDivulgador(self):
        """Retorna todos os divulgadores cadastrados no sistema até o momento """
        SQL = 'SELECT id_divulgador, nome FROM divulgador WHERE D_E_L_E_T_ IS NULL '
        c = Consulta(SQL, my_usuario, my_senha, my_banco, my_servidor, 'mysql')
        return c.getRegistros()

    def getDivulgadorFilial(self, id_filial):
        """ Retorna o ID e nome do divulgador recebendo o id_filial repassado """
        SQL = 'SELECT d.id_divulgador, d.nome FROM divulgador d INNER JOIN adm_filial_divulgador afd ON afd.id_divulgador = d.id_divulgador         WHERE afd.id_filial = %d AND d.D_E_L_E_T_ IS NULL' % int(id_filial)
        c = Consulta(SQL, my_usuario, my_senha, my_banco, my_servidor, 'mysql')
        return c.getRegistros()

    def verificaMenu(self, menu):
        """ Verifica o menu do usuario se o mesmo tiver este menu retorna True senao retorna False"""
        for _, m in self.getMenu():
            if m.find(menu) != -1:
                return True
                continue

        return False


def converter(valor):
    valor = str(valor)
    verificar = len(valor[valor.find('.') + 1:])
    if verificar == 2:
        pass
    else:
        valor = valor + '0'
    valor = valor.replace('.', ',')
    x = 0
    d = ''
    rever = valor[::-1]
    for i in rever:
        if x < 4:
            x += 1
            d += i
        elif x % 3 == 0:
            d += '.' + i
            x += 1
        else:
            d += i
            x += 1

    d = 'R$ ' + d[::-1]
    return d