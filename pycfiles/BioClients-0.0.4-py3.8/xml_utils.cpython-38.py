# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/BioClients/util/xml_utils.py
# Compiled at: 2020-03-11 09:26:37
# Size of source mod 2**32: 6080 bytes
"""
        XML utility functions.
"""
import sys, os, re, argparse, logging
from xml.etree import ElementTree
from xml.parsers import expat

def DOM_NodeText(node):
    if type(node) in (ElementTree.Element, ElementTree.ElementTree):
        return DOM_NodeText_ET(node)
    return DOM_NodeText_minidom(node)


def DOM_NodeText_ET(node):
    return node.text


def DOM_NodeText_minidom(node):
    for cnode in node.childNodes:
        if cnode.nodeType == cnode.TEXT_NODE:
            return cnode.nodeValue.strip()
        return ''


def DOM_GetLeafValsByTagName(root, tag):
    if type(root) in (ElementTree.Element, ElementTree.ElementTree):
        return DOM_GetLeafValsByTagName_ET(root, tag)
    return DOM_GetLeafValsByTagName_minidom(root, tag)


def DOM_GetLeafValsByTagName_ET(root, tag):
    vals = []
    for node in root.iter(tag):
        txt = DOM_NodeText(node)
        if txt:
            vals.append(txt)
        return vals


def DOM_GetLeafValsByTagName_minidom(root, tag):
    vals = []
    for node in root.getElementsByTagName(tag):
        txt = DOM_NodeText(node)
        if txt:
            vals.append(txt)
        return vals


def DOM_GetAttr(root, tag, attname):
    if type(root) in (ElementTree.Element, ElementTree.ElementTree):
        return DOM_GetAttr_ET(root, tag, attname)
    return DOM_GetAttr_minidom(root, tag, attname)


def DOM_GetAttr_ET(root, tag, attname):
    vals = []
    for node in root.iter(tag):
        if node.attrib.has_key(attname):
            vals.append(node.attrib[attname])
        return vals


def DOM_GetAttr_minidom(root, tag, attname):
    vals = []
    for node in root.getElementsByTagName(tag):
        if node.attributes.has_key(attname):
            vals.append(node.attributes[attname].value)
        return vals


def DOM_GetNodeAttr(node, attname):
    if type(node) in (ElementTree.Element, ElementTree.ElementTree):
        return DOM_GetNodeAttr_ET(node, attname)
    return DOM_GetNodeAttr_minidom(node, attname)


def DOM_GetNodeAttr_ET(node, attname):
    if node.attrib.has_key(attname):
        return node.attrib[attname]


def DOM_GetNodeAttr_minidom(node, attname):
    if node.attributes.has_key(attname):
        return node.attributes[attname].value


def XpathFind(xp, root):
    if type(root) in (ElementTree.Element, ElementTree.ElementTree):
        return root.findall(xp)
    import xpath
    return xpath.find(xp, root)


