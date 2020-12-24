# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/object.py
# Compiled at: 2009-08-25 18:19:45
import sys

class ConfigKlass:
    """
    A ConfigObject is an abstract representation of something
    that has configuration. We can perform common configuration
    operations on ConfigObjects, based on what their configuration
    is.
    """

    def __init__(self, name):
        self.name = name
        self.attrib = {}
        self._can_contain = {}
        self._can_connect = {}

    def attribute(self, name, attrib_type):
        """
        Add an attribute to this config object
        """
        self.attrib[name] = Attribute(name, attrib_type)

    def can_contain(self, klassname, min=0, max=sys.maxint):
        """
        Add a containment relationship to the list
        """
        r = Contains(klassname, min, max)
        self._can_contain[klassname] = r

    def can_connect_to(self, klassname, min=0, max=sys.maxint):
        r = ConnectsTo(klassname, min, max)
        self._can_connect[klassname] = r

    def __str__(self):
        retstr = [
         'ConfigKlass: %s' % self.name]
        retstr += ['  Attributes:'] + [ '    %s' % a for a in self.attrib.values() ]
        retstr += ['  Contains:'] + [ '    %s' % a for a in self._can_contain.values() ]
        retstr += ['  Connects to:'] + [ '    %s' % a for a in self._can_connect.values() ]
        return ('\n').join(retstr)


class Attribute:
    """
    An Attribute is a description of a single attribute that
    a configuration object can have.

    Attributes are stored in a database in some method. This
    could be, in postgres, a set of tables, one for each type,
    so the table would be something like:

    attrib_int ( object_id FOREIGN_KEY, name VARCHAR, value INTEGER )
    attrib_ipaddr ( object_id FOREIGN_KEY, name VARCHAR, value IPADDR )

    which would key into the main object entity table:

    objects ( object_id PRIMARY_KEY, klass VARCHAR UNIQUE )

    Then, to get a particular object's information:

    select * from objects LEFT JOIN attrib_int,attrib_varchar,attrib_ipaddr... etc for all tables
    joining on the object_id

    To track changes to configuration values over time, you would want to add a
    timestamp TIMESTAMP column to each attribute table. You could then track how a particular
    object's attributes change configuration over time.
    
    """

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return 'Attribute: %s [%s]' % (self.name, self.type)


class RelationshipType:
    """
    Objects are related to one another by a Relationship, which
    will be of a particular RelationshipType that constrains
    the nature of the relationship.

    Stored in a database thus:

    relationships = ( object_id FOREIGN_KEY, relation_type, related_obj
    """

    def __init__(self, klass, min, max):
        self.related_klass = klass
        self.related_min = min
        self.related_max = max

    def __str__(self):
        return '<%s: %s [min: %d, max: %d]>' % (self.__class__.__name__, self.related_klass, self.related_min, self.related_max)


class Contains(RelationshipType):
    """
    The contains relationship says that an object contains
    some number of other objects.
    """
    pass


class ConnectsTo(RelationshipType):
    """
    An object connects to another by some mechanism.
    """
    pass


