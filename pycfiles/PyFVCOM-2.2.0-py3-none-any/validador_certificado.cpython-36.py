# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfva/soap/validador_certificado.py
# Compiled at: 2018-11-01 16:27:49
# Size of source mod 2**32: 5565 bytes
from soapfish import soap, xsd
from pyfva.soap import settings
BaseHeader = xsd.ComplexType

class ResultadoDeLaSolicitud(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    CodigoDeError = xsd.Element((xsd.Int), minOccurs=1)
    FueExitosa = xsd.Element((xsd.Boolean), minOccurs=1)
    InformacionDelCertificado = xsd.Element((__name__ + '.InformacionDelCertificado'), minOccurs=0)

    @classmethod
    def create(cls, CodigoDeError, FueExitosa):
        instance = cls()
        instance.CodigoDeError = CodigoDeError
        instance.FueExitosa = FueExitosa
        return instance


class InformacionDelCertificado(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    Identificacion = xsd.Element((xsd.String), minOccurs=0)
    TipoDeIdentificacion = xsd.Element((xsd.Int), minOccurs=1)
    NombreCompleto = xsd.Element((xsd.String), minOccurs=0)
    FechaInicioDeLaVigencia = xsd.Element((xsd.DateTime), minOccurs=1)
    FechaFinalDeLaVigencia = xsd.Element((xsd.DateTime), minOccurs=1)

    @classmethod
    def create(cls, TipoDeIdentificacion, FechaInicioDeLaVigencia, FechaFinalDeLaVigencia):
        instance = cls()
        instance.TipoDeIdentificacion = TipoDeIdentificacion
        instance.FechaInicioDeLaVigencia = FechaInicioDeLaVigencia
        instance.FechaFinalDeLaVigencia = FechaFinalDeLaVigencia
        return instance


class SoliciteLaValidacionDelCertificadoDeAutenticacion(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    elCertificadoDeAutenticacion = xsd.Element((xsd.Base64Binary), minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SoliciteLaValidacionDelCertificadoDeAutenticacionResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    SoliciteLaValidacionDelCertificadoDeAutenticacionResult = xsd.Element(ResultadoDeLaSolicitud, minOccurs=0)

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
 ResultadoDeLaSolicitud, InformacionDelCertificado],
  elements={'SoliciteLaValidacionDelCertificadoDeAutenticacion':xsd.Element(SoliciteLaValidacionDelCertificadoDeAutenticacion()), 
 'SoliciteLaValidacionDelCertificadoDeAutenticacionResponse':xsd.Element(SoliciteLaValidacionDelCertificadoDeAutenticacionResponse()),  'ValideElServicio':xsd.Element(ValideElServicio()),  'ValideElServicioResponse':xsd.Element(ValideElServicioResponse())})
SoliciteLaValidacionDelCertificadoDeAutenticacion_method = xsd.Method(soapAction=(settings.FVA_HOST + 'SoliciteLaValidacionDelCertificadoDeAutenticacion'),
  input='SoliciteLaValidacionDelCertificadoDeAutenticacion',
  inputPartName='parameters',
  output='SoliciteLaValidacionDelCertificadoDeAutenticacionResponse',
  outputPartName='parameters',
  operationName='SoliciteLaValidacionDelCertificadoDeAutenticacion',
  style='document')
ValideElServicio_method = xsd.Method(soapAction=(settings.FVA_HOST + 'ValideElServicio'),
  input='ValideElServicio',
  inputPartName='parameters',
  output='ValideElServicioResponse',
  outputPartName='parameters',
  operationName='ValideElServicio',
  style='document')
ValidadorDeCertificadoSoap_SERVICE = soap.Service(name='ValidadorDeCertificadoSoap',
  targetNamespace=(settings.FVA_HOST),
  location=('${scheme}://${host}/' + settings.SERVICE_URLS['valida_certificado']),
  schemas=[
 Schema_c49e7],
  version=(soap.SOAPVersion.SOAP12),
  methods=[
 SoliciteLaValidacionDelCertificadoDeAutenticacion_method, ValideElServicio_method])

class ValidadorDeCertificadoSoapServiceStub(soap.Stub):
    SERVICE = ValidadorDeCertificadoSoap_SERVICE
    SCHEME = settings.STUB_SCHEME
    HOST = settings.STUB_HOST

    def SoliciteLaValidacionDelCertificadoDeAutenticacion(self, SoliciteLaValidacionDelCertificadoDeAutenticacion, header=None):
        return self.call('SoliciteLaValidacionDelCertificadoDeAutenticacion', SoliciteLaValidacionDelCertificadoDeAutenticacion, header=header)

    def ValideElServicio(self, ValideElServicio, header=None):
        return self.call('ValideElServicio', ValideElServicio, header=header)