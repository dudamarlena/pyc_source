# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\xmldict.py
# Compiled at: 2020-01-13 13:07:08
# Size of source mod 2**32: 3199 bytes
import xml.dom.minidom, pdb

class NotTextNodeError:
    pass


def getTextFromNode(node):
    """
    scans through all children of node and gathers the
    text. if node has non-text child-nodes, then
    NotTextNodeError is raised.
    """
    t = ''
    for n in node.childNodes:
        if n.nodeType == n.TEXT_NODE:
            t += n.nodeValue
        else:
            raise NotTextNodeError

    return t


def nodeToDic(node):
    """
    nodeToDic() scans through the children of node and makes a
    dictionary from the content.
    three cases are differentiated:
    - if the node contains no other nodes, it is a text-node
    and {nodeName:text} is merged into the dictionary.
    - if there is more than one child with the same name
    then these children will be appended to a list and this
    list is merged to the dictionary in the form: {nodeName:list}.
    - else, nodeToDic() will call itself recursively on
    the nodes children (merging {nodeName:nodeToDic()} to
    the dictionary).
    """
    dic = {}
    multlist = {}
    sibs = []
    for n in node.childNodes:
        sibs.append(n.nodeName)

    for n in node.childNodes:
        multiple = False
        if n.nodeType != n.ELEMENT_NODE:
            pass
        else:
            if sibs.count(n.nodeName) > 1:
                multiple = True
                if n.nodeName not in multlist:
                    multlist[n.nodeName] = []
            try:
                text = getTextFromNode(n).strip().encode('utf-8')
            except NotTextNodeError:
                if multiple:
                    multlist[n.nodeName].append(nodeToDic(n))
                    dic.update({n.nodeName: multlist[n.nodeName]})
                    continue
                else:
                    dic.update({n.nodeName: nodeToDic(n)})
                    continue

            if multiple:
                multlist[n.nodeName].append(text)
                dic.update({n.nodeName: multlist[n.nodeName]})
            else:
                dic.update({n.nodeName: text})

    return dic


def readXmlFile(filename):
    dom = xml.dom.minidom.parse(filename)
    return nodeToDic(dom)


def readXmlString(xmlstring):
    dom = xml.dom.minidom.parseString(xmlstring)
    return nodeToDic(dom)


if __name__ == '__main__':
    dic = readXmlFile('history.tcx')
    pdb.set_trace()