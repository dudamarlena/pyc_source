# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/acl/core.py
# Compiled at: 2009-04-26 16:10:38
"""
Base definitions for the Access Control Lists handling.

"""

class ACE(object):
    """
    Access Control Entry.
    
    """
    decisions = {'deny': -1, 
       'allow': 1}

    def __init__(self, aro, operation, decision, condition=None, reason=None):
        """
        
        :param aro: The ARO/subject(s) this ACE applies to.
        :param operation: The target operation on the resource in question.
        :param decision: The ACE decision (i.e., allow or deny) to be used
            when the ARO is found; see :attr:`decisions`.
        :param condition: The condition that must be met for this ACE's decision
            to be taken into account (a predicate checker or a TALES string).
        :param reason: A comment that explains the ``decision``.
        
        """
        self.aro = aro
        self.operation = operation
        self.decision = decision
        self.condition = condition
        self.reason = reason


class ACL(object):
    """
    Access Control List.
    
    The collection of Access Control Entries (ACEs) assigned to a given Access
    Control Object (ACO).
    
    """

    def __init__(self, aco, aces, recursive=True):
        """
        
        :param aces: The ACEs that make up this ACL.
        
        """
        self.aces = list(aces)
        self.recursive = recursive


class AccessManager(object):

    def __init__(self, app_aco, acl_collection):
        self.app_aco = app_aco
        self.acl_collection = acl_collection

    def check_authorization(self, aco, aro, request):
        """
        Check if the ``aro`` can access ``aco`` via ``request``.
        
        """
        accepted_by_somebody = False
        for ace in self.acl_collection.filter_aces(aco, aro, include_parents=True):
            if not ace.condition_is_met(request):
                continue
            if ace.decision == ACE.decisions['deny']:
                return False
            assert ace.decision == ACE.decisions['allow']
            accepted_by_somebody = True

        if accepted_by_somebody:
            return True
        return self.acl_collection.fallback_decision