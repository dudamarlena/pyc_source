# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/DN_grep.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner

@Miner.register
class DNGrep(Miner):
    _name_ = 'DNGrep'
    _desc_ = 'DN grepper'
    _uses_ = ['raw.datatable']

    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument('--cn', help='Look for objects with given CN and print their DN')

    def run(self, options, doc):
        doc.add('Listing DN of all objects whose CN matches [%s]' % options.cn)
        l = doc.create_list('List of CN')

        def find_dn(r):
            if not r:
                return ''
            else:
                cn = r.get('cn') or r.get('name')
                if cn is None or cn.startswith('$ROOT_OBJECT$'):
                    return ''
                r2 = self.datatable.find_one({'DNT_col': r['PDNT_col']})
                return find_dn(r2) + '.' + cn

        c = self.datatable.find({'cn': {'$regex': '.*%s.*' % options.cn, '$options': 'i'}})
        for r in c:
            l.add('%s: %s' % (('None' or r.get)('cn') if 1 else '', find_dn(r)))

        l.finished()

    def assert_consistency(self):
        Miner.assert_consistency(self)
        self.assert_field_exists(self.datatable, 'PDNT_col')
        self.assert_field_type(self.datatable, 'cn', str, unicode)
        self.assert_field_type(self.datatable, 'name', str, unicode)
        self.assert_field_type(self.datatable, 'PDNT_col', int)