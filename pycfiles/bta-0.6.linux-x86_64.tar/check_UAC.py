# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/check_UAC.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner
from bta.datatable import UserAccountControl
from bta.tools.expr import Field

@Miner.register
class CheckUAC(Miner):
    _name_ = 'CheckUAC'
    _desc_ = 'Weird paswword policy (No password or password never expire)'
    _uses_ = ['virtual.datasd', 'special.categories']

    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument('flags', help='List weird user access control', nargs='*', choices=UserAccountControl._flags_.keys() + [[]])

    def findRogue(self, flags):
        req = ((Field('objectCategory') == self.categories.person) | (Field('objectCategory') == self.categories.computer)) & Field('userAccountControl').present()
        for f in flags:
            req &= Field('userAccountControl').flag_on(f)

        result = [['cn', 'SID', 'Flags'], []]
        for subject in self.datasd.find(req):
            result.append([subject['name'], subject['objectSid'], (', ').join([ a for a, b in subject['userAccountControl']['flags'].items() if b ])])

        return result

    def run(self, options, doc):
        rogues = self.findRogue(options.flags)
        t = doc.create_table('Weird account rights with all flags: %s' % (', ').join(options.flags))
        for disp in rogues:
            t.add(disp)

        t.flush()
        t.finished()