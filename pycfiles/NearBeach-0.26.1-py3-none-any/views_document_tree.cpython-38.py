# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/views_document_tree.py
# Compiled at: 2020-05-03 01:13:24
# Size of source mod 2**32: 13886 bytes
from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from django.db.models import Q
from .user_permissions import return_user_permission_level
import simplejson

@login_required(login_url='login', redirect_field_name='')
def delete_document(request, document_key):
    if request.method == 'POST':
        document_instance = document.objects.get(document_key=document_key)
        document_instance.is_deleted = 'TRUE'
        document_instance.change_user = request.user
        document_instance.save()
        document_permission_save = document_permission.objects.get(document_key=document_key)
        document_permission_save.is_deleted = 'TRUE'
        document_permission_save.change_user = request.user
        document_permission_save.save()
        print('Deleted Document: ' + document_key)
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Can only do this action in post.')


@login_required(login_url='login', redirect_field_name='')
def delete_folder(request, folder_id):
    if request.method == 'POST':
        folder_results = folder.objects.get(folder_id=folder_id)
        folder_results.is_deleted = 'TRUE'
        folder_results.change_user = request.user
        folder_results.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this request has to be post')


@login_required(login_url='login', redirect_field_name='')
def document_tree_folder--- This code section failed: ---

 L.  59         0  LOAD_FAST                'request'
                2  LOAD_ATTR                method
                4  LOAD_STR                 'POST'
                6  COMPARE_OP               ==
             8_10  POP_JUMP_IF_FALSE   370  'to 370'

 L.  60        12  LOAD_GLOBAL              new_folder_form
               14  LOAD_FAST                'request'
               16  LOAD_ATTR                POST
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'form'

 L.  61        22  LOAD_FAST                'form'
               24  LOAD_METHOD              is_valid
               26  CALL_METHOD_0         0  ''
            28_30  POP_JUMP_IF_FALSE   350  'to 350'

 L.  62        32  LOAD_GLOBAL              folder

 L.  63        34  LOAD_FAST                'form'
               36  LOAD_ATTR                cleaned_data
               38  LOAD_STR                 'folder_description'
               40  BINARY_SUBSCR    

 L.  64        42  LOAD_FAST                'request'
               44  LOAD_ATTR                user

 L.  62        46  LOAD_CONST               ('folder_description', 'change_user')
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  STORE_FAST               'folder_submit'

 L.  67        52  LOAD_FAST                'folder_id'
               54  LOAD_STR                 ''
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_TRUE     84  'to 84'
               60  LOAD_FAST                'folder_id'
               62  LOAD_CONST               None
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_TRUE     84  'to 84'
               68  LOAD_FAST                'folder_id'
               70  LOAD_STR                 '0'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_TRUE     84  'to 84'
               76  LOAD_FAST                'folder_id'
               78  LOAD_CONST               0
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    94  'to 94'
             84_0  COME_FROM            74  '74'
             84_1  COME_FROM            66  '66'
             84_2  COME_FROM            58  '58'

 L.  68        84  LOAD_GLOBAL              print
               86  LOAD_STR                 'There is a bug in python here'
               88  CALL_FUNCTION_1       1  ''
               90  POP_TOP          
               92  JUMP_FORWARD        126  'to 126'
             94_0  COME_FROM            82  '82'

 L.  70        94  LOAD_GLOBAL              print
               96  LOAD_STR                 'FOLDER ID = '
               98  LOAD_GLOBAL              str
              100  LOAD_FAST                'folder_id'
              102  CALL_FUNCTION_1       1  ''
              104  BINARY_ADD       
              106  CALL_FUNCTION_1       1  ''
              108  POP_TOP          

 L.  71       110  LOAD_GLOBAL              folder
              112  LOAD_ATTR                objects
              114  LOAD_ATTR                get
              116  LOAD_FAST                'folder_id'
              118  LOAD_CONST               ('folder_id',)
              120  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              122  LOAD_FAST                'folder_submit'
              124  STORE_ATTR               parent_folder_id
            126_0  COME_FROM            92  '92'

 L.  73       126  LOAD_FAST                'destination'
              128  LOAD_STR                 'project'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   152  'to 152'

 L.  74       134  LOAD_GLOBAL              project
              136  LOAD_ATTR                objects
              138  LOAD_ATTR                get
              140  LOAD_FAST                'location_id'
              142  LOAD_CONST               ('project_id',)
              144  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              146  LOAD_FAST                'folder_submit'
              148  STORE_ATTR               project_id
              150  JUMP_FORWARD        312  'to 312'
            152_0  COME_FROM           132  '132'

 L.  75       152  LOAD_FAST                'destination'
              154  LOAD_STR                 'task'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   178  'to 178'

 L.  76       160  LOAD_GLOBAL              task
              162  LOAD_ATTR                objects
              164  LOAD_ATTR                get
              166  LOAD_FAST                'location_id'
              168  LOAD_CONST               ('task_id',)
              170  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              172  LOAD_FAST                'folder_submit'
              174  STORE_ATTR               task_id
              176  JUMP_FORWARD        312  'to 312'
            178_0  COME_FROM           158  '158'

 L.  77       178  LOAD_FAST                'destination'
              180  LOAD_STR                 'customer'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   204  'to 204'

 L.  78       186  LOAD_GLOBAL              customer
              188  LOAD_ATTR                objects
              190  LOAD_ATTR                get
              192  LOAD_FAST                'location_id'
              194  LOAD_CONST               ('customer_id',)
              196  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              198  LOAD_FAST                'folder_submit'
              200  STORE_ATTR               customer_id
              202  JUMP_FORWARD        312  'to 312'
            204_0  COME_FROM           184  '184'

 L.  79       204  LOAD_FAST                'destination'
              206  LOAD_STR                 'organisation'
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   230  'to 230'

 L.  80       212  LOAD_GLOBAL              organisation
              214  LOAD_ATTR                objects
              216  LOAD_ATTR                get
              218  LOAD_FAST                'location_id'
              220  LOAD_CONST               ('organisation_id',)
              222  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              224  LOAD_FAST                'folder_submit'
              226  STORE_ATTR               organisation_id
              228  JUMP_FORWARD        312  'to 312'
            230_0  COME_FROM           210  '210'

 L.  81       230  LOAD_FAST                'destination'
              232  LOAD_STR                 'requirement'
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   258  'to 258'

 L.  82       240  LOAD_GLOBAL              requirement
              242  LOAD_ATTR                objects
              244  LOAD_ATTR                get
              246  LOAD_FAST                'location_id'
              248  LOAD_CONST               ('requirement_id',)
              250  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              252  LOAD_FAST                'folder_submit'
              254  STORE_ATTR               requirement
              256  JUMP_FORWARD        312  'to 312'
            258_0  COME_FROM           236  '236'

 L.  83       258  LOAD_FAST                'destination'
              260  LOAD_STR                 'requirement_item'
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   286  'to 286'

 L.  84       268  LOAD_GLOBAL              requirement_item
              270  LOAD_ATTR                objects
              272  LOAD_ATTR                get
              274  LOAD_FAST                'location_id'
              276  LOAD_CONST               ('requirement_item_id',)
              278  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              280  LOAD_FAST                'folder_submit'
              282  STORE_ATTR               requirement_item
              284  JUMP_FORWARD        312  'to 312'
            286_0  COME_FROM           264  '264'

 L.  85       286  LOAD_FAST                'destination'
              288  LOAD_STR                 'request_for_change'
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   312  'to 312'

 L.  86       296  LOAD_GLOBAL              request_for_change
              298  LOAD_ATTR                objects
              300  LOAD_ATTR                get
              302  LOAD_FAST                'location_id'
              304  LOAD_CONST               ('rfc_id',)
              306  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              308  LOAD_FAST                'folder_submit'
              310  STORE_ATTR               request_for_change
            312_0  COME_FROM           292  '292'
            312_1  COME_FROM           284  '284'
            312_2  COME_FROM           256  '256'
            312_3  COME_FROM           228  '228'
            312_4  COME_FROM           202  '202'
            312_5  COME_FROM           176  '176'
            312_6  COME_FROM           150  '150'

 L.  88       312  LOAD_FAST                'folder_submit'
              314  LOAD_METHOD              save
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          

 L.  91       320  LOAD_GLOBAL              loader
              322  LOAD_METHOD              get_template
              324  LOAD_STR                 'NearBeach/blank.html'
              326  CALL_METHOD_1         1  ''
              328  STORE_FAST               't'

 L.  93       330  BUILD_MAP_0           0 
              332  STORE_FAST               'c'

 L.  95       334  LOAD_GLOBAL              HttpResponse
              336  LOAD_FAST                't'
              338  LOAD_METHOD              render
              340  LOAD_FAST                'c'
              342  LOAD_FAST                'request'
              344  CALL_METHOD_2         2  ''
              346  CALL_FUNCTION_1       1  ''
              348  RETURN_VALUE     
            350_0  COME_FROM            28  '28'

 L.  97       350  LOAD_GLOBAL              print
              352  LOAD_FAST                'form'
              354  LOAD_ATTR                errors
              356  CALL_FUNCTION_1       1  ''
              358  POP_TOP          

 L.  98       360  LOAD_GLOBAL              HttpResponseBadRequest
              362  LOAD_STR                 'Form not valid'
              364  CALL_FUNCTION_1       1  ''
              366  RETURN_VALUE     
              368  JUMP_FORWARD        378  'to 378'
            370_0  COME_FROM             8  '8'

 L. 100       370  LOAD_GLOBAL              HttpResponseBadRequest
              372  LOAD_STR                 'Requst must be a POST'
              374  CALL_FUNCTION_1       1  ''
              376  RETURN_VALUE     
            378_0  COME_FROM           368  '368'

