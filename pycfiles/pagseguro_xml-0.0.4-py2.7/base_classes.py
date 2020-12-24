# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\core\base_classes.py
# Compiled at: 2015-12-29 16:38:09
from __future__ import division, print_function, unicode_literals
import locale, re, pytz, lxml.etree as etree
from datetime import datetime, date
from decimal import Decimal
ABERTURA = b'<?xml version="1.0" encoding="utf-8"?>'
try:
    locale.setlocale(locale.LC_ALL, b'pt_BR.UTF-8')
    locale.setlocale(locale.LC_COLLATE, b'pt_BR.UTF-8')
except BaseException as e:
    locale.setlocale(locale.LC_ALL, b'')
    locale.setlocale(locale.LC_COLLATE, b'')

def tirar_acentos(texto):
    if not texto:
        return texto or b''
    texto = texto.replace(b'&', b'&amp;')
    texto = texto.replace(b'<', b'&lt;')
    texto = texto.replace(b'>', b'&gt;')
    texto = texto.replace(b'"', b'&quot;')
    texto = texto.replace(b"'", b'&apos;')
    texto = texto.replace(b'\t', b' ')
    while b'  ' in texto:
        texto = texto.replace(b'  ', b' ')

    return texto


def por_acentos(texto):
    if not texto:
        return texto
    texto = texto.replace(b'&#39;', b"'")
    texto = texto.replace(b'&apos;', b"'")
    texto = texto.replace(b'&quot;', b'"')
    texto = texto.replace(b'&gt;', b'>')
    texto = texto.replace(b'&lt;', b'<')
    texto = texto.replace(b'&amp;', b'&')
    texto = texto.replace(b'&APOS;', b"'")
    texto = texto.replace(b'&QUOT;', b'"')
    texto = texto.replace(b'&GT;', b'>')
    texto = texto.replace(b'&LT;', b'<')
    texto = texto.replace(b'&AMP;', b'&')
    return texto


def tira_abertura(texto):
    if b'?>' in texto:
        texto = texto.split(b'?>')[1:]
        texto = (b'').join(texto)
    return texto


class NohXML(object):

    def __init__(self, *args, **kwargs):
        self._xml = None
        return

    def _le_xml(self, arquivo):
        if arquivo is None:
            return False
        else:
            parser = etree.XMLParser(strip_cdata=False)
            if not isinstance(arquivo, basestring):
                arquivo = etree.tounicode(arquivo)
            if arquivo is not None:
                if isinstance(arquivo, basestring):
                    if isinstance(arquivo, str):
                        arquivo = unicode(arquivo.encode(b'utf-8'))
                    if b'<' in arquivo:
                        self._xml = etree.fromstring(tira_abertura(arquivo).encode(b'utf-8'), parser=parser)
                    else:
                        arq = open(arquivo)
                        txt = (b'').join(arq.readlines())
                        txt = unicode(txt.decode(b'utf-8'))
                        txt = tira_abertura(txt)
                        arq.close()
                        self._xml = etree.fromstring(txt, parser=parser)
                else:
                    self._xml = etree.parse(arquivo, parser=parser)
                return True
            return False

    def _preenche_namespace(self, tag, sigla_ns):
        if sigla_ns != b'':
            sigla_sig = sigla_ns + b':sig'
            sigla_ns = b'/' + sigla_ns + b':'
            tag = sigla_ns.join(tag.split(b'/')).replace(sigla_ns + sigla_ns, b'/' + sigla_ns).replace(sigla_sig, b'sig')
        return tag

    def _le_nohs(self, tag, ns=None, sigla_ns=b''):
        try:
            nohs = self._xml.xpath(tag)
            if len(nohs) >= 1:
                return nohs
        except:
            pass

        namespaces = {}
        if ns is not None:
            namespaces[b'res'] = ns
        if not tag.startswith(b'//*/res'):
            tag = self._preenche_namespace(tag, sigla_ns)
        nohs = self._xml.xpath(tag, namespaces=namespaces)
        if len(nohs) >= 1:
            return nohs
        else:
            return

    def _le_noh(self, tag, ns=None, ocorrencia=1):
        nohs = self._le_nohs(tag, ns)
        if nohs is not None and len(nohs) >= ocorrencia:
            return nohs[(ocorrencia - 1)]
        else:
            return
            return

    def _le_tag(self, tag, propriedade=None, ns=None, ocorrencia=1):
        noh = self._le_noh(tag, ns, ocorrencia)
        if noh is None:
            valor = b''
        elif propriedade is None:
            valor = noh.text
        elif noh.attrib is not None and len(noh.attrib) > 0:
            valor = noh.attrib.get(propriedade, b'')
        else:
            valor = b''
        return valor


