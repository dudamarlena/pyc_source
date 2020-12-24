# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\db\models.py
# Compiled at: 2013-02-02 00:44:14
"""This module contains the data-models used in the rest of the software

Considering the MVC model, is NOT nice to import this module DIRECTLY to a GUI-related code. (or the class into gui code)
It should be imported in a controller. Using _instances_ of objects from this module in code from the GUI is ok (and adviced).
(or using constants from gui code)
"""
from __future__ import absolute_import, unicode_literals, print_function
import datetime, decimal, sha
decimal.getcontext().prec = 4
import persistent as _per, banta.utils
LICENSE_FREE = 0
LICENSE_BASIC = 1
LICENSE_POWER = 2
LICENSE_ADVANCED = 3
LICENSES_ALL = (LICENSE_FREE, LICENSE_BASIC, LICENSE_POWER, LICENSE_ADVANCED)
LICENSES_NOT_FREE = (LICENSE_BASIC, LICENSE_POWER, LICENSE_ADVANCED)
LICENSES_NOT_BASIC = (LICENSE_POWER, LICENSE_ADVANCED)
TAX_MAX = 0.21
TAX_REDUCED = 0.105

class Product(_per.Persistent):
    """Each of the product in the store.
        It can have stock, or not. It can be available or not.
        It just store the properties for each product (like a 'class' for real products)
        """
    name = b''
    code = b''
    external_code = b''
    price = 0.0
    buy_price = 0.0
    ib_type = 0
    prod_type = 0
    stock = 0
    pack_units = 1
    tax_type = None
    provider = None
    category = None
    thumb = None
    description = b''
    IB_NOT_EXEMPT = 0
    IB_EXEMPT = 1
    IB_NAMES = ('Exento', 'No Exento')

    def __init__(self, code, name=b'', price=0.0, stock=0, tax_type=None):
        _per.Persistent.__init__(self)
        self.code = code
        self.setName(name)
        self.price = price
        self.stock = stock
        self.tax_type = tax_type

    def IBStr(self):
        return self.IB_NAMES[self.ib_type]

    def __str__(self):
        return b'[%s] $%s %s' % (self.code, self.price, self.name)

    def setName(self, name):
        self.name = banta.utils.printable(name)


class Item(_per.Persistent):
    """Represents an item in a bill.
        it is related to a product, BUT for historical reasons (ask nande)
        the product data needed to form a bill, must be duplicated and stored SEPARATEDLY"""
    product = None
    tax_type = None
    base_price = 0.0
    unit_price = 0.0
    price = 0.0
    net_price = 0.0
    quantity = 1
    tax = TAX_MAX
    tax_total = 0.0
    description = b''
    reducible = False
    markup = 0.0
    client_exempt = False

    def __init__(self, product=None, quant=1, markup=0.0, client_exempt=False):
        _per.Persistent.__init__(self)
        self.markup = markup
        self.client_exempt = client_exempt
        if product:
            self.setProduct(product)
        self.setQuantity(quant)

    def setProduct(self, product):
        self.product = product
        self.unit_price = self.base_price = product.price
        self.description = product.name
        self.tax_type = product.tax_type

    def setQuantity(self, quant):
        self.quantity = quant

    def calculateTax(self):
        """Calculates the tax for this item
                it depends on :
                sets self.tax for the corresponding tax for this item
                """
        self.tax = 0.0
        if self.tax_type:
            self.tax = self.tax_type.tax

    def calculate(self):
        """Calculates the total
                and other values.
                self.price is the total price of the item (including tax)
                self.tax_total is the total ammount of tax in the price (not a percentaje)
                self.net_price is the total price without tax
                """
        self.calculateTax()
        self.unit_price = round(self.base_price, 4) * (1 + self.markup)
        self.price = self.unit_price * self.quantity
        if self.tax > 0.0:
            self.net_price = round(self.price / (1 + self.tax), 4)
            self.tax_total = self.price - self.net_price
        else:
            self.net_price = self.price
            self.tax_total = 0.0
        return self.price


