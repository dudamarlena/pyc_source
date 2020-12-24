# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/network/mutators.py
# Compiled at: 2012-09-09 23:45:49
"""
mutators module
===============

This module houses operations which act on networks, that can be classified as 
mutations. They manipulate networks explicitly.

Functions
---------
    TODO
    point_mutate_adj:
    point_mutate_mask:
    degree_and_connectivity_preserving_mutation:
    degree_preserving_mutation:
    
 
"""

def point_mutate_adj(network):
    """
    Will result in a series of implicit point mutation of the adjacency matrix
    """
    import numpy as num, logging
    logging.info('Network ' + str(network) + ' is mutated')
    num.random.seed()
    random_i = num.random.randint(0, network.n_nodes)
    random_j = num.random.randint(0, network.n_nodes)
    network.adjacency[random_i][random_j] = not network.adjacency[random_i][random_j]


def point_mutate_mask(network):
    """
    Will result in a series of implicit point mutation of the masks
    """
    import numpy as num, logging
    logging.info('Network ' + str(network) + ' is mutated')
    num.random.seed()
    random_i = num.random.randint(0, network.n_nodes)
    random_j = num.random.randint(0, network.n_nodes)
    network.mask[random_i][random_j] = not network.mask[random_i][random_j]


def degree_and_connectivity_preserving_mutation(network, maximum=0, def_mutation=False):
    """
    A mutation that preserves the degree of the network in concern.
    """
    import numpy as num, logging
    adj = network.adjacency
    logging.debug('Adjacency Matrix:')
    logging.debug(adj)
    n_nodes = len(adj)
    if maximum == 0:
        maximum = 10 * len(adj) ** 2
    columns = adj.sum(axis=0)
    rows = adj.sum(axis=1)
    colsnotzero = num.where([ item != 0 or item != n_nodes for item in columns ])[0]
    rowsnotzero = num.where([ item != 0 or item != n_nodes for item in rows ])[0]
    if len(colsnotzero) > 0 and len(rowsnotzero) > 0:
        for cntr in xrange(maximum):
            logging.debug('    Initiating...')
            randomrow = rowsnotzero[num.random.randint(len(rowsnotzero))]
            randomcol = colsnotzero[num.random.randint(len(colsnotzero))]
            logging.debug('Selected item:')
            logging.debug((randomrow, randomcol))
            adj_debug = num.array(adj[:], dtype=str)
            logging.debug(adj_debug)
            adj_debug[randomrow][randomcol] = '1'
            boolean = adj[randomrow][randomcol]
            row = adj[randomrow, :]
            col = adj[:, randomcol]
            colitemsnot = num.where(col != boolean)[0]
            rowitemsnot = num.where(row != boolean)[0]
            randomrowitem = rowitemsnot[num.random.randint(len(rowitemsnot))]
            randomcolitem = colitemsnot[num.random.randint(len(colitemsnot))]
            if adj[randomrowitem][randomcolitem] == boolean:
                adj[(randomrowitem, randomcolitem)] = not adj[(randomrowitem, randomcolitem)]
                adj[(randomcolitem, randomcol)] = not adj[(randomcolitem, randomcol)]
                adj[(randomrow, randomrowitem)] = not adj[(randomrow, randomrowitem)]
                adj[(randomrow, randomcol)] = not adj[(randomrow, randomcol)]
                logging.debug('New Network:')
                logging.debug(num.array(adj[:], dtype=str))
                if network.is_connected():
                    return network

        logging.info('This network ' + str(network) + 'is unlikely to have a degree preserving                      mutation. The network is returned as is.')
    else:
        logging.info('Network ' + str(network) + " evolved such that there's no connection left.                      The network is returned as is.")


def degree_preserving_mutation(network, maximum=0, def_mutation=False):
    """
    A mutation that preserves the degree of the network in concern.
    """
    import numpy as num, logging
    adj = network.adjacency
    n_nodes = len(adj)
    logging.debug('Adjacency Matrix:')
    logging.debug(adj)
    if maximum == 0:
        maximum = 10 * len(adj) ** 2
    columns = adj.sum(axis=0)
    rows = adj.sum(axis=1)
    colsnotzero = num.where([ item != 0 and item != n_nodes for item in columns ])[0]
    rowsnotzero = num.where([ item != 0 and item != n_nodes for item in rows ])[0]
    logging.debug('Columns that are non zero and full:')
    logging.debug(colsnotzero)
    logging.debug('Rows that are non zero and full:')
    logging.debug(rowsnotzero)
    if len(colsnotzero) > 0 and len(rowsnotzero) > 0:
        for cntr in xrange(maximum):
            logging.debug('    Initiating...')
            randomrow = rowsnotzero[num.random.randint(len(rowsnotzero))]
            randomcol = colsnotzero[num.random.randint(len(colsnotzero))]
            logging.debug('Selected item:')
            logging.debug((randomrow, randomcol))
            adj_debug = num.array(adj[:], dtype=str)
            logging.debug(adj_debug)
            adj_debug[randomrow][randomcol] = '1'
            boolean = adj[randomrow][randomcol]
            row = adj[randomrow, :]
            col = adj[:, randomcol]
            colitemsnot = num.where(col != boolean)[0]
            rowitemsnot = num.where(row != boolean)[0]
            randomrowitem = rowitemsnot[num.random.randint(len(rowitemsnot))]
            randomcolitem = colitemsnot[num.random.randint(len(colitemsnot))]
            adj_debug[(randomcolitem, randomcol)] = '2'
            adj_debug[(randomrow, randomrowitem)] = '3'
            adj_debug[(randomcolitem, randomrowitem)] = '4'
            logging.debug(adj_debug)
            if adj[randomcolitem][randomrowitem] == boolean:
                logging.debug('Success!')
                adj[(randomcolitem, randomrowitem)] = not adj[(randomcolitem, randomrowitem)]
                adj[(randomcolitem, randomcol)] = not adj[(randomcolitem, randomcol)]
                adj[(randomrow, randomrowitem)] = not adj[(randomrow, randomrowitem)]
                adj[(randomrow, randomcol)] = not adj[(randomrow, randomcol)]
                logging.debug('New Network:')
                logging.debug(num.array(adj[:], dtype=str))
                return network

        logging.info('This network ' + str(network) + 'is unlikely to have a degree preserving                      mutation. The network is returned as is.')
    else:
        logging.info('Network ' + str(network) + " evolved such that there's no connection left.                      The network is returned as is.")