class ErroObrigatorio(Exception):

    def __init__(self, raiz, nome, propriedade):
        if propriedade:
            self.value = b'%(raiz)s No campo "%(nome)s", a propriedade "%(propriedade)s" é de envio obrigatório, mas não foi preenchida.' % {b'nome': nome, 
               b'propriedade': propriedade, 
               b'raiz': raiz}
        else:
            self.value = b'%(raiz)s O campo "%(nome)s" é de envio obrigatório, mas não foi preenchido.' % {b'nome': nome, 
               b'raiz': raiz}

    def __str__(self):
        return repr(self.value)

    def __unicode__(self):
        return self.value


class TamanhoInvalido(Exception):

    def __init__(self, raiz, nome, valor, tam_min=None, tam_max=None, dec_min=None, dec_max=None):
        if tam_min:
            self.value = b'%(raiz)s O campo "%(nome)s", deve ter o tamanho mínimo de %(tam_min)s, mas o tamanho enviado foi %(tam_env)s: %(valor)s' % {b'nome': nome, 
               b'tam_min': unicode(tam_min), 
               b'tam_env': unicode(len(unicode(valor))), 
               b'valor': unicode(valor), 
               b'raiz': raiz}
        elif tam_max:
            self.value = b'%(raiz)s O campo "%(nome)s", deve ter o tamanho máximo de %(tam_max)s, mas o tamanho enviado foi %(tam_env)s: %(valor)s' % {b'nome': nome, 
               b'tam_max': unicode(tam_max), 
               b'tam_env': unicode(len(unicode(valor))), 
               b'valor': unicode(valor), 
               b'raiz': raiz}
        if dec_min:
            self.value = b'%(raiz)s O campo "%(nome)s", deve ter o tamanho mínimo de %(dec_min)s casa(s) decimal(is): %(valor)s' % {b'nome': nome, 
               b'dec_min': unicode(dec_min), 
               b'valor': unicode(valor), 
               b'raiz': raiz}
        elif dec_max:
            self.value = b'%(raiz)s O campo "%(nome)s", deve ter o tamanho máximo de %(dec_max)s casa(s) decimal(is): %(valor)s' % {b'nome': nome, 
               b'dec_max': unicode(dec_max), 
               b'valor': unicode(valor), 
               b'raiz': raiz}

    def __str__(self):
        return repr(self.value)

    def __unicode__(self):
        return self.value


class OpcaoInvalida(Exception):

    def __init__(self, raiz, nome, propriedade, opcoes, valor):
        opcoes = [ unicode(o) for o in opcoes ]
        opcoes = (b', ').join(opcoes)
        if propriedade:
            self.value = b'%(raiz)s No campo "%(nome)s", a propriedade "%(propriedade)s" possui valor inválido "%(valor)s", as opções sao: "%(opcoes)s".' % {b'nome': nome, 
               b'propriedade': propriedade, 
               b'raiz': raiz, 
               b'opcoes': opcoes, 
               b'valor': valor}
        else:
            self.value = b'%(raiz)s O campo "%(nome)s" possui valor inválido "%(valor)s", as opções sao: "%(opcoes)s".' % {b'nome': nome, 
               b'raiz': raiz, 
               b'opcoes': opcoes, 
               b'valor': valor}

    def __str__(self):
        return repr(self.value)

    def __unicode__(self):
        return self.value