class TypePay(_per.Persistent):
    name = b''
    markup = 0.0

    def __init__(self, name, markup=0.0):
        _per.Persistent.__init__(self)
        self.name = name
        self.markup = markup

    def __str__(self):
        return b'%s - %s%%' % (self.name, self.markup * 100)


class Client(_per.Persistent):
    """Class for the Clients"""
    DOC_CUIT = 0
    DOC_LIBRETA_ENROLAMIENTO = 1
    DOC_LIBRETA_CIVICA = 2
    DOC_DNI = 3
    DOC_PASAPORTE = 4
    DOC_CEDULA = 5
    DOC_SIN_CALIFICADOR = 6
    DOC_NAMES = ('CUIT', 'Libreta de Enrolamiento', 'Libreta Cívica', 'DNI', 'Pasaporte',
                 'Cédula', 'Sin Calificador')
    TAX_CONSUMIDOR_FINAL = 0
    TAX_RESPONSABLE_INSCRIPTO = 1
    TAX_RESPONSABLE_NO_INSCRIPTO = 2
    TAX_EXENTO = 3
    TAX_NO_RESPONSABLE = 4
    TAX_RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO = 5
    TAX_RESPONSABLE_MONOTRIBUTO = 6
    TAX_MONOTRIBUTISTA_SOCIAL = 7
    TAX_PEQUENIO_CONTRIBUYENTE_EVENTUAL = 8
    TAX_PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL = 9
    TAX_NO_CATEGORIZADO = 10
    TAX_NAMES = ('Consumidor Final', 'Responsable Inscripto', 'Responsable no Inscripto',
                 'Exento', 'No Responsable', 'Responsable No Inscripto Bienes de Uso',
                 'Monotributista', 'Monotributista Social', 'Pequeño Contribuyente Eventual',
                 'Pequeño Contribuyente Eventual Social', 'No categorizado')
    IB_UNREGISTERED = 0
    IB_REGISTERED = 1
    IB_EXEMPT = 2
    IB_NAMES = ('No registrado', 'Registrado', 'Exento')
    idn = -1
    name = b''
    code = b''
    address = b''
    tax_type = 0
    doc_type = 0
    ib_type = 0
    balance = 0.0

    def __init__(self, code, name=b'', address=b'', doc_type=DOC_SIN_CALIFICADOR, tax_type=TAX_CONSUMIDOR_FINAL, ib_type=IB_UNREGISTERED, save=True):
        """Creates a new instance of a client, it uses an internal id, so it's persisted in the db automatically"""
        _per.Persistent.__init__(self)
        self.code = code
        self.setName(name)
        self.setAddress(address)
        self.address = address
        self.tax_type = tax_type
        self.doc_type = doc_type
        self.ib_type = ib_type
        if save:
            self.save()

    def setName(self, name):
        self.name = banta.utils.printable(name)

    def setAddress(self, address):
        self.address = banta.utils.printable(address)

    def getPossibleBillTypes(self):
        if self.tax_type == self.TAX_RESPONSABLE_INSCRIPTO:
            return (Bill.TYPE_A, Bill.TYPE_NOTA_CRED_A, Bill.TYPE_NOTA_DEB_A)
        else:
            if self.tax_type in (self.TAX_RESPONSABLE_MONOTRIBUTO, self.TAX_MONOTRIBUTISTA_SOCIAL):
                return (Bill.TYPE_B, Bill.TYPE_NOTA_CRED_B, Bill.TYPE_NOTA_DEB_B)
            if self.tax_type in (self.TAX_CONSUMIDOR_FINAL, self.TAX_NO_CATEGORIZADO, self.TAX_NO_RESPONSABLE, self.TAX_EXENTO):
                return (Bill.TYPE_B, Bill.TYPE_C, Bill.TYPE_NOTA_CRED_B, Bill.TYPE_NOTA_DEB_B)
            return (Bill.TYPE_B, Bill.TYPE_A, Bill.TYPE_C, Bill.TYPE_NOTA_CRED_A, Bill.TYPE_NOTA_CRED_B, Bill.TYPE_NOTA_DEB_A)

    def save(self):
        """Saves a client into the database and returns an id.
                selff.idn holds the key for the inserted client
                """
        if self.idn > -1:
            return
        import banta.db
        if len(banta.db.DB.clients):
            self.idn = banta.db.DB.clients.maxKey() + 1
        else:
            self.idn = 0
        banta.db.DB.clients[self.idn] = self
        return self.idn

    def taxStr(self):
        return self.TAX_NAMES[self.tax_type]

    def docStr(self):
        return self.DOC_NAMES[self.doc_type]

    def IBStr(self):
        return self.IB_NAMES[self.ib_type]

    def __str__(self):
        return (b'\n').join((self.code, self.name, self.address, self.taxStr()))


