# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/admin_count_check.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner
from bta.miners import list_group

@Miner.register
class AdminCountCheck(Miner):
    _name_ = 'AdminCountCheck'
    _desc_ = 'list accounts that have admincount=1 but are not admin account'
    _uses_ = ['raw.datatable', 'raw.guid', 'special.categories']

    def get_group_of(self, account):
        return self.guid.find_one({'id': account.get('objectGUID')}).get('name')

    def get_name_of(self, nodeSid):
        return self.datatable.find_one({'objectSid': nodeSid}).get('name')

    def run(self, options, doc):
        adminAccounts = [
         'Schema Admins',
         'Enterprise Admins',
         'Domain Admins',
         'Administrators',
         'Server Operators',
         'Account Operators',
         'Print Operators',
         'Backup Operators',
         'Remote Desktop Users',
         'Group Policy Creator Owners',
         'Incoming Forest Trust Builders',
         'Cert Publishers']
        adminAccountsObjects = list()
        for account in adminAccounts:
            match = {'$and': [{'objectCategory': self.categories.group}, {'$or': [{'name': {'$regex': account}}, {'objectSid': {'$regex': account}}]}]}
            l = self.datatable.find(match)
            for i in l:
                adminAccountsObjects.append(i)

        LGMiner = list_group.ListGroup(self.backend)
        adminAccountsMembers = list()
        for account in adminAccountsObjects:
            adminAccountsMembers += LGMiner.get_members_of(account['objectSid'], True)

        adminAccountsMembersSid = [ a for a, _, _, _ in adminAccountsMembers ]
        accountsWithAdminCount = list()
        for a in self.datatable.find({'$and': [{'objectCategory': self.categories.person}, {'adminCount': 1}]}):
            accountsWithAdminCount.append(a)

        headers = ['Account', 'Group', 'adminCount']
        t = doc.create_table('Members of %s' % (', ').join(adminAccounts))
        t.add(headers)
        t.add()
        for account in accountsWithAdminCount:
            if account.get('objectSid') not in adminAccountsMembersSid:
                t.add(('%s (%s)' % (account.get('name'), account.get('objectSid')), self.get_group_of(account), account.get('adminCount')))

        t.finished()