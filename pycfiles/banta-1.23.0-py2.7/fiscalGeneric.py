# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\printer\fiscalGeneric.py
# Compiled at: 2012-08-23 19:58:22


class PrinterException(RuntimeError):
    pass


class FieldFormatter(object):
    nonFiscalText = 40
    customerName = 30
    custAddressSize = 40
    paymentDescription = 30
    fiscalText = 20
    lineItem = 20
    lastItemDiscount = 20
    generalDiscount = 20
    embarkItem = 108
    receiptText = 106

    def _formatText(self, text, context):
        sizeDict = self.textSizeDict.get(self.model)
        if not sizeDict:
            sizeDict = self.textSizeDict['615']
        return formatText(text)[:sizeDict.get(context, 20)]


class PrinterInterface:
    """Interfaz que deben cumplir las impresoras fiscales."""
    MODEL_NAMES = []

    def openNonFiscalReceipt(self):
        """Abre documento no fiscal"""
        raise NotImplementedError

    def printNonFiscalText(self, text):
        u"""Imprime texto fiscal. Si supera el límite de la linea se trunca."""
        raise NotImplementedError

    NON_FISCAL_TEXT_MAX_LENGTH = 40

    def closeDocument(self):
        u"""Cierra el documento que esté abierto"""
        raise NotImplementedError

    def cancelDocument(self):
        u"""Cancela el documento que esté abierto"""
        raise NotImplementedError

    def addItem(self, description, quantity, price, iva, discount, discountDescription, negative=False):
        u"""Agrega un item a la FC.
                                                @param description                                      Descripción del item. Puede ser un string o una lista.
                                                                Si es una lista cada valor va en una línea.
                                                @param quantity                                          Cantidad
                                                @param price                                                            Precio (incluye el iva si la FC es B o C, si es A no lo incluye)
                                                @param iva                                                                      Porcentaje de iva
                                                @param negative                                          True->Resta de la FC
                                                @param discount                                          Importe de descuento
                                                @param discountDescription      Descripción del descuento
                                """
        raise NotImplementedError

    def addPayment(self, description, payment):
        u"""Agrega un pago a la FC.
                                                @param description      Descripción
                                                @param payment                  Importe
                                """
        raise NotImplementedError

    DOC_TYPE_CUIT = 'C'
    DOC_TYPE_LIBRETA_ENROLAMIENTO = '0'
    DOC_TYPE_LIBRETA_CIVICA = '1'
    DOC_TYPE_DNI = '2'
    DOC_TYPE_PASAPORTE = '3'
    DOC_TYPE_CEDULA = '4'
    DOC_TYPE_SIN_CALIFICADOR = ' '
    docTypeNames = {DOC_TYPE_CUIT: 'CUIT', 
       DOC_TYPE_LIBRETA_ENROLAMIENTO: 'L.E.', 
       DOC_TYPE_LIBRETA_CIVICA: 'L.C.', 
       DOC_TYPE_DNI: 'DNI', 
       DOC_TYPE_PASAPORTE: 'PASAP', 
       DOC_TYPE_CEDULA: 'CED', 
       DOC_TYPE_SIN_CALIFICADOR: 'S/C'}
    IVA_TYPE_RESPONSABLE_INSCRIPTO = 'I'
    IVA_TYPE_RESPONSABLE_NO_INSCRIPTO = 'N'
    IVA_TYPE_EXENTO = 'E'
    IVA_TYPE_NO_RESPONSABLE = 'A'
    IVA_TYPE_CONSUMIDOR_FINAL = 'C'
    IVA_TYPE_RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO = 'B'
    IVA_TYPE_RESPONSABLE_MONOTRIBUTO = 'M'
    IVA_TYPE_MONOTRIBUTISTA_SOCIAL = 'S'
    IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL = 'V'
    IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL = 'W'
    IVA_TYPE_NO_CATEGORIZADO = 'T'

    def openTicket(self):
        """Abre documento fiscal"""
        raise NotImplementedError

    def openBillTicket(self, type, name, address, doc, docType, ivaType):
        u"""
                                Abre un ticket-factura
                                                @param  type                            Tipo de Factura "A", "B", o "C"
                                                @param  name                            Nombre del cliente
                                                @param  address          Domicilio
                                                @param  doc                              Documento del cliente según docType
                                                @param  docType          Tipo de documento
                                                @param  ivaType          Tipo de IVA
                                """
        raise NotImplementedError

    def openBillCreditTicket(self, type, name, address, doc, docType, ivaType, reference='NC'):
        u"""
                                Abre un ticket-NC
                                                @param  type                            Tipo de Factura "A", "B", o "C"
                                                @param  name                            Nombre del cliente
                                                @param  address          Domicilio
                                                @param  doc                              Documento del cliente según docType
                                                @param  docType          Tipo de documento
                                                @param  ivaType          Tipo de IVA
                                                @param  reference
                                """
        raise NotImplementedError

    def openDebitNoteTicket(self, type, name, address, doc, docType, ivaType):
        u"""
                                Abre una Nota de Débito
                                                @param  type                            Tipo de Factura "A", "B", o "C"
                                                @param  name                            Nombre del cliente
                                                @param  address          Domicilio
                                                @param  doc                              Documento del cliente según docType
                                                @param  docType          Tipo de documento
                                                @param  ivaType          Tipo de IVA
                                                @param  reference
                                """
        raise NotImplementedError

    def openRemit(self, name, address, doc, docType, ivaType):
        u"""
                                Abre un remito
                                                @param  name                            Nombre del cliente
                                                @param  address          Domicilio
                                                @param  doc                              Documento del cliente según docType
                                                @param  docType          Tipo de documento
                                                @param  ivaType          Tipo de IVA
                                """
        raise NotImplementedError

    def openReceipt(self, name, address, doc, docType, ivaType, number):
        u"""
                                Abre un recibo
                                                @param  name                            Nombre del cliente
                                                @param  address          Domicilio
                                                @param  doc                              Documento del cliente según docType
                                                @param  docType          Tipo de documento
                                                @param  ivaType          Tipo de IVA
                                                @param  number                  Número de identificación del recibo (arbitrario)
                                """
        raise NotImplementedError

    def addRemitItem(self, description, quantity):
        u"""Agrega un item al remito
                                                @param description      Descripción
                                                @param quantity          Cantidad
                                """
        raise NotImplementedError

    def addReceiptDetail(self, descriptions, amount):
        """Agrega el detalle del recibo
                                                @param descriptions Lista de descripciones (lineas)
                                                @param amount                    Importe total del recibo
                                """
        raise NotImplementedError

    def addAdditional(self, description, amount, iva, negative=False):
        u"""Agrega un adicional a la FC.
                                                @param description      Descripción
                                                @param amount                    Importe (sin iva en FC A, sino con IVA)
                                                @param iva                                      Porcentaje de Iva
                                                @param negative True->Descuento, False->Recargo"""
        raise NotImplementedError

    def getLastNumber(self, letter):
        u"""Obtiene el último número de FC"""
        raise NotImplementedError

    def getLastCreditNoteNumber(self, letter):
        u"""Obtiene el último número de FC"""
        raise NotImplementedError

    def getLastRemitNumber(self):
        u"""Obtiene el último número de Remtio"""
        raise NotImplementedError

    def cancelAnyDocument(self):
        """Cancela cualquier documento abierto, sea del tipo que sea.
                                         No requiere que previamente se haya abierto el documento por este objeto.
                                         Se usa para destrabar la impresora."""
        raise NotImplementedError

    def dailyClose(self, type):
        """Cierre Z (diario) o X (parcial)
                                                @param type              Z (diario), X (parcial)
                                """
        raise NotImplementedError

    def close(self):
        """Cierra la impresora"""
        raise NotImplementedError

    def getWarnings(self):
        return []

    def openDrawer(self):
        u"""Abrir cajón del dinero - No es mandatory implementarlo"""
        pass

    def getStatus(self):
        return []