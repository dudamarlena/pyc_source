# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/SID_history.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner

@Miner.register
class SIDHistory(Miner):
    _name_ = 'SIDHistory'
    _desc_ = 'Checking user with Sid history'
    _uses_ = ['raw.datatable']

    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument('--list', action='store_true', help='list all user having a sidhistory setted')
        parser.add_argument('--match', help='Look only for users matching REGEX', metavar='REGEX')

    def run(self, options, doc):
        if options.list:
            users = self.datatable.find({'sIDHistory': {'$exists': True}})
            table = doc.create_table('Users which have SIDHistory not Null')
            table.add(['Name', 'SIDHistory'])
            table.add()
            for u in users:
                table.add([u['name'], u['sIDHistory']])

            table.finished()
        if options.match:
            users = self.datatable.find({'sIDHistory': {'$regex': options.match}})
            t = doc.create_list('The SID %s can be found in th SIDHistory of the following users' % options.match)
            for u in users:
                t.add(u['name'])

    def assert_consistency(self):
        Miner.assert_consistency(self)
        self.assert_field_type(self.datatable, 'dn', str, unicode)