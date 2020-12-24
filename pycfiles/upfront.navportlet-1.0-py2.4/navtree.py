# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/upfront/navportlet/navtree.py
# Compiled at: 2010-10-13 15:04:43
from types import StringType
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import NavtreeStrategyBase

def buildFolderTree(context, obj=None, query={}, strategy=NavtreeStrategyBase()):
    """Create a tree structure representing a navigation tree. By default,
    it will create a full "sitemap" tree, rooted at the portal, ordered
    by explicit folder order. If the 'query' parameter contains a 'path'
    key, this can be used to override this. To create a navtree rooted
    at the portal root, set query['path'] to:

        {'query' : '/'.join(context.getPhysicalPath()),
         'navtree' : 1}

    to start this 1 level below the portal root, set query['path'] to:

        {'query' : '/'.join(obj.getPhysicalPath()),
         'navtree' : 1,
         'navtree_start' : 1}

    to create a sitemap with depth limit 3, rooted in the portal:

        {'query' : '/'.join(obj.getPhysicalPath()),
         'depth' : 3}

    The parameters:

    - 'context' is the acquisition context, from which tools will be acquired
    - 'obj' is the current object being displayed.
    - 'query' is a catalog query to apply to find nodes in the tree.
    - 'strategy' is an object that can affect how the generation works. It
        should be derived from NavtreeStrategyBase, if given, and contain:

            rootPath -- a string property; the physical path to the root node.

            If not given, it will default to any path set in the query, or the
            portal root. Note that in a navtree query, the root path will
            default to the portal only, possibly adjusted for any navtree_start
            set. If rootPath points to something not returned by the query by
            the query, a dummy node containing only an empty 'children' list
            will be returned.

            showAllParents -- a boolean property; if true and obj is given,
                ensure that all parents of the object, including any that would
                normally be filtered out are included in the tree.

            nodeFilter(node) -- a method returning a boolean; if this returns
                False, the given node will not be inserted in the tree

            subtreeFilter(node) -- a method returning a boolean; if this returns
                False, the given (folderish) node will not be expanded (its
                children will be pruned off)

            decoratorFactory(node) -- a method returning a dict; this can inject
                additional keys in a node being inserted.
                
            showChildrenOf(object) -- a method returning True if children of
                the given object (normally the root) should be returned

    Returns tree where each node is represented by a dict:

        item            -   A catalog brain of this item
        depth           -   The depth of this item, relative to the startAt level
        currentItem     -   True if this is the current item
        currentParent   -   True if this is a direct parent of the current item
        children        -   A list of children nodes of this node

    Note: Any 'decoratorFactory' specified may modify this list, but
    the 'children' property is guaranteed to be there.

    Note: If the query does not return the root node itself, the root
    element of the tree may contain *only* the 'children' list.

    Note: Folder default-pages are not included in the returned result.
    If the 'obj' passed in is a default-page, its parent folder will be
    used for the purposes of selecting the 'currentItem'.
    """
    portal_url = getToolByName(context, 'portal_url')
    nav_catalog = getToolByName(context, 'nav_catalog')
    showAllParents = strategy.showAllParents
    rootPath = strategy.rootPath
    request = getattr(context, 'REQUEST', {})
    objPath = None
    objPhysicalPath = None
    if obj is not None:
        objPhysicalPath = obj.getPhysicalPath()
        if utils.isDefaultPage(obj, request):
            objPhysicalPath = objPhysicalPath[:-1]
        objPath = ('/').join(objPhysicalPath)
    portalPath = portal_url.getPortalPath()
    portalObject = portal_url.getPortalObject()
    if 'path' not in query:
        if rootPath is None:
            rootPath = portalPath
        query['path'] = rootPath
    elif rootPath is None:
        pathQuery = query['path']
        if type(pathQuery) == StringType:
            rootPath = pathQuery
        elif pathQuery.get('navtree', False):
            navtreeLevel = pathQuery.get('navtree_start', 1)
            if navtreeLevel > 1:
                navtreeContextPath = pathQuery['query']
                navtreeContextPathElements = navtreeContextPath[len(portalPath) + 1:].split('/')
                if len(navtreeContextPathElements) < navtreeLevel - 1:
                    return {'children': []}
                rootPath = portalPath + '/' + ('/').join(navtreeContextPathElements[:navtreeLevel - 1])
            else:
                rootPath = portalPath
        else:
            rootPath = pathQuery['query']
    rootDepth = len(rootPath.split('/'))
    pruneRoot = False
    if strategy is not None:
        rootObject = portalObject.unrestrictedTraverse(rootPath, None)
        if rootObject is not None:
            pruneRoot = not strategy.showChildrenOf(rootObject)
    if 'sort_on' not in query:
        query['sort_on'] = 'getObjPositionInParent'
    if 'is_default_page' not in query:
        query['is_default_page'] = False
    results = nav_catalog.searchResults(query)
    itemPaths = {}
    itemPaths[rootPath] = {'children': []}
    if pruneRoot:
        itemPaths[rootPath]['_pruneSubtree'] = True

    def insertElement(itemPaths, item, forceInsert=False):
        """Insert the given 'item' brain into the tree, which is kept in
        'itemPaths'. If 'forceInsert' is True, ignore node- and subtree-
        filters, otherwise any node- or subtree-filter set will be allowed to
        block the insertion of a node.
        """
        itemPath = item.getPath()
        itemInserted = itemPaths.get(itemPath, {}).get('item', None) is not None
        if not forceInsert and itemInserted:
            return
        itemPhysicalPath = itemPath.split('/')
        parentPath = ('/').join(itemPhysicalPath[:-1])
        parentPruned = itemPaths.get(parentPath, {}).get('_pruneSubtree', False)
        if not forceInsert and parentPruned:
            return
        isCurrent = isCurrentParent = False
        if objPath is not None:
            if objPath == itemPath:
                isCurrent = True
            else:
                if objPath.startswith(itemPath + '/'):
                    if len(objPhysicalPath) > len(itemPhysicalPath):
                        isCurrentParent = True
                relativeDepth = len(itemPhysicalPath) - rootDepth
                newNode = {'item': item, 'depth': relativeDepth, 'currentItem': isCurrent, 'currentParent': isCurrentParent}
                insert = True
                if not forceInsert:
                    if strategy is not None:
                        insert = strategy.nodeFilter(newNode)
                    if insert:
                        if strategy is not None:
                            newNode = strategy.decoratorFactory(newNode)
                        if itemPaths.has_key(parentPath):
                            itemParent = itemPaths[parentPath]
                            if forceInsert:
                                nodeAlreadyInserted = False
                                for i in itemParent['children']:
                                    if i['item'].getPath() == itemPath:
                                        nodeAlreadyInserted = True
                                        break

                                nodeAlreadyInserted or itemParent['children'].append(newNode)
                        else:
                            itemParent.get('_pruneSubtree', False) or itemParent['children'].append(newNode)
                else:
                    itemPaths[parentPath] = {'children': [newNode]}
                if strategy.showAllParents and isCurrentParent:
                    expand = True
                else:
                    expand = getattr(item, 'is_folderish', True)
                if expand and not forceInsert and strategy is not None:
                    expand = strategy.subtreeFilter(newNode)
                children = newNode.setdefault('children', [])
                if expand:
                    if itemPaths.has_key(itemPath):
                        children.extend(itemPaths[itemPath]['children'])
                else:
                    newNode['_pruneSubtree'] = True
                itemPaths[itemPath] = newNode
        return

    for r in results:
        insertElement(itemPaths, r)

    if strategy.showAllParents and objPath is not None:
        objSubPathElements = objPath[len(rootPath) + 1:].split('/')
        parentPaths = []
        haveNode = itemPaths.get(rootPath, {}).get('item', None) is None
        if not haveNode:
            parentPaths.append(rootPath)
        parentPath = rootPath
        for i in range(len(objSubPathElements)):
            nodePath = rootPath + '/' + ('/').join(objSubPathElements[:i + 1])
            node = itemPaths.get(nodePath, None)
            if node is None or 'item' not in node:
                parentPaths.append(nodePath)
            else:
                nodeParent = itemPaths.get(parentPath, None)
                if nodeParent is not None:
                    nodeAlreadyInserted = False
                    for i in nodeParent['children']:
                        if i['item'].getPath() == nodePath:
                            nodeAlreadyInserted = True
                            break

                    if not nodeAlreadyInserted:
                        nodeParent['children'].append(node)
            parentPath = nodePath

        if len(parentPaths) > 0:
            query = {'path': {'query': parentPaths, 'depth': 0}}
            results = nav_catalog.unrestrictedSearchResults(query)
            for r in results:
                insertElement(itemPaths, r, forceInsert=True)

    return itemPaths[rootPath]