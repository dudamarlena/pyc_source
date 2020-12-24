# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/dbsubnetgroup.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2825 bytes
__doc__ = '\nRepresents an DBSubnetGroup\n'

class DBSubnetGroup(object):
    """DBSubnetGroup"""

    def __init__(self, connection=None, name=None, description=None, subnet_ids=None):
        self.connection = connection
        self.name = name
        self.description = description
        if subnet_ids is not None:
            self.subnet_ids = subnet_ids
        else:
            self.subnet_ids = []
        self.vpc_id = None
        self.status = None

    def __repr__(self):
        return 'DBSubnetGroup:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'SubnetIdentifier':
            self.subnet_ids.append(value)
        else:
            if name == 'DBSubnetGroupName':
                self.name = value
            else:
                if name == 'DBSubnetGroupDescription':
                    self.description = value
                else:
                    if name == 'VpcId':
                        self.vpc_id = value
                    else:
                        if name == 'SubnetGroupStatus':
                            self.status = value
                        else:
                            setattr(self, name, value)