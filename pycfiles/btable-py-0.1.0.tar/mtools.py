# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/tools/mtools.py
# Compiled at: 2015-10-20 16:27:01
local_relative_domains_sid = None

class Family(object):

    @classmethod
    def find_childs(cls, node, datatable):
        return list(datatable.find({'PDNT_col': node['DNT_col']}))

    @classmethod
    def find_parents(cls, node, datatable):
        parents = list()
        for a in node['Ancestors_col']:
            parents.append(datatable.find({'DNT_col': a}).limit(1)[0])

        return parents

    @classmethod
    def find_offspring(cls, node, datatable, rec=1, need=['name', 'DNT_col']):

        def needed(node, stuffs=need):
            collected = list()
            for a in stuffs:
                try:
                    collected.append(str(node[a]))
                except:
                    collected.append('X')

            return (':').join(collected)

        def find_rec(node, offspring, datatable, rec):
            childs = Family.find_childs(node, datatable)
            for s in childs:
                id_new_node = needed(s)
                if len(Family.find_childs(s, datatable)) == 0 or rec == 0:
                    offspring['leafs'].append(id_new_node)
                else:
                    offspring[id_new_node] = {'leafs': list()}
                    find_rec(s, offspring[id_new_node], datatable, rec - 1)

            return offspring

        init = {needed(node): find_rec(node, {'leafs': list()}, datatable, rec)}
        return init

    @classmethod
    def correlate(cls, tree, criteria, doc, datatable):

        def check_eligibility(criteria, l):
            ok = 0
            for lucky_position, lucky_nodes in criteria:
                if '%s' % l.split(':')[lucky_position] in lucky_nodes.keys():
                    ok += 1

            return ok == len(criteria)

        dico = None
        for k, v in tree.items():
            if k != 'leafs' and check_eligibility(criteria, k):
                dico = doc.create_list(k)
                for lucky_position, lucky_nodes in criteria:
                    for info in lucky_nodes[('%s' % k.split(':')[lucky_position])]:
                        dico.add(info)

            if type(v) == list:
                for l in v:
                    if check_eligibility(criteria, l):
                        ri = doc.create_list(l)
                        for lucky_position, lucky_nodes in criteria:
                            for info in lucky_nodes[('%s' % l.split(':')[lucky_position])]:
                                ri.add(info)

                            ri.finished()

            elif type(v) == dict:
                if dico is None:
                    dico = doc.create_list(k)
                Family.correlate(v, criteria, dico, datatable)
                dico.finished()

        return

    @classmethod
    def find_the_one(cls, cn, datatable):
        steps = cn.split(':')
        the_node = None
        name = '%s' % steps[(-1)]
        name = name.strip()
        nodes = datatable.find({'name': steps[(-1)]})
        for node in nodes:
            ancestors = Family.find_parents(node, datatable)
            if ['$ROOT_OBJECT$\x00'] + steps == [ a['name'] for a in ancestors ]:
                the_node = node
                break

        return the_node


class ObjectClass(object):

    @classmethod
    def find_my_class(cls, node, datatable):
        classes = datatable.find({'DNT_col': node['DNT_col']}, {'objectClass': 1})
        return classes

    @classmethod
    def instanceOfClass(cls, searchedGovernID, datatable):
        all_instances = datatable.find({'objectClass': {'$in': ['%s' % searchedGovernID]}})
        results = dict()
        for i in all_instances:
            results['%s' % i['DNT_col']] = [
             '----------']

        return results

    @classmethod
    def find_my_possuperiors(cls, name, datatable):
        possSuperiors = datatable.find_one({'name': name, 'systemPossSuperiors': {'$exists': True}}, {'systemPossSuperiors': 1})
        if possSuperiors is not None:
            return possSuperiors.get('systemPossSuperiors')
        else:
            return []

    @classmethod
    def test(cls):
        return ''


class Sid(object):

    def __init__(self, sid, dt):
        try:
            self.obj = dt.find_one({'objectSid': sid})
        except:
            self.obj = {'cn': '(null)', 'objectSid': '(null)'}

    def __str__(self):
        if not self.obj:
            return '(null obj)'
        try:
            s = ('{0[name]}').format(self.obj)
        except:
            s = self.obj['sid']

        return s

    def getUserAccountControl(self):
        if 'userAccountControl' in self.obj:
            l = [ f for f, v in self.obj['userAccountControl']['flags'].items() if v ]
            return (', ').join(l)
        else:
            return ''

    @staticmethod
    def resolveRID(sid):
        pos = sid.rfind('-')
        domainpart = sid[:pos]
        userpart = sid[pos:]
        if domainpart in local_relative_domains_sid:
            return local_relative_domains_sid[domainpart] + userpart
        else:
            return sid


class Record(object):

    def __init__(self, **dbrecord):
        self.obj = dbrecord

    def __getattr__(self, attr):
        return self.obj.get(attr, None)

    def __getitem__(self, attr):
        return self.obj.get(attr, None)

    def __contains__(self, attr):
        return self.obj.__contains__(attr)

    def __repr__(self):
        return self.obj.__str__()

    def __str__(self):
        return self.obj.__str__()