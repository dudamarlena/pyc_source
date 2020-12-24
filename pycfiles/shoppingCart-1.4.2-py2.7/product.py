# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/shoppingCart/tests/product.py
# Compiled at: 2015-08-10 04:44:00


class Option(object):
    """
    Option Object.
    """

    def __init__(self, id, name, code=None, values=[]):
        """
        :param id: Unique Id.
        :param name: Option Name.
        :param code: Option Code.
        :param values: Option Values.
        """
        self.id = id
        self.name = name
        self.code = code
        self.values = values

    def add_value(self, *values):
        self.values.extend(values)


class OptionValue(object):
    """
    OptionValue Object.
    """

    def __init__(self, id, name, code=None, price=0.0):
        """
        :param id: Unique Id.
        :param name: Option Value Name.
        :param code: Option Value Code.
        :param price: Option Value Price.
        """
        self.id = id
        self.name = name
        self.code = code
        self.price = price


class Product(object):
    """
    Product Object.
    """

    def __init__(self, id, name, code, price, options=[]):
        """
        :param id: Unique Id.
        :param name: Product Name.
        :param code: Prodcuct Code.
        :param price: Real Price of Product.
        """
        self.id = id
        self.code = code
        self.price = price
        self.name = name
        self.options = options