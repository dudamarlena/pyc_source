# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/app/tagger/SCRDRlearner/SCRDRTree.py
# Compiled at: 2017-01-18 02:57:40
# Size of source mod 2**32: 6400 bytes
from .Node import Node
from .Object import FWObject

class SCRDRTree:
    __doc__ = '\n    Single Classification Ripple Down Rules tree for Part-of-Speech and morphological tagging\n    '

    def __init__(self, root=None):
        self.root = root

    def findDepthNode(self, node, depth):
        while node.depth != depth:
            node = node.father

        return node

    def classify(self, object):
        self.root.check(object)

    def writeToFileWithSeenCases(self, outFile):
        out = open(outFile, 'w')
        self.root.writeToFileWithSeenCases(out, 0)
        out.close()

    def writeToFile(self, outFile):
        out = open(outFile, 'w')
        self.root.writeToFile(out, 0)
        out.close()

    def constructSCRDRtreeFromRDRfile(self, lines):
        self.root = Node(FWObject(False), 'NN', None, None, None, [], 0)
        currentNode = self.root
        currentDepth = 0
        for i in range(1, len(lines)):
            line = lines[i]
            depth = 0
            for c in line:
                if c == '\t':
                    depth = depth + 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                pass
            else:
                temp = line.find('cc')
                if temp == 0:
                    pass
                else:
                    condition = getCondition(line.split(' : ', 1)[0].strip())
                    conclusion = getConcreteValue(line.split(' : ', 1)[1].strip())
                    node = Node(condition, conclusion, None, None, None, [], depth)
                    if depth > currentDepth:
                        currentNode.exceptChild = node
                    else:
                        if depth == currentDepth:
                            currentNode.elseChild = node
                        else:
                            while currentNode.depth != depth:
                                currentNode = currentNode.father

                            currentNode.elseChild = node
            node.father = currentNode
            currentNode = node
            currentDepth = depth

    def findFiredNode(self, fwObject):
        currentNode = self.root
        firedNode = None
        obContext = fwObject.context
        while True:
            cnContext = currentNode.condition.context
            notNoneIds = currentNode.condition.notNoneIds
            satisfied = True
            for i in notNoneIds:
                if cnContext[i] != obContext[i]:
                    satisfied = False
                    break

            if satisfied:
                firedNode = currentNode
                exChild = currentNode.exceptChild
                if exChild is None:
                    break
                else:
                    currentNode = exChild
            else:
                elChild = currentNode.elseChild
                if elChild is None:
                    break
                else:
                    currentNode = elChild

        return firedNode


def getConcreteValue(str):
    if str.find('""') > 0:
        if str.find('Word') > 0:
            return '<W>'
        if str.find('suffixL') > 0:
            return '<SFX>'
        return '<T>'
    return str[str.find('"') + 1:len(str) - 1]


def getCondition(strCondition):
    condition = FWObject(False)
    for rule in strCondition.split(' and '):
        rule = rule.strip()
        key = rule[rule.find('.') + 1:rule.find(' ')]
        value = getConcreteValue(rule)
        if key == 'prevWord2':
            condition.context[0] = value
        elif key == 'prevTag2':
            condition.context[1] = value
        elif key == 'prevWord1':
            condition.context[2] = value
        elif key == 'prevTag1':
            condition.context[3] = value
        elif key == 'word':
            condition.context[4] = value
        elif key == 'tag':
            condition.context[5] = value
        elif key == 'nextWord1':
            condition.context[6] = value
        elif key == 'nextTag1':
            condition.context[7] = value
        elif key == 'nextWord2':
            condition.context[8] = value
        elif key == 'nextTag2':
            condition.context[9] = value
        else:
            if key == 'suffixL2':
                condition.context[10] = value
            else:
                if key == 'suffixL3':
                    condition.context[11] = value
                elif key == 'suffixL4':
                    condition.context[12] = value

    for i in range(13):
        if condition.context[i] is not None:
            condition.notNoneIds.append(i)

    return condition


if __name__ == '__main__':
    pass