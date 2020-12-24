# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/models.py
# Compiled at: 2016-03-14 09:45:17
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Workflow(models.Model):
    """
    For storing Work flow description
    """
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    tasktitle = models.CharField(max_length=100, null=True)

    def __str__(self):
        return (b'Workflow-{}').format(self.id)


class State(models.Model):
    """
    For storing various states of a work flow
    """
    workflow_id = models.ForeignKey(Workflow)
    title = models.CharField(max_length=100)
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    is_automated = models.BooleanField(default=False)

    def __str__(self):
        return (b'State-{}').format(self.id)


class Transition(models.Model):
    """
    For storing various states of a work flow
    """
    workflow_id = models.ForeignKey(Workflow)
    state_id = models.ForeignKey(State)
    action = models.CharField(max_length=100)
    next_state = models.ForeignKey(State, related_name=b'next_state_id')

    def __str__(self):
        return (b'State-{}').format(self.id)


class Task(models.Model):
    """
    Task created by a user
    """
    created_by = models.ForeignKey(User)
    workflow_id = models.ForeignKey(Workflow)
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=300)
    current_state = models.ForeignKey(State, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (b'Task-{}').format(self.id)


class Assignee(models.Model):
    task_id = models.ForeignKey(Task)
    assignee = models.ForeignKey(User, related_name=b'assignee_id')
    assigned_by = models.ForeignKey(User, related_name=b'assigned_by')

    def __str__(self):
        return (b'Assignee-{}').format(self.id)


class Permission(models.Model):
    task_id = models.ForeignKey(Task)
    allow_access = models.CharField(max_length=300, null=True)
    deny_access = models.CharField(max_length=300, null=True)

    def __str__(self):
        return (b'Permission-{}').format(self.id)