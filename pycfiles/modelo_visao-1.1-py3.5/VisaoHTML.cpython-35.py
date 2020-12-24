# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/VisaoHTML.py
# Compiled at: 2018-01-08 08:24:11
# Size of source mod 2**32: 16194 bytes
"""
autor                   :   Marcos Felipe da Silva
versão atual            :   1.0
data da versão atual    :   20-02-2017
-----------------------------------------------------------------------
Notas de versão:

versão 1.0  :   20-02-2017 Classe pagina para retornar uma pagina html

------------------------------------------------------------------------

"""

class Pagina:
    _Pagina__cabecalho = ''
    _Pagina__rodape = ''
    _Pagina__corpo = ''
    _Pagina__pagina = 'Content-type: text/html;charset=utf-8;\n\n'
    _Pagina__menu = ''

    def __init__(self, cabecalho, rodape, corpo=''):
        self._Pagina__cabecalho += cabecalho
        self._Pagina__rodape = rodape
        self._Pagina__corpo = corpo

    def setMenuAdm(self, dicionario, usuario=''):
        """ Recebe um dicionario e itera sobre as chaves para realizar a criação do menu dinâmico. O segundo parametro define o nome do usuario. """
        if not isinstance(dicionario, dict):
            return 'Erro, não é um dicionario'
        menu = "<nav class='navbar navbar-inverse'>         <div class='container-fluid'><div class='navbar-header'>         <button type='button' class='navbar-toggle' data-toggle='collapse' data-target='#myNavbar'>         <span class='icon-bar'></span><span class='icon-bar'></span><span class='icon-bar'></span>         </button></div><div  class='collapse navbar-collapse' id='myNavbar'><ul class='nav navbar-nav'> "
        for chave in sorted(dicionario.keys()):
            if len(dicionario[chave]) >= 2:
                menu += "<li class='dropdown'><a class='dropdown-toggle' data-toggle='dropdown' href='#'>%s<span class='caret'></span>                 </a><ul class='dropdown-menu'>" % chave
            else:
                menu += dicionario[chave].pop()
                continue
            for link in dicionario[chave]:
                menu += str(link)

            menu += '</ul></li>'

        menu += "</ul><ul class='nav navbar-nav navbar-right'><li style='display: none'class='%s' id='baixar'><a href='#'><span class='text-danger glyphicon glyphicon-download-alt'></span> </a></li><li><a href='#'><span class='text-danger glyphicon glyphicon-user'>         </span> Olá %s </a></li><li><a href='altera_senha.html'> Alterar senha</a></li><li class='text-success'><a href='index.html' onclick='obterCookies();'>         <span class='text-danger glyphicon glyphicon-log-out'></span> Logout</a></li></ul></div></div></nav></div>" % (usuario, usuario)
        self._Pagina__menu = menu

    def setCorpo(self, corpo):
        self._Pagina__corpo = corpo

    def getPagina(self):
        """Retorna a pagina do objeto Pagina. Com cabecalho, rodape e corpo """
        if self._Pagina__cabecalho != '' and self._Pagina__rodape != '':
            try:
                cabe = open(self._Pagina__cabecalho, 'r', encoding='utf-8')
                for linha in cabe.readlines():
                    self._Pagina__pagina += linha

                cabe.close()
                self._Pagina__pagina = self._Pagina__pagina.replace('menu_lateral_13', self._Pagina__menu)
                self._Pagina__pagina += self._Pagina__corpo
                roda = open(self._Pagina__rodape, encoding='utf-8')
                for linha in roda.readlines():
                    self._Pagina__pagina += linha

                roda.close()
            except IOError as err:
                print('Erro de arquivo: %s' % str(err))

            return self._Pagina__pagina
        else:
            return


class DivRow:
    _DivRow__conteudo = ''
    _DivRow__livre = 0

    def __init__(self, livre=12):
        """Inicia um objeto div """
        self._DivRow__livre = livre

    def addDiv(self, conteudo, tamanho, classe='', Identificador=''):
        """ Adiciona no container row outra div de tamanho informado. Tamanho nao pode ultrapassar o tamanho maximo"""
        if self._DivRow__livre >= tamanho:
            self._DivRow__conteudo += "<div class='col-sm-%d %s' id='%s'>%s</div>" % (int(tamanho), str(classe), str(Identificador), str(conteudo))
            self._DivRow__livre -= tamanho
        else:
            print('A div não pode ser inserida, seu tamanho excede os limites disponiveis')

    def getDivRow(self):
        """Retorna a div formatada e completa"""
        compo = "<div class='row'>" + self._DivRow__conteudo + '</div>'
        return compo


def para(conteudo='', classe='', Identificador=''):
    """Retorna um paragrafo para o codigo que o chamou"""
    return "<p class='%s' id='%s'>%s</p>" % (str(classe),
     str(Identificador), str(conteudo))