class TagCaracter(NohXML):

    def __init__(self, nome=b'', valor=None, tamanho_min=None, tamanho_max=None, placehold=None, opcoes=None, propriedade=None, namespace=None, namespace_obrigatorio=True, alertas=[], raiz=None, obrigatorio=True, *args, **kwargs):
        super(TagCaracter, self).__init__(*args, **kwargs)
        self.nome = nome
        self._valor_string = b''
        self.obrigatorio = obrigatorio
        self.tamanho_min = tamanho_min
        self.tamanho_max = tamanho_max
        self.placehold = placehold
        self.opcoes = opcoes
        self.propriedade = propriedade
        self.namespace = namespace
        self.namespace_obrigatorio = namespace_obrigatorio
        self.alertas = alertas
        self.raiz = raiz
        self.valor = valor
        for k, v in kwargs.items():
            setattr(self, k, v)

        if kwargs.has_key(b'valor'):
            self.valor = kwargs[b'valor']

    def _testa_opcoes(self, valor):
        if (valor or self.obrigatorio) and self.opcoes and valor not in self.opcoes:
            return OpcaoInvalida(self.raiz, self.nome, self.propriedade, self.opcoes, valor)

    def _testa_obrigatorio(self, valor):
        if self.obrigatorio and not valor:
            return ErroObrigatorio(self.raiz, self.nome, self.propriedade)

    def _testa_tamanho_minimo(self, valor):
        if self.tamanho_min and len(unicode(valor)) < self.tamanho_min and self.obrigatorio:
            return TamanhoInvalido(self.raiz, self.nome, valor, tam_min=self.tamanho_min)

    def _testa_tamanho_maximo(self, valor):
        if self.tamanho_max and len(unicode(valor)) > self.tamanho_max:
            return TamanhoInvalido(self.raiz, self.nome, valor, tam_max=self.tamanho_max)

    def _valida(self, valor):
        self.alertas = []
        if self._testa_obrigatorio(valor):
            self.alertas.append(self._testa_obrigatorio(valor))
        if self._testa_tamanho_minimo(valor):
            self.alertas.append(self._testa_tamanho_minimo(valor))
        if self._testa_tamanho_maximo(valor):
            self.alertas.append(self._testa_tamanho_maximo(valor))
        if self._testa_opcoes(valor):
            self.alertas.append(self._testa_opcoes(valor))
        return self.alertas == []

    def set_valor(self, novo_valor):
        if novo_valor is not None:
            novo_valor = novo_valor.strip()
        if self._valida(novo_valor):
            self._valor_string = unicode(tirar_acentos(novo_valor))
        else:
            self._valor_string = b''
        return

    def get_valor(self):
        return unicode(por_acentos(self._valor_string))

    valor = property(get_valor, set_valor)

    def __unicode__(self):
        texto = b''
        if not self.obrigatorio and not self.valor:
            return texto
        if self.propriedade:
            return b' %s="%s"' % (self.propriedade, self._valor_string)
        texto = b'<%s' % self.nome
        if self.valor or self.placehold and self.tamanho_max:
            texto += b'>%s</%s>' % (self._valor_string, self.nome)
        else:
            texto += b' />'
        return texto

    def __repr__(self):
        return self.__unicode__()

    def get_xml(self):
        return self.__unicode__()

    def set_xml(self, arquivo, ocorrencia=1):
        if self._le_xml(arquivo):
            self._alertas = []
            self.valor = self._le_tag(self.raiz + b'/' + self.nome, propriedade=self.propriedade, ns=self.namespace, ocorrencia=ocorrencia)

    xml = property(get_xml, set_xml)

    def get_text(self):
        if self.propriedade:
            return b'%s_%s=%s' % (self.nome, self.propriedade, self._valor_string)
        else:
            return b'%s=%s' % (self.nome, self._valor_string)

    text = property(get_text)

    def get_txt(self):
        if self.obrigatorio:
            return self._valor_string
        if self.valor:
            return self._valor_string
        return b''

    txt = property(get_txt)