def Describe--- This code section failed: ---

 L. 102         0  BUILD_MAP_0           0 
                2  STORE_FAST               'tags'

 L. 103         4  LOAD_GLOBAL              ElementTree
                6  LOAD_ATTR                iterparse
                8  LOAD_FAST                'fin'
               10  LOAD_CONST               ('start', 'end')
               12  LOAD_CONST               ('events',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  STORE_FAST               'et_itrabl'

 L. 104        18  LOAD_GLOBAL              iter
               20  LOAD_FAST                'et_itrabl'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'et_itr'

 L. 105        26  LOAD_FAST                'et_itr'
               28  LOAD_METHOD              next
               30  CALL_METHOD_0         0  ''
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_FAST               'event'
               36  STORE_FAST               'root'

 L. 106        38  LOAD_CONST               0
               40  STORE_FAST               'n_elem'

 L. 106        42  LOAD_CONST               0
               44  STORE_FAST               'n_term'

 L. 108        46  SETUP_FINALLY        60  'to 60'

 L. 109        48  LOAD_FAST                'et_itr'
               50  LOAD_METHOD              next
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'ee'
               56  POP_BLOCK        
               58  JUMP_FORWARD        102  'to 102'
             60_0  COME_FROM_FINALLY    46  '46'

 L. 110        60  DUP_TOP          
               62  LOAD_GLOBAL              Exception
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE   100  'to 100'
               68  POP_TOP          
               70  STORE_FAST               'e'
               72  POP_TOP          
               74  SETUP_FINALLY        88  'to 88'

 L. 111        76  POP_BLOCK        
               78  POP_EXCEPT       
               80  CALL_FINALLY         88  'to 88'
               82  BREAK_LOOP          238  'to 238'
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM            80  '80'
             88_1  COME_FROM_FINALLY    74  '74'
               88  LOAD_CONST               None
               90  STORE_FAST               'e'
               92  DELETE_FAST              'e'
               94  END_FINALLY      
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            66  '66'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            58  '58'

 L. 112       102  LOAD_FAST                'ee'
              104  UNPACK_SEQUENCE_2     2 
              106  STORE_FAST               'event'
              108  STORE_FAST               'elem'

 L. 113       110  LOAD_FAST                'n_elem'
              112  LOAD_CONST               1
              114  INPLACE_ADD      
              116  STORE_FAST               'n_elem'

 L. 114       118  LOAD_FAST                'event'
              120  LOAD_STR                 'start'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   166  'to 166'

 L. 115       126  LOAD_FAST                'tags'
              128  LOAD_METHOD              has_key
              130  LOAD_FAST                'elem'
              132  LOAD_ATTR                tag
              134  CALL_METHOD_1         1  ''
              136  POP_JUMP_IF_TRUE    148  'to 148'

 L. 116       138  LOAD_CONST               0
              140  LOAD_FAST                'tags'
              142  LOAD_FAST                'elem'
              144  LOAD_ATTR                tag
              146  STORE_SUBSCR     
            148_0  COME_FROM           136  '136'

 L. 117       148  LOAD_FAST                'tags'
              150  LOAD_FAST                'elem'
              152  LOAD_ATTR                tag
              154  DUP_TOP_TWO      
              156  BINARY_SUBSCR    
              158  LOAD_CONST               1
              160  INPLACE_ADD      
              162  ROT_THREE        
              164  STORE_SUBSCR     
            166_0  COME_FROM           124  '124'

 L. 118       166  LOAD_GLOBAL              logging
              168  LOAD_METHOD              debug
              170  LOAD_STR                 'event:%6s, elem.tag:%6s, elem.text:%6s'
              172  LOAD_FAST                'event'
              174  LOAD_FAST                'elem'
              176  LOAD_ATTR                tag
              178  LOAD_FAST                'elem'
              180  LOAD_ATTR                text
              182  BUILD_TUPLE_3         3 
              184  BINARY_MODULO    
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 119       190  LOAD_FAST                'elem'
              192  LOAD_ATTR                attrib
              194  LOAD_METHOD              items
              196  CALL_METHOD_0         0  ''
              198  GET_ITER         
              200  FOR_ITER            228  'to 228'
              202  UNPACK_SEQUENCE_2     2 
              204  STORE_FAST               'k'
              206  STORE_FAST               'v'

 L. 120       208  LOAD_GLOBAL              logging
              210  LOAD_METHOD              debug
              212  LOAD_STR                 '\telem.attrib["%s"]: %s'
              214  LOAD_FAST                'k'
              216  LOAD_FAST                'v'
              218  BUILD_TUPLE_2         2 
              220  BINARY_MODULO    
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
              226  JUMP_BACK           200  'to 200'

 L. 121       228  LOAD_FAST                'n_term'
              230  LOAD_CONST               1
              232  INPLACE_ADD      
              234  STORE_FAST               'n_term'
              236  JUMP_BACK            46  'to 46'

 L. 122       238  LOAD_GLOBAL              logging
              240  LOAD_METHOD              debug
              242  LOAD_STR                 'n_elem: %d'
              244  LOAD_FAST                'n_elem'
              246  BINARY_MODULO    
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          

 L. 123       252  LOAD_GLOBAL              logging
              254  LOAD_METHOD              debug
              256  LOAD_STR                 'n_term: %d'
              258  LOAD_FAST                'n_term'
              260  BINARY_MODULO    
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L. 124       266  LOAD_GLOBAL              sorted
              268  LOAD_FAST                'tags'
              270  LOAD_METHOD              keys
              272  CALL_METHOD_0         0  ''
              274  CALL_FUNCTION_1       1  ''
              276  GET_ITER         
              278  FOR_ITER            308  'to 308'
              280  STORE_FAST               'tag'

 L. 125       282  LOAD_GLOBAL              logging
              284  LOAD_METHOD              info
              286  LOAD_STR                 '%24s: %6d'
              288  LOAD_FAST                'tag'
              290  LOAD_FAST                'tags'
              292  LOAD_FAST                'tag'
              294  BINARY_SUBSCR    
              296  BUILD_TUPLE_2         2 
              298  BINARY_MODULO    
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          
          304_306  JUMP_BACK           278  'to 278'

Parse error at or near `CALL_FINALLY' instruction at offset 80


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XML utility', epilog='clean: UTF-8 encoding compliant')
    ops = [
     'match_xpath', 'describe', 'clean']
    parser.add_argument('op', choices=ops, help='operation')
    parser.add_argument('--i', dest='ifile', help='input XML file')
    parser.add_argument('--xpath', help='xpath pattern')
    parser.add_argument('--force', type=bool, help='ignore UTF-8 encoding errors')
    parser.add_argument('--o', dest='ofile', help='output XML file')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    logging.basicConfig(format='%(levelname)s:%(message)s', level=(logging.DEBUG if args.verbose > 1 else logging.INFO))
    codecs_mode = 'ignore' if args.force else 'replace'
    if args.ifile:
        fin = open(args.ifile, 'r')
    else:
        fin = sys.stdin
    if args.ofile:
        fout = open(args.ofile, 'w')
    else:
        fout = sys.stdout
    if args.op == 'describe':
        Describe(fin)
    else:
        if args.op == 'clean':
            try:
                root = ElementTree.parse(fin)
            except Exception as e:
                try:
                    parser.error('ElementTree.parse(): %s' % str(e))
                finally:
                    e = None
                    del e

            else:
                fin.close()
                root.write(fout, encoding='UTF-8', xml_declaration=True)
        else:
            if args.op == 'match_xpath':
                try:
                    root = ElementTree.parse(fin)
                except Exception as e:
                    try:
                        parser.error('ElementTree.parse(): %s' % str(e))
                    finally:
                        e = None
                        del e

                else:
                    fin.close()
                    if not (xp and ifile):
                        parser.error('--i and --xpath required.')
                    nodes = XpathFind(xp, root)
                    fout.write('"xpath","match"\n')
                    for i, node in enumerate(nodes):
                        fout.write('"%s","%s"\n' % (xp, DOM_NodeText(node)))
                    else:
                        logging.info('matches: %d' % len(nodes))

            else:
                parser.error('Invalid operation. %s' % args.op)