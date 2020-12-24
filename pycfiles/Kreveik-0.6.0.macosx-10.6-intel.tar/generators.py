# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/network/generators.py
# Compiled at: 2012-09-09 23:45:49
"""
family.motifs module
====================
Functions that concern motifs. 

Functions
---------
    create:Generate a network by giving adjacency matrix, the propogator (boolean function) 
    and the mask. 
    
    random:Generates a network with random adjacency matrix.(Configuration.)
    
"""

def create(adjacency_matrix, bool_fcn, function):
    """
    Generates and returns a network with a given adjacency matrix. The initial state 
    is populated with 0's. 
    
    Input Variables:
    ----------------
    
    adjacency_matrix
        The matrix composed of adjacency values between the nodes.
    bool_fcn
        Mask function
    """
    import numpy as num
    from kreveik.classes import Network
    initial_state = num.array([len(adjacency_matrix) * [False]])
    new_network = Network(adjacency_matrix, bool_fcn, function, state_vec=initial_state)
    return new_network


def random(n_nodes, function, probability=(0.5, 0.5, 0.5), connected=False, howmany=1):
    """
    Generates and returns a random network with a random initial conditions.
    The adjacency matrix, initial state, boolean function are populated with 
    1's and 0's with probabilities of 0.5.
    
    Input Variables:
    ---------------
    
    n_nodes        
        Number of nodes in the system.
    function
        A function which maps the state of a network to another. 
    probability (a,b,c)
        (a) The probability of having a connection in any two nodes 
            Defaults to 0.5 
        (b) The probability of having an initial state of a node True.
            Defaults to 0.5
        (c) The probability of having a Boolean function key element True.
            Defaults to 0.5
    connected
        if True, only fully connected networks are generated. Defaults to False.
    howmany
        the number of networks that will be generated. Defaults to 1.
    """
    import numpy as num, kreveik, logging
    num.random.seed()
    adjacency_matrix = num.random.random((n_nodes, n_nodes)) < probability[0]
    state = num.random.random((1, n_nodes)) < probability[1]
    bool_fcn = num.random.random((n_nodes, n_nodes)) < probability[2]
    new_network = kreveik.classes.Network(adjacency_matrix, bool_fcn, function, state_vec=state)
    if connected == False:
        try:
            logging.info('Generating one network of node count ' + str(n_nodes))
            return new_network
        except ValueError as e:
            z = e
            logging.error('Network is too big to model.')
            print z

    elif new_network.is_connected():
        try:
            logging.info('Generating one network of node count ' + str(n_nodes))
            return new_network
        except ValueError as e:
            z = e
            logging.error('Network is too big to model.')
            print z

    else:
        while not new_network.is_connected():
            num.random.seed()
            adjacency_matrix = num.random.random((n_nodes, n_nodes)) < probability[0]
            state = num.random.random((1, n_nodes)) < probability[1]
            bool_fcn = num.random.random((n_nodes, n_nodes)) < probability[2]
            new_network = kreveik.classes.Network(adjacency_matrix, bool_fcn, function, state_vec=state)

        try:
            logging.info('Generating one network of node count ' + str(n_nodes))
            return new_network
        except ValueError as e:
            z = e
            logging.error('Network is too big to model.')
            print z

    return new_network


__all__ = [
 create, random]