Parse error at or near `JUMP_FORWARD' instruction at offset 92


@login_required(login_url='login', redirect_field_name='')
def document_tree_list(request, location_id, destination, folder_id=''):
    permission_results = return_user_permission_level(request, None, destination)
    if destination == 'project':
        folder_results = folder.objects.filter(is_deleted='FALSE',
          project_id=location_id)
        document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
          project_id=location_id)
    else:
        if destination == 'task':
            folder_results = folder.objects.filter(is_deleted='FALSE',
              task_id=location_id)
            document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
              task_id=location_id)
        else:
            if destination == 'customer':
                folder_results = folder.objects.filter(is_deleted='FALSE',
                  customer_id=location_id)
                document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
                  customer_id=location_id)
            else:
                if destination == 'organisation':
                    folder_results = folder.objects.filter(is_deleted='FALSE',
                      organisation_id=location_id)
                    document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
                      organisation_id=location_id)
                else:
                    if destination == 'requirement':
                        folder_results = folder.objects.filter(is_deleted='FALSE',
                          requirement_id=location_id)
                        document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
                          requirement_id=location_id)
                    else:
                        if destination == 'requirement_item':
                            folder_results = folder.objects.filter(is_deleted='FALSE',
                              requirement_item=location_id)
                            document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
                              requirement_item=location_id)
                        else:
                            if destination == 'request_for_change':
                                folder_results = folder.objects.filter(is_deleted='FALSE',
                                  request_for_change=location_id)
                                document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
                                  request_for_change=location_id)
                            elif folder_id:
                                folder_results = folder_results.filter(parent_folder_id=folder_id)
                                document_permission_results = document_permission_results.filter(folder_id=folder_id)
                                current_folder_results = folder.objects.get(folder_id=folder_id)
                            else:
                                folder_results = folder_results.filter(parent_folder_id__isnull=True)
                                document_permission_results = document_permission_results.filter(folder_id__isnull=True)
                                folder_id = 0
                                current_folder_results = ''
                            t = loader.get_template('NearBeach/document_tree/document_tree_list.html')
                            c = {'document_permission_results':document_permission_results, 
                             'folder_results':folder_results, 
                             'destination':destination, 
                             'location_id':location_id, 
                             'folder_id':folder_id, 
                             'document_upload_form':document_upload_form(), 
                             'document_url_form':document_url_form(), 
                             'new_folder_form':new_folder_form(), 
                             'new_whiteboard_form':new_whiteboard_form(), 
                             'current_folder_results':current_folder_results, 
                             'permission_results':permission_results[destination]}
                            return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def document_tree_upload--- This code section failed: ---

 L. 204         0  LOAD_FAST                'request'
                2  LOAD_ATTR                method
                4  LOAD_STR                 'POST'
                6  COMPARE_OP               ==
             8_10  POP_JUMP_IF_FALSE   458  'to 458'

 L. 205        12  LOAD_FAST                'request'
               14  LOAD_ATTR                FILES
               16  LOAD_CONST               None
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 206        22  LOAD_GLOBAL              HttpResponseBadRequest
               24  LOAD_STR                 'File needs to be uploaded'
               26  CALL_FUNCTION_1       1  ''
               28  RETURN_VALUE     
             30_0  COME_FROM            20  '20'

 L. 208        30  LOAD_GLOBAL              document_upload_form
               32  LOAD_FAST                'request'
               34  LOAD_ATTR                POST
               36  LOAD_FAST                'request'
               38  LOAD_ATTR                FILES
               40  CALL_FUNCTION_2       2  ''
               42  STORE_FAST               'form'

 L. 209        44  LOAD_FAST                'form'
               46  LOAD_METHOD              is_valid
               48  CALL_METHOD_0         0  ''
            50_52  POP_JUMP_IF_FALSE   438  'to 438'

 L. 211        54  LOAD_FAST                'form'
               56  LOAD_ATTR                cleaned_data
               58  LOAD_STR                 'document'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'file'

 L. 212        64  LOAD_FAST                'form'
               66  LOAD_ATTR                cleaned_data
               68  LOAD_STR                 'document_description'
               70  BINARY_SUBSCR    
               72  STORE_FAST               'document_description'

 L. 215        74  LOAD_FAST                'document_description'
               76  LOAD_STR                 ''
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 216        82  LOAD_GLOBAL              str
               84  LOAD_FAST                'file'
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'document_description'
             90_0  COME_FROM            80  '80'

 L. 217        90  LOAD_FAST                'file'
               92  LOAD_ATTR                size
               94  STORE_FAST               'file_size'

 L. 222        96  LOAD_GLOBAL              document

 L. 223        98  LOAD_FAST                'document_description'

 L. 224       100  LOAD_FAST                'file'

 L. 225       102  LOAD_FAST                'request'
              104  LOAD_ATTR                user

 L. 222       106  LOAD_CONST               ('document_description', 'document', 'change_user')
              108  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              110  STORE_FAST               'document_submit'

 L. 227       112  LOAD_FAST                'document_submit'
              114  LOAD_METHOD              save
              116  CALL_METHOD_0         0  ''
              118  POP_TOP          

 L. 229       120  LOAD_GLOBAL              document_permission

 L. 230       122  LOAD_FAST                'document_submit'

 L. 231       124  LOAD_FAST                'request'
              126  LOAD_ATTR                user

 L. 229       128  LOAD_CONST               ('document_key', 'change_user')
              130  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              132  STORE_FAST               'document_permissions_submit'

 L. 233       134  LOAD_FAST                'destination'
              136  LOAD_STR                 'project'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   160  'to 160'

 L. 234       142  LOAD_GLOBAL              project
              144  LOAD_ATTR                objects
              146  LOAD_ATTR                get
              148  LOAD_FAST                'location_id'
              150  LOAD_CONST               ('project_id',)
              152  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              154  LOAD_FAST                'document_permissions_submit'
              156  STORE_ATTR               project_id
              158  JUMP_FORWARD        320  'to 320'
            160_0  COME_FROM           140  '140'

 L. 235       160  LOAD_FAST                'destination'
              162  LOAD_STR                 'task'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   186  'to 186'

 L. 236       168  LOAD_GLOBAL              task
              170  LOAD_ATTR                objects
              172  LOAD_ATTR                get
              174  LOAD_FAST                'location_id'
              176  LOAD_CONST               ('task_id',)
              178  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              180  LOAD_FAST                'document_permissions_submit'
              182  STORE_ATTR               task_id
              184  JUMP_FORWARD        320  'to 320'
            186_0  COME_FROM           166  '166'

 L. 237       186  LOAD_FAST                'destination'
              188  LOAD_STR                 'customer'
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   212  'to 212'

 L. 238       194  LOAD_GLOBAL              customer
              196  LOAD_ATTR                objects
              198  LOAD_ATTR                get
              200  LOAD_FAST                'location_id'
              202  LOAD_CONST               ('customer_id',)
              204  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              206  LOAD_FAST                'document_permissions_submit'
              208  STORE_ATTR               customer_id
              210  JUMP_FORWARD        320  'to 320'
            212_0  COME_FROM           192  '192'

 L. 239       212  LOAD_FAST                'destination'
              214  LOAD_STR                 'organisation'
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   238  'to 238'

 L. 240       220  LOAD_GLOBAL              organisation
              222  LOAD_ATTR                objects
              224  LOAD_ATTR                get
              226  LOAD_FAST                'location_id'
              228  LOAD_CONST               ('organisation_id',)
              230  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              232  LOAD_FAST                'document_permissions_submit'
              234  STORE_ATTR               organisation_id
              236  JUMP_FORWARD        320  'to 320'
            238_0  COME_FROM           218  '218'

 L. 241       238  LOAD_FAST                'destination'
              240  LOAD_STR                 'requirement'
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   266  'to 266'

 L. 242       248  LOAD_GLOBAL              requirement
              250  LOAD_ATTR                objects
              252  LOAD_ATTR                get
              254  LOAD_FAST                'location_id'
              256  LOAD_CONST               ('requirement_id',)
              258  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              260  LOAD_FAST                'document_permissions_submit'
              262  STORE_ATTR               requirement
              264  JUMP_FORWARD        320  'to 320'
            266_0  COME_FROM           244  '244'

 L. 243       266  LOAD_FAST                'destination'
              268  LOAD_STR                 'requirement_item'
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   294  'to 294'

 L. 244       276  LOAD_GLOBAL              requirement_item
              278  LOAD_ATTR                objects
              280  LOAD_ATTR                get
              282  LOAD_FAST                'location_id'
              284  LOAD_CONST               ('requirement_item_id',)
              286  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              288  LOAD_FAST                'document_permissions_submit'
              290  STORE_ATTR               requirement_item
              292  JUMP_FORWARD        320  'to 320'
            294_0  COME_FROM           272  '272'

 L. 245       294  LOAD_FAST                'destination'
              296  LOAD_STR                 'request_for_change'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   320  'to 320'

 L. 246       304  LOAD_GLOBAL              request_for_change
              306  LOAD_ATTR                objects
              308  LOAD_ATTR                get
              310  LOAD_FAST                'location_id'
              312  LOAD_CONST               ('rfc_id',)
              314  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              316  LOAD_FAST                'document_permissions_submit'
              318  STORE_ATTR               request_for_change
            320_0  COME_FROM           300  '300'
            320_1  COME_FROM           292  '292'
            320_2  COME_FROM           264  '264'
            320_3  COME_FROM           236  '236'
            320_4  COME_FROM           210  '210'
            320_5  COME_FROM           184  '184'
            320_6  COME_FROM           158  '158'

 L. 249       320  LOAD_FAST                'folder_id'
              322  LOAD_CONST               0
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_TRUE    346  'to 346'
              330  LOAD_FAST                'folder_id'
              332  LOAD_STR                 '0'
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_TRUE    346  'to 346'
              340  LOAD_FAST                'folder_id'
          342_344  POP_JUMP_IF_TRUE    356  'to 356'
            346_0  COME_FROM           336  '336'
            346_1  COME_FROM           326  '326'

 L. 250       346  LOAD_GLOBAL              print
              348  LOAD_STR                 "Due to a python bug. We have to do this like this :'("
              350  CALL_FUNCTION_1       1  ''
              352  POP_TOP          
              354  JUMP_FORWARD        380  'to 380'
            356_0  COME_FROM           342  '342'

 L. 252       356  LOAD_GLOBAL              print
              358  LOAD_STR                 'There is an else'
              360  CALL_FUNCTION_1       1  ''
              362  POP_TOP          

 L. 253       364  LOAD_GLOBAL              folder
              366  LOAD_ATTR                objects
              368  LOAD_ATTR                get
              370  LOAD_FAST                'folder_id'
              372  LOAD_CONST               ('folder_id',)
              374  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              376  LOAD_FAST                'document_permissions_submit'
              378  STORE_ATTR               folder_id
            380_0  COME_FROM           354  '354'

 L. 255       380  LOAD_FAST                'document_permissions_submit'
              382  LOAD_METHOD              save
              384  CALL_METHOD_0         0  ''
              386  POP_TOP          

 L. 257       388  BUILD_LIST_0          0 
              390  STORE_FAST               'result'

 L. 258       392  LOAD_FAST                'result'
              394  LOAD_METHOD              append

 L. 259       396  LOAD_FAST                'document_description'

 L. 260       398  LOAD_FAST                'file_size'

 L. 261       400  LOAD_STR                 ''

 L. 262       402  LOAD_STR                 ''

 L. 263       404  LOAD_STR                 '/'

 L. 264       406  LOAD_STR                 'POST'

 L. 258       408  LOAD_CONST               ('name', 'size', 'url', 'thumbnail_url', 'delete_url', 'delete_type')
              410  BUILD_CONST_KEY_MAP_6     6 
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          

 L. 266       416  LOAD_GLOBAL              simplejson
              418  LOAD_METHOD              dumps
              420  LOAD_FAST                'result'
              422  CALL_METHOD_1         1  ''
              424  STORE_FAST               'response_data'

 L. 267       426  LOAD_GLOBAL              HttpResponse
              428  LOAD_FAST                'response_data'
              430  LOAD_STR                 'application/json'
              432  LOAD_CONST               ('content_type',)
              434  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              436  RETURN_VALUE     
            438_0  COME_FROM            50  '50'

 L. 269       438  LOAD_GLOBAL              print
              440  LOAD_FAST                'form'
              442  LOAD_ATTR                errors
              444  CALL_FUNCTION_1       1  ''
              446  POP_TOP          

 L. 270       448  LOAD_GLOBAL              HttpResponseBadRequest
              450  LOAD_STR                 'Sorry, there was an issue with the form'
              452  CALL_FUNCTION_1       1  ''
              454  RETURN_VALUE     
              456  JUMP_FORWARD        466  'to 466'
            458_0  COME_FROM             8  '8'

 L. 272       458  LOAD_GLOBAL              HttpResponseBadRequest
              460  LOAD_STR                 'Sorry, this function is only a POST function'
              462  CALL_FUNCTION_1       1  ''
              464  RETURN_VALUE     
            466_0  COME_FROM           456  '456'

Parse error at or near `JUMP_FORWARD' instruction at offset 354