class Bill(_per.Persistent):
    """Bill. Factura. Ticket.
        """
    TYPE_A = 0
    TYPE_B = 1
    TYPE_C = 2
    TYPE_NOTA_CRED_A = 3
    TYPE_NOTA_CRED_B = 4
    TYPE_NOTA_DEB_A = 5
    TYPE_NOTA_DEB_B = 6
    TYPE_NAMES = ('A', 'B', 'C', 'Nota de Crédito A', 'Nota de Crédito B', 'Nota de Débito A',
                  'Nota de Débito B')
    number = 0
    date = 0
    markup = 0.0
    tax = 0.0
    total = 0.0
    subtotal = 0.0
    btype = 0
    ptype = None
    client = None
    user = None
    printed = False
    closed = False
    time = 0

    def __init__(self):
        super(Bill, self).__init__()
        self.date = datetime.datetime.now()
        self.items = _per.list.PersistentList()

    def setTypePay(self, tpay):
        self.ptype = tpay
        self.setMarkup(tpay.markup)

    def setTypeBill(self, tb):
        self.btype = tb

    def setClient(self, client):
        self.client = client

    def setMarkup(self, markup):
        """Sets the markup for the bill, which affects all the item.
                Neither the bill nor the items are recalculated"""
        self.markup = markup
        for i in self.items:
            i.markup = markup

    def calculate(self):
        """Recalculate the values for the bill, and sets the values in each variable.
                It can be slow so call it only if it has changed"""
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        for i in self.items:
            i.calculate()
            self.total += i.price
            self.tax += i.tax_total

        self.subtotal = self.total - self.tax

    def copy(self):
        copy = Bill()
        copy.btype = self.btype
        copy.client = self.client
        copy.markup = self.markup
        copy.ptype = self.ptype
        copy.user = self.user
        copy.ptype = self.ptype
        copy.subtotal = self.subtotal
        copy.tax = self.tax
        for i in self.items:
            item = Item()
            item.base_price = i.base_price
            item.client_exempt = i.client_exempt
            item.description = i.description
            item.markup = i.markup
            item.net_price = i.net_price
            item.price = i.price
            item.product = i.product
            item.quantity = i.quantity
            item.reducible = i.reducible
            item.tax_type = i.tax_type
            item.tax = i.tax
            item.tax_total = i.tax_total
            item.unit_price = i.unit_price
            copy.items.append(item)

        return copy

    def close(self):
        """Closes the bill.
                ADDS THE BILL TO THE DATABASE
                Reduces the stock, sets the bill date
                and add it to the bill list
                if the bill is already closed, it does nothing.
                Notice this is pretty destructive and has side-effects, so be careful when using it
                """
        if self.closed:
            return False
        import banta.db
        self.closed = True
        self.date = datetime.datetime.now()
        self.time = banta.utils.dateTimeToInt(self.date)
        if self.btype in (self.TYPE_NOTA_CRED_A, self.TYPE_NOTA_CRED_B):
            sign = 1
        else:
            sign = -1
        for item in self.items:
            prod = item.product
            prod.stock += sign * item.quantity

        while self.time in banta.db.DB.bills:
            self.time += 1

        banta.db.DB.bills[self.time] = self
        return True

    def addItem(self, item):
        """Adds an item to the bill.
                Returns True if ok.
                If the item is already on the bill, or there's an error it returns False."""
        if self.printed:
            return False
        if item in self.items:
            return False
        self.items.append(item)
        return True

    def delItem(self, i):
        del self.items[i]

    def strPrinted(self):
        return self.printed and b'Impresa' or b'Presupuesto'