def titulo(conteudo='', tam=1, classe='', iDentificador=''):
    """Retorna um titulo para o codigo que o chamou"""
    return "<h%d class='%s' id='%s'>%s</h%d>" % (tam, str(classe),
     str(iDentificador), str(conteudo), tam)


def div(conteudo='', classe='', Identificador=''):
    """Retorna uma div utilizando as classes e ids informados pelo usuario """
    return "<div class='%s' id='%s'>%s</div>" % (str(classe),
     str(Identificador), str(conteudo))


def img(local, alt='', classe='', Identificador=''):
    """ Retorna uma tag img. Obrigatorio enviar o caminho da imagem"""
    return "<img src='%s' alt='%s' class='%s' id='%s' />" % (str(local),
     str(alt), str(classe), str(Identificador))


def button(conteudo, classe='', Identificador='', atrPersonalizado=''):
    """Retorna uma tag button o ultimo parametro disponibiliza a possibilidade de criar atributos personalizados"""
    return "<button class='btn %s' id='%s' %s >%s</button>" % (str(classe),
     str(Identificador), str(atrPersonalizado), str(conteudo))


def link(link, nome, classe='', Identificador='', atrPersonalizado=''):
    """Retorna uma tag link (tag a) para o sistema """
    return "<a href='%s' class='%s' id='%s' %s>%s</a>" % (str(link), str(classe),
     str(Identificador), str(atrPersonalizado), str(nome))


def script(link):
    """Retorna uma tag script com o caminho de um arquivo js externo"""
    return "<script type=text/javascript src='%s'></script>" % link


def entrada(tipo, variavel, valor='', classe='', Identificador='', nome='', atrPersonalizado=''):
    """ Cria um campo de entrada personalizado para ser usado nos formularios """
    return "<div class='form-group'>%s<input type='%s' name='%s' value='%s' class='form-control %s' id='%s' %s /></div>" % (str(nome), str(tipo), str(variavel), str(valor), str(classe),
     str(Identificador), str(atrPersonalizado))


def checkBox(nome, variavel, valor='', classe='', Identificador=''):
    """Retorna um checkbox """
    return "%s <input type='checkbox' name='%s' value='%s' class='%s', id='%s' /><br/>" % (str(nome), str(variavel), str(valor), str(classe),
     str(Identificador))


def selecao(nome, variavel, dicionario, classe='', Identificador=''):
    """ Retorna um select usando o dicionario. O campo value é preenchido com o valor e prefixado pela chave"""
    sele = "<div>%s<select name='%s' class='form-control %s' id='%s'>" % (nome, variavel, classe, Identificador)
    opt = "<option value='%s'>%s</option>"
    for key in sorted(dicionario.keys()):
        sele += opt % (str(dicionario[key]), str(key))

    sele += '</select></div>'
    return sele


def selecaoPer(nome, variavel, lista, listaSelecionados=[], classe='', Identificador='lojas', uni=False):
    """
    Recebe Um nome Para o campo, o nome da variavel e uma lista com numeros das filiais. Esta lista é selecionavel
    e as filiais selecionadas no formulario antigo são marcadas de uma vez neste.
    
    Retorna um campo de seleção com os selecionaveis disponiveis todas as vezes que o selecionador for escolhido
    """
    sele = "%s<select name='grupos' multiple class='form-control %s' id='%s'>" % (str(nome), str(classe), str(Identificador))
    filiais = ''
    selecionados = 'selected'
    if not isinstance(lista, list):
        return 'Não é uma lista'
    opt = "<option %s value='%s'>%s</option>"
    for item in lista:
        if item in listaSelecionados:
            sele += opt % (selecionados, str(item), str(item[0:17]))
        else:
            sele += opt % ('', str(item), str(item[0:17]))
        filiais += str(item) + ','

    if not uni:
        optTodas = '<option %s value="%s">%s</option>'
        if 'Todas' in listaSelecionados:
            sele += optTodas % (selecionados, filiais[:-1], 'Todas')
        else:
            sele += optTodas % ('', filiais[:-1], 'Todas')
    else:
        sele = sele.replace('multiple', '')
    sele += '</select>'
    return sele