class TagBoolean(TagCaracter):

    def __init__(self, **kwargs):
        if not kwargs.has_key(b'opcoes'):
            kwargs[b'opcoes'] = (
             True, False)
        super(TagBoolean, self).__init__(**kwargs)
        self._valor_boolean = None
        for k, v in kwargs.items():
            setattr(self, k, v)

        if kwargs.has_key(b'valor'):
            self.valor = kwargs[b'valor']
        return

    def _testa_obrigatorio(self, valor):
        if self.obrigatorio and valor not in self.opcoes:
            return ErroObrigatorio(self.raiz, self.nome, self.propriedade)

    def _valida(self, valor):
        self.alertas = []
        if self._testa_obrigatorio(valor):
            self.alertas.append(self._testa_obrigatorio(valor))
        if self._testa_opcoes(valor):
            self.alertas.append(self._testa_opcoes(valor))
        return self.alertas == []

    def set_valor(self, novo_valor):
        if isinstance(novo_valor, basestring):
            if novo_valor.lower() == b'true':
                novo_valor = True
            elif novo_valor.lower() == b'false':
                novo_valor = False
        if self._valida(novo_valor) and isinstance(novo_valor, bool):
            self._valor_boolean = novo_valor
            if novo_valor == None:
                self._valor_string = b''
            elif novo_valor:
                self._valor_string = b'true'
            else:
                self._valor_string = b'false'
        else:
            self._valor_boolean = None
            self._valor_string = b''
        return

    def get_valor(self):
        return self._valor_boolean

    valor = property(get_valor, set_valor)

    def __unicode__(self):
        if not self.obrigatorio and self.valor == None:
            texto = b''
        else:
            if self.propriedade:
                return b' %s="%s"' % (self.propriedade, self._valor_string)
            texto = b'<%s' % self.nome
            if self.namespace:
                texto += b' xmlns="%s"' % self.namespace
            elif not self.valor == None:
                texto += b'>%s</%s>' % (self._valor_string, self.nome)
            else:
                texto += b' />'
        return texto


class TagInteiro(TagCaracter):

    def __init__(self, **kwargs):
        super(TagInteiro, self).__init__(**kwargs)
        self._valor_inteiro = 0
        self._valor_string = b'0'
        for k, v in kwargs.items():
            setattr(self, k, v)

        if kwargs.has_key(b'valor'):
            self.valor = kwargs[b'valor']

    def set_valor(self, novo_valor):
        if isinstance(novo_valor, basestring):
            if novo_valor:
                novo_valor = int(novo_valor)
            else:
                novo_valor = 0
        if isinstance(novo_valor, (int, long)) and self._valida(novo_valor):
            self._valor_inteiro = novo_valor
            self._valor_string = unicode(self._valor_inteiro)
            if self.placehold and self.tamanho_max and len(self._valor_string) < self.tamanho_max:
                self._valor_string = self._valor_string.rjust(self.tamanho_max, b'0')
        else:
            self._valor_inteiro = 0
            self._valor_string = b'0'

    def get_valor(self):
        return self._valor_inteiro

    valor = property(get_valor, set_valor)

    def _valida(self, valor):
        u"""
        É separado pois o intero só nao tem valor se for '' ou None
        :param valor:
        :return:
        """
        self.alertas = []
        if self._testa_obrigatorio(unicode(valor)):
            self.alertas.append(self._testa_obrigatorio(unicode(valor)))
        if self._testa_tamanho_minimo(valor):
            self.alertas.append(self._testa_tamanho_minimo(valor))
        if self._testa_tamanho_maximo(valor):
            self.alertas.append(self._testa_tamanho_maximo(valor))
        if self._testa_opcoes(valor):
            self.alertas.append(self._testa_opcoes(valor))
        return self.alertas == []

    def __unicode__(self):
        texto = b''
        if not self.obrigatorio and not self.valor:
            return texto
        if self.propriedade:
            return b' %s="%s"' % (self.propriedade, self._valor_string)
        texto = b'<%s' % self.nome
        if unicode(self.valor).isdigit() or self.placehold and self.tamanho_max:
            texto += b'>%s</%s>' % (self._valor_string, self.nome)
        else:
            texto += b' />'
        return texto