@login_required(login_url='login', redirect_field_name='')
def document_tree_url--- This code section failed: ---

 L. 277         0  LOAD_FAST                'request'
                2  LOAD_ATTR                method
                4  LOAD_STR                 'POST'
                6  COMPARE_OP               ==
             8_10  POP_JUMP_IF_FALSE   406  'to 406'

 L. 278        12  LOAD_GLOBAL              document_url_form
               14  LOAD_FAST                'request'
               16  LOAD_ATTR                POST
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'form'

 L. 279        22  LOAD_FAST                'form'
               24  LOAD_METHOD              is_valid
               26  CALL_METHOD_0         0  ''
            28_30  POP_JUMP_IF_FALSE   386  'to 386'

 L. 281        32  LOAD_FAST                'form'
               34  LOAD_ATTR                cleaned_data
               36  LOAD_STR                 'document_description'
               38  BINARY_SUBSCR    
               40  STORE_FAST               'document_description'

 L. 282        42  LOAD_FAST                'document_description'
               44  LOAD_STR                 ''
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 284        50  LOAD_FAST                'form'
               52  LOAD_ATTR                cleaned_data
               54  LOAD_STR                 'document_url_location'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'document_description'
             60_0  COME_FROM            48  '48'

 L. 286        60  LOAD_GLOBAL              document

 L. 287        62  LOAD_FAST                'form'
               64  LOAD_ATTR                cleaned_data
               66  LOAD_STR                 'document_url_location'
               68  BINARY_SUBSCR    

 L. 288        70  LOAD_FAST                'document_description'

 L. 289        72  LOAD_FAST                'request'
               74  LOAD_ATTR                user

 L. 286        76  LOAD_CONST               ('document_url_location', 'document_description', 'change_user')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  STORE_FAST               'document_submit'

 L. 291        82  LOAD_FAST                'document_submit'
               84  LOAD_METHOD              save
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          

 L. 293        90  LOAD_GLOBAL              document_permission

 L. 294        92  LOAD_FAST                'document_submit'

 L. 295        94  LOAD_FAST                'request'
               96  LOAD_ATTR                user

 L. 293        98  LOAD_CONST               ('document_key', 'change_user')
              100  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              102  STORE_FAST               'document_permissions_submit'

 L. 297       104  LOAD_FAST                'destination'
              106  LOAD_STR                 'project'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   130  'to 130'

 L. 298       112  LOAD_GLOBAL              project
              114  LOAD_ATTR                objects
              116  LOAD_ATTR                get
              118  LOAD_FAST                'location_id'
              120  LOAD_CONST               ('project_id',)
              122  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              124  LOAD_FAST                'document_permissions_submit'
              126  STORE_ATTR               project_id
              128  JUMP_FORWARD        288  'to 288'
            130_0  COME_FROM           110  '110'

 L. 299       130  LOAD_FAST                'destination'
              132  LOAD_STR                 'task'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   156  'to 156'

 L. 300       138  LOAD_GLOBAL              task
              140  LOAD_ATTR                objects
              142  LOAD_ATTR                get
              144  LOAD_FAST                'location_id'
              146  LOAD_CONST               ('task_id',)
              148  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              150  LOAD_FAST                'document_permissions_submit'
              152  STORE_ATTR               task_id
              154  JUMP_FORWARD        288  'to 288'
            156_0  COME_FROM           136  '136'

 L. 301       156  LOAD_FAST                'destination'
              158  LOAD_STR                 'customer'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   182  'to 182'

 L. 302       164  LOAD_GLOBAL              customer
              166  LOAD_ATTR                objects
              168  LOAD_ATTR                get
              170  LOAD_FAST                'location_id'
              172  LOAD_CONST               ('customer_id',)
              174  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              176  LOAD_FAST                'document_permissions_submit'
              178  STORE_ATTR               customer_id
              180  JUMP_FORWARD        288  'to 288'
            182_0  COME_FROM           162  '162'

 L. 303       182  LOAD_FAST                'destination'
              184  LOAD_STR                 'organisation'
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE   208  'to 208'

 L. 304       190  LOAD_GLOBAL              organisation
              192  LOAD_ATTR                objects
              194  LOAD_ATTR                get
              196  LOAD_FAST                'location_id'
              198  LOAD_CONST               ('organisation_id',)
              200  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              202  LOAD_FAST                'document_permissions_submit'
              204  STORE_ATTR               organisation_id
              206  JUMP_FORWARD        288  'to 288'
            208_0  COME_FROM           188  '188'

 L. 305       208  LOAD_FAST                'destination'
              210  LOAD_STR                 'requirement'
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   234  'to 234'

 L. 306       216  LOAD_GLOBAL              requirement
              218  LOAD_ATTR                objects
              220  LOAD_ATTR                get
              222  LOAD_FAST                'location_id'
              224  LOAD_CONST               ('requirement_id',)
              226  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              228  LOAD_FAST                'document_permissions_submit'
              230  STORE_ATTR               requirement
              232  JUMP_FORWARD        288  'to 288'
            234_0  COME_FROM           214  '214'

 L. 307       234  LOAD_FAST                'destination'
              236  LOAD_STR                 'requirement_item'
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   262  'to 262'

 L. 308       244  LOAD_GLOBAL              requirement_item
              246  LOAD_ATTR                objects
              248  LOAD_ATTR                get

 L. 309       250  LOAD_FAST                'location_id'

 L. 308       252  LOAD_CONST               ('requirement_item_id',)
              254  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              256  LOAD_FAST                'document_permissions_submit'
              258  STORE_ATTR               requirement_item
              260  JUMP_FORWARD        288  'to 288'
            262_0  COME_FROM           240  '240'

 L. 311       262  LOAD_FAST                'destination'
              264  LOAD_STR                 'request_for_change'
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   288  'to 288'

 L. 312       272  LOAD_GLOBAL              request_for_change
              274  LOAD_ATTR                objects
              276  LOAD_ATTR                get
              278  LOAD_FAST                'location_id'
              280  LOAD_CONST               ('rfc_id',)
              282  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              284  LOAD_FAST                'document_permissions_submit'
              286  STORE_ATTR               request_for_change
            288_0  COME_FROM           268  '268'
            288_1  COME_FROM           260  '260'
            288_2  COME_FROM           232  '232'
            288_3  COME_FROM           206  '206'
            288_4  COME_FROM           180  '180'
            288_5  COME_FROM           154  '154'
            288_6  COME_FROM           128  '128'

 L. 316       288  LOAD_FAST                'folder_id'
              290  LOAD_CONST               0
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_TRUE    314  'to 314'
              298  LOAD_FAST                'folder_id'
              300  LOAD_STR                 '0'
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_TRUE    314  'to 314'
              308  LOAD_FAST                'folder_id'
          310_312  POP_JUMP_IF_TRUE    324  'to 324'
            314_0  COME_FROM           304  '304'
            314_1  COME_FROM           294  '294'

 L. 317       314  LOAD_GLOBAL              print
              316  LOAD_STR                 "Due to a python bug. We have to do this like this :'("
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          
              322  JUMP_FORWARD        348  'to 348'
            324_0  COME_FROM           310  '310'

 L. 319       324  LOAD_GLOBAL              print
              326  LOAD_STR                 'There is an else'
              328  CALL_FUNCTION_1       1  ''
              330  POP_TOP          

 L. 320       332  LOAD_GLOBAL              folder
              334  LOAD_ATTR                objects
              336  LOAD_ATTR                get
              338  LOAD_FAST                'folder_id'
              340  LOAD_CONST               ('folder_id',)
              342  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              344  LOAD_FAST                'document_permissions_submit'
              346  STORE_ATTR               folder_id
            348_0  COME_FROM           322  '322'

 L. 322       348  LOAD_FAST                'document_permissions_submit'
              350  LOAD_METHOD              save
              352  CALL_METHOD_0         0  ''
              354  POP_TOP          

 L. 325       356  LOAD_GLOBAL              loader
              358  LOAD_METHOD              get_template
              360  LOAD_STR                 'NearBeach/blank.html'
              362  CALL_METHOD_1         1  ''
              364  STORE_FAST               't'

 L. 327       366  BUILD_MAP_0           0 
              368  STORE_FAST               'c'

 L. 329       370  LOAD_GLOBAL              HttpResponse
              372  LOAD_FAST                't'
              374  LOAD_METHOD              render
              376  LOAD_FAST                'c'
              378  LOAD_FAST                'request'
              380  CALL_METHOD_2         2  ''
              382  CALL_FUNCTION_1       1  ''
              384  RETURN_VALUE     
            386_0  COME_FROM            28  '28'

 L. 331       386  LOAD_GLOBAL              print
              388  LOAD_FAST                'form'
              390  LOAD_ATTR                errors
              392  CALL_FUNCTION_1       1  ''
              394  POP_TOP          

 L. 333       396  LOAD_GLOBAL              HttpResponseBadRequest
              398  LOAD_STR                 'Form is not valid'
              400  CALL_FUNCTION_1       1  ''
              402  RETURN_VALUE     
              404  JUMP_FORWARD        414  'to 414'
            406_0  COME_FROM             8  '8'

 L. 335       406  LOAD_GLOBAL              HttpResponseBadRequest
              408  LOAD_STR                 'Request can only be post'
              410  CALL_FUNCTION_1       1  ''
              412  RETURN_VALUE     
            414_0  COME_FROM           404  '404'

Parse error at or near `JUMP_FORWARD' instruction at offset 322