# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/who_is.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner
import bson.binary

@Miner.register
class WhoIs(Miner):
    _name_ = 'WhoIs'
    _desc_ = 'Resolve SID'
    _uses_ = ['raw.datatable']

    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument('--sid', help='Look at this SID', metavar='SID')
        parser.add_argument('--noresolve', help='Do not resolve SID', action='store_true')
        parser.add_argument('--verbose', help='Show also deleted users time and RID', action='store_true')

    def run(self, options, doc):
        sec = doc.create_subsection('Who is %s' % options.sid)
        c = self.datatable.find({'objectSid': options.sid})
        for r in c:
            t = sec.create_table('Name=[%s]' % r.get('name', ''))
            for k, v in r.iteritems():
                if type(v) is bson.binary.Binary:
                    t.add([k, v.encode('hex')])
                else:
                    t.add([k, v])

            t.finished()

    def assert_consistency(self):
        Miner.assert_consistency(self)
        self.assert_field_exists(self.datatable, 'objectSid')
        self.assert_field_type(self.datatable, 'objectSid', str, unicode)