class Tabela:
    _Tabela__cabecalho = ''
    _Tabela__corpo = ''
    _Tabela__rodape = ''

    def __init__(self, cabecalho, corpo=[()], rodape=''):
        """Define uma classe que cria tabelas de dados. O unico parametro solicitado é o cabecalho que deve ser uma lista simples. """
        self.setCabecalho(cabecalho)
        self.setRodape(rodape)
        self.setCorpo(corpo)

    def getCabecalho(self):
        """Retorna os dados do cabecalho """
        return self._Tabela__cabecalho

    def getRodape(self):
        """Retorna todos os dados do rodape """
        return self._Tabela__rodape

    def getCorpo(self):
        """Retorna todos os dados do corpo """
        return self._Tabela__corpo

    def setCorpo(self, corpo):
        """Recebe uma lista com tuplas aninhadas para armazenar o corpo das tabelas
        Formato do que o corpo deve receber : [('item','item'),('item2','item2')]
        self.setCorpo([('item','item'),('item2','item2')])
        """
        if isinstance(corpo, list):
            for item in corpo:
                if isinstance(item, tuple):
                    if len(item) == len(self._Tabela__cabecalho):
                        continue
                    else:
                        return 'Existem mais itens por linha no corpo do que no cabecalho'
                else:
                    return 'Os dados nao estao dentro de uma tupla'

        else:
            return 'O que você quer definir como corpo nem mesmo é uma lista'
        self._Tabela__corpo = corpo

    def setCabecalho(self, cabecalho):
        """ Define um cabecalho para a tabela."""
        if isinstance(cabecalho, list):
            self._Tabela__cabecalho = cabecalho
        else:
            return 'O cabecalho da tabela nao e uma lista'

    def setRodape(self, rodape):
        """ Define um rodape para a tabela."""
        if isinstance(rodape, list):
            self._Tabela__rodape = rodape
        else:
            return 'O rodape nao foi enviado como uma lista'

    def getTabela(self):
        """Retorna uma tabela HTML se todos os dados estiverem nos conformes """
        if isinstance(self._Tabela__corpo, list) and isinstance(self._Tabela__cabecalho, list) and isinstance(self._Tabela__rodape, list):
            tab = "<div class='table table-responsive small'><table class='minhaTabela table text-center table-bordered table-responsive small' id='minhaTabela'><thead><tr class='info'>%s</tr></thead><tbody>%s</tbody><tfoot><tr class='info'>%s</tr></tfoot></table></div>"
            tcabe = '<th>%s</th>'
            cabe = ''
            for item in self.getCabecalho():
                cabe += tcabe % item

            tcorpo = '<td>%s</td>'
            corpo = ''
            for reg in self.getCorpo():
                corpo += '<tr>'
                for item in reg:
                    corpo += tcorpo % item

                corpo += '</tr>'

            trodape = '<td>%s</td>'
            roda = ''
            for item in self.getRodape():
                roda += trodape % item

            tab = tab % (cabe, corpo, roda)
            return tab
        else:
            return 'Um dos itens não esta em conformidade com itens das tabelas'


def tagScript(conteudo=''):
    """ Retorna uma tag script com o conteudo desejado dentro dela"""
    tag = '<script type=text/javascript>%s</script>' % conteudo
    return tag


class Grafico:
    _Grafico__opcoes = {}
    _Grafico__dados = []
    _Grafico__tipo = {'pizza': 'PieChart', 'barra': 'BarChart', 'coluna': 'ColumnChart', 'linha': 'LineChart'}

    def __init__(self, dados, opcoes={}):
        """Cria uma tag script para o grafico de pizza e retorna esta tag totalmente formatada para uso no javascript """
        self._Grafico__setDados(dados)
        self._Grafico__setOpcoes(opcoes)

    def __setDados(self, dados):
        """ Recebe os dados como uma lista bidimensional para criacao do grafico de pizza """
        if isinstance(dados, list):
            for item in dados:
                if isinstance(item, list) and len(item) >= 2:
                    continue
                else:
                    return 'Não é uma lista bidimensional ou a quantidade da lista interna não é igual maior á 2'

        else:
            return 'Isto não é nem mesmo uma lista'
        self._Grafico__dados = dados

    def __setOpcoes(self, opcoes):
        """ Verifica se os dados lancados sao como um dicionario e entao os atribui em opcoes"""
        if isinstance(opcoes, dict):
            self._Grafico__opcoes = opcoes
        else:
            return 'Os dados enviados nao sao um dicionario'

    def getGrafico(self, div, tipo='pizza', funcao='drawChart'):
        """ Retorna uma funcao para ser usada na geracao de graficos.
        O tipo do grafico deve ser enviado assim como o id da div e o nome da funcao que se deseja retornar.
        Tipos de dados conhecidos:
        pizza, barra. O padrao é enviar um grafico de pizza
        O id da div deve ser informado corretamente senão o grafico nao sera criado.
        O nome da funcao tambem deve ser passado, caso nenhum seja passado a funcao se chamara drawChart

        """
        dados = ' google.charts.setOnLoadCallback(%s);         function %s() { var data = new google.visualization.arrayToDataTable(' % (funcao, funcao)
        dados += str(self._Grafico__dados)
        dados += ');\n        // Set chart options\n        var options = '
        dados += str(self._Grafico__opcoes) + ';'
        dados += "\n        // Inicializando um objeto pizza na funcao. Funcao esta para ser usada na criacao do grafico em uma div pizza\n        var chart = new google.visualization.%s(document.getElementById('%s'));\n        chart.draw(data, options);\n        } " % (self._Grafico__tipo[tipo], div)
        return dados