# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/util/util.py
# Compiled at: 2019-06-06 17:43:26
# Size of source mod 2**32: 4952 bytes
import json, logging
from collections import deque
from pathlib import Path
from util.models import Node, Category, Automaton, ExportedAutomaton
logger = logging.getLogger('main')

def preorder_traversal_dir(directory, root_node):
    stack = deque([])
    preorder = []
    preorder_nodes = []
    for child in root_node.children:
        stack.append(child)
        preorder.append(child.path)
        preorder_nodes.append(child)

    while len(stack) > 0:
        finished = 0
        top_node = stack[(len(stack) - 1)]
        if type(top_node.val) is Category:
            if len(top_node.children) == 0:
                top_node.children = get_children_for_directory(directory, top_node)
        if len(top_node.children) == 0:
            stack.pop()
        else:
            for child in top_node.children:
                if child.path not in preorder:
                    finished = 1
                    stack.append(child)
                    preorder.append(child.path)
                    preorder_nodes.append(child)
                    break

            if finished == 0:
                stack.pop()

    return preorder_nodes


def get_children_for_directory(directory, node):
    children = []
    for child in Path(directory, node.path).iterdir():
        child_ob = None
        if child.suffix == '.json' and child.is_file():
            child_dict = read_json_file(child)
            if 'latestAutomatonVersion' in child_dict:
                child_ob = Automaton(child_dict)
            else:
                if 'automatonFlow' in child_dict:
                    child_ob = ExportedAutomaton(child_dict)
                elif child.is_dir():
                    logger.debug('Reading directory %s', child.absolute())
                    child_ob = Category({'name':child.name,  'id':'', 
                     'clientId':'', 
                     'parentId':'', 
                     'deleted':False})
                if child_ob is not None:
                    child_node = Node(child_ob.id, child_ob)
                    child_node.path = node.path + '/' + child_ob.name
                    child_node.parent = node
                    children.append(child_node)

    return children


def get_directory_tree(directory):
    logger.debug('Reading directory %s', directory)
    root_category = Category({'name':'automata_root', 
     'id':'root', 
     'clientId':'', 
     'parentId':None, 
     'deleted':False})
    root_node = Node(root_category.id, root_category)
    root_node.path = directory.absolute()
    for child in directory.iterdir():
        child_ob = None
        if child.suffix == '.json' and child.is_file():
            child_dict = read_json_file(child)
            if 'latestAutomatonVersion' in child_dict:
                child_ob = Automaton(child_dict)
            else:
                if 'automatonFlow' in child_dict:
                    child_ob = ExportedAutomaton(child_dict)
                elif child.is_dir():
                    logger.debug('Reading directory %s', child.absolute())
                    child_ob = Category({'name':child.name,  'id':'', 
                     'clientId':'', 
                     'parentId':'', 
                     'deleted':False})
                if child_ob is not None:
                    child_node = Node(child_ob.id, child_ob)
                    child_node.path = child.name
                    root_node.children.append(child_node)

    return preorder_traversal_dir(directory, root_node)


def read_json_file(file):
    logger.debug('Reading file %s', file.absolute())
    return json.loads(file.read_text())


def write_json_file(file, data):
    logger.debug('Writing file %s', file.absolute())
    file.write_text(json.dumps(data, sort_keys=True, indent=4))


def clean_file_name(file_name):
    return file_name.strip().replace('/', '_').replace('\\', '_').replace(':', '_').replace(';', '_').replace('?', '_').replace('!', '_')