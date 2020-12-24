# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/membership.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner
from bta.tools.WellKnownSID import SID2StringFull

@Miner.register
class Membership(Miner):
    _name_ = 'Membership'
    _desc_ = 'List group membership'
    _uses_ = ['raw.datatable', 'raw.category', 'raw.link_table', 'raw.guid']

    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument('--match', help='Look only for users matching REGEX', metavar='REGEX')
        parser.add_argument('--all-groups', action='store_true', help='List all groups of the object direct or by inclusion')

    def list_groups_of(self, username, doc):
        users = self.datatable.find({'name': {'$regex': '%s' % username}, 'primaryGroupID': {'$exists': True}})
        group_category = self.category.find_one({'name': 'Group'})['id']

        def backlinks(obj, ll):
            links = self.link_table.find({'backlink_DNT': obj['DNT_col'], 'link_DNT': {'$exists': True}})
            for l in links:
                upper_obj = self.datatable.find_one({'DNT_col': l['link_DNT'], 'objectCategory': group_category})
                if upper_obj is not None:
                    if not l.has_key('link_deltime') or l['link_deltime'].year == 1970:
                        ll.add(upper_obj['name'])
                        backlinks(upper_obj, ll)

            return

        for u in users:
            l = doc.create_list('Upper groups of %s' % u['name'])
            primary_id = self.datatable.find_one({'objectSid': ('-').join(u['objectSid'].split('-')[:-1]) + '-%s' % u['primaryGroupID']})
            l.add('Primary group : %s' % primary_id['name'])
            backlinks(u, l)

    def run(self, options, doc):
        if options.match is not None and options.all_groups:
            self.list_groups_of(options.match, doc)
            return
        else:
            match = None
            table = doc.create_table('group membership')
            match = {'objectSid': {'$exists': True}, 'primaryGroupID': {'$exists': True}}
            if options.match is not None:
                match = {'$and': [match, {'$or': [{'cn': {'$regex': options.match}}, {'objectSid': {'$regex': options.match}}]}]}
            for user in self.datatable.find(match):
                links = self.link_table.find({'backlink_DNT': user['DNT_col']}, {'link_DNT': True})
                groups = set()
                sid = user['objectSid']
                pgid = sid[:sid.rfind('-') + 1] + str(user['primaryGroupID'])
                primarygroup = self.datatable.find_one({'objectSid': pgid}, {'cn': True})
                groups.add(primarygroup['cn'])
                for link in links:
                    groupRecId = link['link_DNT']
                    group = self.datatable.find_one({'DNT_col': groupRecId, 'cn': {'$exists': True}}, {'cn': True})
                    if group:
                        groups.add(group['cn'])

                table.add([SID2StringFull(user['objectSid'], self.guid), user['cn'], (', ').join(groups)])

            table.finished()
            return

    def assert_consistency(self):
        Miner.assert_consistency(self)
        self.assert_field_type(self.datatable, 'objectSid', str, unicode)
        self.assert_field_type(self.datatable, 'cn', str, unicode)
        self.assert_field_type(self.datatable, 'DNT_col', int)
        self.assert_field_type(self.datatable, 'primaryGroupID', int)
        self.assert_field_type(self.link_table, 'link_DNT', int)
        self.assert_field_type(self.link_table, 'backlink_DNT', int)