# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/list_links.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner

@Miner.register
class ListLinks(Miner):
    _name_ = 'ListLinks'
    _desc_ = 'List links from link_table, from/to designated object(s)'
    _uses_ = ['raw.datatable', 'raw.link_table', 'raw.linkid']

    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument('--name', help='object name', required=True)

    def run(self, options, doc):
        self.options = options
        srcObjects = self.datatable.find({'name': options.name})
        doc.add('List of links for objects matching %s' % options.name)
        for obj in srcObjects:
            table = doc.create_table('Backward links for object %s' % obj['name'])
            table.add(['SrcObject', 'LinkType', 'DstObject', 'DeactiveTime', 'DelTime', 'USNChanged'])
            table.add()
            links = self.link_table.find({'backlink_DNT': obj['DNT_col']})
            for link in links:
                dstObj = self.datatable.find_one({'DNT_col': link['link_DNT']})
                linkType = self.linkid.find_one({'linkid': link['link_base'] * 2})['name']
                dateAttrs = list()
                for attr in ('link_deactivetime', 'link_deltime', 'link_usnchanged'):
                    if attr in link:
                        dateAttrs.append(link[attr])
                    else:
                        dateAttrs.append('')

                table.add([obj['name'], linkType, dstObj['name']] + dateAttrs)

            table.finished()
            table = doc.create_table('Forward links for object %s' % obj['name'])
            table.add(['SrcObject', 'LinkType', 'DstObject', 'DeactiveTime', 'DelTime', 'USNChanged'])
            table.add()
            links = self.link_table.find({'link_DNT': obj['DNT_col']})
            for link in links:
                dstObj = self.datatable.find_one({'DNT_col': link['backlink_DNT']})
                linkType = self.linkid.find_one({'linkid': link['link_base'] * 2})['name']
                table.add([obj['name'], linkType, dstObj['name']])

            table.finished()

    def assert_consistency(self):
        Miner.assert_consistency(self)
        assert self.linkid.find({'name': {'$exists': True}}).count() > 10, 'less than 10 names in linkid table'