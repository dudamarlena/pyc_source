# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/reservedinstance.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 13047 bytes
from boto.resultset import ResultSet
from boto.ec2.ec2object import EC2Object
from boto.utils import parse_ts

class ReservedInstancesOffering(EC2Object):

    def __init__(self, connection=None, id=None, instance_type=None, availability_zone=None, duration=None, fixed_price=None, usage_price=None, description=None, instance_tenancy=None, currency_code=None, offering_type=None, recurring_charges=None, pricing_details=None):
        super(ReservedInstancesOffering, self).__init__(connection)
        self.id = id
        self.instance_type = instance_type
        self.availability_zone = availability_zone
        self.duration = duration
        self.fixed_price = fixed_price
        self.usage_price = usage_price
        self.description = description
        self.instance_tenancy = instance_tenancy
        self.currency_code = currency_code
        self.offering_type = offering_type
        self.recurring_charges = recurring_charges
        self.pricing_details = pricing_details

    def __repr__(self):
        return 'ReservedInstanceOffering:%s' % self.id

    def startElement(self, name, attrs, connection):
        if name == 'recurringCharges':
            self.recurring_charges = ResultSet([('item', RecurringCharge)])
            return self.recurring_charges
        if name == 'pricingDetailsSet':
            self.pricing_details = ResultSet([('item', PricingDetail)])
            return self.pricing_details

    def endElement(self, name, value, connection):
        if name == 'reservedInstancesOfferingId':
            self.id = value
        else:
            if name == 'instanceType':
                self.instance_type = value
            else:
                if name == 'availabilityZone':
                    self.availability_zone = value
                else:
                    if name == 'duration':
                        self.duration = int(value)
                    else:
                        if name == 'fixedPrice':
                            self.fixed_price = value
                        else:
                            if name == 'usagePrice':
                                self.usage_price = value
                            else:
                                if name == 'productDescription':
                                    self.description = value
                                else:
                                    if name == 'instanceTenancy':
                                        self.instance_tenancy = value
                                    else:
                                        if name == 'currencyCode':
                                            self.currency_code = value
                                        else:
                                            if name == 'offeringType':
                                                self.offering_type = value
                                            elif name == 'marketplace':
                                                self.marketplace = True if value == 'true' else False

    def describe(self):
        print('ID=%s' % self.id)
        print('\tInstance Type=%s' % self.instance_type)
        print('\tZone=%s' % self.availability_zone)
        print('\tDuration=%s' % self.duration)
        print('\tFixed Price=%s' % self.fixed_price)
        print('\tUsage Price=%s' % self.usage_price)
        print('\tDescription=%s' % self.description)

    def purchase(self, instance_count=1, dry_run=False):
        return self.connection.purchase_reserved_instance_offering(self.id, instance_count, dry_run=dry_run)


class RecurringCharge(object):

    def __init__(self, connection=None, frequency=None, amount=None):
        self.frequency = frequency
        self.amount = amount

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        setattr(self, name, value)


class PricingDetail(object):

    def __init__(self, connection=None, price=None, count=None):
        self.price = price
        self.count = count

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        setattr(self, name, value)


class ReservedInstance(ReservedInstancesOffering):

    def __init__(self, connection=None, id=None, instance_type=None, availability_zone=None, duration=None, fixed_price=None, usage_price=None, description=None, instance_count=None, state=None):
        super(ReservedInstance, self).__init__(connection, id, instance_type, availability_zone, duration, fixed_price, usage_price, description)
        self.instance_count = instance_count
        self.state = state
        self.start = None
        self.end = None

    def __repr__(self):
        return 'ReservedInstance:%s' % self.id

    def endElement(self, name, value, connection):
        if name == 'reservedInstancesId':
            self.id = value
        if name == 'instanceCount':
            self.instance_count = int(value)
        else:
            if name == 'state':
                self.state = value
            else:
                if name == 'start':
                    self.start = value
                else:
                    if name == 'end':
                        self.end = value
                    else:
                        super(ReservedInstance, self).endElement(name, value, connection)


