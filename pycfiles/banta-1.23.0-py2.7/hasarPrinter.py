# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\printer\hasarPrinter.py
# Compiled at: 2012-12-03 23:07:08
import string, types, logging, unicodedata
from banta.packages.optional.printer.fiscalGeneric import PrinterInterface, PrinterException
from . import epsonFiscalDriver

class ValidationError(Exception):
    pass


class FiscalPrinterError(Exception):
    pass


class FileDriver:

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'a')

    def sendCommand(self, command, parameters, skipStatusErrors=False):
        import random
        self.file.write('Command: %d, Parameters: %s\n' % (command, parameters))
        number = random.randint(2, 12432)
        return [str(number)] * 10

    def close(self):
        self.file.close()


def formatText(text):
    asciiText = unicodedata.normalize('NFKD', unicode(text)).encode('ASCII', 'ignore')
    return asciiText


NUMBER = 999990

class DummyDriver:

    def __init__(self):
        global NUMBER
        NUMBER = NUMBER + 1
        self.number = NUMBER

    def close(self):
        pass

    def sendCommand(self, commandNumber, parameters, skipStatusErrors):
        ret = [
         'C080', '3600', str(self.number), str(self.number), str(self.number), str(self.number),
         str(self.number), str(self.number), str(self.number), str(self.number)]
        print 'sendCommand', ret, parameters
        return ret


