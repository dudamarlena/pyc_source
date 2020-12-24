# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/demos/customer_service.py
# Compiled at: 2019-03-02 23:45:23
# Size of source mod 2**32: 5017 bytes
import tornado.ioloop, pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete

class Customer(object):
    id_customer = int
    name_customer = str
    address_customer = str

    def __init__(self, id_customer=0, name_customer=None, address_customer=None):
        self.id_customer = id_customer
        self.name_customer = name_customer
        self.address_customer = address_customer

    def setId_Customer(self, id_customer):
        self.id_customer = id_customer

    def setName_Customer(self, name_customer):
        self.name_customer = name_customer

    def setAddress_Customer(self, address_customer):
        self.address_customer = address_customer

    def getId_Customer(self):
        return self.id_customer

    def getName_Customer(self):
        return self.name_customer

    def getAddress_Customer(self):
        return self.address_customer


class CustomerDataBase(object):
    customerDB = dict()
    id_seq = 1

    def insert(self, name_customer, address_customer):
        sequence = self.id_seq
        customer = Customer(sequence, str(name_customer), str(address_customer))
        self.customerDB[sequence] = customer
        self.id_seq += 1
        return sequence

    def update(self, id_customer, name_customer, address_customer):
        if self.exists(id_customer):
            customer = self.customerDB[id_customer]
            customer.setName_Customer(str(name_customer))
            customer.setAddress_Customer(str(address_customer))
            self.customerDB[id_customer] = customer
            return True
        return False

    def delete(self, id_customer):
        if self.exists(id_customer):
            del self.customerDB[id_customer]
            return True
        return False

    def find(self, id_customer):
        if self.exists(id_customer):
            return self.customerDB[id_customer]
        return

    def exists(self, id_customer):
        if id_customer in self.customerDB:
            return True
        return False

    def all(self):
        return self.customerDB


class CustomerResource(pyrestful.rest.RestHandler):

    def initialize(self, database):
        self.database = database

    @get(_path='/customer', _produces=(mediatypes.APPLICATION_JSON))
    def getListCustomer(self):
        customers = self.database.all()
        response = dict()
        for k in customers.keys():
            cust = dict()
            cust['id_customer'] = customers[k].getId_Customer()
            cust['name_customer'] = customers[k].getName_Customer()
            cust['address_customer'] = customers[k].getAddress_Customer()
            response[k] = {k: cust}

        return response

    @get(_path='/customer/{id_customer}', _types=[int], _produces=(mediatypes.APPLICATION_JSON))
    def getCustomer(self, id_customer):
        if not self.database.exists(id_customer):
            self.gen_http_error(404, 'Error 404 : do not exists the customer : %d' % id_customer)
            return
        customer = self.database.find(id_customer)
        response = dict()
        response['id_customer'] = customer.getId_Customer()
        response['name_customer'] = customer.getName_Customer()
        response['address_customer'] = customer.getAddress_Customer()
        print(response)
        return response

    @post(_path='/customer', _types=[str, str], _produces=(mediatypes.APPLICATION_JSON))
    def createCustomer(self, name_customer, address_customer):
        id_customer = self.database.insert(name_customer, address_customer)
        return {'created_customer_id': id_customer}

    @put(_path='/customer/{id_customer}', _types=[int, str, str], _produces=(mediatypes.APPLICATION_JSON))
    def updateCustomer(self, id_customer, name_customer, address_customer):
        if not self.database.exists(id_customer):
            self.gen_http_error(404, 'Error 404 : do not exists the customer : %d' % id_customer)
            return
        updated = self.database.update(id_customer, name_customer, address_customer)
        return {'updated_customer_id':id_customer, 
         'success':updated}

    @delete(_path='/customer/{id_customer}', _types=[int], _produces=(mediatypes.APPLICATION_JSON))
    def deleteCustomer(self, id_customer):
        if not self.database.exists(id_customer):
            self.gen_http_error(404, 'Error 404 : do not exists the customer : %d' % id_customer)
            return
        deleted = self.database.delete(id_customer)
        return {'delete_customer_id':id_customer, 
         'success':deleted}


if __name__ == '__main__':
    try:
        print('Start the service')
        database = CustomerDataBase()
        app = pyrestful.rest.RestService([CustomerResource], dict(database=database))
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStop the service')