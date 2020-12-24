# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/templatetags/nearbeach_extras.py
# Compiled at: 2020-05-03 01:13:24
# Size of source mod 2**32: 3139 bytes
import datetime, pytz
from django.utils import timezone
from django.conf import settings
from django.template import Library
register = Library()
from NearBeach.models import *

@register.filter(name='filter_assigned_project')
def filter_assigned_project(value, arg):
    """

    :param value: Use "object_assignment" table
    :param arg: What task ID are we focusing on
    :return:
    """
    return value.filter(project_id__isnull=False,
      task_id=arg)


@register.filter(name='filter_assigned_task')
def filter_assigned_task(value, arg):
    """

    :param value:
    :param arg:
    :return:
    """
    return value.filter(task_id__isnull=False,
      project_id=arg)


@register.filter(name='filter_level_cards')
def filter_level_cards(value, arg):
    """
    :param value: this is the python object being passed through
    :param arg: these are the co-ordinates [column,level]
    :return: the filtered python object
    """
    return value.filter(kanban_level=arg)


@register.filter(name='filter_column_cards')
def filter_column_cards(value, arg):
    """
    :param value: this is the python object being passed through
    :param arg: these are the co-ordinates [column,level]
    :return: the filtered python object
    """
    return value.filter(kanban_column=arg)


@register.filter(name='filter_requirement_items')
def filter_requirement_items(value, arg):
    """
    :param value: this is the python object being passed through
    :param arg: this is the requirement_id we will filter by
    :return: the filtered python object
    """
    return value.filter(is_deleted='FALSE')


@register.filter(name='filter_requirement_item_cards')
def filter_requirement_item_cards(value, arg):
    """
    :param value: this is the python object being passed through
    :param arg: these are the stages of the requirement_item ['draft']
    :return: the filtered python object i.e. ['draft']
    """
    return value.filter(requirement_item_status=arg)


@register.filter
def hours_ago(time, hours):
    """
    :param time:
    :param hours:
    :return:
    """
    location = pytz.timezone(settings.TIME_ZONE)
    local_time = location.localize(datetime.datetime.now())
    try:
        return local_time - time > -datetime.timedelta(hours=hours)
    except:
        return datetime.datetime.now() - time > -datetime.timedelta(hours=hours)


@register.filter
def in_future--- This code section failed: ---

 L. 102         0  LOAD_GLOBAL              pytz
                2  LOAD_METHOD              timezone
                4  LOAD_GLOBAL              settings
                6  LOAD_ATTR                TIME_ZONE
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'location'

 L. 103        12  LOAD_FAST                'location'
               14  LOAD_METHOD              localize
               16  LOAD_GLOBAL              datetime
               18  LOAD_ATTR                datetime
               20  LOAD_METHOD              now
               22  CALL_METHOD_0         0  ''
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'local_time'

 L. 105        28  SETUP_FINALLY        52  'to 52'

 L. 106        30  LOAD_FAST                'local_time'
               32  LOAD_GLOBAL              datetime
               34  LOAD_ATTR                timedelta
               36  LOAD_FAST                'hours'
               38  LOAD_CONST               ('hours',)
               40  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               42  BINARY_ADD       
               44  LOAD_FAST                'time'
               46  COMPARE_OP               <
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    28  '28'

 L. 107        52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 108        58  POP_EXCEPT       
               60  LOAD_CONST               False
               62  RETURN_VALUE     
               64  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 58


@register.filter
def task_related_groups(task_id):
    """

    :param task_id:
    :return:
    """
    group_results = group.objects.filter(is_deleted='FALSE',
      group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id,
      group_id__isnull=False).values('group_id')))
    return group_results