class TagDecimal(TagCaracter):

    def __init__(self, *args, **kwargs):
        self.decimal_digitos = kwargs.pop(b'decimal_digitos', 0)
        super(TagDecimal, self).__init__(*args, **kwargs)
        self._valor_decimal = Decimal(b'0.0')
        self._valor_string = self._formata(self._valor_decimal)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _parte_inteira(self, valor=None):
        if valor is None:
            valor = self._valor_decimal
        valor = unicode(valor).strip()
        if b'.' in valor:
            valor = valor.split(b'.')[0]
        return valor

    def _parte_decimal(self, valor=None):
        if valor is None:
            valor = self._valor_decimal
        valor = unicode(valor).strip()
        if b'.' in valor:
            valor = valor.split(b'.')[1]
        else:
            valor = b''
        return valor

    def _formata(self, valor):
        texto = self._parte_inteira(valor)
        dec = self._parte_decimal(valor)
        if not dec:
            dec = b'0'
        if self.decimal_digitos and len(dec) < self.decimal_digitos:
            dec = dec.ljust(self.decimal_digitos, b'0')
        texto += b'.' + dec
        return texto

    def _testa_decimais_maximo(self, decimal):
        if self.decimal_digitos and len(unicode(decimal)) > self.decimal_digitos:
            raise TamanhoInvalido(self.raiz, self.nome, decimal, dec_max=self.tamanho_max)

    def _testa_obrigatorio(self, valor):
        if self.obrigatorio and not valor and valor != Decimal(b'0.0'):
            return ErroObrigatorio(self.raiz, self.nome, self.propriedade)

    def _valida(self, valor):
        self.alertas = []
        if self._testa_obrigatorio(valor):
            self.alertas.append(self._testa_obrigatorio(valor))
        inteiro = self._parte_inteira(valor)
        decimal = self._parte_decimal(valor)
        if self._testa_tamanho_minimo(inteiro):
            self.alertas.append(self._testa_tamanho_minimo(inteiro))
        if self._testa_tamanho_maximo(inteiro):
            self.alertas.append(self._testa_tamanho_maximo(inteiro))
        if self._testa_decimais_maximo(decimal):
            self.alertas.append(self._testa_decimais_maximo(decimal))
        return self.alertas == []

    def set_valor(self, novo_valor):
        if isinstance(novo_valor, basestring):
            if novo_valor:
                novo_valor = Decimal(novo_valor)
            else:
                novo_valor = Decimal(b'0.0')
        if isinstance(novo_valor, (int, long, Decimal)) and self._valida(novo_valor):
            self._valor_decimal = Decimal(novo_valor)
            self._valor_string = self._formata(self._valor_decimal)
        else:
            self._valor_decimal = Decimal(b'0.0')
            self._valor_string = self._formata(self._valor_decimal)

    def get_valor(self):
        return self._valor_decimal

    valor = property(get_valor, set_valor)


def fuso_horario_sistema():
    from time import timezone
    diferenca = timezone // 3600
    if diferenca < 0:
        return pytz.timezone(b'Etc/GMT+' + str(diferenca * -1))
    if diferenca > 0:
        return pytz.timezone(b'Etc/GMT-' + str(diferenca))
    return pytz.UTC