class HasarPrinter(PrinterInterface):
    CMD_OPEN_FISCAL_RECEIPT = 64
    CMD_OPEN_CREDIT_NOTE = 128
    CMD_PRINT_TEXT_IN_FISCAL = 65
    CMD_PRINT_LINE_ITEM = 66
    CMD_PRINT_SUBTOTAL = 67
    CMD_ADD_PAYMENT = 68
    CMD_CLOSE_FISCAL_RECEIPT = 69
    CMD_DAILY_CLOSE = 57
    CMD_STATUS_REQUEST = 42
    CMD_CLOSE_CREDIT_NOTE = 129
    CMD_CREDIT_NOTE_REFERENCE = 147
    CMD_SET_CUSTOMER_DATA = 98
    CMD_LAST_ITEM_DISCOUNT = 85
    CMD_GENERAL_DISCOUNT = 84
    CMD_OPEN_NON_FISCAL_RECEIPT = 72
    CMD_PRINT_NON_FISCAL_TEXT = 73
    CMD_CLOSE_NON_FISCAL_RECEIPT = 74
    CMD_CANCEL_ANY_DOCUMENT = 152
    CMD_OPEN_DRAWER = 123
    CMD_SET_HEADER_TRAILER = 93
    CMD_OPEN_DNFH = 128
    CMD_PRINT_EMBARK_ITEM = 130
    CMD_PRINT_ACCOUNT_ITEM = 131
    CMD_PRINT_QUOTATION_ITEM = 132
    CMD_PRINT_DNFH_INFO = 133
    CMD_PRINT_RECEIPT_TEXT = 151
    CMD_CLOSE_DNFH = 129
    CMD_REPRINT = 153
    CURRENT_DOC_TICKET = 1
    CURRENT_DOC_BILL_TICKET = 2
    CURRENT_DOC_NON_FISCAL = 3
    CURRENT_DOC_CREDIT_BILL_TICKET = 4
    CURRENT_DOC_CREDIT_TICKET = 5
    CURRENT_DOC_DNFH = 6
    MODEL_615 = 0
    MODEL_715v1 = 1
    MODEL_715v2 = 2
    MODEL_320 = 3
    MODEL_NAMES = ('615', '715v1', '715v2', '320F - 441')
    AVAILABLE_MODELS = (
     '615', '715v1', '715v2', MODEL_320)
    ivaTypeMap = {PrinterInterface.IVA_TYPE_RESPONSABLE_INSCRIPTO: 'I', 
       PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO: 'N', 
       PrinterInterface.IVA_TYPE_EXENTO: 'E', 
       PrinterInterface.IVA_TYPE_NO_RESPONSABLE: 'A', 
       PrinterInterface.IVA_TYPE_CONSUMIDOR_FINAL: 'C', 
       PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO: 'B', 
       PrinterInterface.IVA_TYPE_RESPONSABLE_MONOTRIBUTO: 'M', 
       PrinterInterface.IVA_TYPE_MONOTRIBUTISTA_SOCIAL: 'S', 
       PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL: 'V', 
       PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL: 'W', 
       PrinterInterface.IVA_TYPE_NO_CATEGORIZADO: 'T'}
    textSizeDict = {'615': {'nonFiscalText': 40, 'customerName': 30, 
               'custAddressSize': 40, 
               'paymentDescription': 30, 
               'fiscalText': 20, 
               'lineItem': 20, 
               'lastItemDiscount': 20, 
               'generalDiscount': 20, 
               'embarkItem': 108, 
               'receiptText': 106}, 
       MODEL_320: {'nonFiscalText': 120, 
                   'customerName': 50, 
                   'custAddressSize': 50, 
                   'paymentDescription': 50, 
                   'fiscalText': 50, 
                   'lineItem': 50, 
                   'lastItemDiscount': 50, 
                   'generalDiscount': 50, 
                   'embarkItem': 108, 
                   'receiptText': 106}}
    ADDRESS_SIZE = 40
    DAILY_CLOSE_X = 'X'
    DAILY_CLOSE_Z = 'Z'

    def __init__(self, deviceFile=None, speed=9600, host=None, port=None, model='615', dummy=False, connectOnEveryCommand=False):
        try:
            if dummy:
                self.driver = DummyDriver()
            elif host:
                self.driver = epsonFiscalDriver.EpsonFiscalDriverProxy(host, port, connectOnEveryCommand)
            else:
                deviceFile = deviceFile or 0
                self.driver = epsonFiscalDriver.HasarFiscalDriver(deviceFile, speed)
        except Exception as e:
            raise FiscalPrinterError('Imposible establecer comunicación.', e)

        self.model = model

    def _sendCommand(self, commandNumber, parameters=(), skipStatusErrors=False):
        commandString = 'SEND|0x%x|%s|%s' % (commandNumber, skipStatusErrors and 'T' or 'F',
         str(parameters))
        try:
            logging.getLogger().info('sendCommand: %s' % commandString)
            ret = self.driver.sendCommand(commandNumber, parameters, skipStatusErrors)
            logging.getLogger().info('reply: %s' % ret)
            return ret
        except epsonFiscalDriver.PrinterException as e:
            logging.getLogger().error('epsonFiscalDriver.PrinterException: %s' % str(e))
            raise PrinterException('Error de la impresora fiscal: %s.\nComando enviado: %s' % (
             str(e), commandString))

    def openNonFiscalReceipt(self):
        status = self._sendCommand(self.CMD_OPEN_NON_FISCAL_RECEIPT, [])

        def checkStatusInComprobante(x):
            fiscalStatus = int(x, 16)
            return fiscalStatus & 8192 == 8192

        if not checkStatusInComprobante(status[1]):
            status = self._sendCommand(self.CMD_OPEN_NON_FISCAL_RECEIPT, [])
            if not checkStatusInComprobante(status[1]):
                raise PrinterException('Error de la impresora fiscal, no acepta el comando de iniciar un ticket no fiscal')
        self._currentDocument = self.CURRENT_DOC_NON_FISCAL
        return status

    def _formatText(self, text, context):
        sizeDict = self.textSizeDict.get(self.model)
        if not sizeDict:
            sizeDict = self.textSizeDict['615']
        return formatText(text)[:sizeDict.get(context, 20)]

    def printNonFiscalText(self, text):
        return self._sendCommand(self.CMD_PRINT_NON_FISCAL_TEXT, [
         self._formatText(text, 'nonFiscalText') or ' ', '0'])

    def _setHeaderTrailer(self, line, text):
        return self._sendCommand(self.CMD_SET_HEADER_TRAILER, (str(line), text))

    def setHeader(self, header=None):
        """Establecer encabezados"""
        if not header:
            header = []
            if self.model == self.MODEL_320:
                header = [
                 '-', '-', '-']
        line = 3
        for text in (header + [chr(127)] * 3)[:3]:
            self._setHeaderTrailer(line, text)
            line += 1

    def setTrailer(self, trailer=None):
        """Establecer pie"""
        if not trailer:
            trailer = []
        fill = '\x7f'
        if self.model == self.MODEL_320:
            fill = '-'
        lines = len(trailer)
        trailer.extend([fill] * (9 - lines))
        for line, text in enumerate(trailer, 11):
            self._setHeaderTrailer(line, text)

    def _setCustomerData(self, name, address, doc, docType, ivaType):
        """Agrega los datos del cliente"""
        self.setHeader()
        self.setTrailer()
        doc = doc.replace('-', '').replace('.', '')
        if doc and docType != '3' and filter(lambda x: x not in string.digits, doc):
            doc, docType = (' ', ' ')
        if not doc.strip():
            docType = ' '
        ivaType = self.ivaTypeMap.get(ivaType, 'C')
        if ivaType != 'C' and (not doc or docType != self.DOC_TYPE_CUIT):
            raise ValidationError('Error, si el tipo de IVA del cliente NO es consumidor final, debe ingresar su número de CUIT.')
        parameters = [self._formatText(name, 'customerName'),
         doc or ' ',
         ivaType,
         docType or ' ']
        if self.model in ['715v1', '715v2', self.MODEL_320]:
            parameters.append(self._formatText(address, 'custAddressSize') or ' ')
        self._sendCommand(self.CMD_SET_CUSTOMER_DATA, parameters)

    def openBillTicket(self, type_, name, address, doc, docType, ivaType):
        """Inicia una factura A/B
                                :param type_: tipo de factura. 'A' o 'B'
                                :param name: nombre del cliente
                                :param address: direccion del cliente
                                :param doc: dni o identificacion
                                :param docType: tipo de identificacion
                                """
        self._setCustomerData(name, address, doc, docType, ivaType)
        if type_ != 'A':
            type_ = 'B'
        self._currentDocument = self.CURRENT_DOC_BILL_TICKET
        self._savedPayments = []
        return self._sendCommand(self.CMD_OPEN_FISCAL_RECEIPT, [type_, 'T'])

    def openTicket(self):
        """Inicia un ticket (Vendedor monotributista)"""
        if self.model == self.MODEL_320:
            self._sendCommand(self.CMD_OPEN_FISCAL_RECEIPT, ['B', 'T'])
        else:
            self._sendCommand(self.CMD_OPEN_FISCAL_RECEIPT, ['T', 'T'])
        self._currentDocument = self.CURRENT_DOC_TICKET
        self._savedPayments = []

    def openDebitNoteTicket(self, type, name, address, doc, docType, ivaType):
        self._setCustomerData(name, address, doc, docType, ivaType)
        if type == 'A':
            type = 'D'
        else:
            type = 'E'
        self._currentDocument = self.CURRENT_DOC_BILL_TICKET
        self._savedPayments = []
        return self._sendCommand(self.CMD_OPEN_FISCAL_RECEIPT, [type, 'T'])

    def openBillCreditTicket(self, type, name, address, doc, docType, ivaType, reference='NC'):
        self._setCustomerData(name, address, doc, docType, ivaType)
        if type == 'A':
            type = 'R'
        else:
            type = 'S'
        self._currentDocument = self.CURRENT_DOC_CREDIT_BILL_TICKET
        self._savedPayments = []
        self._sendCommand(self.CMD_CREDIT_NOTE_REFERENCE, ['1', reference])
        return self._sendCommand(self.CMD_OPEN_CREDIT_NOTE, [type, 'T'])

    def openRemit(self, name, address, doc, docType, ivaType, copies=1):
        self._setCustomerData(name, address, doc, docType, ivaType)
        self._currentDocument = self.CURRENT_DOC_DNFH
        self._savedPayments = []
        self._copies = copies
        return self._sendCommand(self.CMD_OPEN_DNFH, ['r', 'T'])

    def openReceipt(self, name, address, doc, docType, ivaType, number, copies=1):
        self._setCustomerData(name, address, doc, docType, ivaType)
        self._currentDocument = self.CURRENT_DOC_DNFH
        self._savedPayments = []
        self._copies = copies
        return self._sendCommand(self.CMD_OPEN_DNFH, ['x', 'T', number[:20]])

    def closeDocument(self):
        if self._currentDocument in (self.CURRENT_DOC_TICKET, self.CURRENT_DOC_BILL_TICKET):
            for desc, payment in self._savedPayments:
                r = self._sendCommand(self.CMD_ADD_PAYMENT, [
                 self._formatText(desc, 'paymentDescription'), payment, 'T', '1'])

            del self._savedPayments
            reply = self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT)
            return reply[2]
        if self._currentDocument in (self.CURRENT_DOC_NON_FISCAL,):
            return self._sendCommand(self.CMD_CLOSE_NON_FISCAL_RECEIPT)
        if self._currentDocument in (self.CURRENT_DOC_CREDIT_BILL_TICKET, self.CURRENT_DOC_CREDIT_TICKET):
            reply = self._sendCommand(self.CMD_CLOSE_CREDIT_NOTE)
            return reply[2]
        if self._currentDocument in (self.CURRENT_DOC_DNFH,):
            reply = self._sendCommand(self.CMD_CLOSE_DNFH)
            for copy in range(self._copies - 1):
                self._sendCommand(self.CMD_REPRINT)

            return reply[2]
        raise NotImplementedError

    def cancelDocument(self):
        if not hasattr(self, '_currentDocument'):
            return self.cancelAnyDocument()
        if self._currentDocument in (self.CURRENT_DOC_TICKET, self.CURRENT_DOC_BILL_TICKET,
         self.CURRENT_DOC_CREDIT_BILL_TICKET, self.CURRENT_DOC_CREDIT_TICKET):
            try:
                status = self._sendCommand(self.CMD_ADD_PAYMENT, ['Cancelar', '0.00', 'C', '1'])
            except:
                self.cancelAnyDocument()
                status = []

            return status
        if self._currentDocument in (self.CURRENT_DOC_NON_FISCAL,):
            self.printNonFiscalText('CANCELADO')
            return self.closeDocument()
        if self._currentDocument in (self.CURRENT_DOC_DNFH,):
            self.cancelAnyDocument()
            status = []
            return status
        raise NotImplementedError

    def addItem(self, description, quantity, price, iva, discount=0.0, discountDescription=None, negative=False):
        if type(description) in types.StringTypes:
            description = [
             description]
        if negative:
            sign = 'm'
        else:
            sign = 'M'
        quantityStr = str(float(quantity)).replace(',', '.')
        priceUnit = price
        priceUnitStr = str(priceUnit).replace(',', '.')
        ivaStr = str(float(iva)).replace(',', '.')
        for d in description[:-1]:
            self._sendCommand(self.CMD_PRINT_TEXT_IN_FISCAL, [self._formatText(d, 'fiscalText'), '0'])

        reply = self._sendCommand(self.CMD_PRINT_LINE_ITEM, [
         self._formatText(description[(-1)], 'lineItem'),
         quantityStr, priceUnitStr, ivaStr, sign, '0.0', '1', 'T'])
        if discount:
            discountStr = str(float(discount)).replace(',', '.')
            self._sendCommand(self.CMD_LAST_ITEM_DISCOUNT, [
             self._formatText(discountDescription, 'discountDescription'), discountStr,
             'm', '1', 'T'])
        return reply

    def addPayment(self, description, payment):
        paymentStr = ('%.2f' % round(payment, 2)).replace(',', '.')
        self._savedPayments.append((description, paymentStr))

    def addAdditional(self, description, amount, iva, negative=False):
        u"""Agrega un adicional a la FC.
                                                @param description  Descripción
                                                @param amount       Importe (sin iva en FC A, sino con IVA)
                                                @param iva          Porcentaje de Iva
                                                @param negative True->Descuento, False->Recargo"""
        if negative:
            sign = 'm'
        else:
            sign = 'M'
        priceUnit = amount
        priceUnitStr = str(priceUnit).replace(',', '.')
        reply = self._sendCommand(self.CMD_GENERAL_DISCOUNT, [
         self._formatText(description, 'generalDiscount'), priceUnitStr, sign, '1', 'T'])
        return reply

    def addRemitItem(self, description, quantity):
        quantityStr = str(float(quantity)).replace(',', '.')
        return self._sendCommand(self.CMD_PRINT_EMBARK_ITEM, [
         self._formatText(description, 'embarkItem'), quantityStr, '1'])

    def addReceiptDetail(self, descriptions, amount):
        sign = 'M'
        quantityStr = str(float(1)).replace(',', '.')
        priceUnitStr = str(amount).replace(',', '.')
        ivaStr = str(float(0)).replace(',', '.')
        reply = self._sendCommand(self.CMD_PRINT_LINE_ITEM, [
         'Total', quantityStr, priceUnitStr, ivaStr, sign, '0.0', '1', 'T'])
        for d in descriptions[:9]:
            reply = self._sendCommand(self.CMD_PRINT_RECEIPT_TEXT, [
             self._formatText(d, 'receiptText')])

        return reply

    def openDrawer(self):
        if self.model not in (self.MODEL_320, '615'):
            self._sendCommand(self.CMD_OPEN_DRAWER, [])

    def dailyClose(self, type_):
        reply = self._sendCommand(self.CMD_DAILY_CLOSE, [type_])
        return reply[2:]

    def getLastNumber(self, letter):
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, [], True)
        if len(reply) < 3:
            reply = self._sendCommand(self.CMD_STATUS_REQUEST, [], False)
        if letter == 'A':
            return int(reply[4])
        else:
            return int(reply[2])

    def getLastCreditNoteNumber(self, letter):
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, [], True)
        if len(reply) < 3:
            reply = self._sendCommand(self.CMD_STATUS_REQUEST, [], False)
        if letter == 'A':
            return int(reply[7])
        else:
            return int(reply[6])

    def getLastRemitNumber(self):
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, [], True)
        if len(reply) < 3:
            reply = self._sendCommand(self.CMD_STATUS_REQUEST, [], False)
        return int(reply[8])

    def cancelAnyDocument(self):
        try:
            self._sendCommand(self.CMD_CANCEL_ANY_DOCUMENT)
        except:
            pass

        try:
            self._sendCommand(self.CMD_ADD_PAYMENT, ['Cancelar', '0.00', 'C', '1'])
            return True
        except:
            pass

        try:
            self._sendCommand(self.CMD_CLOSE_NON_FISCAL_RECEIPT)
            return True
        except:
            pass

        try:
            logging.getLogger().info('Cerrando comprobante con CLOSE')
            self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT)
            return True
        except:
            pass

        return False

    def close(self):
        self.driver.close()
        self.driver = None
        return

    def getStatus(self):
        return self._sendCommand(self.CMD_STATUS_REQUEST, [], True)