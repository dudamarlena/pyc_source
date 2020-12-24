# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfva/soap/verificador.py
# Compiled at: 2018-11-01 16:30:20
# Size of source mod 2**32: 4484 bytes
from soapfish import soap, xsd
from pyfva.soap import settings
BaseHeader = xsd.ComplexType

class RespuestaDeLaSolicitud(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    CodigoDeError = xsd.Element((xsd.Int), minOccurs=1)
    ExisteUnaFirmaCompleta = xsd.Element((xsd.Boolean), minOccurs=1)
    FueExitosa = xsd.Element((xsd.Boolean), minOccurs=1)

    @classmethod
    def create(cls, CodigoDeError, ExisteUnaFirmaCompleta, FueExitosa):
        instance = cls()
        instance.CodigoDeError = CodigoDeError
        instance.ExisteUnaFirmaCompleta = ExisteUnaFirmaCompleta
        instance.FueExitosa = FueExitosa
        return instance


class ExisteUnaSolicitudDeFirmaCompleta(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    laCedulaDelUsuario = xsd.Element((xsd.String), minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class ExisteUnaSolicitudDeFirmaCompletaResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    ExisteUnaSolicitudDeFirmaCompletaResult = xsd.Element(RespuestaDeLaSolicitud, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class ValideElServicio(xsd.ComplexType):
    pass


class ValideElServicioResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    ValideElServicioResult = xsd.Element((xsd.Boolean), minOccurs=1)

    @classmethod
    def create(cls, ValideElServicioResult):
        instance = cls()
        instance.ValideElServicioResult = ValideElServicioResult
        return instance


Schema_c49e7 = xsd.Schema(imports=[], includes=[], targetNamespace=(settings.FVA_HOST),
  elementFormDefault='qualified',
  simpleTypes=[],
  attributeGroups=[],
  groups=[],
  complexTypes=[
 RespuestaDeLaSolicitud],
  elements={'ExisteUnaSolicitudDeFirmaCompleta':xsd.Element(ExisteUnaSolicitudDeFirmaCompleta()), 
 'ExisteUnaSolicitudDeFirmaCompletaResponse':xsd.Element(ExisteUnaSolicitudDeFirmaCompletaResponse()),  'ValideElServicio':xsd.Element(ValideElServicio()),  'ValideElServicioResponse':xsd.Element(ValideElServicioResponse())})
ExisteUnaSolicitudDeFirmaCompleta_method = xsd.Method(soapAction=(settings.FVA_HOST + 'ExisteUnaSolicitudDeFirmaCompleta'),
  input='ExisteUnaSolicitudDeFirmaCompleta',
  inputPartName='parameters',
  output='ExisteUnaSolicitudDeFirmaCompletaResponse',
  outputPartName='parameters',
  operationName='ExisteUnaSolicitudDeFirmaCompleta',
  style='document')
ValideElServicio_method = xsd.Method(soapAction=(settings.FVA_HOST + 'ValideElServicio'),
  input='ValideElServicio',
  inputPartName='parameters',
  output='ValideElServicioResponse',
  outputPartName='parameters',
  operationName='ValideElServicio',
  style='document')
VerificadorSoap_SERVICE = soap.Service(name='VerificadorSoap',
  targetNamespace=(settings.FVA_HOST),
  location=('${scheme}://${host}/' + settings.SERVICE_URLS['verifica']),
  schemas=[
 Schema_c49e7],
  version=(soap.SOAPVersion.SOAP12),
  methods=[
 ExisteUnaSolicitudDeFirmaCompleta_method, ValideElServicio_method])

class VerificadorSoapServiceStub(soap.Stub):
    SERVICE = VerificadorSoap_SERVICE
    SCHEME = settings.STUB_SCHEME
    HOST = settings.STUB_HOST

    def ExisteUnaSolicitudDeFirmaCompleta(self, ExisteUnaSolicitudDeFirmaCompleta, header=None):
        return self.call('ExisteUnaSolicitudDeFirmaCompleta', ExisteUnaSolicitudDeFirmaCompleta, header=header)

    def ValideElServicio(self, ValideElServicio, header=None):
        return self.call('ValideElServicio', ValideElServicio, header=header)