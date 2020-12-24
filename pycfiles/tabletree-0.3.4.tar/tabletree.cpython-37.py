# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xluo/Personal/Computing/DSKit/tabletree/src/tabletree/tabletree.py
# Compiled at: 2019-11-09 14:06:58
# Size of source mod 2**32: 7369 bytes
import pandas as pd
from tabletree import __version__
__author__ = 'Xi Rossi LUO'
__copyright__ = 'Xi Rossi LUO'
__license__ = 'GPLv3'

class TableNode:
    __doc__ = 'Node for holding tables\n    should have upper-stream nodes (parent) or lower-stream nodes (children)\n    It can have multiple children but only 1 parent (not fully implemented yet)\n    '

    def __init__(self, name, df, parent=None, children=None, plink=None, clink=None):
        self.name = name
        self.parent = parent
        if children is None:
            self.children = children
        else:
            if isinstance(children, list):
                self.children = children
            else:
                self.children = [
                 children]
        self.df = df
        self.plink = plink
        self.clink = clink

    def add_child(self, child, clink):
        if self.children is None:
            self.children = []
            self.clink = []
        child.plink = clink.reversed()
        self.children.append(child)
        self.clink.append(clink)


class TableLink:
    __doc__ = 'Linking Data Nodes together\n    should be a one-to-one link  \n    '

    def __init__(self, fromid, toid):
        self.fromid = fromid
        self.toid = toid

    def reversed(self):
        return TableLink(self.toid, self.fromid)


class TableTree:

    def __init__(self, root_tn):
        self.root = root_tn

    def addChildren(self, newDN, datalink):
        cur = self.root
        bottom = False
        if cur.children is None:
            bottom = True
        else:
            while not bottom:
                cur = cur.children[0]
                if cur.children is None:
                    bottom = True

            newDN.plink = datalink.reversed()
            newDN.parent = cur
            if isinstance(newDN, list):
                cur.children = newDN
            else:
                if isinstance(newDN, TableNode):
                    cur.children = [
                     newDN]
                else:
                    raise 'child class wrong'
            if isinstance(datalink, list):
                cur.clink = datalink
            else:
                if isinstance(datalink, TableLink):
                    cur.clink = [
                     datalink]
                else:
                    raise 'child tablelink class wrong'
        TableTree.checkDataLink(cur, newDN, datalink)

    def addTN(self, nodename, newtn, datalink):
        cur_tn = self.getTN(nodename)
        newtn.parent = cur_tn
        cur_tn.add_child(newtn, datalink)
        return cur_tn

    def getAncestors(self, name):
        cur_tn = self.getTN(name)
        ret = [cur_tn.name]
        while cur_tn.parent is not None:
            ret.insert(0, cur_tn.parent.name)
            cur_tn = cur_tn.parent

        return ret

    def getPath(self, name, offspring):
        cur_tn = self.getTN(offspring)
        ret = [cur_tn.name]
        while cur_tn.parent is not None:
            ret.insert(0, cur_tn.parent.name)
            if cur_tn.parent.name == name:
                return ret
            cur_tn = cur_tn.parent

        raise 'Path not found'

    def reset_children(self, tn):
        if tn.children is None:
            tn.parent = None
            return 1
        for child in tn.children:
            child.parent = None
            self.reset_children(child)

    def reset(self):
        cur = self.root
        self.reset_children(cur)
        return 1

    def getTN(self, name):
        """return TableNode by name
        
        Arguments:
            name {str} -- table node name
        
        Returns:
            table node -- None if not found
        """
        cur = self.root
        return self.search_children(cur, name)

    def search_children(self, cur, name):
        if cur.name == name:
            return cur
        if cur.children is None:
            return
        for child in cur.children:
            ret = self.search_children(child, name)
            if ret is not None:
                return ret

    def findMatched(self, retDNname, matchDNname, matchsel):
        """find matched rows in one table tree node
        
        Args:
            retDNname ([type]): [description]
            matchDNname ([type]): [description]
            matchsel ([type]): [description]
        
        Raises:
            ValueError: [description]
        
        Returns:
            [pandas DataFrame]: pandas DF of the matched data
        """
        mDN = self.getTN(matchDNname)
        ancesters = self.getAncestors(retDNname)
        down_tree = False
        if matchDNname in ancesters:
            down_tree = True
            pathlist = ancesters[ancesters.index(matchDNname):]
        if not down_tree:
            pathlist = self.getPath(retDNname, matchDNname)
        if len(pathlist) < 2:
            raise 'Pathlist too short'
        if down_tree:
            pathlist.pop(0)
            for child_name in pathlist:
                idlist = TableTree.propogate(mDN, matchsel, up=False, child_name=child_name)
                children_names = [cc.name for cc in mDN.children]
                idx = children_names.index(child_name)
                toid = mDN.clink[idx].toid
                mDN = mDN.children[idx]
                matchsel = mDN.df[toid].isin(idlist)

        else:
            pathlist.pop()
            for _ in pathlist.reverse():
                idlist = TableTree.propogate(mDN, matchsel, up=True)
                toid = mDN.plink.toid
                mDN = mDN.parent
                matchsel = mDN.df[toid].isin(idlist)

        return mDN.df.loc[matchsel]

    def get_offsprings(self, cur_tn):
        if cur_tn.children == None:
            return [
             cur_tn.name]
        return [cur_tn.name, [self.get_offsprings(child) for child in cur_tn.children]]

    def print(self):
        ret = self.get_offsprings(self.root)
        return ret

    def __str__(self):
        return str(self.print())

    @staticmethod
    def propogate(fromDN, from_df_rowsel, up=True, child_name=None):
        if not up:
            if child_name is None:
                raise 'Need to input child_name when propogate down the tree!'
        if up:
            return fromDN.df.loc[from_df_rowsel][fromDN.plink.fromid]
        children_names = [ch.name for ch in fromDN.children]
        idx = children_names.index(child_name)
        return fromDN.df.loc[from_df_rowsel][fromDN.clink[idx].fromid]

    @staticmethod
    def checkDataLink(fromDN, toDN, datalink):
        if datalink.fromid not in fromDN.df.columns:
            print('from id not exist in {}'.format(fromDN.name))
            raise ValueError
        if datalink.toid not in toDN.df.columns:
            print('to id not exist in {}'.format(toDN.name))
            raise ValueError