# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/views_quotes.py
# Compiled at: 2020-05-03 01:13:24
# Size of source mod 2**32: 9366 bytes
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from NearBeach.forms import *
from .models import *
from NearBeach.models import *
from django.db.models import Sum, F
from NearBeach.user_permissions import *

@login_required(login_url='login', redirect_field_name='')
def delete_line_item(request, line_item_id):
    line_item = quote_product_and_service.objects.get(quotes_product_and_service_id=line_item_id)
    line_item.is_deleted = 'TRUE'
    line_item.change_user = request.user
    line_item.save()
    t = loader.get_template('NearBeach/blank.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def delete_responsible_customer(request, quote_id, customer_id):
    if request.method == 'POST':
        quote_responsible_customer.objects.filter(is_deleted='FALSE',
          quote_id=quote.objects.get(quote_id=quote_id),
          customer_id=customer.objects.get(customer_id=customer_id)).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Delete Responsible Customer has to be done in POST')


@login_required(login_url='login', redirect_field_name='')
def list_of_line_items(request, quote_id):
    line_item_results = quote_product_and_service.objects.filter(is_deleted='FALSE',
      quote_id=quote_id)
    product_line_items = quote_product_and_service.objects.filter(quote_id=quote_id,
      product_and_service__product_or_service='Product',
      is_deleted='FALSE')
    service_line_items = quote_product_and_service.objects.filter(quote_id=quote_id,
      product_and_service__product_or_service='Service',
      is_deleted='FALSE')
    t = loader.get_template('NearBeach/quote_information/list_of_line_items.html')
    c = {'quote_id':quote_id, 
     'line_item_results':line_item_results, 
     'product_line_items':product_line_items, 
     'service_line_items':service_line_items}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_line_item(request, quote_id):
    quotes_results = quote.objects.get(quote_id=quote_id)
    permission_results = return_user_permission_level(request, None, 'quote')
    if request.POST:
        form = new_line_item_form(request.POST, request.FILES)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            product_description = form.cleaned_data['product_description']
            discount_choice = form.cleaned_data['discount_choice']
            discount_percent = form.cleaned_data['discount_percent']
            discount_amount = form.cleaned_data['discount_amount']
            sales_price = form.cleaned_data['sales_price']
            product_price = form.cleaned_data['product_price']
            tax = form.cleaned_data['tax']
            tax_amount = form.cleaned_data['tax_amount']
            total = form.cleaned_data['total']
            product_note = form.cleaned_data['product_note']
            quote_instance = quote.objects.get(quote_id=quote_id)
            product_instance = product_and_service.objects.get(product_id=(form.cleaned_data['product_and_service']))
            if not (discount_percent == '' or discount_percent):
                discount_percent = 0
            if not (discount_amount == '' or discount_amount):
                discount_amount = 0
            submit_line_item = quote_product_and_service(product_and_service=product_instance,
              quantity=quantity,
              product_description=product_description,
              product_cost=(product_instance.product_cost),
              discount_choice=discount_choice,
              discount_percent=discount_percent,
              discount_amount=discount_amount,
              product_price=product_price,
              tax=tax,
              tax_amount=tax_amount,
              total=total,
              product_note=product_note,
              change_user=(request.user),
              quote_id=(quote_instance.quote_id),
              sales_price=sales_price)
            submit_line_item.save()
        else:
            print(form.errors)
    product_and_service_results = product_and_service.objects.filter(is_deleted='FALSE')
    t = loader.get_template('NearBeach/quote_information/new_line_item.html')
    c = {'quote_id':quote_id, 
     'new_line_item_form':new_line_item_form(), 
     'quote_permission':permission_results['quote'], 
     'product_and_service_results':product_and_service_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def responsible_customer--- This code section failed: ---

 L. 161         0  LOAD_GLOBAL              return_user_permission_level
                2  LOAD_FAST                'request'
                4  LOAD_CONST               None
                6  LOAD_STR                 'quote'
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'permission_results'

 L. 163        12  LOAD_FAST                'request'
               14  LOAD_ATTR                method
               16  LOAD_STR                 'POST'
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    90  'to 90'

 L. 164        22  LOAD_FAST                'customer_id'
               24  LOAD_STR                 ''
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 165        30  LOAD_GLOBAL              HttpResponseBadRequest
               32  LOAD_STR                 'Customer ID is required!'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
             38_0  COME_FROM            28  '28'

 L. 167        38  LOAD_GLOBAL              customer
               40  LOAD_ATTR                objects
               42  LOAD_ATTR                get
               44  LOAD_FAST                'customer_id'
               46  LOAD_CONST               ('customer_id',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  STORE_FAST               'customer_instance'

 L. 168        52  LOAD_GLOBAL              quote
               54  LOAD_ATTR                objects
               56  LOAD_ATTR                get
               58  LOAD_FAST                'quote_id'
               60  LOAD_CONST               ('quote_id',)
               62  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               64  STORE_FAST               'quote_instance'

 L. 170        66  LOAD_GLOBAL              quote_responsible_customer

 L. 171        68  LOAD_FAST                'customer_instance'

 L. 172        70  LOAD_FAST                'quote_instance'

 L. 173        72  LOAD_FAST                'request'
               74  LOAD_ATTR                user

 L. 170        76  LOAD_CONST               ('customer_id', 'quote_id', 'change_user')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  STORE_FAST               'responsible_customer_save'

 L. 175        82  LOAD_FAST                'responsible_customer_save'
               84  LOAD_METHOD              save
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          
             90_0  COME_FROM            20  '20'

 L. 177        90  LOAD_GLOBAL              customer
               92  LOAD_ATTR                objects
               94  LOAD_ATTR                filter

 L. 178        96  LOAD_GLOBAL              quote_responsible_customer
               98  LOAD_ATTR                objects
              100  LOAD_ATTR                filter

 L. 179       102  LOAD_FAST                'quote_id'

 L. 180       104  LOAD_STR                 'FALSE'

 L. 178       106  LOAD_CONST               ('quote_id', 'is_deleted')
              108  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              110  LOAD_METHOD              values

 L. 181       112  LOAD_STR                 'customer_id'

 L. 178       114  CALL_METHOD_1         1  ''
              116  LOAD_METHOD              distinct
              118  CALL_METHOD_0         0  ''

 L. 177       120  LOAD_CONST               ('customer_id__in',)
              122  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              124  STORE_FAST               'responsible_customer_results'

 L. 183       126  LOAD_GLOBAL              quote
              128  LOAD_ATTR                objects
              130  LOAD_ATTR                get
              132  LOAD_FAST                'quote_id'
              134  LOAD_CONST               ('quote_id',)
              136  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              138  STORE_FAST               'quote_results'

 L. 189       140  LOAD_FAST                'quote_results'
              142  LOAD_ATTR                project_id
              144  LOAD_CONST               None
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_TRUE    208  'to 208'

 L. 190       150  SETUP_FINALLY       188  'to 188'

 L. 191       152  LOAD_GLOBAL              customer
              154  LOAD_ATTR                objects
              156  LOAD_ATTR                filter

 L. 192       158  LOAD_FAST                'quote_results'
              160  LOAD_ATTR                project_id
              162  LOAD_ATTR                organisation_id_id

 L. 191       164  LOAD_CONST               ('organisation_id',)
              166  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              168  LOAD_ATTR                exclude

 L. 193       170  LOAD_FAST                'responsible_customer_results'
              172  LOAD_METHOD              values
              174  LOAD_STR                 'customer_id'
              176  CALL_METHOD_1         1  ''

 L. 191       178  LOAD_CONST               ('customer_id__in',)
              180  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              182  STORE_FAST               'customer_results'
              184  POP_BLOCK        
              186  JUMP_FORWARD        524  'to 524'
            188_0  COME_FROM_FINALLY   150  '150'

 L. 194       188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L. 195       194  LOAD_CONST               None
              196  STORE_FAST               'customer_results'
              198  POP_EXCEPT       
              200  JUMP_FORWARD        524  'to 524'
              202  END_FINALLY      
          204_206  JUMP_FORWARD        524  'to 524'
            208_0  COME_FROM           148  '148'

 L. 196       208  LOAD_FAST                'quote_results'
              210  LOAD_ATTR                organisation_id
              212  LOAD_CONST               None
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_TRUE    252  'to 252'

 L. 197       218  LOAD_GLOBAL              customer
              220  LOAD_ATTR                objects
              222  LOAD_ATTR                filter

 L. 198       224  LOAD_FAST                'quote_results'
              226  LOAD_ATTR                organisation_id_id

 L. 197       228  LOAD_CONST               ('organisation_id',)
              230  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              232  LOAD_ATTR                exclude

 L. 199       234  LOAD_FAST                'responsible_customer_results'
              236  LOAD_METHOD              values
              238  LOAD_STR                 'customer_id'
              240  CALL_METHOD_1         1  ''

 L. 197       242  LOAD_CONST               ('customer_id__in',)
              244  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              246  STORE_FAST               'customer_results'
          248_250  JUMP_FORWARD        524  'to 524'
            252_0  COME_FROM           216  '216'

 L. 200       252  LOAD_FAST                'quote_results'
              254  LOAD_ATTR                task_id
              256  LOAD_CONST               None
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_TRUE    314  'to 314'

 L. 201       264  LOAD_GLOBAL              customer
              266  LOAD_ATTR                objects
              268  LOAD_ATTR                filter

 L. 202       270  LOAD_GLOBAL              task_customer
              272  LOAD_ATTR                objects
              274  LOAD_ATTR                filter

 L. 203       276  LOAD_STR                 'FALSE'

 L. 204       278  LOAD_FAST                'quote_results'
              280  LOAD_ATTR                task_id_id

 L. 202       282  LOAD_CONST               ('is_deleted', 'task_id')
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  LOAD_METHOD              values

 L. 205       288  LOAD_STR                 'customer_id'

 L. 202       290  CALL_METHOD_1         1  ''

 L. 201       292  LOAD_CONST               ('customer_id__in',)
              294  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              296  LOAD_ATTR                exclude

 L. 206       298  LOAD_FAST                'responsible_customer_results'
              300  LOAD_METHOD              values
              302  LOAD_STR                 'customer_id'
              304  CALL_METHOD_1         1  ''

 L. 201       306  LOAD_CONST               ('customer_id__in',)
              308  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              310  STORE_FAST               'customer_results'
              312  JUMP_FORWARD        524  'to 524'
            314_0  COME_FROM           260  '260'

 L. 207       314  LOAD_FAST                'quote_results'
              316  LOAD_ATTR                opportunity_id
              318  LOAD_CONST               None
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_TRUE    436  'to 436'

 L. 208       326  SETUP_FINALLY       366  'to 366'

 L. 209       328  LOAD_GLOBAL              customer
              330  LOAD_ATTR                objects
              332  LOAD_ATTR                filter

 L. 210       334  LOAD_FAST                'quote_results'
              336  LOAD_ATTR                opportunity_id
              338  LOAD_ATTR                organisation_id
              340  LOAD_ATTR                organisation_id

 L. 209       342  LOAD_CONST               ('organisation_id',)
              344  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              346  LOAD_ATTR                exclude

 L. 211       348  LOAD_FAST                'responsible_customer_results'
              350  LOAD_METHOD              values
              352  LOAD_STR                 'customer_id'
              354  CALL_METHOD_1         1  ''

 L. 209       356  LOAD_CONST               ('customer_id__in',)
              358  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              360  STORE_FAST               'customer_results'
              362  POP_BLOCK        
              364  JUMP_FORWARD        434  'to 434'
            366_0  COME_FROM_FINALLY   326  '326'

 L. 212       366  POP_TOP          
              368  POP_TOP          
              370  POP_TOP          

 L. 213       372  SETUP_FINALLY       412  'to 412'

 L. 214       374  LOAD_GLOBAL              customer
              376  LOAD_ATTR                objects
              378  LOAD_ATTR                filter

 L. 215       380  LOAD_FAST                'quote_results'
              382  LOAD_ATTR                opportunity_id
              384  LOAD_ATTR                customer_id
              386  LOAD_ATTR                customer_id

 L. 214       388  LOAD_CONST               ('organisation_id',)
              390  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              392  LOAD_ATTR                exclude

 L. 216       394  LOAD_FAST                'responsible_customer_results'
              396  LOAD_METHOD              values
              398  LOAD_STR                 'customer_id'
              400  CALL_METHOD_1         1  ''

 L. 214       402  LOAD_CONST               ('customer_id__in',)
              404  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              406  STORE_FAST               'customer_results'
              408  POP_BLOCK        
              410  JUMP_FORWARD        428  'to 428'
            412_0  COME_FROM_FINALLY   372  '372'

 L. 217       412  POP_TOP          
              414  POP_TOP          
              416  POP_TOP          

 L. 218       418  LOAD_STR                 ''
              420  STORE_FAST               'customer_results'
              422  POP_EXCEPT       
              424  JUMP_FORWARD        428  'to 428'
              426  END_FINALLY      
            428_0  COME_FROM           424  '424'
            428_1  COME_FROM           410  '410'
              428  POP_EXCEPT       
              430  JUMP_FORWARD        434  'to 434'
              432  END_FINALLY      
            434_0  COME_FROM           430  '430'
            434_1  COME_FROM           364  '364'
              434  JUMP_FORWARD        524  'to 524'
            436_0  COME_FROM           322  '322'

 L. 219       436  LOAD_FAST                'quote_results'
              438  LOAD_ATTR                customer_id
              440  LOAD_CONST               None
              442  COMPARE_OP               ==
          444_446  POP_JUMP_IF_TRUE    482  'to 482'

 L. 220       448  LOAD_GLOBAL              customer
              450  LOAD_ATTR                objects
              452  LOAD_ATTR                filter

 L. 221       454  LOAD_FAST                'quote_results'
              456  LOAD_ATTR                customer_id
              458  LOAD_ATTR                customer_id

 L. 220       460  LOAD_CONST               ('customer_id',)
              462  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              464  LOAD_ATTR                exclude

 L. 222       466  LOAD_FAST                'responsible_customer_results'
              468  LOAD_METHOD              values
              470  LOAD_STR                 'customer_id'
              472  CALL_METHOD_1         1  ''

 L. 220       474  LOAD_CONST               ('customer_id__in',)
              476  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              478  STORE_FAST               'customer_results'
              480  JUMP_FORWARD        524  'to 524'
            482_0  COME_FROM           444  '444'

 L. 223       482  LOAD_FAST                'quote_results'
              484  LOAD_ATTR                organisation_id
              486  LOAD_CONST               None
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_TRUE    524  'to 524'

 L. 224       494  LOAD_GLOBAL              customer
              496  LOAD_ATTR                objects
              498  LOAD_ATTR                filter

 L. 225       500  LOAD_FAST                'quote_results'
              502  LOAD_ATTR                organisation_id
            504_0  COME_FROM           186  '186'

 L. 224       504  LOAD_CONST               ('organisation_id',)
              506  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              508  LOAD_ATTR                exclude

 L. 226       510  LOAD_FAST                'responsible_customer_results'
              512  LOAD_METHOD              values
              514  LOAD_STR                 'customer_id'
              516  CALL_METHOD_1         1  ''
            518_0  COME_FROM           200  '200'

 L. 224       518  LOAD_CONST               ('customer_id__in',)
              520  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              522  STORE_FAST               'customer_results'
            524_0  COME_FROM           490  '490'
            524_1  COME_FROM           480  '480'
            524_2  COME_FROM           434  '434'
            524_3  COME_FROM           312  '312'
            524_4  COME_FROM           248  '248'
            524_5  COME_FROM           204  '204'

 L. 229       524  LOAD_GLOBAL              loader
              526  LOAD_METHOD              get_template
              528  LOAD_STR                 'NearBeach/quote_information/responsible_customer.html'
              530  CALL_METHOD_1         1  ''
              532  STORE_FAST               't'

 L. 233       534  LOAD_FAST                'quote_id'

 L. 234       536  LOAD_FAST                'customer_results'

 L. 235       538  LOAD_FAST                'responsible_customer_results'

 L. 236       540  LOAD_FAST                'permission_results'
              542  LOAD_STR                 'quote'
              544  BINARY_SUBSCR    

 L. 232       546  LOAD_CONST               ('quote_id', 'customer_results', 'responsible_customer_results', 'quote_permission')
              548  BUILD_CONST_KEY_MAP_4     4 
              550  STORE_FAST               'c'

 L. 240       552  LOAD_GLOBAL              HttpResponse
              554  LOAD_FAST                't'
              556  LOAD_METHOD              render
              558  LOAD_FAST                'c'
              560  LOAD_FAST                'request'
              562  CALL_METHOD_2         2  ''
              564  CALL_FUNCTION_1       1  ''
              566  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 504_0


from collections import namedtuple

def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]