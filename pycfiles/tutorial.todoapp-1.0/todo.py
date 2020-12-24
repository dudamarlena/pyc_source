# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/tutorial.todoapp/src/tutorial/todoapp/browser/todo.py
# Compiled at: 2012-09-05 10:51:38
"""A Folder view that lists Todo Items."""
from five import grok
from plone import api
from plone.dexterity.content import Item
from Products.ATContentTypes.interface import IATFolder
import json
grok.templatedir('.')

class Todo(grok.View):
    """A BrowserView to display the Todo listing on a Folder."""
    grok.context(IATFolder)
    grok.require('zope2.View')


class WorkflowTransition(grok.View):
    """
    Change the state of an item. The context is implied by the url.
    Returns state of the object after the transition, and possible
    transitions in that state
    """
    grok.context(Item)
    grok.require('zope2.View')
    grok.name('update_workflow')

    def render(self):
        transition = self.request.form.get('transition', '')
        results = {'results': None, 'success': False, 
           'message': ''}
        if transition:
            try:
                api.content.transition(self.context, transition=transition)
                results['success'] = True
            except api.exc.InvalidParameterError as e:
                results['message'] = '%s' % e

            results['results'] = {'state': api.content.get_state(self.context), 
               'transitions': self.get_possible_transitions(self.context)}
        self.request.response.setHeader('Content-Type', 'application/json; charset=utf-8')
        return json.dumps(results)

    def get_possible_transitions(self, item):
        """
        Return the posible transitions for an item. This should
        eventually get out of this tutorial, since its NASTY.
        """
        workflow_tool = api.portal.get_tool('portal_workflow')
        items = workflow_tool.getTransitionsFor(item)
        return [ item['id'] for item in items ]