class ReservedInstanceListing(EC2Object):

    def __init__(self, connection=None, listing_id=None, id=None, create_date=None, update_date=None, status=None, status_message=None, client_token=None):
        self.connection = connection
        self.listing_id = listing_id
        self.id = id
        self.create_date = create_date
        self.update_date = update_date
        self.status = status
        self.status_message = status_message
        self.client_token = client_token

    def startElement(self, name, attrs, connection):
        if name == 'instanceCounts':
            self.instance_counts = ResultSet([('item', InstanceCount)])
            return self.instance_counts
        if name == 'priceSchedules':
            self.price_schedules = ResultSet([('item', PriceSchedule)])
            return self.price_schedules

    def endElement(self, name, value, connection):
        if name == 'reservedInstancesListingId':
            self.listing_id = value
        else:
            if name == 'reservedInstancesId':
                self.id = value
            else:
                if name == 'createDate':
                    self.create_date = value
                else:
                    if name == 'updateDate':
                        self.update_date = value
                    else:
                        if name == 'status':
                            self.status = value
                        else:
                            if name == 'statusMessage':
                                self.status_message = value
                            else:
                                setattr(self, name, value)


class InstanceCount(object):

    def __init__(self, connection=None, state=None, instance_count=None):
        self.state = state
        self.instance_count = instance_count

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'state':
            self.state = value
        else:
            if name == 'instanceCount':
                self.instance_count = int(value)
            else:
                setattr(self, name, value)


class PriceSchedule(object):

    def __init__(self, connection=None, term=None, price=None, currency_code=None, active=None):
        self.connection = connection
        self.term = term
        self.price = price
        self.currency_code = currency_code
        self.active = active

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'term':
            self.term = int(value)
        else:
            if name == 'price':
                self.price = value
            else:
                if name == 'currencyCode':
                    self.currency_code = value
                else:
                    if name == 'active':
                        self.active = True if value == 'true' else False
                    else:
                        setattr(self, name, value)


class ReservedInstancesConfiguration(object):

    def __init__(self, connection=None, availability_zone=None, platform=None, instance_count=None, instance_type=None):
        self.connection = connection
        self.availability_zone = availability_zone
        self.platform = platform
        self.instance_count = instance_count
        self.instance_type = instance_type

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'availabilityZone':
            self.availability_zone = value
        else:
            if name == 'platform':
                self.platform = value
            else:
                if name == 'instanceCount':
                    self.instance_count = int(value)
                else:
                    if name == 'instanceType':
                        self.instance_type = value
                    else:
                        setattr(self, name, value)


class ModifyReservedInstancesResult(object):

    def __init__(self, connection=None, modification_id=None):
        self.connection = connection
        self.modification_id = modification_id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'reservedInstancesModificationId':
            self.modification_id = value
        else:
            setattr(self, name, value)


class ModificationResult(object):

    def __init__(self, connection=None, modification_id=None, availability_zone=None, platform=None, instance_count=None, instance_type=None):
        self.connection = connection
        self.modification_id = modification_id
        self.availability_zone = availability_zone
        self.platform = platform
        self.instance_count = instance_count
        self.instance_type = instance_type

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'reservedInstancesModificationId':
            self.modification_id = value
        else:
            if name == 'availabilityZone':
                self.availability_zone = value
            else:
                if name == 'platform':
                    self.platform = value
                else:
                    if name == 'instanceCount':
                        self.instance_count = int(value)
                    else:
                        if name == 'instanceType':
                            self.instance_type = value
                        else:
                            setattr(self, name, value)


class ReservedInstancesModification(object):

    def __init__(self, connection=None, modification_id=None, reserved_instances=None, modification_results=None, create_date=None, update_date=None, effective_date=None, status=None, status_message=None, client_token=None):
        self.connection = connection
        self.modification_id = modification_id
        self.reserved_instances = reserved_instances
        self.modification_results = modification_results
        self.create_date = create_date
        self.update_date = update_date
        self.effective_date = effective_date
        self.status = status
        self.status_message = status_message
        self.client_token = client_token

    def startElement(self, name, attrs, connection):
        if name == 'reservedInstancesSet':
            self.reserved_instances = ResultSet([
             (
              'item', ReservedInstance)])
            return self.reserved_instances
        if name == 'modificationResultSet':
            self.modification_results = ResultSet([
             (
              'item', ModificationResult)])
            return self.modification_results

    def endElement(self, name, value, connection):
        if name == 'reservedInstancesModificationId':
            self.modification_id = value
        else:
            if name == 'createDate':
                self.create_date = parse_ts(value)
            else:
                if name == 'updateDate':
                    self.update_date = parse_ts(value)
                else:
                    if name == 'effectiveDate':
                        self.effective_date = parse_ts(value)
                    else:
                        if name == 'status':
                            self.status = value
                        else:
                            if name == 'statusMessage':
                                self.status_message = value
                            else:
                                if name == 'clientToken':
                                    self.client_token = value
                                else:
                                    setattr(self, name, value)