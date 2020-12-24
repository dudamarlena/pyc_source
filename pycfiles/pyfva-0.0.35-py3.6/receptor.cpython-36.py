# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfva/soap/receptor.py
# Compiled at: 2017-07-24 16:54:40
# Size of source mod 2**32: 4630 bytes
from soapfish import soap, xsd
BaseHeader = xsd.ComplexType
from pyfva.soap import settings

class ResultadoDeFirma(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    IdDeLaSolicitud = xsd.Element((xsd.Int), minOccurs=1)
    DocumentoFirmado = xsd.Element((xsd.Base64Binary),
      minOccurs=1, nillable=True)
    FueExitosa = xsd.Element((xsd.Boolean), minOccurs=1)
    CodigoDeError = xsd.Element((xsd.Int), minOccurs=1)

    @classmethod
    def create(cls, IdDeLaSolicitud, DocumentoFirmado, FueExitosa, CodigoDeError):
        instance = cls()
        instance.IdDeLaSolicitud = IdDeLaSolicitud
        instance.DocumentoFirmado = DocumentoFirmado
        instance.FueExitosa = FueExitosa
        instance.CodigoDeError = CodigoDeError
        return instance


class NotifiqueLaRespuesta(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    elResultado = xsd.Element(ResultadoDeFirma, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class NotifiqueLaRespuestaResponse(xsd.ComplexType):
    pass


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


Schema_c49e7 = xsd.Schema(imports=[], includes=[], targetNamespace=(settings.RECEPTOR_HOST),
  elementFormDefault='qualified',
  simpleTypes=[],
  attributeGroups=[],
  groups=[],
  complexTypes=[
 ResultadoDeFirma],
  elements={'NotifiqueLaRespuesta':xsd.Element(NotifiqueLaRespuesta()), 
 'NotifiqueLaRespuestaResponse':xsd.Element(NotifiqueLaRespuestaResponse()),  'ValideElServicio':xsd.Element(ValideElServicio()), 
 'ValideElServicioResponse':xsd.Element(ValideElServicioResponse())})

def NotifiqueLaRespuesta(request, NotifiqueLaRespuesta):
    return NotifiqueLaRespuestaResponse


def ValideElServicio(request, ValideElServicio):
    return ValideElServicioResponse


NotifiqueLaRespuesta_method = xsd.Method(function=NotifiqueLaRespuesta,
  soapAction=(settings.RECEPTOR_HOST + 'NotifiqueLaRespuesta'),
  input='NotifiqueLaRespuesta',
  inputPartName='parameters',
  output='NotifiqueLaRespuestaResponse',
  outputPartName='parameters',
  operationName='NotifiqueLaRespuesta',
  style='document')
ValideElServicio_method = xsd.Method(function=ValideElServicio,
  soapAction=(settings.RECEPTOR_HOST + 'ValideElServicio'),
  input='ValideElServicio',
  inputPartName='parameters',
  output='ValideElServicioResponse',
  outputPartName='parameters',
  operationName='ValideElServicio',
  style='document')
ResultadoDeSolicitudSoap_SERVICE = soap.Service(name='ResultadoDeSolicitudSoap',
  targetNamespace=(settings.RECEPTOR_HOST),
  location='${scheme}://${host}/wcfv2/Bccr.Sinpe.Fva.EntidadDePruebas.Notificador/ResultadoDeSolicitud.asmx',
  schemas=[
 Schema_c49e7],
  version=(soap.SOAPVersion.SOAP12),
  methods=[
 NotifiqueLaRespuesta_method, ValideElServicio_method])