class TagData(TagCaracter):

    def __init__(self, **kwargs):
        super(TagData, self).__init__(**kwargs)
        self._valor_data = None
        for k, v in kwargs.items():
            setattr(self, k, v)

        if kwargs.has_key(b'valor'):
            self.valor = kwargs[b'valor']
        return

    def _valida(self, valor):
        self.alertas = []
        if self._testa_obrigatorio(valor):
            self.alertas.append(self._testa_obrigatorio(valor))
        return self.alertas == []

    def set_valor(self, novo_valor):
        if isinstance(novo_valor, basestring):
            if novo_valor:
                novo_valor = datetime.strptime(novo_valor, b'%Y-%m-%d')
            else:
                novo_valor = None
        if isinstance(novo_valor, (datetime, date)) and self._valida(novo_valor):
            self._valor_data = novo_valor
            self._valor_string = b'%04d-%02d-%02d' % (
             self._valor_data.year, self._valor_data.month, self._valor_data.day)
        else:
            self._valor_data = None
            self._valor_string = b''
        return

    def get_valor(self):
        return self._valor_data

    valor = property(get_valor, set_valor)

    def formato_danfe(self):
        if self._valor_data is None:
            return b''
        else:
            return self._valor_data.strftime(b'%d/%m/%Y')
            return


class TagDataHoraUTC(TagData):

    def __init__(self, **kwargs):
        super(TagDataHoraUTC, self).__init__(**kwargs)
        self._validacao = re.compile(b'((20(([02468][048])|([13579][26]))-02-29)|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))T(20|21|22|23|[0-1]\\d):[0-5]\\d:[0-5]\\d(-0[1-4]:00)?')
        self._valida_fuso = re.compile(b'.*[-+]0[0-9]:00$')
        self._brasilia = pytz.timezone(b'America/Sao_Paulo')
        self.fuso_horario = b'America/Sao_Paulo'

    def set_valor(self, novo_valor):
        if isinstance(novo_valor, basestring):
            if self._validacao.match(novo_valor):
                if self._valida_fuso.match(novo_valor):
                    self.fuso_horario = novo_valor[19:]
                    novo_valor = novo_valor[:19]
                novo_valor = self.fuso_horario.localize(datetime.strptime(novo_valor, b'%Y-%m-%dT%H:%M:%S'))
            else:
                novo_valor = None
        if isinstance(novo_valor, datetime) and self._valida(novo_valor):
            if not novo_valor.tzinfo:
                novo_valor = fuso_horario_sistema().localize(novo_valor)
                novo_valor = pytz.UTC.normalize(novo_valor)
                novo_valor = self._brasilia.normalize(novo_valor)
            self._valor_data = novo_valor
            self._valor_data = self._valor_data.replace(microsecond=0)
            try:
                self._valor_data = self.fuso_horario.localize(self._valor_data)
            except:
                pass

            self._valor_string = self._valor_data.isoformat()
        else:
            self._valor_data = None
            self._valor_string = b''
        return

    def get_valor(self):
        return self._valor_data

    valor = property(get_valor, set_valor)

    def set_fuso_horaro(self, novo_valor):
        if novo_valor in pytz.country_timezones[b'br']:
            self._fuso_horario = pytz.timezone(novo_valor)
        elif novo_valor == b'-04:00' or novo_valor == b'-0400':
            self._fuso_horario = pytz.timezone(b'Etc/GMT+4')
        elif novo_valor == b'-03:00' or novo_valor == b'-0300':
            self._fuso_horario = pytz.timezone(b'Etc/GMT+3')
        elif novo_valor == b'-02:00' or novo_valor == b'-0200':
            self._fuso_horario = pytz.timezone(b'Etc/GMT+2')
        elif novo_valor == b'-01:00' or novo_valor == b'-0100':
            self._fuso_horario = pytz.timezone(b'Etc/GMT+1')

    def get_fuso_horario(self):
        return self._fuso_horario

    fuso_horario = property(get_fuso_horario, set_fuso_horaro)


class XMLAPI(NohXML):

    def __init__(self, *args, **kwargs):
        super(XMLAPI, self).__init__(*args, **kwargs)
        self._xml = None
        return

    def get_xml(self):
        return b''

    def valido(self):
        return False

    def le_grupo(self, raiz_grupo, classe_grupo, sigla_ns=b''):
        tags = []
        grupos = self._le_nohs(raiz_grupo, sigla_ns=sigla_ns)
        if grupos is not None:
            tags = [ classe_grupo() for g in grupos ]
            for i in range(len(grupos)):
                tags[i].xml = grupos[i]

        return tags