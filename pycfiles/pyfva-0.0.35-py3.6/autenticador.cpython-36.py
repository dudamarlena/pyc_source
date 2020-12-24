# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfva/soap/autenticador.py
# Compiled at: 2019-05-15 12:56:18
# Size of source mod 2**32: 6820 bytes
from soapfish import soap, xsd
from pyfva.soap import settings
BaseHeader = xsd.ComplexType

class SolicitudDeAutenticacion(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    ExtensionData = xsd.Element((__name__ + '.ExtensionDataObject'), minOccurs=0)
    CodNegocio = xsd.Element((xsd.Int), minOccurs=1)
    FechaDeReferenciaDeLaEntidad = xsd.Element((xsd.DateTime), minOccurs=1)
    IdFuncionalidad = xsd.Element((xsd.Int), minOccurs=1)
    IdReferenciaEntidad = xsd.Element((xsd.Int), minOccurs=1)
    IdentificacionDelSuscriptor = xsd.Element((xsd.String), minOccurs=0)

    @classmethod
    def create(cls, CodNegocio, FechaDeReferenciaDeLaEntidad, IdFuncionalidad, IdReferenciaEntidad, IdentificacionDelSuscriptor):
        instance = cls()
        instance.CodNegocio = CodNegocio
        instance.FechaDeReferenciaDeLaEntidad = FechaDeReferenciaDeLaEntidad
        instance.IdFuncionalidad = IdFuncionalidad
        instance.IdReferenciaEntidad = IdReferenciaEntidad
        instance.IdentificacionDelSuscriptor = IdentificacionDelSuscriptor
        return instance


class ExtensionDataObject(xsd.ComplexType):
    pass


class RespuestaDeLaSolicitud(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    CodigoDeError = xsd.Element((xsd.Int), minOccurs=1)
    CodigoDeVerificacion = xsd.Element((xsd.String), minOccurs=0)
    TiempoMaximoDeFirmaEnSegundos = xsd.Element((xsd.Int), minOccurs=1)
    IdDeLaSolicitud = xsd.Element((xsd.Int), minOccurs=1)
    ResumenDelDocumento = xsd.Element((xsd.String), minOccurs=0)
    InformacionSuscriptorDesconectado = xsd.Element((__name__ + '.InformacionSuscriptorDesconectado'), minOccurs=0)

    @classmethod
    def create(cls, CodigoDeError, TiempoMaximoDeFirmaEnSegundos, IdDeLaSolicitud, CodigoDeVerificacion=None, ResumenDelDocumento=None, InformacionSuscriptorDesconectado=None):
        instance = cls()
        instance.CodigoDeError = CodigoDeError
        instance.TiempoMaximoDeFirmaEnSegundos = TiempoMaximoDeFirmaEnSegundos
        instance.IdDeLaSolicitud = IdDeLaSolicitud
        if CodigoDeVerificacion:
            instance.CodigoDeVerificacion = CodigoDeVerificacion
        if ResumenDelDocumento:
            instance.ResumenDelDocumento = ResumenDelDocumento
        if InformacionSuscriptorDesconectado:
            instance.InformacionSuscriptorDesconectado = InformacionSuscriptorDesconectado
        return instance


class InformacionSuscriptorDesconectado(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    HaIniciadoSesionEnElFirmador = xsd.Element((xsd.Boolean), minOccurs=1)
    RutaDeDescargaDelFirmador = xsd.Element((xsd.String), minOccurs=0)

    @classmethod
    def create(cls, HaIniciadoSesionEnElFirmador):
        instance = cls()
        instance.HaIniciadoSesionEnElFirmador = HaIniciadoSesionEnElFirmador
        return instance


class RecibaLaSolicitudDeAutenticacion(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    laSolicitud = xsd.Element(SolicitudDeAutenticacion, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class RecibaLaSolicitudDeAutenticacionResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    RecibaLaSolicitudDeAutenticacionResult = xsd.Element(RespuestaDeLaSolicitud,
      minOccurs=0)

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
 SolicitudDeAutenticacion,
 ExtensionDataObject, RespuestaDeLaSolicitud, InformacionSuscriptorDesconectado],
  elements={'RecibaLaSolicitudDeAutenticacion':xsd.Element(RecibaLaSolicitudDeAutenticacion()), 
 'RecibaLaSolicitudDeAutenticacionResponse':xsd.Element(RecibaLaSolicitudDeAutenticacionResponse()), 
 'ValideElServicio':xsd.Element(ValideElServicio()),  'ValideElServicioResponse':xsd.Element(ValideElServicioResponse())})
RecibaLaSolicitudDeAutenticacion_method = xsd.Method(soapAction=(settings.FVA_HOST + 'RecibaLaSolicitudDeAutenticacion'),
  input='RecibaLaSolicitudDeAutenticacion',
  inputPartName='parameters',
  output='RecibaLaSolicitudDeAutenticacionResponse',
  outputPartName='parameters',
  operationName='RecibaLaSolicitudDeAutenticacion',
  style='document')
ValideElServicio_method = xsd.Method(soapAction=(settings.FVA_HOST + 'ValideElServicio'),
  input='ValideElServicio',
  inputPartName='parameters',
  output='ValideElServicioResponse',
  outputPartName='parameters',
  operationName='ValideElServicio',
  style='document')
AutenticadorSoap_SERVICE = soap.Service(name='AutenticadorSoap',
  targetNamespace=(settings.FVA_HOST),
  location=('${scheme}://${host}/' + settings.SERVICE_URLS['autenticacion']),
  schemas=[
 Schema_c49e7],
  version=(soap.SOAPVersion.SOAP12),
  methods=[
 RecibaLaSolicitudDeAutenticacion_method, ValideElServicio_method])

class AutenticadorSoapServiceStub(soap.Stub):
    SERVICE = AutenticadorSoap_SERVICE
    SCHEME = settings.STUB_SCHEME
    HOST = settings.STUB_HOST

    def RecibaLaSolicitudDeAutenticacion(self, RecibaLaSolicitudDeAutenticacion, header=None):
        return self.call('RecibaLaSolicitudDeAutenticacion', RecibaLaSolicitudDeAutenticacion, header=header)

    def ValideElServicio(self, ValideElServicio, header=None):
        return self.call('ValideElServicio', ValideElServicio, header=header)