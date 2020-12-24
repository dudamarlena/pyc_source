# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/onedesk/category/category.py
# Compiled at: 2019-06-06 17:43:26
# Size of source mod 2**32: 7542 bytes
import logging
from collections import deque
from tqdm import tqdm
from onedesk.automaton.automaton import get_automaton_list_for_category
from util.models import Node, Category, Automaton
from util.util import clean_file_name
logger = logging.getLogger('main')

def get_category_list_for_client(session, instance, client):
    logger.debug('Getting categories for client: %s', client['name'])
    response = session.get('{}/api/categories/client/{}'.format(instance, client['id']))
    logger.debug('Response: %s', response.status_code)
    if response.ok:
        return response.json()
    logger.error('Failed to get category list: %s', response.reason)
    return []


def get_category_list_for_category(session, instance, category):
    logger.debug('Getting categories for parent category: %s', category.name)
    response = session.get('{}/api/categories/parent/{}'.format(instance, category.id))
    logger.debug('Response: %s', response.status_code)
    if response.ok:
        return response.json()
    logger.error('Failed to get category list: %s', response.reason)
    return []


def create_category(session, instance, client, name, parent):
    headers = {'Content-Type':'application/json;charset=UTF-8', 
     'Accept':'application/json, text/plain, */*', 
     'Accept-Encoding':'gzip, deflate, br'}
    if parent is not None:
        parent_id = parent.json()['id']
    else:
        parent_id = None
    category_payload = {'name':name,  'clientId':client['id'],  'parentId':parent_id}
    response = session.put(('{}/api/categories/'.format(instance)), headers=headers, json=category_payload)
    logger.debug('Create category response: %s', response.status_code)
    if response.ok:
        return response.json()
    logger.error('Failed to create category %s', name)
    return


def create_parent(session, instance, client, path):
    parent = None
    for part in path.split('/')[:-1]:
        if parent is None:
            full_list = get_category_list_for_client(session, instance, client)
            category_list = []
            for item in full_list:
                if item['parentId'] is None:
                    category_list.append(item)

        else:
            category_list = get_category_list_for_category(session, instance, parent)
        exists = False
        for category in category_list:
            if category['name'] == part:
                exists = True
                parent = Category(category)
                break

        if exists:
            continue
        else:
            category = create_category(session, instance, client, part, parent)
            if category is not None:
                parent = Category(category)
            else:
                logger.error('Can not continue creating parent path')
                return

    return parent


def get_category(session, instance, node):
    logger.debug('>>Getting category %s | %s', node.val.name, node.key)
    data = session.get('{}/api/categories/{}'.format(instance, node.key))
    logger.debug('Get category response: %s', data.status_code)
    return data.json()


def delete_category(session, instance, category):
    logging.debug('!!Deleting category %s', category['name'])
    delete_response = session.delete('{}/api/categories/{}'.format(instance, str(category['id'])))
    logging.debug('Response: %s', delete_response.status_code)


def get_category_tree(session, instance, client, root_category_name=None):
    category_list = get_category_list_for_client(session, instance, client)
    if root_category_name is not None:
        for item in category_list:
            if item['name'] == root_category_name:
                category_list = [
                 item]
                break

        if len(category_list) != 1:
            logger.warning('No category with name %s was found', root_category_name)
            return []
    root_category = Category({'name':client['name'] + 'automata_root', 
     'id':'root',  'clientId':'',  'parentId':None,  'deleted':False})
    root_node = Node(root_category.id, root_category)
    root_node.path = ''
    for item in category_list:
        if item['parentId'] is None:
            category = Category(item)
            category_node = Node(category.id, category)
            category_node.path = category.name
            root_node.children.append(category_node)

    return preorder_traversal_cat(session, instance, root_node)


def preorder_traversal_cat(session, instance, root_node):
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
                top_node.children = get_children_for_category(session, instance, top_node)
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


def get_children_for_category(session, instance, node):
    children = []
    category_list = get_category_list_for_category(session, instance, node.val)
    automaton_list = get_automaton_list_for_category(session, instance, node.val)
    for child in tqdm(category_list, desc=('Getting categories for {}'.format(node.path))):
        category = Category(child)
        category_node = Node(category.id, category)
        category_node.path = node.path + '/' + clean_file_name(category.name)
        category_node.parent = node
        children.append(category_node)

    for child in tqdm(automaton_list, desc=('Getting automata for {}'.format(node.path))):
        automaton = Automaton(child)
        automaton_node = Node(automaton.id, automaton)
        automaton_node.path = node.path + '/' + clean_file_name(automaton.name)
        automaton_node.parent = node
        children.append(automaton_node)

    return children