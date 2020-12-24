# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/domains.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner
from bta.tools.mtools import Family

@Miner.register
class Domains(Miner):
    _name_ = 'Domains'
    _desc_ = 'Display Informations about domains'
    _uses_ = ['raw.datatable']

    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument('--dn', help='Schema Partition Distinghuish name')

    def run(self, options, doc):
        if not options.dn:
            print 'the schema partition distinguish name is mandatory'
            exit(1)
        the_node = Family.find_the_one(options.dn, self.datatable)
        partition = Family.find_the_one('%s:Configuration:Partitions' % options.dn, self.datatable)
        t = doc.create_list('The Domain Functional level of %s is' % options.dn)
        t.add('%s' % the_node['msDS_Behavior_Version'])
        t.flush()
        t.finished()
        u = doc.create_list('The Forest Functional level of %s is' % options.dn)
        u.add('%s' % partition['msDS_Behavior_Version'])
        u.flush()
        u.finished()
        return t

    def assert_consistency(self):
        Miner.assert_consistency(self)
        self.assert_field_type(self.datatable, 'dn', str, unicode)