class Printer(_per.Persistent):
    BRAND_NAMES = ('Hasar', 'Epson')
    BRAND_HASAR = 0
    BRAND_EPSON = 1
    SPEEDS = (2400, 4800, 9600, 19200, 38400, 57600, 115200)
    name = b'Hasar P/320F'
    brand = BRAND_HASAR
    device = b'COM1'
    speed = 2
    model = 3


class Provider(_per.Persistent):
    name = b''
    address = b''
    code = b''
    phone = b''
    mail = b''

    def __init__(self, code, name=b'', address=b'', phone=b'', mail=b''):
        _per.Persistent.__init__(self)
        self.code = code
        self.name = name
        self.address = address
        self.phone = phone
        self.mail = mail


class User(_per.Persistent):
    name = b''
    password = b''

    def __init__(self, name=b''):
        _per.Persistent.__init__(self)
        self.name = name

    def setPassword(self, pwd):
        self.password = sha.new(pwd).hexdigest()


class Category(_per.Persistent):
    name = b''

    def __init__(self, name=b''):
        _per.Persistent.__init__(self)
        self.name = name


class Move(_per.Persistent):
    date = 0
    time = 0
    product = None
    diff = 0
    reason = b''

    def __init__(self, product, reason, diff, root=None):
        """
        Represents a movement in stock
        stores the product changed, the reason, and the diff in quantity (relative number)
        Instantiating a move adds it on the db, that's important because when you add it, it depends on the time
         so it could break several stuff if its saved 2 times
         If the object is created from another thread, the parameter "root" is needed, which is the root dictionary for
         the current thread.
         (still you have to commit)
         """
        _per.Persistent.__init__(self)
        self.reason = reason
        self.product = product
        self.diff = diff
        self.date = datetime.datetime.now()
        self.time = banta.utils.dateTimeToInt(self.date)
        if not root:
            root = banta.db.DB.root
        moves = root[b'moves']
        while self.time in moves:
            self.time += 1

        moves[self.time] = self


class Buy(_per.Persistent):
    date = 0
    time = 0
    product = None
    quantity = 0
    total = 0.0

    def __init__(self, product, quantity):
        """
        Represents a movement in stock
        stores the product changed, the reason, and the diff in quantity (relative number)
        Instantiating a move adds it on the db, that's important because when you add it, it depends on the time
         so it could break several stuff if its saved 2 times
         (still you have to commit)"""
        _per.Persistent.__init__(self)
        import banta.db
        self.product = product
        self.quantity = quantity
        self.total = self.product.buy_price * quantity
        self.date = datetime.datetime.now()
        self.time = banta.utils.dateTimeToInt(self.date)
        while self.time in banta.db.DB.buys:
            self.time += 1

        banta.db.DB.buys[self.time] = self
        m = Move(product, b'Compra', quantity)


class Limit(_per.Persistent):
    """Holds a limit-rule to be used for the current month"""
    product = None
    quantity = 0
    amount = 0


class TypeTax(_per.Persistent):
    name = b''
    tax = 0.0

    def __init__(self, name=b'', tax=0.0):
        _per.Persistent.__init__(self)
        self.name = name
        self.tax = tax

    def __str__(self):
        return (b'{:} ({:.2%})').format(self.name, self.tax)