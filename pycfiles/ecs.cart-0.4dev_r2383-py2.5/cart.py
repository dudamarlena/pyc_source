# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ecs/cart/cart.py
# Compiled at: 2009-01-13 06:18:21
"""Cart module for ecscart"""
from price import Price
from rules.rules_config import RulesInit

class Cart(object):
    """Cart object to manage an user caddy"""
    products = {}
    cart_reference = None
    validation_statut = None
    _update = False

    def __init__(self, reference=None, rules_conf=None):
        """Instantiate the cart"""
        self.rules = RulesInit(conf_file=rules_conf)
        if reference is not None:
            self.cart_reference = reference
            self.name = self.cart_reference
            self.validation_statut = False
            self.products = {}
            self.cart = {}
            self.logistic = {}
        else:
            self.reference_error(reference)
        return

    def reference_error(self, reference):
        """Error while a a reference is uncorrect"""
        raise ValueError('Invalid reference %s' % str(reference))

    def add_product(self, reference=None, price=0.0, vat=0.0, quantity=1.0, included_tax=True, weight=0):
        """Add the product into the cart"""
        if reference is not None:
            self._update = False
            if reference not in self.products:
                price = float(price)
                if included_tax:
                    price = Price(price, vat=vat)
                else:
                    price = Price(without_tax=price, vat=vat)
                self.products[reference] = {}
                self.products[reference]['price'] = price()
                self.products[reference]['weight'] = weight
                self.products[reference]['quantity'] = float(quantity)
            else:
                self.products[reference]['quantity'] += float(quantity)
        else:
            self.reference_error(reference)
        return

    def del_all_product(self, reference=None):
        """Delete a product into the cart"""
        if reference in self.products:
            self._update = False
            del self.products[reference]

    def del_product(self, reference=None, quantity=1):
        """Delete a product into the cart"""
        if reference in self.products:
            self._update = False
            self.products[reference]['quantity'] -= quantity
            if self.products[reference]['quantity'] < 1:
                self.del_all_product(reference=reference)

    def validation(self, flag=True):
        """Set the state of the caddy"""
        self.validation_statut = flag

    def remove(self):
        """User method to delete the cart from the persistence"""
        self._update = False
        self.products = {}

    def add_reduction(self, value, percentage=False, ref=None, number=None):
        if ref is None:
            self._update = False
            reduction = {'value': value, 'percentage': percentage}
            if 'reductions' not in self.cart:
                self.cart['reductions'] = [
                 reduction]
            else:
                self.cart['reductions'].append(reduction)
        elif ref in self.products:
            self._update = False
            product = self.products[ref]
            reduction = {'value': value, 'percentage': percentage}
            if 'reductions' not in product:
                product['reductions'] = [
                 reduction]
            else:
                product['reductions'].append(reduction)
        return

    def set_quantity(self, reference, quantity=0):
        """Change the quantity of a product in the cart"""
        if reference in self.products:
            self._update = False
            if quantity == 0:
                self.del_all_product(reference)
            else:
                quantity = int(quantity)
                self.products[reference]['quantity'] = float(quantity)
        else:
            self.reference_error(reference)

    def get_product_property(self, reference, property):
        """Return the quantity of a product"""
        if reference in self.products:
            return self.products[reference].get(property)
        else:
            self.reference_error(reference)

    def update(self):
        self.rules.amount_chain(self)
        self._update = True

    def get_cart_amount(self):
        """Return the amount of the caddy"""
        if not self._update:
            self.update()
        return round(self.cart['amount'], 2)

    def get_cart_detail_amount(self):
        if not self._update:
            self.update()
        return self.cart

    def update_country_shipping(self, iso):
        self._update = False
        self.logistic['country_iso'] = iso