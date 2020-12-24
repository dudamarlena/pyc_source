# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/views_whiteboard.py
# Compiled at: 2020-03-01 01:12:07
# Size of source mod 2**32: 5672 bytes
"""
VIEWS - task information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the TASK INFORMATION MODULES. This is to help keep the VIEWS
file clean from AJAX (spray and wipe).
"""
from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.template import loader
from NearBeach.forms import *
from .models import *
from django.db.models import Q
from .misc_functions import *
from .user_permissions import return_user_permission_level
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def whiteboard_common_xml(request):
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_common.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_graph_xml(request):
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_graph.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_editor_xml(request):
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_editor.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_information--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL              object_assignment
                2  LOAD_ATTR                objects
                4  LOAD_ATTR                filter

 L.  67         6  LOAD_STR                 'FALSE'

 L.  68         8  LOAD_FAST                'whiteboard_id'
               10  LOAD_CONST               ('is_deleted', 'whiteboard_id')
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_FAST               'whiteboard_object_results'

 L.  71        16  LOAD_GLOBAL              object_assignment
               18  LOAD_ATTR                objects
               20  LOAD_METHOD              filter

 L.  72        22  LOAD_GLOBAL              Q

 L.  73        24  LOAD_STR                 'FALSE'
               26  LOAD_CONST               ('is_deleted',)
               28  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  74        30  LOAD_GLOBAL              Q

 L.  95        32  LOAD_GLOBAL              Q
               34  LOAD_FAST                'whiteboard_object_results'
               36  LOAD_ATTR                filter
               38  LOAD_CONST               False
               40  LOAD_CONST               ('task_id__isnull',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  LOAD_METHOD              values
               46  LOAD_STR                 'task_id'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  LOAD_CONST               ('task_id__in',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  LOAD_GLOBAL              Q
               56  LOAD_FAST                'whiteboard_object_results'
               58  LOAD_ATTR                filter
               60  LOAD_CONST               False
               62  LOAD_CONST               ('project_id__isnull',)
               64  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               66  LOAD_METHOD              values
               68  LOAD_STR                 'project_id'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  LOAD_CONST               ('project_id__in',)
               74  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               76  BINARY_OR        
               78  LOAD_GLOBAL              Q
               80  LOAD_FAST                'whiteboard_object_results'
               82  LOAD_ATTR                filter
               84  LOAD_CONST               False
               86  LOAD_CONST               ('requirement_id__isnull',)
               88  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               90  LOAD_METHOD              values
               92  LOAD_STR                 'requirement_id'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  LOAD_CONST               ('requirement_id__in',)
               98  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              100  BINARY_OR        
              102  LOAD_GLOBAL              Q
              104  LOAD_FAST                'whiteboard_object_results'
              106  LOAD_ATTR                filter
              108  LOAD_CONST               False
              110  LOAD_CONST               ('request_for_change__isnull',)
              112  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              114  LOAD_METHOD              values
              116  LOAD_STR                 'request_for_change'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  LOAD_CONST               ('request_for_change__in',)
              122  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              124  BINARY_OR        
              126  LOAD_GLOBAL              Q

 L.  97       128  LOAD_FAST                'whiteboard_object_results'
              130  LOAD_ATTR                filter

 L.  98       132  LOAD_CONST               False
              134  LOAD_CONST               ('opportunity_id__isnull',)
              136  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              138  LOAD_METHOD              values

 L.  99       140  LOAD_STR                 'opportunity_id'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  LOAD_CONST               ('opportunity_id__in',)
              146  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              148  BINARY_OR        
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  BINARY_AND       
              154  CALL_METHOD_1         1  '1 positional argument'
              156  LOAD_METHOD              values

 L. 102       158  LOAD_STR                 'group_id_id'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  STORE_FAST               'whiteboard_group_results'

 L. 104       164  LOAD_GLOBAL              return_user_permission_level

 L. 105       166  LOAD_FAST                'request'

 L. 106       168  LOAD_FAST                'whiteboard_group_results'

 L. 108       170  LOAD_STR                 'project'

 L. 109       172  LOAD_STR                 'task'

 L. 110       174  LOAD_STR                 'requirement'

 L. 111       176  LOAD_STR                 'request_for_change'

 L. 112       178  LOAD_STR                 'opportunity'
              180  BUILD_LIST_5          5 
              182  CALL_FUNCTION_3       3  '3 positional arguments'
              184  STORE_FAST               'permission_results'

 L. 117       186  LOAD_FAST                'permission_results'
              188  LOAD_STR                 'project'
              190  BINARY_SUBSCR    
              192  LOAD_CONST               0
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_TRUE    248  'to 248'

 L. 118       198  LOAD_FAST                'permission_results'
              200  LOAD_STR                 'task'
              202  BINARY_SUBSCR    
              204  LOAD_CONST               0
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_TRUE    248  'to 248'

 L. 119       210  LOAD_FAST                'permission_results'
              212  LOAD_STR                 'requirement'
              214  BINARY_SUBSCR    
              216  LOAD_CONST               0
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_TRUE    248  'to 248'

 L. 120       222  LOAD_FAST                'permission_results'
              224  LOAD_STR                 'request_for_change'
              226  BINARY_SUBSCR    
              228  LOAD_CONST               0
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_TRUE    248  'to 248'

 L. 121       234  LOAD_FAST                'permission_results'
              236  LOAD_STR                 'opportunity'
              238  BINARY_SUBSCR    
              240  LOAD_CONST               0
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   260  'to 260'
            248_0  COME_FROM           232  '232'
            248_1  COME_FROM           220  '220'
            248_2  COME_FROM           208  '208'
            248_3  COME_FROM           196  '196'

 L. 123       248  LOAD_GLOBAL              HttpResponseRedirect
              250  LOAD_GLOBAL              reverse
              252  LOAD_STR                 'permission_denied'
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  RETURN_VALUE     
            260_0  COME_FROM           244  '244'

 L. 126       260  LOAD_GLOBAL              get_object_or_404
              262  LOAD_GLOBAL              whiteboard
              264  LOAD_FAST                'whiteboard_id'
              266  LOAD_CONST               ('whiteboard_id',)
              268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              270  STORE_FAST               'whiteboard_results'

 L. 129       272  LOAD_GLOBAL              loader
              274  LOAD_METHOD              get_template
              276  LOAD_STR                 'NearBeach/whiteboard/whiteboard_information.html'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  STORE_FAST               't'

 L. 133       282  LOAD_FAST                'whiteboard_results'

 L. 134       284  LOAD_FAST                'whiteboard_id'

 L. 135       286  LOAD_FAST                'permission_results'

 L. 136       288  LOAD_FAST                'permission_results'
              290  LOAD_STR                 'new_item'
              292  BINARY_SUBSCR    

 L. 137       294  LOAD_FAST                'permission_results'
              296  LOAD_STR                 'administration'
              298  BINARY_SUBSCR    
              300  LOAD_CONST               ('whiteboard_results', 'whiteboard_id', 'permission_results', 'new_item_permission', 'administration_permission')
              302  BUILD_CONST_KEY_MAP_5     5 
              304  STORE_FAST               'c'

 L. 140       306  LOAD_GLOBAL              HttpResponse
              308  LOAD_FAST                't'
              310  LOAD_METHOD              render
              312  LOAD_FAST                'c'
              314  LOAD_FAST                'request'
              316  CALL_METHOD_2         2  '2 positional arguments'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 320


@login_required(login_url='login')
def whiteboard_save(request, whiteboard_id):
    if request.method == 'POST':
        whiteboard_update = whiteboard.objects.get(whiteboard_id=whiteboard_id)
        whiteboard_update.whiteboard_xml = request.POST['whiteboard_xml']
        whiteboard_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this function only requests POST')


@login_required(login_url='login')
def whiteboard_toolbar_xml(request):
    print('Made contact with Whiteboard POST :)')
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_toolbar.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')