class ConfigObject:
    """
    A ConfigObject is a specific instance of a ConfigKlass.

    The ConfigKlass governs the possible configuration parameters
    of this object.
    """

    def __init__(self, klass):
        self.klass = klass
        self.attrib = {}
        self.contained = []
        self.contained_by = []
        self.connected = []

    def __setitem__(self, name, value):
        """
        Set attribute named 'name' to value.
        Performs various constraint checks on the
        attribute first.
        """
        try:
            self.klass.attrib[name]
        except KeyError, e:
            raise KeyError("ConfigObject klass type '%s' does not support attribute: %s" % (self.klass.name, e))

        self.attrib[name] = value

    def __getitem__(self, name):
        """
        Try fetching an attribute value
        """
        try:
            return self.attrib[name]
        except KeyError:
            if not self.klass.attrib.has_key(name):
                raise KeyError('Attribute %s is not available on objects of type %s' % (name, self.klass.name))

    def get_config_klass(self):
        """
        Return my ConfigKlass
        """
        return self.klass

    def contains(self, obj):
        """
        Used to actually add an object to this container.
        @param obj: The object to be contained.

        Checks to ensure that the object's klassname exists
        in this container's _can_contain constraint.
        """
        objklassname = obj.get_config_klass().name
        try:
            r = self.klass._can_contain[objklassname]
            contained = [ x for x in self.contained if x.get_config_klass().name == objklassname ]
            if len(contained) >= r.related_max:
                raise ValueError("%s cannot contain more than %d objects of type '%s'" % (self, r.related_max, obj.get_config_klass()))
            else:
                self.contained.append(obj)
        except KeyError:
            raise ValueError("'%s' cannot contain objects of type '%s'" % (self.get_config_klass().name, objklassname))

    def connects_to(self, obj, bidirectional=True):
        """
        Used to connect an object to this object.

        @param obj: The object to be connected.
        @param bidirectional: Also connects the other object to this one.
        Checks to ensure that the object's klassname exists in
        this object's _can_connect_to constraint.
        """
        objklassname = obj.get_config_klass().name
        try:
            r = self.klass._can_connect[objklassname]
            if len([ x for x in self.connected if x.name == objklassname ]) >= r.related_max:
                raise ValueError('%s cannot connect to any more objects of type %s' % (self.name, objklassname))
            else:
                if bidirectional == True:
                    obj.connects_to(self, bidirectional=False)
                self.connected.append(obj)
        except KeyError:
            raise ValueError("'%s' cannot connect to objects of type '%s'" % (self.get_config_klass().name, objklassname))

    def __repr__(self):
        """
        Provide a string representation of this object.
        """
        retstr = '<ConfigObject: %s, attributes: %s' % (self.klass.name, self.attrib)
        retstr += '>'
        return retstr

    def __contains__(self, obj):
        """
        Returns True if this object, or any of its contained objects,
        contains obj

        @param obj: The ConfigObject to check to see if it is contained by
        this object.
        """
        if obj in self.contained:
            return True
        for x in self.contained:
            if obj in x:
                return True

        return False

    def is_connected_to(self, obj, checked=[]):
        """
        Returns True if this object, or any of the object it is connected to,
        is connected to obj.

        @param obj: The ConfigObject to check to see if it is connected to
        this object.
        @param checked: A list of objects that we have already checked for
        connectedness, so there is no need to do it again. This helps us
        avoid infinite loops.
        """
        if self not in checked:
            if obj in self.connected:
                return True
            else:
                checked.append(self)
            for x in self.connected:
                if x.is_connected_to(obj, checked):
                    return True

            return False
        else:
            return False


if __name__ == '__main__':
    klasslist = {}
    dc = ConfigKlass('datacenter')
    dc.attribute('name', 'varchar')
    dc.can_contain('switch')
    klasslist['datacenter'] = dc
    switch = ConfigKlass('switch')
    switch.attribute('name', 'varchar')
    switch.can_contain('switchport', 24, 24)
    switch.can_contain('cpu', 1)
    switch.can_connect_to('switch')
    cpu = ConfigKlass('cpu')
    klasslist['switch'] = switch
    port = ConfigKlass('switchport')
    port.attribute('name', 'varchar')
    klasslist['port'] = port
    switch1 = ConfigObject(klasslist['switch'])
    switch2 = ConfigObject(klasslist['switch'])
    switch3 = ConfigObject(klasslist['switch'])
    switch4 = ConfigObject(klasslist['switch'])
    datacentre = ConfigObject(klasslist['datacenter'])
    for klass in klasslist.values():
        print '%s' % klass

    switch1['name'] = 'switch1'
    switch2['name'] = 'switch2'
    switch3['name'] = 'switch3'
    switch4['name'] = 'switch4'
    datacentre['name'] = 'datacentre'
    for i in range(23):
        aport = ConfigObject(klasslist['port'])
        aport['name'] = 'port_%d' % i
        switch1.contains(aport)

    for i in range(14):
        aport = ConfigObject(klasslist['port'])
        aport['name'] = 'port_%d' % i
        switch2.contains(aport)

    switch1.connects_to(switch2, bidirectional=False)
    switch2.connects_to(switch3, bidirectional=False)
    switch3.connects_to(switch1, bidirectional=False)
    datacentre.contains(switch1)
    datacentre.contains(switch2)
    print aport in switch1
    print aport in switch2
    print aport in datacentre
    print 'checking if switch1 is_connected to switch4:', switch1.is_connected_to(switch4)