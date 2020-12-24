# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/filter_analysis/family_analysis.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 51764 bytes
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Min, Max
from django.core import serializers
from django.views.generic import UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from .forms import FilterWiZardForm1, FilterWiZardForm2, FilterWiZardForm3, FamilyAnalysisForm
from datetime import datetime
import operator
from django.conf import settings
from .forms import *
import csv
from individuals.models import *
from filter_analysis.forms import *
from filter_analysis.models import *
from genes.models import GeneGroup, Gene, CGDEntry, GeneList
from .filter_options import *
from diseases.models import Disease, HGMDGene, HGMDPhenotype
import diseases.models as GeneDisease
import django_tables2 as tables
from django_tables2 import RequestConfig

@login_required
def family_analysis--- This code section failed: ---

 L.  40         0  BUILD_MAP_0           0 
                2  STORE_FAST               'query'

 L.  41         4  BUILD_MAP_0           0 
                6  STORE_FAST               'exclude'

 L.  42         8  BUILD_MAP_0           0 
               10  STORE_FAST               'summary'

 L.  43        12  BUILD_LIST_0          0 
               14  STORE_FAST               'args'

 L.  44        16  LOAD_FAST                'request'
               18  LOAD_ATTR                META
               20  LOAD_STR                 'QUERY_STRING'
               22  BINARY_SUBSCR    
               24  STORE_FAST               'query_string'

 L.  45        26  BUILD_LIST_0          0 
               28  STORE_FAST               'new_query_string'

 L.  46        30  SETUP_LOOP           70  'to 70'
               32  LOAD_FAST                'query_string'
               34  LOAD_METHOD              split
               36  LOAD_STR                 '&'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  GET_ITER         
             42_0  COME_FROM            54  '54'
               42  FOR_ITER             68  'to 68'
               44  STORE_FAST               'item'

 L.  47        46  LOAD_FAST                'item'
               48  LOAD_METHOD              startswith
               50  LOAD_STR                 'page'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_JUMP_IF_TRUE     42  'to 42'

 L.  48        56  LOAD_FAST                'new_query_string'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'item'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_TOP          
               66  JUMP_BACK            42  'to 42'
               68  POP_BLOCK        
             70_0  COME_FROM_LOOP       30  '30'

 L.  49        70  LOAD_STR                 '&'
               72  LOAD_METHOD              join
               74  LOAD_FAST                'new_query_string'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  STORE_FAST               'query_string'

 L.  51        80  LOAD_GLOBAL              print
               82  LOAD_STR                 'query string'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  POP_TOP          

 L.  52        88  LOAD_GLOBAL              print
               90  LOAD_FAST                'query_string'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  POP_TOP          

 L.  53        96  LOAD_GLOBAL              FilterAnalysis
               98  LOAD_ATTR                objects
              100  LOAD_METHOD              all
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  LOAD_METHOD              prefetch_related
              106  LOAD_STR                 'user'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  STORE_FAST               'filteranalysis'

 L.  54       112  LOAD_GLOBAL              FilterConfig
              114  LOAD_ATTR                objects
              116  LOAD_METHOD              all
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  LOAD_METHOD              prefetch_related
              122  LOAD_STR                 'user'
              124  CALL_METHOD_1         1  '1 positional argument'
              126  STORE_FAST               'filterconfigs'

 L.  55       128  LOAD_FAST                'query_string'
              130  LOAD_STR                 ''
              132  BUILD_LIST_1          1 
              134  COMPARE_OP               !=
          136_138  POP_JUMP_IF_FALSE  2652  'to 2652'
              140  LOAD_FAST                'query_string'
              142  LOAD_STR                 ''
              144  COMPARE_OP               !=
          146_148  POP_JUMP_IF_FALSE  2652  'to 2652'

 L.  56       150  LOAD_FAST                'request'
              152  LOAD_ATTR                method
              154  LOAD_STR                 'GET'
              156  COMPARE_OP               ==
          158_160  POP_JUMP_IF_FALSE  2698  'to 2698'

 L.  58       162  LOAD_GLOBAL              FilterAnalysisForm
              164  LOAD_FAST                'request'
              166  LOAD_ATTR                GET
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  STORE_FAST               'form'

 L.  60       172  LOAD_STR                 'sort_by'
              174  LOAD_FAST                'request'
              176  LOAD_ATTR                GET
              178  COMPARE_OP               in
              180  POP_JUMP_IF_FALSE   212  'to 212'

 L.  61       182  LOAD_FAST                'request'
              184  LOAD_ATTR                GET
              186  LOAD_STR                 'sort_by'
              188  BINARY_SUBSCR    
              190  STORE_FAST               'sort_by'

 L.  62       192  LOAD_FAST                'sort_by'
              194  LOAD_STR                 'desc'
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   206  'to 206'

 L.  63       200  LOAD_STR                 'asc'
              202  STORE_FAST               'sort'
              204  JUMP_ABSOLUTE       216  'to 216'
            206_0  COME_FROM           198  '198'

 L.  65       206  LOAD_STR                 'desc'
              208  STORE_FAST               'sort'
              210  JUMP_FORWARD        216  'to 216'
            212_0  COME_FROM           180  '180'

 L.  67       212  LOAD_STR                 'asc'
              214  STORE_FAST               'sort'
            216_0  COME_FROM           210  '210'

 L.  69       216  LOAD_STR                 'order_by'
              218  LOAD_FAST                'request'
              220  LOAD_ATTR                GET
              222  COMPARE_OP               in
          224_226  POP_JUMP_IF_FALSE   264  'to 264'

 L.  70       228  LOAD_FAST                'sort_by'
              230  LOAD_STR                 'desc'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   252  'to 252'

 L.  71       236  LOAD_STR                 '-%s'
              238  LOAD_FAST                'request'
              240  LOAD_ATTR                GET
              242  LOAD_STR                 'order_by'
              244  BINARY_SUBSCR    
              246  BINARY_MODULO    
              248  STORE_FAST               'order_by'
              250  JUMP_FORWARD        262  'to 262'
            252_0  COME_FROM           234  '234'

 L.  73       252  LOAD_FAST                'request'
              254  LOAD_ATTR                GET
              256  LOAD_STR                 'order_by'
              258  BINARY_SUBSCR    
              260  STORE_FAST               'order_by'
            262_0  COME_FROM           250  '250'
              262  JUMP_FORWARD        268  'to 268'
            264_0  COME_FROM           224  '224'

 L.  75       264  LOAD_STR                 'gene_name'
              266  STORE_FAST               'order_by'
            268_0  COME_FROM           262  '262'

 L.  78       268  LOAD_GLOBAL              filter_chr
              270  LOAD_FAST                'request'
              272  LOAD_FAST                'query'
              274  CALL_FUNCTION_2       2  '2 positional arguments'
              276  POP_TOP          

 L.  80       278  LOAD_GLOBAL              filter_pos
              280  LOAD_FAST                'request'
              282  LOAD_FAST                'query'
              284  CALL_FUNCTION_2       2  '2 positional arguments'
              286  POP_TOP          

 L.  82       288  LOAD_GLOBAL              filter_snp_list
              290  LOAD_FAST                'request'
              292  LOAD_FAST                'query'
              294  CALL_FUNCTION_2       2  '2 positional arguments'
              296  POP_TOP          

 L.  84       298  LOAD_GLOBAL              filter_gene_list
              300  LOAD_FAST                'request'
              302  LOAD_FAST                'query'
              304  LOAD_FAST                'args'
              306  CALL_FUNCTION_3       3  '3 positional arguments'
              308  POP_TOP          

 L.  86       310  LOAD_GLOBAL              filter_mutation_type
              312  LOAD_FAST                'request'
              314  LOAD_FAST                'args'
              316  CALL_FUNCTION_2       2  '2 positional arguments'
              318  POP_TOP          

 L.  88       320  LOAD_GLOBAL              filter_cln
              322  LOAD_FAST                'request'
              324  LOAD_FAST                'query'
              326  CALL_FUNCTION_2       2  '2 positional arguments'
              328  POP_TOP          

 L.  90       330  LOAD_GLOBAL              filter_variant_type_snpeff
              332  LOAD_FAST                'request'
              334  LOAD_FAST                'query'
              336  CALL_FUNCTION_2       2  '2 positional arguments'
              338  POP_TOP          

 L.  92       340  LOAD_GLOBAL              filter_dbsnp
              342  LOAD_FAST                'request'
              344  LOAD_FAST                'query'
              346  CALL_FUNCTION_2       2  '2 positional arguments'
              348  POP_TOP          

 L.  94       350  LOAD_GLOBAL              filter_by_1000g
              352  LOAD_FAST                'request'
              354  LOAD_FAST                'args'
              356  CALL_FUNCTION_2       2  '2 positional arguments'
              358  POP_TOP          

 L.  96       360  LOAD_GLOBAL              filter_by_dbsnp
              362  LOAD_FAST                'request'
              364  LOAD_FAST                'args'
              366  CALL_FUNCTION_2       2  '2 positional arguments'
              368  POP_TOP          

 L.  98       370  LOAD_GLOBAL              filter_by_esp
              372  LOAD_FAST                'request'
              374  LOAD_FAST                'args'
              376  CALL_FUNCTION_2       2  '2 positional arguments'
              378  POP_TOP          

 L. 100       380  LOAD_GLOBAL              filter_by_hi_score
              382  LOAD_FAST                'request'
              384  LOAD_FAST                'args'
              386  CALL_FUNCTION_2       2  '2 positional arguments'
              388  POP_TOP          

 L. 102       390  LOAD_GLOBAL              filter_by_sift
              392  LOAD_FAST                'request'
              394  LOAD_FAST                'args'
              396  CALL_FUNCTION_2       2  '2 positional arguments'
              398  POP_TOP          

 L. 104       400  LOAD_GLOBAL              filter_by_pp2
              402  LOAD_FAST                'request'
              404  LOAD_FAST                'args'
              406  CALL_FUNCTION_2       2  '2 positional arguments'
              408  POP_TOP          

 L. 105       410  LOAD_GLOBAL              filter_by_segdup
              412  LOAD_FAST                'request'
              414  LOAD_FAST                'args'
              416  CALL_FUNCTION_2       2  '2 positional arguments'
              418  POP_TOP          

 L. 107       420  LOAD_GLOBAL              filter_omim
              422  LOAD_FAST                'request'
              424  LOAD_FAST                'args'
              426  CALL_FUNCTION_2       2  '2 positional arguments'
              428  POP_TOP          

 L. 108       430  LOAD_GLOBAL              filter_cgd
              432  LOAD_FAST                'request'
              434  LOAD_FAST                'args'
              436  CALL_FUNCTION_2       2  '2 positional arguments'
              438  POP_TOP          

 L. 109       440  LOAD_GLOBAL              filter_hgmd
              442  LOAD_FAST                'request'
              444  LOAD_FAST                'args'
              446  CALL_FUNCTION_2       2  '2 positional arguments'
              448  POP_TOP          

 L. 110       450  LOAD_GLOBAL              filter_genelists
              452  LOAD_FAST                'request'
              454  LOAD_FAST                'query'
              456  LOAD_FAST                'args'
              458  LOAD_FAST                'exclude'
              460  CALL_FUNCTION_4       4  '4 positional arguments'
              462  POP_TOP          

 L. 112       464  LOAD_GLOBAL              filter_dbsnp_build
              466  LOAD_FAST                'request'
              468  LOAD_FAST                'query'
              470  CALL_FUNCTION_2       2  '2 positional arguments'
              472  POP_TOP          

 L. 114       474  LOAD_GLOBAL              filter_read_depth
              476  LOAD_FAST                'request'
              478  LOAD_FAST                'args'
              480  CALL_FUNCTION_2       2  '2 positional arguments'
              482  POP_TOP          

 L. 115       484  LOAD_GLOBAL              filter_qual
              486  LOAD_FAST                'request'
              488  LOAD_FAST                'args'
              490  CALL_FUNCTION_2       2  '2 positional arguments'
              492  POP_TOP          

 L. 116       494  LOAD_GLOBAL              filter_filter
              496  LOAD_FAST                'request'
              498  LOAD_FAST                'query'
              500  CALL_FUNCTION_2       2  '2 positional arguments'
              502  POP_TOP          

 L. 118       504  LOAD_GLOBAL              filter_func_class
              506  LOAD_FAST                'request'
              508  LOAD_FAST                'query'
              510  CALL_FUNCTION_2       2  '2 positional arguments'
              512  POP_TOP          

 L. 120       514  LOAD_GLOBAL              filter_impact
              516  LOAD_FAST                'request'
              518  LOAD_FAST                'query'
              520  CALL_FUNCTION_2       2  '2 positional arguments'
              522  POP_TOP          

 L. 123       524  LOAD_FAST                'request'
              526  LOAD_ATTR                GET
              528  LOAD_METHOD              getlist
              530  LOAD_STR                 'exclude_individuals'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  STORE_FAST               'exclude_individuals'

 L. 127       536  LOAD_FAST                'request'
              538  LOAD_ATTR                GET
              540  LOAD_METHOD              getlist
              542  LOAD_STR                 'exclude_groups'
              544  CALL_METHOD_1         1  '1 positional argument'
              546  STORE_FAST               'exclude_groups'

 L. 129       548  BUILD_LIST_0          0 
              550  STORE_FAST               'exclude_individuals_list'

 L. 130       552  LOAD_GLOBAL              len
              554  LOAD_FAST                'exclude_groups'
              556  CALL_FUNCTION_1       1  '1 positional argument'
              558  LOAD_CONST               0
              560  COMPARE_OP               >
          562_564  POP_JUMP_IF_FALSE   640  'to 640'

 L. 131       566  SETUP_LOOP          640  'to 640'
              568  LOAD_FAST                'exclude_groups'
              570  GET_ITER         
              572  FOR_ITER            638  'to 638'
              574  STORE_FAST               'group_id'

 L. 132       576  LOAD_GLOBAL              get_object_or_404
              578  LOAD_GLOBAL              Group
              580  LOAD_FAST                'group_id'
              582  LOAD_CONST               ('pk',)
              584  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              586  LOAD_ATTR                members
              588  LOAD_ATTR                values_list
              590  LOAD_STR                 'id'
              592  LOAD_CONST               True
              594  LOAD_CONST               ('flat',)
              596  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              598  STORE_FAST               'group_individuals'

 L. 133       600  SETUP_LOOP          634  'to 634'
              602  LOAD_FAST                'group_individuals'
              604  GET_ITER         
              606  FOR_ITER            632  'to 632'
              608  STORE_FAST               'individual'

 L. 134       610  LOAD_FAST                'exclude_individuals_list'
              612  LOAD_METHOD              append
              614  LOAD_GLOBAL              str
              616  LOAD_GLOBAL              str
              618  LOAD_FAST                'individual'
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  CALL_FUNCTION_1       1  '1 positional argument'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  POP_TOP          
          628_630  JUMP_BACK           606  'to 606'
              632  POP_BLOCK        
            634_0  COME_FROM_LOOP      600  '600'
          634_636  JUMP_BACK           572  'to 572'
              638  POP_BLOCK        
            640_0  COME_FROM_LOOP      566  '566'
            640_1  COME_FROM           562  '562'

 L. 137       640  LOAD_FAST                'exclude_individuals_list'
              642  LOAD_FAST                'exclude_individuals'
              644  BINARY_ADD       
              646  STORE_FAST               'exclude_individuals_list'

 L. 139       648  BUILD_MAP_0           0 
              650  STORE_FAST               'exclude_individuals_variants'

 L. 141       652  LOAD_GLOBAL              len
              654  LOAD_FAST                'exclude_individuals_list'
              656  CALL_FUNCTION_1       1  '1 positional argument'
              658  LOAD_CONST               0
              660  COMPARE_OP               >
          662_664  POP_JUMP_IF_FALSE   810  'to 810'

 L. 144       666  SETUP_LOOP          810  'to 810'
              668  LOAD_FAST                'exclude_individuals_list'
              670  GET_ITER         
              672  FOR_ITER            808  'to 808'
              674  STORE_FAST               'individual'

 L. 145       676  LOAD_GLOBAL              Variant
              678  LOAD_ATTR                objects
              680  LOAD_ATTR                filter
              682  LOAD_FAST                'args'
              684  LOAD_STR                 'individual__id'
              686  LOAD_FAST                'individual'
              688  BUILD_MAP_1           1 
              690  LOAD_FAST                'query'
              692  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              694  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              696  LOAD_ATTR                exclude
              698  BUILD_TUPLE_0         0 
              700  LOAD_FAST                'exclude'
              702  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              704  LOAD_METHOD              values
              706  LOAD_STR                 'chromossome'
              708  LOAD_STR                 'pos'
              710  LOAD_STR                 'genotype'
              712  CALL_METHOD_3         3  '3 positional arguments'
              714  STORE_FAST               'individual_variants'

 L. 146       716  SETUP_LOOP          804  'to 804'
              718  LOAD_FAST                'individual_variants'
              720  GET_ITER         
              722  FOR_ITER            802  'to 802'
              724  STORE_FAST               'variant'

 L. 147       726  LOAD_STR                 '%s-%s'
              728  LOAD_FAST                'variant'
              730  LOAD_STR                 'chromossome'
              732  BINARY_SUBSCR    
              734  LOAD_FAST                'variant'
              736  LOAD_STR                 'pos'
              738  BINARY_SUBSCR    
              740  BUILD_TUPLE_2         2 
              742  BINARY_MODULO    
              744  STORE_FAST               'id'

 L. 148       746  LOAD_FAST                'id'
              748  LOAD_FAST                'exclude_individuals_variants'
              750  COMPARE_OP               in
          752_754  POP_JUMP_IF_FALSE   774  'to 774'

 L. 149       756  LOAD_CONST               0
              758  LOAD_FAST                'exclude_individuals_variants'
              760  LOAD_FAST                'id'
              762  BINARY_SUBSCR    
              764  LOAD_FAST                'variant'
              766  LOAD_STR                 'genotype'
              768  BINARY_SUBSCR    
              770  STORE_SUBSCR     
              772  JUMP_BACK           722  'to 722'
            774_0  COME_FROM           752  '752'

 L. 151       774  BUILD_MAP_0           0 
              776  LOAD_FAST                'exclude_individuals_variants'
              778  LOAD_FAST                'id'
              780  STORE_SUBSCR     

 L. 152       782  LOAD_CONST               0
              784  LOAD_FAST                'exclude_individuals_variants'
              786  LOAD_FAST                'id'
              788  BINARY_SUBSCR    
              790  LOAD_FAST                'variant'
              792  LOAD_STR                 'genotype'
              794  BINARY_SUBSCR    
              796  STORE_SUBSCR     
          798_800  JUMP_BACK           722  'to 722'
              802  POP_BLOCK        
            804_0  COME_FROM_LOOP      716  '716'
          804_806  JUMP_BACK           672  'to 672'
              808  POP_BLOCK        
            810_0  COME_FROM_LOOP      666  '666'
            810_1  COME_FROM           662  '662'

 L. 155       810  LOAD_FAST                'request'
              812  LOAD_ATTR                GET
              814  LOAD_METHOD              getlist
              816  LOAD_STR                 'individuals'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  STORE_FAST               'individuals'

 L. 157       822  LOAD_FAST                'request'
              824  LOAD_ATTR                GET
              826  LOAD_METHOD              getlist
              828  LOAD_STR                 'groups'
              830  CALL_METHOD_1         1  '1 positional argument'
              832  STORE_FAST               'groups'

 L. 158       834  LOAD_GLOBAL              print
              836  LOAD_FAST                'groups'
              838  CALL_FUNCTION_1       1  '1 positional argument'
              840  POP_TOP          

 L. 159       842  BUILD_LIST_0          0 
              844  STORE_FAST               'individuals_list'

 L. 160       846  LOAD_GLOBAL              len
              848  LOAD_FAST                'groups'
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  LOAD_CONST               0
              854  COMPARE_OP               >
          856_858  POP_JUMP_IF_FALSE   942  'to 942'

 L. 161       860  SETUP_LOOP          942  'to 942'
              862  LOAD_FAST                'groups'
              864  GET_ITER         
              866  FOR_ITER            940  'to 940'
              868  STORE_FAST               'group_id'

 L. 162       870  LOAD_GLOBAL              get_object_or_404
              872  LOAD_GLOBAL              Group
              874  LOAD_FAST                'group_id'
              876  LOAD_CONST               ('pk',)
              878  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              880  LOAD_ATTR                members
              882  LOAD_ATTR                values_list
              884  LOAD_STR                 'id'
              886  LOAD_CONST               True
              888  LOAD_CONST               ('flat',)
              890  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              892  STORE_FAST               'group_individuals'

 L. 163       894  SETUP_LOOP          928  'to 928'
              896  LOAD_FAST                'group_individuals'
              898  GET_ITER         
              900  FOR_ITER            926  'to 926'
              902  STORE_FAST               'individual'

 L. 164       904  LOAD_FAST                'individuals_list'
              906  LOAD_METHOD              append
              908  LOAD_GLOBAL              str
              910  LOAD_GLOBAL              str
              912  LOAD_FAST                'individual'
              914  CALL_FUNCTION_1       1  '1 positional argument'
              916  CALL_FUNCTION_1       1  '1 positional argument'
              918  CALL_METHOD_1         1  '1 positional argument'
              920  POP_TOP          
          922_924  JUMP_BACK           900  'to 900'
              926  POP_BLOCK        
            928_0  COME_FROM_LOOP      894  '894'

 L. 165       928  LOAD_GLOBAL              print
              930  LOAD_FAST                'individuals_list'
              932  CALL_FUNCTION_1       1  '1 positional argument'
              934  POP_TOP          
          936_938  JUMP_BACK           866  'to 866'
              940  POP_BLOCK        
            942_0  COME_FROM_LOOP      860  '860'
            942_1  COME_FROM           856  '856'

 L. 167       942  LOAD_FAST                'individuals_list'
              944  LOAD_FAST                'individuals'
              946  BINARY_ADD       
              948  STORE_FAST               'individuals_list'

 L. 169       950  LOAD_GLOBAL              len
              952  LOAD_FAST                'individuals_list'
              954  CALL_FUNCTION_1       1  '1 positional argument'
              956  LOAD_CONST               0
              958  COMPARE_OP               >
          960_962  POP_JUMP_IF_FALSE  1860  'to 1860'

 L. 170       964  LOAD_FAST                'individuals_list'
              966  LOAD_FAST                'query'
              968  LOAD_STR                 'individual_id__in'
              970  STORE_SUBSCR     

 L. 172       972  LOAD_GLOBAL              len
              974  LOAD_FAST                'exclude_individuals_list'
              976  CALL_FUNCTION_1       1  '1 positional argument'
              978  LOAD_CONST               0
              980  COMPARE_OP               >
          982_984  POP_JUMP_IF_FALSE  1126  'to 1126'

 L. 174       986  BUILD_LIST_0          0 
              988  STORE_FAST               'variants_ids'

 L. 176       990  LOAD_GLOBAL              Variant
              992  LOAD_ATTR                objects
              994  LOAD_ATTR                filter
              996  LOAD_FAST                'args'
              998  LOAD_FAST                'query'
             1000  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1002  LOAD_ATTR                exclude
             1004  BUILD_TUPLE_0         0 
             1006  LOAD_FAST                'exclude'
             1008  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1010  LOAD_METHOD              values
             1012  LOAD_STR                 'id'
             1014  LOAD_STR                 'chromossome'
             1016  LOAD_STR                 'pos'
             1018  LOAD_STR                 'genotype'
             1020  CALL_METHOD_4         4  '4 positional arguments'
             1022  STORE_FAST               'variants'

 L. 177      1024  SETUP_LOOP         1118  'to 1118'
             1026  LOAD_FAST                'variants'
             1028  GET_ITER         
             1030  FOR_ITER           1116  'to 1116'
             1032  STORE_FAST               'variant'

 L. 178      1034  LOAD_STR                 '%s-%s'
             1036  LOAD_FAST                'variant'
             1038  LOAD_STR                 'chromossome'
             1040  BINARY_SUBSCR    
             1042  LOAD_FAST                'variant'
             1044  LOAD_STR                 'pos'
             1046  BINARY_SUBSCR    
             1048  BUILD_TUPLE_2         2 
             1050  BINARY_MODULO    
             1052  STORE_FAST               'id'

 L. 179      1054  LOAD_FAST                'id'
             1056  LOAD_FAST                'exclude_individuals_variants'
             1058  COMPARE_OP               in
         1060_1062  POP_JUMP_IF_FALSE  1098  'to 1098'

 L. 180      1064  LOAD_FAST                'variant'
             1066  LOAD_STR                 'genotype'
             1068  BINARY_SUBSCR    
             1070  LOAD_FAST                'exclude_individuals_variants'
             1072  LOAD_FAST                'id'
             1074  BINARY_SUBSCR    
             1076  COMPARE_OP               not-in
         1078_1080  POP_JUMP_IF_FALSE  1112  'to 1112'

 L. 181      1082  LOAD_FAST                'variants_ids'
             1084  LOAD_METHOD              append
             1086  LOAD_FAST                'variant'
             1088  LOAD_STR                 'id'
             1090  BINARY_SUBSCR    
             1092  CALL_METHOD_1         1  '1 positional argument'
             1094  POP_TOP          
             1096  JUMP_BACK          1030  'to 1030'
           1098_0  COME_FROM          1060  '1060'

 L. 183      1098  LOAD_FAST                'variants_ids'
             1100  LOAD_METHOD              append
             1102  LOAD_FAST                'variant'
             1104  LOAD_STR                 'id'
             1106  BINARY_SUBSCR    
             1108  CALL_METHOD_1         1  '1 positional argument'
             1110  POP_TOP          
           1112_0  COME_FROM          1078  '1078'
         1112_1114  JUMP_BACK          1030  'to 1030'
             1116  POP_BLOCK        
           1118_0  COME_FROM_LOOP     1024  '1024'

 L. 185      1118  LOAD_FAST                'variants_ids'
             1120  LOAD_FAST                'query'
             1122  LOAD_STR                 'pk__in'
             1124  STORE_SUBSCR     
           1126_0  COME_FROM           982  '982'

 L. 189      1126  LOAD_FAST                'request'
             1128  LOAD_ATTR                GET
             1130  LOAD_METHOD              get
             1132  LOAD_STR                 'variants_per_gene'
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  STORE_FAST               'variants_per_gene'

 L. 191      1138  LOAD_FAST                'request'
             1140  LOAD_ATTR                GET
             1142  LOAD_METHOD              get
             1144  LOAD_STR                 'genes_in_common'
             1146  LOAD_STR                 ''
             1148  CALL_METHOD_2         2  '2 positional arguments'
             1150  STORE_FAST               'genes_in_common'

 L. 193      1152  LOAD_GLOBAL              print
             1154  LOAD_STR                 'variants per gene'
             1156  CALL_FUNCTION_1       1  '1 positional argument'
             1158  POP_TOP          

 L. 194      1160  LOAD_GLOBAL              print
             1162  LOAD_FAST                'variants_per_gene'
             1164  CALL_FUNCTION_1       1  '1 positional argument'
             1166  POP_TOP          

 L. 195      1168  LOAD_FAST                'variants_per_gene'
             1170  LOAD_STR                 ''
             1172  COMPARE_OP               !=
         1174_1176  POP_JUMP_IF_FALSE  1610  'to 1610'

 L. 197      1178  LOAD_GLOBAL              int
             1180  LOAD_FAST                'variants_per_gene'
             1182  CALL_FUNCTION_1       1  '1 positional argument'
             1184  STORE_FAST               'variants_per_gene'

 L. 199      1186  LOAD_FAST                'request'
             1188  LOAD_ATTR                GET
             1190  LOAD_METHOD              get
             1192  LOAD_STR                 'variants_per_gene_option'
             1194  LOAD_STR                 ''
             1196  CALL_METHOD_2         2  '2 positional arguments'
             1198  STORE_FAST               'variants_per_gene_option'

 L. 201      1200  LOAD_GLOBAL              print
             1202  LOAD_STR                 'Debugging'
             1204  CALL_FUNCTION_1       1  '1 positional argument'
             1206  POP_TOP          

 L. 202      1208  LOAD_GLOBAL              print
             1210  LOAD_FAST                'variants_per_gene'
             1212  CALL_FUNCTION_1       1  '1 positional argument'
             1214  POP_TOP          

 L. 203      1216  LOAD_GLOBAL              print
             1218  LOAD_FAST                'variants_per_gene_option'
             1220  CALL_FUNCTION_1       1  '1 positional argument'
             1222  POP_TOP          

 L. 204      1224  BUILD_LIST_0          0 
             1226  STORE_FAST               'genes_exclude_list'

 L. 205      1228  BUILD_LIST_0          0 
             1230  STORE_FAST               'genes_only_list'

 L. 207  1232_1234  SETUP_LOOP         1576  'to 1576'
             1236  LOAD_FAST                'individuals_list'
             1238  GET_ITER         
           1240_0  COME_FROM          1496  '1496'
         1240_1242  FOR_ITER           1574  'to 1574'
             1244  STORE_FAST               'individual'

 L. 211      1246  LOAD_GLOBAL              print
             1248  LOAD_STR                 'get list of all genes for each individual'
             1250  CALL_FUNCTION_1       1  '1 positional argument'
             1252  POP_TOP          

 L. 212      1254  LOAD_GLOBAL              Variant
             1256  LOAD_ATTR                objects
             1258  LOAD_ATTR                filter
             1260  LOAD_FAST                'args'
             1262  LOAD_STR                 'individual__id'
             1264  LOAD_FAST                'individual'
             1266  BUILD_MAP_1           1 
             1268  LOAD_FAST                'query'
             1270  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1272  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1274  LOAD_ATTR                exclude
             1276  BUILD_TUPLE_0         0 
             1278  LOAD_FAST                'exclude'
             1280  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1282  LOAD_METHOD              values
             1284  LOAD_STR                 'gene_name'
             1286  CALL_METHOD_1         1  '1 positional argument'
             1288  LOAD_ATTR                exclude
             1290  LOAD_STR                 ''
             1292  LOAD_CONST               ('gene_name',)
             1294  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1296  LOAD_ATTR                annotate
             1298  LOAD_GLOBAL              Count
             1300  LOAD_STR                 'gene_name'
             1302  CALL_FUNCTION_1       1  '1 positional argument'
             1304  LOAD_CONST               ('count',)
             1306  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1308  LOAD_METHOD              distinct
             1310  CALL_METHOD_0         0  '0 positional arguments'
             1312  STORE_FAST               'individual_genes'

 L. 213      1314  LOAD_GLOBAL              print
             1316  LOAD_GLOBAL              len
             1318  LOAD_FAST                'individual_genes'
             1320  CALL_FUNCTION_1       1  '1 positional argument'
             1322  CALL_FUNCTION_1       1  '1 positional argument'
             1324  POP_TOP          

 L. 215      1326  LOAD_FAST                'variants_per_gene_option'
             1328  LOAD_STR                 '>'
             1330  COMPARE_OP               ==
         1332_1334  POP_JUMP_IF_FALSE  1408  'to 1408'

 L. 216      1336  SETUP_LOOP         1570  'to 1570'
             1338  LOAD_FAST                'individual_genes'
             1340  GET_ITER         
           1342_0  COME_FROM          1382  '1382'
             1342  FOR_ITER           1404  'to 1404'
             1344  STORE_FAST               'gene'

 L. 217      1346  LOAD_FAST                'gene'
             1348  LOAD_STR                 'count'
             1350  BINARY_SUBSCR    
             1352  LOAD_FAST                'variants_per_gene'
             1354  COMPARE_OP               >=
         1356_1358  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 218      1360  LOAD_FAST                'genes_only_list'
             1362  LOAD_METHOD              append
             1364  LOAD_FAST                'gene'
             1366  LOAD_STR                 'gene_name'
             1368  BINARY_SUBSCR    
             1370  CALL_METHOD_1         1  '1 positional argument'
             1372  POP_TOP          
             1374  JUMP_BACK          1342  'to 1342'
           1376_0  COME_FROM          1356  '1356'

 L. 220      1376  LOAD_FAST                'genes_in_common'
             1378  LOAD_STR                 'on'
             1380  COMPARE_OP               ==
         1382_1384  POP_JUMP_IF_FALSE  1342  'to 1342'

 L. 221      1386  LOAD_FAST                'genes_exclude_list'
             1388  LOAD_METHOD              append
             1390  LOAD_FAST                'gene'
             1392  LOAD_STR                 'gene_name'
             1394  BINARY_SUBSCR    
             1396  CALL_METHOD_1         1  '1 positional argument'
             1398  POP_TOP          
         1400_1402  JUMP_BACK          1342  'to 1342'
             1404  POP_BLOCK        
             1406  JUMP_BACK          1240  'to 1240'
           1408_0  COME_FROM          1332  '1332'

 L. 223      1408  LOAD_FAST                'variants_per_gene_option'
             1410  LOAD_STR                 '<'
             1412  COMPARE_OP               ==
         1414_1416  POP_JUMP_IF_FALSE  1490  'to 1490'

 L. 224      1418  SETUP_LOOP         1570  'to 1570'
             1420  LOAD_FAST                'individual_genes'
             1422  GET_ITER         
           1424_0  COME_FROM          1464  '1464'
             1424  FOR_ITER           1486  'to 1486'
             1426  STORE_FAST               'gene'

 L. 225      1428  LOAD_FAST                'gene'
             1430  LOAD_STR                 'count'
             1432  BINARY_SUBSCR    
             1434  LOAD_FAST                'variants_per_gene'
             1436  COMPARE_OP               <=
         1438_1440  POP_JUMP_IF_FALSE  1458  'to 1458'

 L. 226      1442  LOAD_FAST                'genes_only_list'
             1444  LOAD_METHOD              append
             1446  LOAD_FAST                'gene'
             1448  LOAD_STR                 'gene_name'
             1450  BINARY_SUBSCR    
             1452  CALL_METHOD_1         1  '1 positional argument'
             1454  POP_TOP          
             1456  JUMP_BACK          1424  'to 1424'
           1458_0  COME_FROM          1438  '1438'

 L. 228      1458  LOAD_FAST                'genes_in_common'
             1460  LOAD_STR                 'on'
             1462  COMPARE_OP               ==
         1464_1466  POP_JUMP_IF_FALSE  1424  'to 1424'

 L. 229      1468  LOAD_FAST                'genes_exclude_list'
             1470  LOAD_METHOD              append
             1472  LOAD_FAST                'gene'
             1474  LOAD_STR                 'gene_name'
             1476  BINARY_SUBSCR    
             1478  CALL_METHOD_1         1  '1 positional argument'
             1480  POP_TOP          
         1482_1484  JUMP_BACK          1424  'to 1424'
             1486  POP_BLOCK        
             1488  JUMP_BACK          1240  'to 1240'
           1490_0  COME_FROM          1414  '1414'

 L. 230      1490  LOAD_FAST                'variants_per_gene_option'
             1492  LOAD_STR                 '='
             1494  COMPARE_OP               ==
         1496_1498  POP_JUMP_IF_FALSE  1240  'to 1240'

 L. 231      1500  SETUP_LOOP         1570  'to 1570'
             1502  LOAD_FAST                'individual_genes'
             1504  GET_ITER         
           1506_0  COME_FROM          1546  '1546'
             1506  FOR_ITER           1568  'to 1568'
             1508  STORE_FAST               'gene'

 L. 232      1510  LOAD_FAST                'gene'
             1512  LOAD_STR                 'count'
             1514  BINARY_SUBSCR    
             1516  LOAD_FAST                'variants_per_gene'
             1518  COMPARE_OP               ==
         1520_1522  POP_JUMP_IF_FALSE  1540  'to 1540'

 L. 233      1524  LOAD_FAST                'genes_only_list'
             1526  LOAD_METHOD              append
             1528  LOAD_FAST                'gene'
             1530  LOAD_STR                 'gene_name'
             1532  BINARY_SUBSCR    
             1534  CALL_METHOD_1         1  '1 positional argument'
             1536  POP_TOP          
             1538  JUMP_BACK          1506  'to 1506'
           1540_0  COME_FROM          1520  '1520'

 L. 235      1540  LOAD_FAST                'genes_in_common'
             1542  LOAD_STR                 'on'
             1544  COMPARE_OP               ==
         1546_1548  POP_JUMP_IF_FALSE  1506  'to 1506'

 L. 236      1550  LOAD_FAST                'genes_exclude_list'
             1552  LOAD_METHOD              append
             1554  LOAD_FAST                'gene'
             1556  LOAD_STR                 'gene_name'
             1558  BINARY_SUBSCR    
             1560  CALL_METHOD_1         1  '1 positional argument'
             1562  POP_TOP          
         1564_1566  JUMP_BACK          1506  'to 1506'
             1568  POP_BLOCK        
           1570_0  COME_FROM_LOOP     1500  '1500'
           1570_1  COME_FROM_LOOP     1418  '1418'
           1570_2  COME_FROM_LOOP     1336  '1336'
         1570_1572  JUMP_BACK          1240  'to 1240'
             1574  POP_BLOCK        
           1576_0  COME_FROM_LOOP     1232  '1232'

 L. 238      1576  LOAD_FAST                'args'
             1578  LOAD_METHOD              append
             1580  LOAD_GLOBAL              Q
             1582  LOAD_FAST                'genes_only_list'
             1584  LOAD_CONST               ('gene_name__in',)
             1586  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1588  CALL_METHOD_1         1  '1 positional argument'
             1590  POP_TOP          

 L. 239      1592  LOAD_FAST                'args'
             1594  LOAD_METHOD              append
             1596  LOAD_GLOBAL              Q
             1598  LOAD_FAST                'genes_exclude_list'
             1600  LOAD_CONST               ('gene_name__in',)
             1602  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1604  UNARY_INVERT     
             1606  CALL_METHOD_1         1  '1 positional argument'
             1608  POP_TOP          
           1610_0  COME_FROM          1174  '1174'

 L. 241      1610  LOAD_FAST                'genes_in_common'
             1612  LOAD_STR                 'on'
             1614  COMPARE_OP               ==
         1616_1618  POP_JUMP_IF_FALSE  1732  'to 1732'

 L. 243      1620  BUILD_LIST_0          0 
             1622  STORE_FAST               'individual_gene_list'

 L. 244      1624  SETUP_LOOP         1714  'to 1714'
             1626  LOAD_FAST                'individuals_list'
             1628  GET_ITER         
             1630  FOR_ITER           1712  'to 1712'
             1632  STORE_FAST               'individual'

 L. 245      1634  LOAD_GLOBAL              Variant
             1636  LOAD_ATTR                objects
             1638  LOAD_ATTR                filter
             1640  LOAD_FAST                'args'
             1642  LOAD_STR                 'individual__id'
             1644  LOAD_FAST                'individual'
             1646  BUILD_MAP_1           1 
             1648  LOAD_FAST                'query'
             1650  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1652  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1654  LOAD_ATTR                exclude
             1656  BUILD_TUPLE_0         0 
             1658  LOAD_FAST                'exclude'
             1660  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1662  LOAD_ATTR                values_list
             1664  LOAD_STR                 'gene_name'
             1666  LOAD_CONST               True
             1668  LOAD_CONST               ('flat',)
             1670  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1672  LOAD_ATTR                exclude
             1674  LOAD_STR                 ''
             1676  LOAD_CONST               ('gene_name',)
             1678  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1680  LOAD_METHOD              distinct
             1682  CALL_METHOD_0         0  '0 positional arguments'
             1684  STORE_FAST               'individual_genes'

 L. 246      1686  LOAD_GLOBAL              set
             1688  LOAD_GLOBAL              list
             1690  LOAD_FAST                'individual_genes'
             1692  CALL_FUNCTION_1       1  '1 positional argument'
             1694  CALL_FUNCTION_1       1  '1 positional argument'
             1696  STORE_FAST               'individual_genes'

 L. 247      1698  LOAD_FAST                'individual_gene_list'
             1700  LOAD_METHOD              append
             1702  LOAD_FAST                'individual_genes'
             1704  CALL_METHOD_1         1  '1 positional argument'
             1706  POP_TOP          
         1708_1710  JUMP_BACK          1630  'to 1630'
             1712  POP_BLOCK        
           1714_0  COME_FROM_LOOP     1624  '1624'

 L. 248      1714  LOAD_GLOBAL              set
             1716  LOAD_ATTR                intersection
             1718  LOAD_FAST                'individual_gene_list'
             1720  CALL_FUNCTION_EX      0  'positional arguments only'
             1722  STORE_FAST               'genes_in_common_list'

 L. 249      1724  LOAD_FAST                'genes_in_common_list'
             1726  LOAD_FAST                'query'
             1728  LOAD_STR                 'gene_name__in'
             1730  STORE_SUBSCR     
           1732_0  COME_FROM          1616  '1616'

 L. 252      1732  LOAD_FAST                'request'
             1734  LOAD_ATTR                GET
             1736  LOAD_METHOD              get
             1738  LOAD_STR                 'positions_in_common'
             1740  LOAD_STR                 ''
             1742  CALL_METHOD_2         2  '2 positional arguments'
             1744  STORE_FAST               'positions_in_common'

 L. 253      1746  LOAD_FAST                'positions_in_common'
             1748  LOAD_STR                 'on'
             1750  COMPARE_OP               ==
         1752_1754  POP_JUMP_IF_FALSE  1860  'to 1860'

 L. 255      1756  BUILD_LIST_0          0 
             1758  STORE_FAST               'individual_positions_list'

 L. 256      1760  SETUP_LOOP         1842  'to 1842'
             1762  LOAD_FAST                'individuals_list'
             1764  GET_ITER         
             1766  FOR_ITER           1840  'to 1840'
             1768  STORE_FAST               'individual'

 L. 258      1770  LOAD_GLOBAL              Variant
             1772  LOAD_ATTR                objects
             1774  LOAD_ATTR                filter
             1776  LOAD_FAST                'args'
             1778  LOAD_STR                 'individual__id'
             1780  LOAD_FAST                'individual'
             1782  BUILD_MAP_1           1 
             1784  LOAD_FAST                'query'
             1786  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1788  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1790  LOAD_ATTR                exclude
             1792  BUILD_TUPLE_0         0 
             1794  LOAD_FAST                'exclude'
             1796  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1798  LOAD_ATTR                values_list
             1800  LOAD_STR                 'pos'
             1802  LOAD_CONST               True
             1804  LOAD_CONST               ('flat',)
             1806  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1808  LOAD_METHOD              distinct
             1810  CALL_METHOD_0         0  '0 positional arguments'
             1812  STORE_FAST               'individual_positions'

 L. 259      1814  LOAD_GLOBAL              set
             1816  LOAD_GLOBAL              list
             1818  LOAD_FAST                'individual_positions'
             1820  CALL_FUNCTION_1       1  '1 positional argument'
             1822  CALL_FUNCTION_1       1  '1 positional argument'
             1824  STORE_FAST               'individual_positions'

 L. 260      1826  LOAD_FAST                'individual_positions_list'
             1828  LOAD_METHOD              append
             1830  LOAD_FAST                'individual_positions'
             1832  CALL_METHOD_1         1  '1 positional argument'
             1834  POP_TOP          
         1836_1838  JUMP_BACK          1766  'to 1766'
             1840  POP_BLOCK        
           1842_0  COME_FROM_LOOP     1760  '1760'

 L. 261      1842  LOAD_GLOBAL              set
             1844  LOAD_ATTR                intersection
             1846  LOAD_FAST                'individual_positions_list'
             1848  CALL_FUNCTION_EX      0  'positional arguments only'
             1850  STORE_FAST               'positions_in_common_list'

 L. 262      1852  LOAD_FAST                'positions_in_common_list'
             1854  LOAD_FAST                'query'
             1856  LOAD_STR                 'pos__in'
             1858  STORE_SUBSCR     
           1860_0  COME_FROM          1752  '1752'
           1860_1  COME_FROM           960  '960'

 L. 265      1860  LOAD_GLOBAL              Variant
             1862  LOAD_ATTR                objects
             1864  LOAD_ATTR                filter
             1866  LOAD_FAST                'args'
             1868  LOAD_FAST                'query'
             1870  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1872  LOAD_ATTR                exclude
             1874  BUILD_TUPLE_0         0 
             1876  LOAD_FAST                'exclude'
             1878  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1880  LOAD_METHOD              prefetch_related
             1882  LOAD_STR                 'individual'
             1884  CALL_METHOD_1         1  '1 positional argument'
             1886  LOAD_METHOD              order_by
             1888  LOAD_FAST                'order_by'
             1890  CALL_METHOD_1         1  '1 positional argument'
             1892  STORE_FAST               'variants'

 L. 267      1894  LOAD_FAST                'request'
             1896  LOAD_ATTR                GET
             1898  LOAD_METHOD              get
             1900  LOAD_STR                 'export'
             1902  LOAD_STR                 ''
             1904  CALL_METHOD_2         2  '2 positional arguments'
             1906  STORE_FAST               'export'

 L. 268      1908  LOAD_FAST                'export'
             1910  LOAD_STR                 ''
             1912  COMPARE_OP               !=
         1914_1916  POP_JUMP_IF_FALSE  2206  'to 2206'

 L. 269      1918  LOAD_FAST                'export'
             1920  LOAD_STR                 'csv'
             1922  COMPARE_OP               ==
         1924_1926  POP_JUMP_IF_FALSE  1958  'to 1958'

 L. 270      1928  LOAD_GLOBAL              HttpResponse
             1930  LOAD_STR                 'text/csv'
             1932  LOAD_CONST               ('mimetype',)
             1934  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1936  STORE_FAST               'response'

 L. 271      1938  LOAD_STR                 'attachment; filename=export.csv'
             1940  LOAD_FAST                'response'
             1942  LOAD_STR                 'Content-Disposition'
             1944  STORE_SUBSCR     

 L. 272      1946  LOAD_GLOBAL              csv
             1948  LOAD_METHOD              writer
             1950  LOAD_FAST                'response'
             1952  CALL_METHOD_1         1  '1 positional argument'
             1954  STORE_FAST               'writer'
             1956  JUMP_FORWARD       2004  'to 2004'
           1958_0  COME_FROM          1924  '1924'

 L. 274      1958  LOAD_FAST                'export'
             1960  LOAD_STR                 'txt'
             1962  COMPARE_OP               ==
         1964_1966  POP_JUMP_IF_FALSE  2004  'to 2004'

 L. 275      1968  LOAD_GLOBAL              HttpResponse
             1970  LOAD_STR                 'text/plain'
             1972  LOAD_CONST               ('mimetype',)
             1974  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1976  STORE_FAST               'response'

 L. 276      1978  LOAD_STR                 'attachment; filename=export.txt'
             1980  LOAD_FAST                'response'
             1982  LOAD_STR                 'Content-Disposition'
             1984  STORE_SUBSCR     

 L. 277      1986  LOAD_GLOBAL              csv
             1988  LOAD_ATTR                writer
             1990  LOAD_FAST                'response'
             1992  LOAD_STR                 '\t'
             1994  LOAD_GLOBAL              csv
             1996  LOAD_ATTR                QUOTE_NONE
             1998  LOAD_CONST               ('delimiter', 'quoting')
             2000  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2002  STORE_FAST               'writer'
           2004_0  COME_FROM          1964  '1964'
           2004_1  COME_FROM          1956  '1956'

 L. 278      2004  LOAD_FAST                'writer'
             2006  LOAD_METHOD              writerow
             2008  LOAD_STR                 'Individual'

 L. 279      2010  LOAD_STR                 'Chromossome'
             2012  LOAD_STR                 'Variant Id'
             2014  LOAD_STR                 'Pos'
             2016  LOAD_STR                 'Qual'
             2018  LOAD_STR                 'Ref'
             2020  LOAD_STR                 'Alt'
             2022  LOAD_STR                 'Genotype'

 L. 280      2024  LOAD_STR                 'Genotype Info'
             2026  LOAD_STR                 'Read Depth'
             2028  LOAD_STR                 'Snpe Eff'
             2030  LOAD_STR                 'Functional Class'
             2032  LOAD_STR                 'Gene'

 L. 281      2034  LOAD_STR                 'Impact'
             2036  LOAD_STR                 'Variant is Clinical'
             2038  LOAD_STR                 '100Genomes Frequency'
             2040  LOAD_STR                 'dbSNP135 Frequency'

 L. 282      2042  LOAD_STR                 'ESP5400 Frequency'
             2044  LOAD_STR                 'ESP5400 EA/AA/ALL'
             2046  LOAD_STR                 'ESP5400 Total Allele Count'

 L. 283      2048  LOAD_STR                 'SIFT'
             2050  LOAD_STR                 'Polyphen2'
             2052  LOAD_STR                 'dbSNP Build'
             2054  LOAD_STR                 'Amino Acid Change'

 L. 284      2056  LOAD_STR                 'Cdna Position'
             2058  LOAD_STR                 'Granthamscore'
             2060  LOAD_STR                 'Protein Position'
             2062  BUILD_LIST_27        27 
             2064  CALL_METHOD_1         1  '1 positional argument'
             2066  POP_TOP          

 L. 285      2068  SETUP_LOOP         2202  'to 2202'
             2070  LOAD_FAST                'variants'
             2072  GET_ITER         
             2074  FOR_ITER           2200  'to 2200'
             2076  STORE_FAST               'variant'

 L. 286      2078  LOAD_FAST                'writer'
             2080  LOAD_METHOD              writerow
             2082  LOAD_FAST                'variant'
             2084  LOAD_ATTR                individual
             2086  LOAD_FAST                'variant'
             2088  LOAD_ATTR                chromossome

 L. 287      2090  LOAD_FAST                'variant'
             2092  LOAD_ATTR                variant_id
             2094  LOAD_FAST                'variant'
             2096  LOAD_ATTR                pos
             2098  LOAD_FAST                'variant'
             2100  LOAD_ATTR                qual
             2102  LOAD_FAST                'variant'
             2104  LOAD_ATTR                ref

 L. 288      2106  LOAD_FAST                'variant'
             2108  LOAD_ATTR                alt
             2110  LOAD_FAST                'variant'
             2112  LOAD_ATTR                genotype
             2114  LOAD_FAST                'variant'
             2116  LOAD_ATTR                genotype_info

 L. 289      2118  LOAD_FAST                'variant'
             2120  LOAD_ATTR                read_depth
             2122  LOAD_FAST                'variant'
             2124  LOAD_ATTR                snp_eff

 L. 290      2126  LOAD_FAST                'variant'
             2128  LOAD_ATTR                snp_eff_functional_class
             2130  LOAD_FAST                'variant'
             2132  LOAD_ATTR                gene_name
             2134  LOAD_FAST                'variant'
             2136  LOAD_ATTR                impact

 L. 291      2138  LOAD_FAST                'variant'
             2140  LOAD_ATTR                dbsnp_pm
             2142  LOAD_FAST                'variant'
             2144  LOAD_ATTR                genomes1k_maf
             2146  LOAD_FAST                'variant'
             2148  LOAD_ATTR                dbsnp_gmaf

 L. 292      2150  LOAD_FAST                'variant'
             2152  LOAD_ATTR                esp_maf_total
             2154  LOAD_FAST                'variant'
             2156  LOAD_ATTR                ann_esp_maf
             2158  LOAD_FAST                'variant'
             2160  LOAD_ATTR                tac

 L. 293      2162  LOAD_FAST                'variant'
             2164  LOAD_ATTR                sift
             2166  LOAD_FAST                'variant'
             2168  LOAD_ATTR                polyphen
             2170  LOAD_FAST                'variant'
             2172  LOAD_ATTR                dbsnp_build

 L. 294      2174  LOAD_FAST                'variant'
             2176  LOAD_ATTR                amino_acid_change
             2178  LOAD_FAST                'variant'
             2180  LOAD_ATTR                cdna_position

 L. 295      2182  LOAD_FAST                'variant'
             2184  LOAD_ATTR                granthamscore
             2186  LOAD_FAST                'variant'
             2188  LOAD_ATTR                protein_position
             2190  BUILD_LIST_27        27 
             2192  CALL_METHOD_1         1  '1 positional argument'
             2194  POP_TOP          
         2196_2198  JUMP_BACK          2074  'to 2074'
             2200  POP_BLOCK        
           2202_0  COME_FROM_LOOP     2068  '2068'

 L. 296      2202  LOAD_FAST                'response'
             2204  RETURN_VALUE     
           2206_0  COME_FROM          1914  '1914'

 L. 298      2206  LOAD_FAST                'variants'
             2208  LOAD_ATTR                values_list
             2210  LOAD_STR                 'gene_name'
             2212  LOAD_CONST               True
             2214  LOAD_CONST               ('flat',)
             2216  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2218  LOAD_FAST                'summary'
             2220  LOAD_STR                 'genes'
             2222  STORE_SUBSCR     

 L. 299      2224  LOAD_GLOBAL              sorted
             2226  LOAD_GLOBAL              list
             2228  LOAD_GLOBAL              set
             2230  LOAD_FAST                'summary'
             2232  LOAD_STR                 'genes'
             2234  BINARY_SUBSCR    
             2236  CALL_FUNCTION_1       1  '1 positional argument'
             2238  CALL_FUNCTION_1       1  '1 positional argument'
             2240  CALL_FUNCTION_1       1  '1 positional argument'
             2242  LOAD_FAST                'summary'
             2244  LOAD_STR                 'genes'
             2246  STORE_SUBSCR     

 L. 300      2248  LOAD_GLOBAL              len
             2250  LOAD_FAST                'summary'
             2252  LOAD_STR                 'genes'
             2254  BINARY_SUBSCR    
             2256  CALL_FUNCTION_1       1  '1 positional argument'
             2258  LOAD_FAST                'summary'
             2260  LOAD_STR                 'n_genes'
             2262  STORE_SUBSCR     

 L. 301      2264  LOAD_CONST               True
             2266  LOAD_FAST                'summary'
             2268  LOAD_STR                 'has_variants'
             2270  STORE_SUBSCR     

 L. 303      2272  LOAD_FAST                'summary'
             2274  LOAD_STR                 'n_genes'
             2276  BINARY_SUBSCR    
             2278  LOAD_CONST               500
             2280  COMPARE_OP               <
         2282_2284  POP_JUMP_IF_FALSE  2482  'to 2482'

 L. 304      2286  LOAD_GLOBAL              Gene
             2288  LOAD_ATTR                objects
             2290  LOAD_ATTR                filter
             2292  LOAD_GLOBAL              list
             2294  LOAD_FAST                'summary'
             2296  LOAD_STR                 'genes'
             2298  BINARY_SUBSCR    
             2300  CALL_FUNCTION_1       1  '1 positional argument'
             2302  LOAD_CONST               ('symbol__in',)
             2304  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2306  LOAD_METHOD              values
             2308  LOAD_STR                 'symbol'
             2310  LOAD_STR                 'diseases'
             2312  CALL_METHOD_2         2  '2 positional arguments'
             2314  LOAD_METHOD              prefetch_related
             2316  LOAD_STR                 'diseases'
             2318  CALL_METHOD_1         1  '1 positional argument'
             2320  STORE_FAST               'genes'

 L. 305      2322  LOAD_GLOBAL              HGMDGene
             2324  LOAD_ATTR                objects
             2326  LOAD_ATTR                filter
             2328  LOAD_GLOBAL              list
             2330  LOAD_FAST                'summary'
             2332  LOAD_STR                 'genes'
             2334  BINARY_SUBSCR    
             2336  CALL_FUNCTION_1       1  '1 positional argument'
             2338  LOAD_CONST               ('symbol__in',)
             2340  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2342  LOAD_METHOD              prefetch_related
             2344  LOAD_STR                 'diseases'
             2346  CALL_METHOD_1         1  '1 positional argument'
             2348  STORE_FAST               'genes_hgmd'

 L. 308      2350  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2352  LOAD_STR                 'family_analysis.<locals>.<listcomp>'
             2354  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2356  LOAD_GLOBAL              list
             2358  LOAD_FAST                'summary'
             2360  LOAD_STR                 'genes'
             2362  BINARY_SUBSCR    
             2364  CALL_FUNCTION_1       1  '1 positional argument'
             2366  GET_ITER         
             2368  CALL_FUNCTION_1       1  '1 positional argument'
             2370  STORE_FAST               'queries'

 L. 309      2372  LOAD_GLOBAL              len
             2374  LOAD_FAST                'queries'
             2376  CALL_FUNCTION_1       1  '1 positional argument'
             2378  LOAD_CONST               0
             2380  COMPARE_OP               >
         2382_2384  POP_JUMP_IF_FALSE  2448  'to 2448'

 L. 310      2386  LOAD_FAST                'queries'
             2388  LOAD_METHOD              pop
             2390  CALL_METHOD_0         0  '0 positional arguments'
             2392  STORE_FAST               'query'

 L. 311      2394  SETUP_LOOP         2418  'to 2418'
             2396  LOAD_FAST                'queries'
             2398  GET_ITER         
             2400  FOR_ITER           2416  'to 2416'
             2402  STORE_FAST               'item'

 L. 312      2404  LOAD_FAST                'query'
             2406  LOAD_FAST                'item'
             2408  INPLACE_OR       
             2410  STORE_FAST               'query'
         2412_2414  JUMP_BACK          2400  'to 2400'
             2416  POP_BLOCK        
           2418_0  COME_FROM_LOOP     2394  '2394'

 L. 313      2418  LOAD_GLOBAL              GeneDisease
             2420  LOAD_ATTR                objects
             2422  LOAD_ATTR                filter
             2424  LOAD_GLOBAL              list
             2426  LOAD_FAST                'summary'
             2428  LOAD_STR                 'genes'
             2430  BINARY_SUBSCR    
             2432  CALL_FUNCTION_1       1  '1 positional argument'
             2434  LOAD_CONST               ('official_name__in',)
             2436  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2438  LOAD_METHOD              prefetch_related
             2440  LOAD_STR                 'diseases'
             2442  CALL_METHOD_1         1  '1 positional argument'
             2444  STORE_FAST               'genes_omim'
             2446  JUMP_FORWARD       2452  'to 2452'
           2448_0  COME_FROM          2382  '2382'

 L. 315      2448  BUILD_LIST_0          0 
             2450  STORE_FAST               'genes_omim'
           2452_0  COME_FROM          2446  '2446'

 L. 317      2452  LOAD_GLOBAL              CGDEntry
             2454  LOAD_ATTR                objects
             2456  LOAD_ATTR                filter
             2458  LOAD_GLOBAL              list
             2460  LOAD_FAST                'summary'
             2462  LOAD_STR                 'genes'
             2464  BINARY_SUBSCR    
             2466  CALL_FUNCTION_1       1  '1 positional argument'
             2468  LOAD_CONST               ('GENE__in',)
             2470  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2472  LOAD_METHOD              prefetch_related
             2474  LOAD_STR                 'CONDITIONS'
             2476  CALL_METHOD_1         1  '1 positional argument'
             2478  STORE_FAST               'genes_cgd'
             2480  JUMP_FORWARD       2498  'to 2498'
           2482_0  COME_FROM          2282  '2282'

 L. 320      2482  BUILD_LIST_0          0 
             2484  STORE_FAST               'genes'

 L. 321      2486  BUILD_LIST_0          0 
             2488  STORE_FAST               'genes_hgmd'

 L. 322      2490  BUILD_LIST_0          0 
             2492  STORE_FAST               'genes_omim'

 L. 323      2494  BUILD_LIST_0          0 
             2496  STORE_FAST               'genes_cgd'
           2498_0  COME_FROM          2480  '2480'

 L. 325      2498  LOAD_GLOBAL              len
             2500  LOAD_FAST                'variants'
             2502  CALL_FUNCTION_1       1  '1 positional argument'
             2504  LOAD_FAST                'summary'
             2506  LOAD_STR                 'n_variants'
             2508  STORE_SUBSCR     

 L. 326      2510  LOAD_GLOBAL              Paginator
             2512  LOAD_FAST                'variants'
             2514  LOAD_CONST               25
             2516  CALL_FUNCTION_2       2  '2 positional arguments'
             2518  STORE_FAST               'paginator'

 L. 327      2520  SETUP_EXCEPT       2544  'to 2544'

 L. 328      2522  LOAD_GLOBAL              int
             2524  LOAD_FAST                'request'
             2526  LOAD_ATTR                GET
             2528  LOAD_METHOD              get
             2530  LOAD_STR                 'page'
             2532  LOAD_STR                 '1'
             2534  CALL_METHOD_2         2  '2 positional arguments'
             2536  CALL_FUNCTION_1       1  '1 positional argument'
             2538  STORE_FAST               'page'
             2540  POP_BLOCK        
             2542  JUMP_FORWARD       2570  'to 2570'
           2544_0  COME_FROM_EXCEPT   2520  '2520'

 L. 329      2544  DUP_TOP          
             2546  LOAD_GLOBAL              ValueError
             2548  COMPARE_OP               exception-match
         2550_2552  POP_JUMP_IF_FALSE  2568  'to 2568'
             2554  POP_TOP          
             2556  POP_TOP          
             2558  POP_TOP          

 L. 330      2560  LOAD_CONST               1
             2562  STORE_FAST               'page'
             2564  POP_EXCEPT       
             2566  JUMP_FORWARD       2570  'to 2570'
           2568_0  COME_FROM          2550  '2550'
             2568  END_FINALLY      
           2570_0  COME_FROM          2566  '2566'
           2570_1  COME_FROM          2542  '2542'

 L. 331      2570  SETUP_EXCEPT       2586  'to 2586'

 L. 332      2572  LOAD_FAST                'paginator'
             2574  LOAD_METHOD              page
             2576  LOAD_FAST                'page'
             2578  CALL_METHOD_1         1  '1 positional argument'
             2580  STORE_FAST               'variants'
             2582  POP_BLOCK        
             2584  JUMP_FORWARD       2650  'to 2650'
           2586_0  COME_FROM_EXCEPT   2570  '2570'

 L. 333      2586  DUP_TOP          
             2588  LOAD_GLOBAL              PageNotAnInteger
             2590  COMPARE_OP               exception-match
         2592_2594  POP_JUMP_IF_FALSE  2616  'to 2616'
             2596  POP_TOP          
             2598  POP_TOP          
             2600  POP_TOP          

 L. 335      2602  LOAD_FAST                'paginator'
             2604  LOAD_METHOD              page
             2606  LOAD_CONST               1
             2608  CALL_METHOD_1         1  '1 positional argument'
             2610  STORE_FAST               'variants'
             2612  POP_EXCEPT       
             2614  JUMP_FORWARD       2650  'to 2650'
           2616_0  COME_FROM          2592  '2592'

 L. 336      2616  DUP_TOP          
             2618  LOAD_GLOBAL              EmptyPage
             2620  COMPARE_OP               exception-match
         2622_2624  POP_JUMP_IF_FALSE  2648  'to 2648'
             2626  POP_TOP          
             2628  POP_TOP          
             2630  POP_TOP          

 L. 338      2632  LOAD_FAST                'paginator'
             2634  LOAD_METHOD              page
             2636  LOAD_FAST                'paginator'
             2638  LOAD_ATTR                num_pages
             2640  CALL_METHOD_1         1  '1 positional argument'
             2642  STORE_FAST               'variants'
             2644  POP_EXCEPT       
             2646  JUMP_FORWARD       2650  'to 2650'
           2648_0  COME_FROM          2622  '2622'
             2648  END_FINALLY      
           2650_0  COME_FROM          2646  '2646'
           2650_1  COME_FROM          2614  '2614'
           2650_2  COME_FROM          2584  '2584'
             2650  JUMP_FORWARD       2698  'to 2698'
           2652_0  COME_FROM           146  '146'
           2652_1  COME_FROM           136  '136'

 L. 341      2652  BUILD_LIST_0          0 
             2654  STORE_FAST               'variants'

 L. 342      2656  BUILD_MAP_0           0 
             2658  STORE_FAST               'summary'

 L. 343      2660  LOAD_CONST               False
             2662  LOAD_FAST                'summary'
             2664  LOAD_STR                 'has_variants'
             2666  STORE_SUBSCR     

 L. 345      2668  LOAD_CONST               1000
             2670  LOAD_FAST                'summary'
             2672  LOAD_STR                 'n_genes'
             2674  STORE_SUBSCR     

 L. 346      2676  BUILD_LIST_0          0 
             2678  STORE_FAST               'genes'

 L. 347      2680  BUILD_LIST_0          0 
             2682  STORE_FAST               'genes_hgmd'

 L. 348      2684  BUILD_LIST_0          0 
             2686  STORE_FAST               'genes_omim'

 L. 349      2688  BUILD_LIST_0          0 
             2690  STORE_FAST               'genes_cgd'

 L. 351      2692  LOAD_GLOBAL              FilterAnalysisForm
             2694  CALL_FUNCTION_0       0  '0 positional arguments'
             2696  STORE_FAST               'form'
           2698_0  COME_FROM          2650  '2650'
           2698_1  COME_FROM           158  '158'

 L. 352      2698  LOAD_GLOBAL              render
             2700  LOAD_FAST                'request'
             2702  LOAD_STR                 'filter_analysis/index.html'

 L. 353      2704  LOAD_FAST                'variants'

 L. 354      2706  LOAD_FAST                'form'

 L. 355      2708  LOAD_FAST                'summary'

 L. 356      2710  LOAD_FAST                'query_string'

 L. 357      2712  LOAD_FAST                'filteranalysis'

 L. 358      2714  LOAD_FAST                'filterconfigs'

 L. 359      2716  LOAD_FAST                'genes'

 L. 360      2718  LOAD_FAST                'genes_hgmd'

 L. 361      2720  LOAD_FAST                'genes_omim'

 L. 362      2722  LOAD_FAST                'genes_cgd'
             2724  LOAD_CONST               ('variants', 'form', 'summary', 'query_string', 'filteranalysis', 'filterconfigs', 'genes', 'genes_hgmd', 'genes_omim', 'genes_cgd')
             2726  BUILD_CONST_KEY_MAP_10    10 
             2728  CALL_FUNCTION_3       3  '3 positional arguments'
             2730  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 1570_1


@login_required
def oldfamily_analysis--- This code section failed: ---

 L. 368         0  BUILD_MAP_0           0 
                2  STORE_FAST               'query'

 L. 369         4  BUILD_MAP_0           0 
                6  STORE_FAST               'exclude'

 L. 370         8  BUILD_MAP_0           0 
               10  STORE_FAST               'summary'

 L. 371        12  BUILD_LIST_0          0 
               14  STORE_FAST               'args'

 L. 372        16  LOAD_FAST                'request'
               18  LOAD_ATTR                META
               20  LOAD_STR                 'QUERY_STRING'
               22  BINARY_SUBSCR    
               24  STORE_FAST               'query_string'

 L. 373        26  BUILD_LIST_0          0 
               28  STORE_FAST               'new_query_string'

 L. 375        30  SETUP_LOOP           70  'to 70'
               32  LOAD_FAST                'query_string'
               34  LOAD_METHOD              split
               36  LOAD_STR                 '&'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  GET_ITER         
             42_0  COME_FROM            54  '54'
               42  FOR_ITER             68  'to 68'
               44  STORE_FAST               'item'

 L. 376        46  LOAD_FAST                'item'
               48  LOAD_METHOD              startswith
               50  LOAD_STR                 'page'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_JUMP_IF_TRUE     42  'to 42'

 L. 377        56  LOAD_FAST                'new_query_string'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'item'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_TOP          
               66  JUMP_BACK            42  'to 42'
               68  POP_BLOCK        
             70_0  COME_FROM_LOOP       30  '30'

 L. 378        70  LOAD_STR                 '&'
               72  LOAD_METHOD              join
               74  LOAD_FAST                'new_query_string'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  STORE_FAST               'query_string'

 L. 380        80  LOAD_GLOBAL              print
               82  LOAD_STR                 'query string'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  POP_TOP          

 L. 381        88  LOAD_GLOBAL              print
               90  LOAD_FAST                'query_string'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  POP_TOP          

 L. 383        96  LOAD_GLOBAL              FamilyFilterAnalysis
               98  LOAD_ATTR                objects
              100  LOAD_METHOD              all
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  STORE_FAST               'filteranalysis'

 L. 384       106  LOAD_GLOBAL              FilterConfig
              108  LOAD_ATTR                objects
              110  LOAD_METHOD              all
              112  CALL_METHOD_0         0  '0 positional arguments'
              114  STORE_FAST               'filterconfigs'

 L. 386       116  LOAD_FAST                'query_string'
              118  LOAD_STR                 ''
              120  BUILD_LIST_1          1 
              122  COMPARE_OP               !=
          124_126  POP_JUMP_IF_FALSE  4144  'to 4144'
              128  LOAD_FAST                'query_string'
              130  LOAD_STR                 ''
              132  COMPARE_OP               !=
          134_136  POP_JUMP_IF_FALSE  4144  'to 4144'

 L. 387       138  LOAD_FAST                'request'
              140  LOAD_ATTR                method
              142  LOAD_STR                 'GET'
              144  COMPARE_OP               ==
          146_148  POP_JUMP_IF_FALSE  4158  'to 4158'

 L. 388       150  LOAD_FAST                'request'
              152  LOAD_ATTR                GET
              154  LOAD_METHOD              copy
              156  CALL_METHOD_0         0  '0 positional arguments'
              158  LOAD_FAST                'request'
              160  STORE_ATTR               GET

 L. 389       162  LOAD_GLOBAL              FamilyAnalysisForm
              164  LOAD_FAST                'request'
              166  LOAD_ATTR                GET
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  STORE_FAST               'form'

 L. 391       172  LOAD_FAST                'request'
              174  LOAD_ATTR                GET
              176  LOAD_METHOD              get
              178  LOAD_STR                 'inheritance_option'
              180  LOAD_STR                 ''
              182  CALL_METHOD_2         2  '2 positional arguments'
              184  STORE_FAST               'inheritance_option'

 L. 392       186  LOAD_FAST                'request'
              188  LOAD_ATTR                GET
              190  LOAD_METHOD              get
              192  LOAD_STR                 'remove_not_in_parents'
              194  LOAD_STR                 ''
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  STORE_FAST               'remove_not_in_parents'

 L. 393       200  LOAD_FAST                'request'
              202  LOAD_ATTR                GET
              204  LOAD_METHOD              get
              206  LOAD_STR                 'remove_in_both_parents'
              208  LOAD_STR                 ''
              210  CALL_METHOD_2         2  '2 positional arguments'
              212  STORE_FAST               'remove_in_both_parents'

 L. 396       214  LOAD_GLOBAL              filter_inheritance_option
              216  LOAD_FAST                'request'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  POP_TOP          

 L. 398       222  LOAD_GLOBAL              filter_chr
              224  LOAD_FAST                'request'
              226  LOAD_FAST                'query'
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  POP_TOP          

 L. 400       232  LOAD_GLOBAL              filter_pos
              234  LOAD_FAST                'request'
              236  LOAD_FAST                'query'
              238  CALL_FUNCTION_2       2  '2 positional arguments'
              240  POP_TOP          

 L. 402       242  LOAD_GLOBAL              filter_snp_list
              244  LOAD_FAST                'request'
              246  LOAD_FAST                'query'
              248  CALL_FUNCTION_2       2  '2 positional arguments'
              250  POP_TOP          

 L. 404       252  LOAD_GLOBAL              filter_gene_list
              254  LOAD_FAST                'request'
              256  LOAD_FAST                'query'
              258  LOAD_FAST                'args'
              260  CALL_FUNCTION_3       3  '3 positional arguments'
              262  POP_TOP          

 L. 406       264  LOAD_GLOBAL              filter_mutation_type
              266  LOAD_FAST                'request'
              268  LOAD_FAST                'args'
              270  CALL_FUNCTION_2       2  '2 positional arguments'
              272  POP_TOP          

 L. 408       274  LOAD_GLOBAL              filter_cln
              276  LOAD_FAST                'request'
              278  LOAD_FAST                'query'
              280  CALL_FUNCTION_2       2  '2 positional arguments'
              282  POP_TOP          

 L. 410       284  LOAD_GLOBAL              filter_variant_type_snpeff
              286  LOAD_FAST                'request'
              288  LOAD_FAST                'query'
              290  CALL_FUNCTION_2       2  '2 positional arguments'
              292  POP_TOP          

 L. 412       294  LOAD_GLOBAL              filter_dbsnp
              296  LOAD_FAST                'request'
              298  LOAD_FAST                'query'
              300  CALL_FUNCTION_2       2  '2 positional arguments'
              302  POP_TOP          

 L. 414       304  LOAD_GLOBAL              filter_by_1000g
              306  LOAD_FAST                'request'
              308  LOAD_FAST                'args'
              310  CALL_FUNCTION_2       2  '2 positional arguments'
              312  POP_TOP          

 L. 416       314  LOAD_GLOBAL              filter_by_dbsnp
              316  LOAD_FAST                'request'
              318  LOAD_FAST                'args'
              320  CALL_FUNCTION_2       2  '2 positional arguments'
              322  POP_TOP          

 L. 418       324  LOAD_GLOBAL              filter_by_esp
              326  LOAD_FAST                'request'
              328  LOAD_FAST                'args'
              330  CALL_FUNCTION_2       2  '2 positional arguments'
              332  POP_TOP          

 L. 420       334  LOAD_GLOBAL              filter_by_hi_score
              336  LOAD_FAST                'request'
              338  LOAD_FAST                'args'
              340  CALL_FUNCTION_2       2  '2 positional arguments'
              342  POP_TOP          

 L. 422       344  LOAD_GLOBAL              filter_by_sift
              346  LOAD_FAST                'request'
              348  LOAD_FAST                'args'
              350  CALL_FUNCTION_2       2  '2 positional arguments'
              352  POP_TOP          

 L. 424       354  LOAD_GLOBAL              filter_by_pp2
              356  LOAD_FAST                'request'
              358  LOAD_FAST                'args'
              360  CALL_FUNCTION_2       2  '2 positional arguments'
              362  POP_TOP          

 L. 425       364  LOAD_GLOBAL              filter_by_segdup
              366  LOAD_FAST                'request'
              368  LOAD_FAST                'args'
              370  CALL_FUNCTION_2       2  '2 positional arguments'
              372  POP_TOP          

 L. 427       374  LOAD_GLOBAL              filter_omim
              376  LOAD_FAST                'request'
              378  LOAD_FAST                'args'
              380  CALL_FUNCTION_2       2  '2 positional arguments'
              382  POP_TOP          

 L. 428       384  LOAD_GLOBAL              filter_cgd
              386  LOAD_FAST                'request'
              388  LOAD_FAST                'args'
              390  CALL_FUNCTION_2       2  '2 positional arguments'
              392  POP_TOP          

 L. 429       394  LOAD_GLOBAL              filter_hgmd
              396  LOAD_FAST                'request'
              398  LOAD_FAST                'args'
              400  CALL_FUNCTION_2       2  '2 positional arguments'
              402  POP_TOP          

 L. 430       404  LOAD_GLOBAL              filter_genelists
              406  LOAD_FAST                'request'
              408  LOAD_FAST                'query'
              410  LOAD_FAST                'args'
              412  LOAD_FAST                'exclude'
              414  CALL_FUNCTION_4       4  '4 positional arguments'
              416  POP_TOP          

 L. 432       418  LOAD_GLOBAL              filter_dbsnp_build
              420  LOAD_FAST                'request'
              422  LOAD_FAST                'query'
              424  CALL_FUNCTION_2       2  '2 positional arguments'
              426  POP_TOP          

 L. 434       428  LOAD_GLOBAL              filter_read_depth
              430  LOAD_FAST                'request'
              432  LOAD_FAST                'args'
              434  CALL_FUNCTION_2       2  '2 positional arguments'
              436  POP_TOP          

 L. 435       438  LOAD_GLOBAL              filter_qual
              440  LOAD_FAST                'request'
              442  LOAD_FAST                'args'
              444  CALL_FUNCTION_2       2  '2 positional arguments'
              446  POP_TOP          

 L. 436       448  LOAD_GLOBAL              filter_filter
              450  LOAD_FAST                'request'
              452  LOAD_FAST                'query'
              454  CALL_FUNCTION_2       2  '2 positional arguments'
              456  POP_TOP          

 L. 438       458  LOAD_GLOBAL              filter_func_class
              460  LOAD_FAST                'request'
              462  LOAD_FAST                'query'
              464  CALL_FUNCTION_2       2  '2 positional arguments'
              466  POP_TOP          

 L. 440       468  LOAD_GLOBAL              filter_impact
              470  LOAD_FAST                'request'
              472  LOAD_FAST                'query'
              474  CALL_FUNCTION_2       2  '2 positional arguments'
              476  POP_TOP          

 L. 445       478  LOAD_GLOBAL              print
              480  LOAD_STR                 'Get family variants'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  POP_TOP          

 L. 446       486  LOAD_FAST                'request'
              488  LOAD_ATTR                GET
              490  LOAD_METHOD              get
              492  LOAD_STR                 'father'
              494  LOAD_STR                 ''
              496  CALL_METHOD_2         2  '2 positional arguments'
              498  STORE_FAST               'father'

 L. 447       500  LOAD_FAST                'request'
              502  LOAD_ATTR                GET
              504  LOAD_METHOD              get
              506  LOAD_STR                 'mother'
              508  LOAD_STR                 ''
              510  CALL_METHOD_2         2  '2 positional arguments'
              512  STORE_FAST               'mother'

 L. 448       514  LOAD_FAST                'request'
              516  LOAD_ATTR                GET
              518  LOAD_METHOD              getlist
              520  LOAD_STR                 'children'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  STORE_FAST               'children'

 L. 450       526  BUILD_MAP_0           0 
              528  BUILD_MAP_0           0 
              530  LOAD_CONST               ('father', 'mother')
              532  BUILD_CONST_KEY_MAP_2     2 
              534  STORE_FAST               'parents_variants'

 L. 451       536  LOAD_FAST                'father'
              538  LOAD_FAST                'mother'
              540  LOAD_CONST               ('father', 'mother')
              542  BUILD_CONST_KEY_MAP_2     2 
              544  STORE_FAST               'parents'

 L. 453       546  SETUP_LOOP          754  'to 754'
              548  LOAD_FAST                'parents'
              550  GET_ITER         
              552  FOR_ITER            752  'to 752'
              554  STORE_FAST               'individual'

 L. 454       556  LOAD_FAST                'parents'
              558  LOAD_FAST                'individual'
              560  BINARY_SUBSCR    
              562  BUILD_LIST_1          1 
              564  LOAD_FAST                'query'
              566  LOAD_STR                 'individual_id__in'
              568  STORE_SUBSCR     

 L. 455       570  LOAD_GLOBAL              print
              572  LOAD_FAST                'query'
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  POP_TOP          

 L. 456       578  LOAD_GLOBAL              Variant
              580  LOAD_ATTR                objects
              582  LOAD_ATTR                filter
              584  LOAD_FAST                'args'
              586  LOAD_FAST                'query'
              588  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              590  LOAD_METHOD              values
              592  LOAD_STR                 'chromossome'
              594  LOAD_STR                 'pos'
              596  LOAD_STR                 'genotype'
              598  LOAD_STR                 'gene_name'
              600  CALL_METHOD_4         4  '4 positional arguments'
              602  STORE_FAST               'individual_variants'

 L. 457       604  LOAD_GLOBAL              print
              606  LOAD_STR                 'individual variants'
              608  CALL_FUNCTION_1       1  '1 positional argument'
              610  POP_TOP          

 L. 458       612  LOAD_GLOBAL              print
              614  LOAD_FAST                'individual'
              616  LOAD_FAST                'parents'
              618  LOAD_FAST                'individual'
              620  BINARY_SUBSCR    
              622  CALL_FUNCTION_2       2  '2 positional arguments'
              624  POP_TOP          

 L. 459       626  LOAD_GLOBAL              print
              628  LOAD_GLOBAL              len
              630  LOAD_FAST                'individual_variants'
              632  CALL_FUNCTION_1       1  '1 positional argument'
              634  CALL_FUNCTION_1       1  '1 positional argument'
              636  POP_TOP          

 L. 460       638  SETUP_LOOP          748  'to 748'
              640  LOAD_FAST                'individual_variants'
              642  GET_ITER         
              644  FOR_ITER            746  'to 746'
              646  STORE_FAST               'variant'

 L. 461       648  LOAD_STR                 '%s-%s'
              650  LOAD_FAST                'variant'
              652  LOAD_STR                 'chromossome'
              654  BINARY_SUBSCR    
              656  LOAD_FAST                'variant'
              658  LOAD_STR                 'pos'
              660  BINARY_SUBSCR    
              662  BUILD_TUPLE_2         2 
              664  BINARY_MODULO    
              666  STORE_FAST               'id'

 L. 462       668  LOAD_FAST                'variant'
              670  LOAD_STR                 'gene_name'
              672  BINARY_SUBSCR    
              674  STORE_FAST               'gene'

 L. 464       676  LOAD_FAST                'gene'
              678  LOAD_FAST                'parents_variants'
              680  LOAD_FAST                'individual'
              682  BINARY_SUBSCR    
              684  COMPARE_OP               not-in
          686_688  POP_JUMP_IF_FALSE   702  'to 702'

 L. 465       690  BUILD_MAP_0           0 
              692  LOAD_FAST                'parents_variants'
              694  LOAD_FAST                'individual'
              696  BINARY_SUBSCR    
              698  LOAD_FAST                'gene'
              700  STORE_SUBSCR     
            702_0  COME_FROM           686  '686'

 L. 466       702  BUILD_MAP_0           0 
              704  LOAD_FAST                'parents_variants'
              706  LOAD_FAST                'individual'
              708  BINARY_SUBSCR    
              710  LOAD_FAST                'gene'
              712  BINARY_SUBSCR    
              714  LOAD_FAST                'id'
              716  STORE_SUBSCR     

 L. 467       718  LOAD_CONST               0
              720  LOAD_FAST                'parents_variants'
              722  LOAD_FAST                'individual'
              724  BINARY_SUBSCR    
              726  LOAD_FAST                'gene'
              728  BINARY_SUBSCR    
              730  LOAD_FAST                'id'
              732  BINARY_SUBSCR    
              734  LOAD_FAST                'variant'
              736  LOAD_STR                 'genotype'
              738  BINARY_SUBSCR    
              740  STORE_SUBSCR     
          742_744  JUMP_BACK           644  'to 644'
              746  POP_BLOCK        
            748_0  COME_FROM_LOOP      638  '638'
          748_750  JUMP_BACK           552  'to 552'
              752  POP_BLOCK        
            754_0  COME_FROM_LOOP      546  '546'

 L. 470       754  LOAD_GLOBAL              filter_inheritance_option_exclude_individuals
              756  LOAD_FAST                'request'
              758  CALL_FUNCTION_1       1  '1 positional argument'
              760  POP_TOP          

 L. 472       762  LOAD_FAST                'request'
              764  LOAD_ATTR                GET
              766  LOAD_METHOD              getlist
              768  LOAD_STR                 'exclude_individuals'
              770  CALL_METHOD_1         1  '1 positional argument'
              772  STORE_FAST               'exclude_individuals'

 L. 474       774  LOAD_GLOBAL              print
              776  LOAD_STR                 'exclude individuals %s'
              778  LOAD_FAST                'exclude_individuals'
              780  BINARY_MODULO    
              782  CALL_FUNCTION_1       1  '1 positional argument'
              784  POP_TOP          

 L. 477       786  LOAD_FAST                'request'
              788  LOAD_ATTR                GET
              790  LOAD_METHOD              getlist
              792  LOAD_STR                 'exclude_groups'
              794  CALL_METHOD_1         1  '1 positional argument'
              796  STORE_FAST               'exclude_groups'

 L. 478       798  LOAD_GLOBAL              print
              800  LOAD_FAST                'exclude_groups'
              802  CALL_FUNCTION_1       1  '1 positional argument'
              804  POP_TOP          

 L. 479       806  BUILD_LIST_0          0 
              808  STORE_FAST               'exclude_individuals_list'

 L. 480       810  LOAD_GLOBAL              len
              812  LOAD_FAST                'exclude_groups'
              814  CALL_FUNCTION_1       1  '1 positional argument'
              816  LOAD_CONST               0
              818  COMPARE_OP               >
          820_822  POP_JUMP_IF_FALSE   898  'to 898'

 L. 481       824  SETUP_LOOP          898  'to 898'
              826  LOAD_FAST                'exclude_groups'
              828  GET_ITER         
              830  FOR_ITER            896  'to 896'
              832  STORE_FAST               'group_id'

 L. 482       834  LOAD_GLOBAL              get_object_or_404
              836  LOAD_GLOBAL              Group
              838  LOAD_FAST                'group_id'
              840  LOAD_CONST               ('pk',)
              842  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              844  LOAD_ATTR                members
              846  LOAD_ATTR                values_list
              848  LOAD_STR                 'id'
              850  LOAD_CONST               True
              852  LOAD_CONST               ('flat',)
              854  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              856  STORE_FAST               'group_individuals'

 L. 483       858  SETUP_LOOP          892  'to 892'
              860  LOAD_FAST                'group_individuals'
              862  GET_ITER         
              864  FOR_ITER            890  'to 890'
              866  STORE_FAST               'individual'

 L. 484       868  LOAD_FAST                'exclude_individuals_list'
              870  LOAD_METHOD              append
              872  LOAD_GLOBAL              str
              874  LOAD_GLOBAL              str
              876  LOAD_FAST                'individual'
              878  CALL_FUNCTION_1       1  '1 positional argument'
              880  CALL_FUNCTION_1       1  '1 positional argument'
              882  CALL_METHOD_1         1  '1 positional argument'
              884  POP_TOP          
          886_888  JUMP_BACK           864  'to 864'
              890  POP_BLOCK        
            892_0  COME_FROM_LOOP      858  '858'
          892_894  JUMP_BACK           830  'to 830'
              896  POP_BLOCK        
            898_0  COME_FROM_LOOP      824  '824'
            898_1  COME_FROM           820  '820'

 L. 487       898  LOAD_FAST                'exclude_individuals_list'
              900  LOAD_FAST                'exclude_individuals'
              902  BINARY_ADD       
              904  STORE_FAST               'exclude_individuals_list'

 L. 488       906  LOAD_GLOBAL              print
              908  LOAD_FAST                'exclude_individuals_list'
              910  CALL_FUNCTION_1       1  '1 positional argument'
              912  POP_TOP          

 L. 489       914  BUILD_MAP_0           0 
              916  STORE_FAST               'exclude_individuals_variants'

 L. 491       918  LOAD_GLOBAL              print
              920  LOAD_STR                 '#exclude variants from individuals'
              922  CALL_FUNCTION_1       1  '1 positional argument'
              924  POP_TOP          

 L. 492       926  LOAD_GLOBAL              len
              928  LOAD_FAST                'exclude_individuals_list'
              930  CALL_FUNCTION_1       1  '1 positional argument'
              932  LOAD_CONST               0
              934  COMPARE_OP               >
          936_938  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 494       940  SETUP_LOOP         1106  'to 1106'
              942  LOAD_FAST                'exclude_individuals_list'
              944  GET_ITER         
              946  FOR_ITER           1104  'to 1104'
              948  STORE_FAST               'individual'

 L. 495       950  LOAD_FAST                'individual'
              952  BUILD_LIST_1          1 
              954  LOAD_FAST                'query'
              956  LOAD_STR                 'individual_id__in'
              958  STORE_SUBSCR     

 L. 496       960  LOAD_GLOBAL              print
              962  LOAD_FAST                'query'
              964  CALL_FUNCTION_1       1  '1 positional argument'
              966  POP_TOP          

 L. 498       968  LOAD_GLOBAL              Variant
              970  LOAD_ATTR                objects
              972  LOAD_ATTR                filter
              974  LOAD_FAST                'args'
              976  LOAD_FAST                'query'
              978  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              980  LOAD_ATTR                exclude
              982  BUILD_TUPLE_0         0 
              984  LOAD_FAST                'exclude'
              986  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              988  LOAD_METHOD              values
              990  LOAD_STR                 'chromossome'
              992  LOAD_STR                 'pos'
              994  LOAD_STR                 'genotype'
              996  CALL_METHOD_3         3  '3 positional arguments'
              998  STORE_FAST               'individual_variants'

 L. 499      1000  LOAD_GLOBAL              print
             1002  LOAD_GLOBAL              len
             1004  LOAD_FAST                'individual_variants'
             1006  CALL_FUNCTION_1       1  '1 positional argument'
             1008  CALL_FUNCTION_1       1  '1 positional argument'
             1010  POP_TOP          

 L. 500      1012  SETUP_LOOP         1100  'to 1100'
             1014  LOAD_FAST                'individual_variants'
             1016  GET_ITER         
             1018  FOR_ITER           1098  'to 1098'
             1020  STORE_FAST               'variant'

 L. 501      1022  LOAD_STR                 '%s-%s'
             1024  LOAD_FAST                'variant'
             1026  LOAD_STR                 'chromossome'
             1028  BINARY_SUBSCR    
             1030  LOAD_FAST                'variant'
             1032  LOAD_STR                 'pos'
             1034  BINARY_SUBSCR    
             1036  BUILD_TUPLE_2         2 
             1038  BINARY_MODULO    
             1040  STORE_FAST               'id'

 L. 502      1042  LOAD_FAST                'id'
             1044  LOAD_FAST                'exclude_individuals_variants'
             1046  COMPARE_OP               in
         1048_1050  POP_JUMP_IF_FALSE  1070  'to 1070'

 L. 503      1052  LOAD_CONST               0
             1054  LOAD_FAST                'exclude_individuals_variants'
             1056  LOAD_FAST                'id'
             1058  BINARY_SUBSCR    
             1060  LOAD_FAST                'variant'
             1062  LOAD_STR                 'genotype'
             1064  BINARY_SUBSCR    
             1066  STORE_SUBSCR     
             1068  JUMP_BACK          1018  'to 1018'
           1070_0  COME_FROM          1048  '1048'

 L. 505      1070  BUILD_MAP_0           0 
             1072  LOAD_FAST                'exclude_individuals_variants'
             1074  LOAD_FAST                'id'
             1076  STORE_SUBSCR     

 L. 506      1078  LOAD_CONST               0
             1080  LOAD_FAST                'exclude_individuals_variants'
             1082  LOAD_FAST                'id'
             1084  BINARY_SUBSCR    
             1086  LOAD_FAST                'variant'
             1088  LOAD_STR                 'genotype'
             1090  BINARY_SUBSCR    
             1092  STORE_SUBSCR     
         1094_1096  JUMP_BACK          1018  'to 1018'
             1098  POP_BLOCK        
           1100_0  COME_FROM_LOOP     1012  '1012'
         1100_1102  JUMP_BACK           946  'to 946'
             1104  POP_BLOCK        
           1106_0  COME_FROM_LOOP      940  '940'
           1106_1  COME_FROM           936  '936'

 L. 510      1106  LOAD_GLOBAL              filter_mutation_type
             1108  LOAD_FAST                'request'
             1110  LOAD_FAST                'args'
             1112  CALL_FUNCTION_2       2  '2 positional arguments'
             1114  POP_TOP          

 L. 511      1116  LOAD_GLOBAL              filter_inheritance_option_mutation_type
             1118  LOAD_FAST                'request'
             1120  LOAD_FAST                'args'
             1122  CALL_FUNCTION_2       2  '2 positional arguments'
             1124  POP_TOP          

 L. 516      1126  LOAD_FAST                'request'
             1128  LOAD_ATTR                GET
             1130  LOAD_METHOD              getlist
             1132  LOAD_STR                 'individuals'
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  STORE_FAST               'individuals'

 L. 517      1138  LOAD_FAST                'request'
             1140  LOAD_ATTR                GET
             1142  LOAD_METHOD              getlist
             1144  LOAD_STR                 'groups'
             1146  CALL_METHOD_1         1  '1 positional argument'
             1148  STORE_FAST               'groups'

 L. 519      1150  BUILD_LIST_0          0 
             1152  STORE_FAST               'individuals_list'

 L. 520      1154  LOAD_GLOBAL              len
             1156  LOAD_FAST                'groups'
             1158  CALL_FUNCTION_1       1  '1 positional argument'
             1160  LOAD_CONST               0
             1162  COMPARE_OP               >
         1164_1166  POP_JUMP_IF_FALSE  1250  'to 1250'

 L. 521      1168  SETUP_LOOP         1250  'to 1250'
             1170  LOAD_FAST                'groups'
             1172  GET_ITER         
             1174  FOR_ITER           1248  'to 1248'
             1176  STORE_FAST               'group_id'

 L. 522      1178  LOAD_GLOBAL              get_object_or_404
             1180  LOAD_GLOBAL              Group
             1182  LOAD_FAST                'group_id'
             1184  LOAD_CONST               ('pk',)
             1186  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1188  LOAD_ATTR                members
             1190  LOAD_ATTR                values_list
             1192  LOAD_STR                 'id'
             1194  LOAD_CONST               True
             1196  LOAD_CONST               ('flat',)
             1198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1200  STORE_FAST               'group_individuals'

 L. 523      1202  SETUP_LOOP         1236  'to 1236'
             1204  LOAD_FAST                'group_individuals'
             1206  GET_ITER         
             1208  FOR_ITER           1234  'to 1234'
             1210  STORE_FAST               'individual'

 L. 524      1212  LOAD_FAST                'individuals_list'
             1214  LOAD_METHOD              append
             1216  LOAD_GLOBAL              str
             1218  LOAD_GLOBAL              str
             1220  LOAD_FAST                'individual'
             1222  CALL_FUNCTION_1       1  '1 positional argument'
             1224  CALL_FUNCTION_1       1  '1 positional argument'
             1226  CALL_METHOD_1         1  '1 positional argument'
             1228  POP_TOP          
         1230_1232  JUMP_BACK          1208  'to 1208'
             1234  POP_BLOCK        
           1236_0  COME_FROM_LOOP     1202  '1202'

 L. 525      1236  LOAD_GLOBAL              print
             1238  LOAD_FAST                'individuals_list'
             1240  CALL_FUNCTION_1       1  '1 positional argument'
             1242  POP_TOP          
         1244_1246  JUMP_BACK          1174  'to 1174'
             1248  POP_BLOCK        
           1250_0  COME_FROM_LOOP     1168  '1168'
           1250_1  COME_FROM          1164  '1164'

 L. 527      1250  LOAD_FAST                'individuals_list'
             1252  LOAD_FAST                'individuals'
             1254  BINARY_ADD       
             1256  STORE_FAST               'individuals_list'

 L. 530      1258  LOAD_GLOBAL              len
             1260  LOAD_FAST                'children'
             1262  CALL_FUNCTION_1       1  '1 positional argument'
             1264  LOAD_CONST               0
             1266  COMPARE_OP               >
         1268_1270  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 531      1272  SETUP_LOOP         1298  'to 1298'
             1274  LOAD_FAST                'children'
             1276  GET_ITER         
             1278  FOR_ITER           1296  'to 1296'
             1280  STORE_FAST               'child'

 L. 532      1282  LOAD_FAST                'individuals_list'
             1284  LOAD_METHOD              append
             1286  LOAD_FAST                'child'
             1288  CALL_METHOD_1         1  '1 positional argument'
             1290  POP_TOP          
         1292_1294  JUMP_BACK          1278  'to 1278'
             1296  POP_BLOCK        
           1298_0  COME_FROM_LOOP     1272  '1272'
           1298_1  COME_FROM          1268  '1268'

 L. 540      1298  LOAD_FAST                'individuals_list'
             1300  LOAD_FAST                'query'
             1302  LOAD_STR                 'individual_id__in'
             1304  STORE_SUBSCR     

 L. 541      1306  LOAD_GLOBAL              Variant
             1308  LOAD_ATTR                objects
             1310  LOAD_ATTR                filter
             1312  LOAD_FAST                'args'
             1314  LOAD_FAST                'query'
             1316  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1318  LOAD_ATTR                exclude
             1320  BUILD_TUPLE_0         0 
             1322  LOAD_FAST                'exclude'
             1324  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1326  LOAD_METHOD              order_by
             1328  LOAD_STR                 'gene_name'
             1330  CALL_METHOD_1         1  '1 positional argument'
             1332  STORE_FAST               'variants'

 L. 542      1334  LOAD_GLOBAL              print
             1336  LOAD_GLOBAL              len
             1338  LOAD_FAST                'variants'
             1340  CALL_FUNCTION_1       1  '1 positional argument'
             1342  CALL_FUNCTION_1       1  '1 positional argument'
             1344  POP_TOP          

 L. 547      1346  LOAD_FAST                'inheritance_option'
             1348  LOAD_STR                 '1'
             1350  COMPARE_OP               ==
         1352_1354  POP_JUMP_IF_FALSE  1972  'to 1972'

 L. 548      1356  LOAD_GLOBAL              print
             1358  LOAD_STR                 'Usando modelo recessivo'
             1360  CALL_FUNCTION_1       1  '1 positional argument'
             1362  POP_TOP          

 L. 549      1364  LOAD_FAST                'remove_not_in_parents'
             1366  LOAD_STR                 'on'
             1368  COMPARE_OP               ==
         1370_1372  POP_JUMP_IF_FALSE  1972  'to 1972'

 L. 550      1374  LOAD_GLOBAL              print
             1376  LOAD_STR                 'remove not seing in parents'
             1378  CALL_FUNCTION_1       1  '1 positional argument'
             1380  POP_TOP          

 L. 551      1382  BUILD_MAP_0           0 
             1384  STORE_FAST               'children_dict'

 L. 552      1386  SETUP_LOOP         1608  'to 1608'
             1388  LOAD_FAST                'children'
             1390  GET_ITER         
             1392  FOR_ITER           1606  'to 1606'
             1394  STORE_FAST               'child'

 L. 553      1396  LOAD_GLOBAL              print
             1398  LOAD_STR                 'child %s'
             1400  LOAD_FAST                'child'
             1402  BINARY_MODULO    
             1404  CALL_FUNCTION_1       1  '1 positional argument'
             1406  POP_TOP          

 L. 554      1408  BUILD_MAP_0           0 
             1410  LOAD_FAST                'children_dict'
             1412  LOAD_FAST                'child'
             1414  STORE_SUBSCR     

 L. 555      1416  LOAD_GLOBAL              print
             1418  LOAD_GLOBAL              len
             1420  LOAD_FAST                'variants'
             1422  CALL_FUNCTION_1       1  '1 positional argument'
             1424  CALL_FUNCTION_1       1  '1 positional argument'
             1426  POP_TOP          

 L. 556      1428  SETUP_LOOP         1602  'to 1602'
             1430  LOAD_FAST                'variants'
             1432  GET_ITER         
           1434_0  COME_FROM          1456  '1456'
             1434  FOR_ITER           1600  'to 1600'
             1436  STORE_FAST               'variant'

 L. 558      1438  LOAD_GLOBAL              str
             1440  LOAD_FAST                'variant'
             1442  LOAD_ATTR                individual
             1444  LOAD_ATTR                id
             1446  CALL_FUNCTION_1       1  '1 positional argument'
             1448  LOAD_GLOBAL              str
             1450  LOAD_FAST                'child'
             1452  CALL_FUNCTION_1       1  '1 positional argument'
             1454  COMPARE_OP               ==
         1456_1458  POP_JUMP_IF_FALSE  1434  'to 1434'

 L. 559      1460  LOAD_GLOBAL              print
             1462  LOAD_STR                 'variant == child'
             1464  CALL_FUNCTION_1       1  '1 positional argument'
             1466  POP_TOP          

 L. 560      1468  LOAD_STR                 '%s-%s'
             1470  LOAD_FAST                'variant'
             1472  LOAD_ATTR                chromossome
             1474  LOAD_FAST                'variant'
             1476  LOAD_ATTR                pos
             1478  BUILD_TUPLE_2         2 
             1480  BINARY_MODULO    
             1482  STORE_FAST               'id'

 L. 561      1484  LOAD_FAST                'variant'
             1486  LOAD_ATTR                gene_name
             1488  STORE_FAST               'gene'

 L. 563      1490  LOAD_FAST                'gene'
             1492  LOAD_FAST                'children_dict'
             1494  LOAD_FAST                'child'
             1496  BINARY_SUBSCR    
             1498  COMPARE_OP               not-in
         1500_1502  POP_JUMP_IF_FALSE  1516  'to 1516'

 L. 564      1504  BUILD_MAP_0           0 
             1506  LOAD_FAST                'children_dict'
             1508  LOAD_FAST                'child'
             1510  BINARY_SUBSCR    
             1512  LOAD_FAST                'gene'
             1514  STORE_SUBSCR     
           1516_0  COME_FROM          1500  '1500'

 L. 565      1516  LOAD_FAST                'id'
             1518  LOAD_FAST                'children_dict'
             1520  LOAD_FAST                'child'
             1522  BINARY_SUBSCR    
             1524  LOAD_FAST                'gene'
             1526  BINARY_SUBSCR    
             1528  COMPARE_OP               not-in
         1530_1532  POP_JUMP_IF_FALSE  1550  'to 1550'

 L. 566      1534  BUILD_MAP_0           0 
             1536  LOAD_FAST                'children_dict'
             1538  LOAD_FAST                'child'
             1540  BINARY_SUBSCR    
             1542  LOAD_FAST                'gene'
             1544  BINARY_SUBSCR    
             1546  LOAD_FAST                'id'
             1548  STORE_SUBSCR     
           1550_0  COME_FROM          1530  '1530'

 L. 567      1550  LOAD_FAST                'variant'
             1552  LOAD_ATTR                id
             1554  LOAD_FAST                'children_dict'
             1556  LOAD_FAST                'child'
             1558  BINARY_SUBSCR    
             1560  LOAD_FAST                'gene'
             1562  BINARY_SUBSCR    
             1564  LOAD_FAST                'id'
             1566  BINARY_SUBSCR    
             1568  LOAD_FAST                'variant'
             1570  LOAD_ATTR                genotype
             1572  STORE_SUBSCR     

 L. 568      1574  LOAD_FAST                'variant'
             1576  LOAD_ATTR                id
             1578  LOAD_FAST                'children_dict'
             1580  LOAD_FAST                'child'
             1582  BINARY_SUBSCR    
             1584  LOAD_FAST                'gene'
             1586  BINARY_SUBSCR    
             1588  LOAD_FAST                'id'
             1590  BINARY_SUBSCR    
             1592  LOAD_STR                 'id'
             1594  STORE_SUBSCR     
         1596_1598  JUMP_BACK          1434  'to 1434'
             1600  POP_BLOCK        
           1602_0  COME_FROM_LOOP     1428  '1428'
         1602_1604  JUMP_BACK          1392  'to 1392'
             1606  POP_BLOCK        
           1608_0  COME_FROM_LOOP     1386  '1386'

 L. 570      1608  BUILD_LIST_0          0 
             1610  STORE_FAST               'exclude_gene_list'

 L. 571      1612  BUILD_LIST_0          0 
             1614  STORE_FAST               'exclude_variant_list'

 L. 573      1616  SETUP_LOOP         1866  'to 1866'
             1618  LOAD_FAST                'children'
             1620  GET_ITER         
             1622  FOR_ITER           1864  'to 1864'
             1624  STORE_FAST               'child'

 L. 575      1626  SETUP_LOOP         1860  'to 1860'
             1628  LOAD_FAST                'children_dict'
             1630  LOAD_FAST                'child'
             1632  BINARY_SUBSCR    
             1634  GET_ITER         
             1636  FOR_ITER           1858  'to 1858'
             1638  STORE_FAST               'gene'

 L. 577      1640  LOAD_FAST                'gene'
             1642  LOAD_FAST                'parents_variants'
             1644  LOAD_STR                 'father'
             1646  BINARY_SUBSCR    
             1648  COMPARE_OP               in
         1650_1652  POP_JUMP_IF_FALSE  1844  'to 1844'
             1654  LOAD_FAST                'gene'
             1656  LOAD_FAST                'parents_variants'
             1658  LOAD_STR                 'mother'
             1660  BINARY_SUBSCR    
             1662  COMPARE_OP               in
         1664_1666  POP_JUMP_IF_FALSE  1844  'to 1844'

 L. 578      1668  SETUP_LOOP         1854  'to 1854'
             1670  LOAD_FAST                'children_dict'
             1672  LOAD_FAST                'child'
             1674  BINARY_SUBSCR    
             1676  LOAD_FAST                'gene'
             1678  BINARY_SUBSCR    
             1680  GET_ITER         
             1682  FOR_ITER           1840  'to 1840'
             1684  STORE_FAST               'id'

 L. 580      1686  LOAD_FAST                'id'
             1688  LOAD_FAST                'parents_variants'
             1690  LOAD_STR                 'father'
             1692  BINARY_SUBSCR    
             1694  LOAD_FAST                'gene'
             1696  BINARY_SUBSCR    
             1698  COMPARE_OP               in
         1700_1702  POP_JUMP_IF_FALSE  1802  'to 1802'
             1704  LOAD_FAST                'id'
             1706  LOAD_FAST                'parents_variants'
             1708  LOAD_STR                 'mother'
             1710  BINARY_SUBSCR    
             1712  LOAD_FAST                'gene'
             1714  BINARY_SUBSCR    
             1716  COMPARE_OP               in
         1718_1720  POP_JUMP_IF_FALSE  1802  'to 1802'

 L. 581      1722  LOAD_STR                 '1/1'
             1724  LOAD_FAST                'parents_variants'
             1726  LOAD_STR                 'mother'
             1728  BINARY_SUBSCR    
             1730  LOAD_FAST                'gene'
             1732  BINARY_SUBSCR    
             1734  LOAD_FAST                'id'
             1736  BINARY_SUBSCR    
             1738  COMPARE_OP               in
         1740_1742  POP_JUMP_IF_TRUE   1766  'to 1766'
             1744  LOAD_STR                 '1/1'
             1746  LOAD_FAST                'parents_variants'
             1748  LOAD_STR                 'mother'
             1750  BINARY_SUBSCR    
             1752  LOAD_FAST                'gene'
             1754  BINARY_SUBSCR    
             1756  LOAD_FAST                'id'
             1758  BINARY_SUBSCR    
             1760  COMPARE_OP               in
         1762_1764  POP_JUMP_IF_FALSE  1836  'to 1836'
           1766_0  COME_FROM          1740  '1740'

 L. 582      1766  LOAD_FAST                'exclude_variant_list'
             1768  LOAD_METHOD              append
             1770  LOAD_GLOBAL              list
             1772  LOAD_FAST                'children_dict'
             1774  LOAD_FAST                'child'
             1776  BINARY_SUBSCR    
             1778  LOAD_FAST                'gene'
             1780  BINARY_SUBSCR    
             1782  LOAD_FAST                'id'
             1784  BINARY_SUBSCR    
             1786  LOAD_METHOD              values
             1788  CALL_METHOD_0         0  '0 positional arguments'
             1790  CALL_FUNCTION_1       1  '1 positional argument'
             1792  LOAD_CONST               0
             1794  BINARY_SUBSCR    
             1796  CALL_METHOD_1         1  '1 positional argument'
             1798  POP_TOP          
             1800  JUMP_BACK          1682  'to 1682'
           1802_0  COME_FROM          1718  '1718'
           1802_1  COME_FROM          1700  '1700'

 L. 584      1802  LOAD_FAST                'exclude_variant_list'
             1804  LOAD_METHOD              append
             1806  LOAD_GLOBAL              list
             1808  LOAD_FAST                'children_dict'
             1810  LOAD_FAST                'child'
             1812  BINARY_SUBSCR    
             1814  LOAD_FAST                'gene'
             1816  BINARY_SUBSCR    
             1818  LOAD_FAST                'id'
             1820  BINARY_SUBSCR    
             1822  LOAD_METHOD              values
             1824  CALL_METHOD_0         0  '0 positional arguments'
             1826  CALL_FUNCTION_1       1  '1 positional argument'
             1828  LOAD_CONST               0
             1830  BINARY_SUBSCR    
             1832  CALL_METHOD_1         1  '1 positional argument'
             1834  POP_TOP          
           1836_0  COME_FROM          1762  '1762'
         1836_1838  JUMP_BACK          1682  'to 1682'
             1840  POP_BLOCK        
             1842  JUMP_BACK          1636  'to 1636'
           1844_0  COME_FROM          1664  '1664'
           1844_1  COME_FROM          1650  '1650'

 L. 587      1844  LOAD_FAST                'exclude_gene_list'
             1846  LOAD_METHOD              append
             1848  LOAD_FAST                'gene'
             1850  CALL_METHOD_1         1  '1 positional argument'
             1852  POP_TOP          
           1854_0  COME_FROM_LOOP     1668  '1668'
         1854_1856  JUMP_BACK          1636  'to 1636'
             1858  POP_BLOCK        
           1860_0  COME_FROM_LOOP     1626  '1626'
         1860_1862  JUMP_BACK          1622  'to 1622'
             1864  POP_BLOCK        
           1866_0  COME_FROM_LOOP     1616  '1616'

 L. 588      1866  LOAD_GLOBAL              print
             1868  LOAD_GLOBAL              len
             1870  LOAD_FAST                'exclude_gene_list'
             1872  CALL_FUNCTION_1       1  '1 positional argument'
             1874  CALL_FUNCTION_1       1  '1 positional argument'
             1876  POP_TOP          

 L. 590      1878  LOAD_STR                 'gene_name__in'
             1880  LOAD_FAST                'exclude'
             1882  COMPARE_OP               in
         1884_1886  POP_JUMP_IF_FALSE  1906  'to 1906'

 L. 591      1888  LOAD_FAST                'exclude'
             1890  LOAD_STR                 'gene_name__in'
             1892  BINARY_SUBSCR    
             1894  LOAD_FAST                'exclude_gene_list'
             1896  BINARY_ADD       
             1898  LOAD_FAST                'exclude'
             1900  LOAD_STR                 'gene_name__in'
             1902  STORE_SUBSCR     
             1904  JUMP_FORWARD       1914  'to 1914'
           1906_0  COME_FROM          1884  '1884'

 L. 593      1906  LOAD_FAST                'exclude_gene_list'
             1908  LOAD_FAST                'exclude'
             1910  LOAD_STR                 'gene_name__in'
             1912  STORE_SUBSCR     
           1914_0  COME_FROM          1904  '1904'

 L. 595      1914  LOAD_FAST                'args'
             1916  LOAD_METHOD              append
             1918  LOAD_GLOBAL              Q
             1920  LOAD_FAST                'exclude_variant_list'
             1922  LOAD_CONST               ('id__in',)
             1924  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1926  UNARY_INVERT     
             1928  CALL_METHOD_1         1  '1 positional argument'
             1930  POP_TOP          

 L. 596      1932  LOAD_GLOBAL              Variant
             1934  LOAD_ATTR                objects
             1936  LOAD_ATTR                filter
             1938  LOAD_FAST                'args'
             1940  LOAD_FAST                'query'
             1942  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1944  LOAD_ATTR                exclude
             1946  BUILD_TUPLE_0         0 
             1948  LOAD_FAST                'exclude'
             1950  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1952  LOAD_METHOD              order_by
             1954  LOAD_STR                 'gene_name'
             1956  CALL_METHOD_1         1  '1 positional argument'
             1958  STORE_FAST               'variants'

 L. 597      1960  LOAD_GLOBAL              print
             1962  LOAD_GLOBAL              len
             1964  LOAD_FAST                'variants'
             1966  CALL_FUNCTION_1       1  '1 positional argument'
             1968  CALL_FUNCTION_1       1  '1 positional argument'
             1970  POP_TOP          
           1972_0  COME_FROM          1370  '1370'
           1972_1  COME_FROM          1352  '1352'

 L. 603      1972  LOAD_FAST                'inheritance_option'
             1974  LOAD_STR                 '3'
             1976  COMPARE_OP               ==
         1978_1980  POP_JUMP_IF_FALSE  2884  'to 2884'

 L. 604      1982  LOAD_GLOBAL              print
             1984  LOAD_STR                 'doing compound heterozygous'
             1986  CALL_FUNCTION_1       1  '1 positional argument'
             1988  POP_TOP          

 L. 606      1990  BUILD_MAP_0           0 
             1992  STORE_FAST               'children_dict'

 L. 607      1994  SETUP_LOOP         2184  'to 2184'
             1996  LOAD_FAST                'children'
             1998  GET_ITER         
             2000  FOR_ITER           2182  'to 2182'
             2002  STORE_FAST               'child'

 L. 608      2004  BUILD_MAP_0           0 
             2006  LOAD_FAST                'children_dict'
             2008  LOAD_FAST                'child'
             2010  STORE_SUBSCR     

 L. 610      2012  SETUP_LOOP         2178  'to 2178'
             2014  LOAD_FAST                'variants'
             2016  GET_ITER         
           2018_0  COME_FROM          2040  '2040'
             2018  FOR_ITER           2176  'to 2176'
             2020  STORE_FAST               'variant'

 L. 611      2022  LOAD_GLOBAL              str
             2024  LOAD_FAST                'variant'
             2026  LOAD_ATTR                individual
             2028  LOAD_ATTR                id
             2030  CALL_FUNCTION_1       1  '1 positional argument'
             2032  LOAD_GLOBAL              str
             2034  LOAD_FAST                'child'
             2036  CALL_FUNCTION_1       1  '1 positional argument'
             2038  COMPARE_OP               ==
         2040_2042  POP_JUMP_IF_FALSE  2018  'to 2018'

 L. 612      2044  LOAD_STR                 '%s-%s'
             2046  LOAD_FAST                'variant'
             2048  LOAD_ATTR                chromossome
             2050  LOAD_FAST                'variant'
             2052  LOAD_ATTR                pos
             2054  BUILD_TUPLE_2         2 
             2056  BINARY_MODULO    
             2058  STORE_FAST               'id'

 L. 613      2060  LOAD_FAST                'variant'
             2062  LOAD_ATTR                gene_name
             2064  STORE_FAST               'gene'

 L. 615      2066  LOAD_FAST                'gene'
             2068  LOAD_FAST                'children_dict'
             2070  LOAD_FAST                'child'
             2072  BINARY_SUBSCR    
             2074  COMPARE_OP               not-in
         2076_2078  POP_JUMP_IF_FALSE  2092  'to 2092'

 L. 616      2080  BUILD_MAP_0           0 
             2082  LOAD_FAST                'children_dict'
             2084  LOAD_FAST                'child'
             2086  BINARY_SUBSCR    
             2088  LOAD_FAST                'gene'
             2090  STORE_SUBSCR     
           2092_0  COME_FROM          2076  '2076'

 L. 617      2092  LOAD_FAST                'id'
             2094  LOAD_FAST                'children_dict'
             2096  LOAD_FAST                'child'
             2098  BINARY_SUBSCR    
             2100  LOAD_FAST                'gene'
             2102  BINARY_SUBSCR    
             2104  COMPARE_OP               not-in
         2106_2108  POP_JUMP_IF_FALSE  2126  'to 2126'

 L. 618      2110  BUILD_MAP_0           0 
             2112  LOAD_FAST                'children_dict'
             2114  LOAD_FAST                'child'
             2116  BINARY_SUBSCR    
             2118  LOAD_FAST                'gene'
             2120  BINARY_SUBSCR    
             2122  LOAD_FAST                'id'
             2124  STORE_SUBSCR     
           2126_0  COME_FROM          2106  '2106'

 L. 619      2126  LOAD_FAST                'variant'
             2128  LOAD_ATTR                id
             2130  LOAD_FAST                'children_dict'
             2132  LOAD_FAST                'child'
             2134  BINARY_SUBSCR    
             2136  LOAD_FAST                'gene'
             2138  BINARY_SUBSCR    
             2140  LOAD_FAST                'id'
             2142  BINARY_SUBSCR    
             2144  LOAD_FAST                'variant'
             2146  LOAD_ATTR                genotype
             2148  STORE_SUBSCR     

 L. 620      2150  LOAD_FAST                'variant'
             2152  LOAD_ATTR                id
             2154  LOAD_FAST                'children_dict'
             2156  LOAD_FAST                'child'
             2158  BINARY_SUBSCR    
             2160  LOAD_FAST                'gene'
             2162  BINARY_SUBSCR    
             2164  LOAD_FAST                'id'
             2166  BINARY_SUBSCR    
             2168  LOAD_STR                 'id'
             2170  STORE_SUBSCR     
         2172_2174  JUMP_BACK          2018  'to 2018'
             2176  POP_BLOCK        
           2178_0  COME_FROM_LOOP     2012  '2012'
         2178_2180  JUMP_BACK          2000  'to 2000'
             2182  POP_BLOCK        
           2184_0  COME_FROM_LOOP     1994  '1994'

 L. 628      2184  BUILD_LIST_0          0 
             2186  STORE_FAST               'exclude_gene_list'

 L. 629      2188  BUILD_LIST_0          0 
             2190  STORE_FAST               'exclude_variant_list'

 L. 632  2192_2194  SETUP_LOOP         2778  'to 2778'
             2196  LOAD_FAST                'children'
             2198  GET_ITER         
         2200_2202  FOR_ITER           2776  'to 2776'
             2204  STORE_FAST               'child'

 L. 634  2206_2208  SETUP_LOOP         2772  'to 2772'
             2210  LOAD_FAST                'children_dict'
             2212  LOAD_FAST                'child'
             2214  BINARY_SUBSCR    
             2216  GET_ITER         
           2218_0  COME_FROM          2752  '2752'
         2218_2220  FOR_ITER           2770  'to 2770'
             2222  STORE_FAST               'gene'

 L. 637      2224  LOAD_CONST               False
             2226  STORE_FAST               'one_comes_only_from_father'

 L. 638      2228  LOAD_CONST               False
             2230  STORE_FAST               'one_comes_only_from_mother'

 L. 644      2232  LOAD_FAST                'gene'
             2234  LOAD_FAST                'parents_variants'
             2236  LOAD_STR                 'father'
             2238  BINARY_SUBSCR    
             2240  COMPARE_OP               in
         2242_2244  POP_JUMP_IF_FALSE  2746  'to 2746'
             2246  LOAD_FAST                'gene'
             2248  LOAD_FAST                'parents_variants'
             2250  LOAD_STR                 'mother'
             2252  BINARY_SUBSCR    
             2254  COMPARE_OP               in
         2256_2258  POP_JUMP_IF_FALSE  2746  'to 2746'

 L. 652  2260_2262  SETUP_LOOP         2720  'to 2720'
             2264  LOAD_FAST                'children_dict'
             2266  LOAD_FAST                'child'
             2268  BINARY_SUBSCR    
             2270  LOAD_FAST                'gene'
             2272  BINARY_SUBSCR    
             2274  GET_ITER         
           2276_0  COME_FROM          2676  '2676'
           2276_1  COME_FROM          2658  '2658'
           2276_2  COME_FROM          2640  '2640'
         2276_2278  FOR_ITER           2718  'to 2718'
             2280  STORE_FAST               'id'

 L. 654      2282  LOAD_FAST                'id'
             2284  LOAD_FAST                'parents_variants'
             2286  LOAD_STR                 'father'
             2288  BINARY_SUBSCR    
             2290  LOAD_FAST                'gene'
             2292  BINARY_SUBSCR    
             2294  COMPARE_OP               in
         2296_2298  POP_JUMP_IF_FALSE  2344  'to 2344'
             2300  LOAD_FAST                'id'
             2302  LOAD_FAST                'parents_variants'
             2304  LOAD_STR                 'mother'
             2306  BINARY_SUBSCR    
             2308  LOAD_FAST                'gene'
             2310  BINARY_SUBSCR    
             2312  COMPARE_OP               not-in
         2314_2316  POP_JUMP_IF_FALSE  2344  'to 2344'

 L. 655      2318  LOAD_STR                 '1/1'
             2320  LOAD_FAST                'parents_variants'
             2322  LOAD_STR                 'father'
             2324  BINARY_SUBSCR    
             2326  LOAD_FAST                'gene'
             2328  BINARY_SUBSCR    
             2330  LOAD_FAST                'id'
             2332  BINARY_SUBSCR    
             2334  COMPARE_OP               not-in
         2336_2338  POP_JUMP_IF_FALSE  2344  'to 2344'

 L. 656      2340  LOAD_CONST               True
             2342  STORE_FAST               'one_comes_only_from_father'
           2344_0  COME_FROM          2336  '2336'
           2344_1  COME_FROM          2314  '2314'
           2344_2  COME_FROM          2296  '2296'

 L. 657      2344  LOAD_FAST                'id'
             2346  LOAD_FAST                'parents_variants'
             2348  LOAD_STR                 'mother'
             2350  BINARY_SUBSCR    
             2352  LOAD_FAST                'gene'
             2354  BINARY_SUBSCR    
             2356  COMPARE_OP               in
         2358_2360  POP_JUMP_IF_FALSE  2406  'to 2406'
             2362  LOAD_FAST                'id'
             2364  LOAD_FAST                'parents_variants'
             2366  LOAD_STR                 'father'
             2368  BINARY_SUBSCR    
             2370  LOAD_FAST                'gene'
             2372  BINARY_SUBSCR    
             2374  COMPARE_OP               not-in
         2376_2378  POP_JUMP_IF_FALSE  2406  'to 2406'

 L. 658      2380  LOAD_STR                 '1/1'
             2382  LOAD_FAST                'parents_variants'
             2384  LOAD_STR                 'mother'
             2386  BINARY_SUBSCR    
             2388  LOAD_FAST                'gene'
             2390  BINARY_SUBSCR    
             2392  LOAD_FAST                'id'
             2394  BINARY_SUBSCR    
             2396  COMPARE_OP               not-in
         2398_2400  POP_JUMP_IF_FALSE  2406  'to 2406'

 L. 659      2402  LOAD_CONST               True
             2404  STORE_FAST               'one_comes_only_from_mother'
           2406_0  COME_FROM          2398  '2398'
           2406_1  COME_FROM          2376  '2376'
           2406_2  COME_FROM          2358  '2358'

 L. 660      2406  LOAD_FAST                'id'
             2408  LOAD_FAST                'parents_variants'
             2410  LOAD_STR                 'mother'
             2412  BINARY_SUBSCR    
             2414  LOAD_FAST                'gene'
             2416  BINARY_SUBSCR    
             2418  COMPARE_OP               in
         2420_2422  POP_JUMP_IF_FALSE  2480  'to 2480'

 L. 661      2424  LOAD_STR                 '1/1'
             2426  LOAD_FAST                'parents_variants'
             2428  LOAD_STR                 'mother'
             2430  BINARY_SUBSCR    
             2432  LOAD_FAST                'gene'
             2434  BINARY_SUBSCR    
             2436  LOAD_FAST                'id'
             2438  BINARY_SUBSCR    
             2440  COMPARE_OP               in
         2442_2444  POP_JUMP_IF_FALSE  2480  'to 2480'

 L. 662      2446  LOAD_FAST                'exclude_variant_list'
             2448  LOAD_METHOD              append
             2450  LOAD_GLOBAL              list
             2452  LOAD_FAST                'children_dict'
             2454  LOAD_FAST                'child'
             2456  BINARY_SUBSCR    
             2458  LOAD_FAST                'gene'
             2460  BINARY_SUBSCR    
             2462  LOAD_FAST                'id'
             2464  BINARY_SUBSCR    
             2466  LOAD_METHOD              values
             2468  CALL_METHOD_0         0  '0 positional arguments'
             2470  CALL_FUNCTION_1       1  '1 positional argument'
             2472  LOAD_CONST               0
             2474  BINARY_SUBSCR    
             2476  CALL_METHOD_1         1  '1 positional argument'
             2478  POP_TOP          
           2480_0  COME_FROM          2442  '2442'
           2480_1  COME_FROM          2420  '2420'

 L. 663      2480  LOAD_FAST                'id'
             2482  LOAD_FAST                'parents_variants'
             2484  LOAD_STR                 'father'
             2486  BINARY_SUBSCR    
             2488  LOAD_FAST                'gene'
             2490  BINARY_SUBSCR    
             2492  COMPARE_OP               in
         2494_2496  POP_JUMP_IF_FALSE  2554  'to 2554'

 L. 664      2498  LOAD_STR                 '1/1'
             2500  LOAD_FAST                'parents_variants'
             2502  LOAD_STR                 'father'
             2504  BINARY_SUBSCR    
             2506  LOAD_FAST                'gene'
             2508  BINARY_SUBSCR    
             2510  LOAD_FAST                'id'
             2512  BINARY_SUBSCR    
             2514  COMPARE_OP               in
         2516_2518  POP_JUMP_IF_FALSE  2554  'to 2554'

 L. 665      2520  LOAD_FAST                'exclude_variant_list'
             2522  LOAD_METHOD              append
             2524  LOAD_GLOBAL              list
             2526  LOAD_FAST                'children_dict'
             2528  LOAD_FAST                'child'
             2530  BINARY_SUBSCR    
             2532  LOAD_FAST                'gene'
             2534  BINARY_SUBSCR    
             2536  LOAD_FAST                'id'
             2538  BINARY_SUBSCR    
             2540  LOAD_METHOD              values
             2542  CALL_METHOD_0         0  '0 positional arguments'
             2544  CALL_FUNCTION_1       1  '1 positional argument'
             2546  LOAD_CONST               0
             2548  BINARY_SUBSCR    
             2550  CALL_METHOD_1         1  '1 positional argument'
             2552  POP_TOP          
           2554_0  COME_FROM          2516  '2516'
           2554_1  COME_FROM          2494  '2494'

 L. 667      2554  LOAD_FAST                'remove_in_both_parents'
             2556  LOAD_STR                 'on'
             2558  COMPARE_OP               ==
         2560_2562  POP_JUMP_IF_FALSE  2634  'to 2634'

 L. 668      2564  LOAD_FAST                'id'
             2566  LOAD_FAST                'parents_variants'
             2568  LOAD_STR                 'father'
             2570  BINARY_SUBSCR    
             2572  LOAD_FAST                'gene'
             2574  BINARY_SUBSCR    
             2576  COMPARE_OP               in
         2578_2580  POP_JUMP_IF_FALSE  2634  'to 2634'
             2582  LOAD_FAST                'id'
             2584  LOAD_FAST                'parents_variants'
             2586  LOAD_STR                 'mother'
             2588  BINARY_SUBSCR    
             2590  LOAD_FAST                'gene'
             2592  BINARY_SUBSCR    
             2594  COMPARE_OP               in
         2596_2598  POP_JUMP_IF_FALSE  2634  'to 2634'

 L. 669      2600  LOAD_FAST                'exclude_variant_list'
             2602  LOAD_METHOD              append
             2604  LOAD_GLOBAL              list
             2606  LOAD_FAST                'children_dict'
             2608  LOAD_FAST                'child'
             2610  BINARY_SUBSCR    
             2612  LOAD_FAST                'gene'
             2614  BINARY_SUBSCR    
             2616  LOAD_FAST                'id'
             2618  BINARY_SUBSCR    
             2620  LOAD_METHOD              values
             2622  CALL_METHOD_0         0  '0 positional arguments'
             2624  CALL_FUNCTION_1       1  '1 positional argument'
             2626  LOAD_CONST               0
             2628  BINARY_SUBSCR    
             2630  CALL_METHOD_1         1  '1 positional argument'
             2632  POP_TOP          
           2634_0  COME_FROM          2596  '2596'
           2634_1  COME_FROM          2578  '2578'
           2634_2  COME_FROM          2560  '2560'

 L. 672      2634  LOAD_FAST                'remove_not_in_parents'
             2636  LOAD_STR                 'on'
             2638  COMPARE_OP               ==
         2640_2642  POP_JUMP_IF_FALSE  2276  'to 2276'

 L. 673      2644  LOAD_FAST                'id'
             2646  LOAD_FAST                'parents_variants'
             2648  LOAD_STR                 'mother'
             2650  BINARY_SUBSCR    
             2652  LOAD_FAST                'gene'
             2654  BINARY_SUBSCR    
             2656  COMPARE_OP               not-in
         2658_2660  POP_JUMP_IF_FALSE  2276  'to 2276'

 L. 674      2662  LOAD_FAST                'id'
             2664  LOAD_FAST                'parents_variants'
             2666  LOAD_STR                 'father'
             2668  BINARY_SUBSCR    
             2670  LOAD_FAST                'gene'
             2672  BINARY_SUBSCR    
             2674  COMPARE_OP               not-in
         2676_2678  POP_JUMP_IF_FALSE  2276  'to 2276'

 L. 676      2680  LOAD_FAST                'exclude_variant_list'
             2682  LOAD_METHOD              append
             2684  LOAD_GLOBAL              list
             2686  LOAD_FAST                'children_dict'
             2688  LOAD_FAST                'child'
             2690  BINARY_SUBSCR    
             2692  LOAD_FAST                'gene'
             2694  BINARY_SUBSCR    
             2696  LOAD_FAST                'id'
             2698  BINARY_SUBSCR    
             2700  LOAD_METHOD              values
             2702  CALL_METHOD_0         0  '0 positional arguments'
             2704  CALL_FUNCTION_1       1  '1 positional argument'
             2706  LOAD_CONST               0
             2708  BINARY_SUBSCR    
             2710  CALL_METHOD_1         1  '1 positional argument'
             2712  POP_TOP          
         2714_2716  JUMP_BACK          2276  'to 2276'
             2718  POP_BLOCK        
           2720_0  COME_FROM_LOOP     2260  '2260'

 L. 677      2720  LOAD_FAST                'one_comes_only_from_father'
         2722_2724  POP_JUMP_IF_FALSE  2734  'to 2734'
             2726  LOAD_FAST                'one_comes_only_from_mother'
         2728_2730  POP_JUMP_IF_FALSE  2734  'to 2734'

 L. 678      2732  JUMP_FORWARD       2744  'to 2744'
           2734_0  COME_FROM          2728  '2728'
           2734_1  COME_FROM          2722  '2722'

 L. 680      2734  LOAD_FAST                'exclude_gene_list'
             2736  LOAD_METHOD              append
             2738  LOAD_FAST                'gene'
             2740  CALL_METHOD_1         1  '1 positional argument'
             2742  POP_TOP          
           2744_0  COME_FROM          2732  '2732'
             2744  JUMP_BACK          2218  'to 2218'
           2746_0  COME_FROM          2256  '2256'
           2746_1  COME_FROM          2242  '2242'

 L. 683      2746  LOAD_FAST                'remove_not_in_parents'
             2748  LOAD_STR                 'on'
             2750  COMPARE_OP               ==
         2752_2754  POP_JUMP_IF_FALSE  2218  'to 2218'

 L. 684      2756  LOAD_FAST                'exclude_gene_list'
             2758  LOAD_METHOD              append
             2760  LOAD_FAST                'gene'
             2762  CALL_METHOD_1         1  '1 positional argument'
             2764  POP_TOP          
         2766_2768  JUMP_BACK          2218  'to 2218'
             2770  POP_BLOCK        
           2772_0  COME_FROM_LOOP     2206  '2206'
         2772_2774  JUMP_BACK          2200  'to 2200'
             2776  POP_BLOCK        
           2778_0  COME_FROM_LOOP     2192  '2192'

 L. 686      2778  LOAD_GLOBAL              print
             2780  LOAD_GLOBAL              len
             2782  LOAD_FAST                'exclude_gene_list'
             2784  CALL_FUNCTION_1       1  '1 positional argument'
             2786  CALL_FUNCTION_1       1  '1 positional argument'
             2788  POP_TOP          

 L. 687      2790  LOAD_STR                 'gene_name__in'
             2792  LOAD_FAST                'exclude'
             2794  COMPARE_OP               in
         2796_2798  POP_JUMP_IF_FALSE  2818  'to 2818'

 L. 688      2800  LOAD_FAST                'exclude'
             2802  LOAD_STR                 'gene_name__in'
             2804  BINARY_SUBSCR    
             2806  LOAD_FAST                'exclude_gene_list'
             2808  BINARY_ADD       
             2810  LOAD_FAST                'exclude'
             2812  LOAD_STR                 'gene_name__in'
             2814  STORE_SUBSCR     
             2816  JUMP_FORWARD       2826  'to 2826'
           2818_0  COME_FROM          2796  '2796'

 L. 690      2818  LOAD_FAST                'exclude_gene_list'
             2820  LOAD_FAST                'exclude'
             2822  LOAD_STR                 'gene_name__in'
             2824  STORE_SUBSCR     
           2826_0  COME_FROM          2816  '2816'

 L. 692      2826  LOAD_FAST                'args'
             2828  LOAD_METHOD              append
             2830  LOAD_GLOBAL              Q
             2832  LOAD_FAST                'exclude_variant_list'
             2834  LOAD_CONST               ('id__in',)
             2836  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2838  UNARY_INVERT     
             2840  CALL_METHOD_1         1  '1 positional argument'
             2842  POP_TOP          

 L. 694      2844  LOAD_GLOBAL              Variant
             2846  LOAD_ATTR                objects
             2848  LOAD_ATTR                filter
             2850  LOAD_FAST                'args'
             2852  LOAD_FAST                'query'
             2854  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             2856  LOAD_ATTR                exclude
             2858  BUILD_TUPLE_0         0 
             2860  LOAD_FAST                'exclude'
             2862  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             2864  LOAD_METHOD              order_by
             2866  LOAD_STR                 'gene_name'
             2868  CALL_METHOD_1         1  '1 positional argument'
             2870  STORE_FAST               'variants'

 L. 695      2872  LOAD_GLOBAL              print
             2874  LOAD_GLOBAL              len
             2876  LOAD_FAST                'variants'
             2878  CALL_FUNCTION_1       1  '1 positional argument'
             2880  CALL_FUNCTION_1       1  '1 positional argument'
             2882  POP_TOP          
           2884_0  COME_FROM          1978  '1978'

 L. 702      2884  LOAD_GLOBAL              len
             2886  LOAD_FAST                'individuals_list'
             2888  CALL_FUNCTION_1       1  '1 positional argument'
             2890  LOAD_CONST               0
             2892  COMPARE_OP               >
         2894_2896  POP_JUMP_IF_FALSE  3672  'to 3672'

 L. 703      2898  LOAD_FAST                'individuals_list'
             2900  LOAD_FAST                'query'
             2902  LOAD_STR                 'individual_id__in'
             2904  STORE_SUBSCR     

 L. 705      2906  LOAD_GLOBAL              len
             2908  LOAD_FAST                'exclude_individuals_list'
             2910  CALL_FUNCTION_1       1  '1 positional argument'
             2912  LOAD_CONST               0
             2914  COMPARE_OP               >
         2916_2918  POP_JUMP_IF_FALSE  3154  'to 3154'

 L. 707      2920  BUILD_LIST_0          0 
             2922  STORE_FAST               'variants_ids'

 L. 709      2924  LOAD_GLOBAL              Variant
             2926  LOAD_ATTR                objects
             2928  LOAD_ATTR                filter
             2930  LOAD_FAST                'args'
             2932  LOAD_FAST                'query'
             2934  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             2936  LOAD_ATTR                exclude
             2938  BUILD_TUPLE_0         0 
             2940  LOAD_FAST                'exclude'
             2942  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             2944  LOAD_METHOD              values
             2946  LOAD_STR                 'id'
             2948  LOAD_STR                 'chromossome'
             2950  LOAD_STR                 'pos'
             2952  LOAD_STR                 'genotype'
             2954  CALL_METHOD_4         4  '4 positional arguments'
             2956  STORE_FAST               'variants'

 L. 713      2958  SETUP_LOOP         3146  'to 3146'
             2960  LOAD_FAST                'variants'
             2962  GET_ITER         
             2964  FOR_ITER           3144  'to 3144'
             2966  STORE_FAST               'variant'

 L. 714      2968  LOAD_STR                 '%s-%s'
             2970  LOAD_FAST                'variant'
             2972  LOAD_STR                 'chromossome'
             2974  BINARY_SUBSCR    
             2976  LOAD_FAST                'variant'
             2978  LOAD_STR                 'pos'
             2980  BINARY_SUBSCR    
             2982  BUILD_TUPLE_2         2 
             2984  BINARY_MODULO    
             2986  STORE_FAST               'id'

 L. 715      2988  LOAD_FAST                'id'
             2990  LOAD_FAST                'exclude_individuals_variants'
             2992  COMPARE_OP               in
         2994_2996  POP_JUMP_IF_FALSE  3126  'to 3126'

 L. 716      2998  LOAD_FAST                'variant'
             3000  LOAD_STR                 'genotype'
             3002  BINARY_SUBSCR    
             3004  LOAD_FAST                'exclude_individuals_variants'
             3006  LOAD_FAST                'id'
             3008  BINARY_SUBSCR    
             3010  COMPARE_OP               not-in
         3012_3014  POP_JUMP_IF_FALSE  3140  'to 3140'

 L. 718      3016  LOAD_FAST                'inheritance_option'
             3018  LOAD_STR                 '2'
             3020  COMPARE_OP               ==
         3022_3024  POP_JUMP_IF_FALSE  3070  'to 3070'

 L. 719      3026  LOAD_STR                 '1/1'
             3028  LOAD_FAST                'exclude_individuals_variants'
             3030  LOAD_FAST                'id'
             3032  BINARY_SUBSCR    
             3034  COMPARE_OP               not-in
         3036_3038  POP_JUMP_IF_FALSE  3124  'to 3124'

 L. 720      3040  LOAD_STR                 '0/1'
             3042  LOAD_FAST                'exclude_individuals_variants'
             3044  LOAD_FAST                'id'
             3046  BINARY_SUBSCR    
             3048  COMPARE_OP               not-in
         3050_3052  POP_JUMP_IF_FALSE  3124  'to 3124'

 L. 721      3054  LOAD_FAST                'variants_ids'
             3056  LOAD_METHOD              append
             3058  LOAD_FAST                'variant'
             3060  LOAD_STR                 'id'
             3062  BINARY_SUBSCR    
             3064  CALL_METHOD_1         1  '1 positional argument'
             3066  POP_TOP          
             3068  JUMP_FORWARD       3124  'to 3124'
           3070_0  COME_FROM          3022  '3022'

 L. 722      3070  LOAD_FAST                'inheritance_option'
             3072  LOAD_STR                 '3'
             3074  COMPARE_OP               ==
         3076_3078  POP_JUMP_IF_FALSE  3110  'to 3110'

 L. 723      3080  LOAD_STR                 '1/1'
             3082  LOAD_FAST                'exclude_individuals_variants'
             3084  LOAD_FAST                'id'
             3086  BINARY_SUBSCR    
             3088  COMPARE_OP               not-in
         3090_3092  POP_JUMP_IF_FALSE  3124  'to 3124'

 L. 724      3094  LOAD_FAST                'variants_ids'
             3096  LOAD_METHOD              append
             3098  LOAD_FAST                'variant'
             3100  LOAD_STR                 'id'
             3102  BINARY_SUBSCR    
             3104  CALL_METHOD_1         1  '1 positional argument'
             3106  POP_TOP          
             3108  JUMP_FORWARD       3124  'to 3124'
           3110_0  COME_FROM          3076  '3076'

 L. 726      3110  LOAD_FAST                'variants_ids'
             3112  LOAD_METHOD              append
             3114  LOAD_FAST                'variant'
             3116  LOAD_STR                 'id'
             3118  BINARY_SUBSCR    
             3120  CALL_METHOD_1         1  '1 positional argument'
             3122  POP_TOP          
           3124_0  COME_FROM          3108  '3108'
           3124_1  COME_FROM          3090  '3090'
           3124_2  COME_FROM          3068  '3068'
           3124_3  COME_FROM          3050  '3050'
           3124_4  COME_FROM          3036  '3036'
             3124  JUMP_BACK          2964  'to 2964'
           3126_0  COME_FROM          2994  '2994'

 L. 728      3126  LOAD_FAST                'variants_ids'
             3128  LOAD_METHOD              append
             3130  LOAD_FAST                'variant'
             3132  LOAD_STR                 'id'
             3134  BINARY_SUBSCR    
             3136  CALL_METHOD_1         1  '1 positional argument'
             3138  POP_TOP          
           3140_0  COME_FROM          3012  '3012'
         3140_3142  JUMP_BACK          2964  'to 2964'
             3144  POP_BLOCK        
           3146_0  COME_FROM_LOOP     2958  '2958'

 L. 730      3146  LOAD_FAST                'variants_ids'
             3148  LOAD_FAST                'query'
             3150  LOAD_STR                 'pk__in'
             3152  STORE_SUBSCR     
           3154_0  COME_FROM          2916  '2916'

 L. 734      3154  LOAD_FAST                'request'
             3156  LOAD_ATTR                GET
             3158  LOAD_METHOD              get
             3160  LOAD_STR                 'variants_per_gene'
             3162  CALL_METHOD_1         1  '1 positional argument'
             3164  STORE_FAST               'variants_per_gene'

 L. 735      3166  LOAD_GLOBAL              print
             3168  LOAD_STR                 'variants per gene'
             3170  CALL_FUNCTION_1       1  '1 positional argument'
             3172  POP_TOP          

 L. 736      3174  LOAD_GLOBAL              print
             3176  LOAD_FAST                'variants_per_gene'
             3178  CALL_FUNCTION_1       1  '1 positional argument'
             3180  POP_TOP          

 L. 737      3182  LOAD_FAST                'variants_per_gene'
             3184  LOAD_STR                 ''
             3186  COMPARE_OP               !=
         3188_3190  POP_JUMP_IF_FALSE  3536  'to 3536'

 L. 739      3192  LOAD_GLOBAL              int
             3194  LOAD_FAST                'variants_per_gene'
             3196  CALL_FUNCTION_1       1  '1 positional argument'
             3198  STORE_FAST               'variants_per_gene'

 L. 740      3200  LOAD_GLOBAL              print
             3202  LOAD_STR                 'Variants per gene'
             3204  CALL_FUNCTION_1       1  '1 positional argument'
             3206  POP_TOP          

 L. 741      3208  LOAD_FAST                'request'
             3210  LOAD_ATTR                GET
             3212  LOAD_METHOD              get
             3214  LOAD_STR                 'variants_per_gene_option'
             3216  LOAD_STR                 ''
             3218  CALL_METHOD_2         2  '2 positional arguments'
             3220  STORE_FAST               'variants_per_gene_option'

 L. 742      3222  BUILD_LIST_0          0 
             3224  STORE_FAST               'genes_exclude_list'

 L. 743  3226_3228  SETUP_LOOP         3490  'to 3490'
             3230  LOAD_FAST                'individuals_list'
             3232  GET_ITER         
           3234_0  COME_FROM          3436  '3436'
             3234  FOR_ITER           3488  'to 3488'
             3236  STORE_FAST               'individual'

 L. 745      3238  LOAD_GLOBAL              Variant
             3240  LOAD_ATTR                objects
             3242  LOAD_ATTR                filter
             3244  LOAD_FAST                'args'
             3246  LOAD_STR                 'individual__id'
             3248  LOAD_FAST                'individual'
             3250  BUILD_MAP_1           1 
             3252  LOAD_FAST                'query'
             3254  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             3256  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             3258  LOAD_ATTR                exclude
             3260  BUILD_TUPLE_0         0 
             3262  LOAD_FAST                'exclude'
             3264  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             3266  LOAD_METHOD              values
             3268  LOAD_STR                 'gene_name'
             3270  CALL_METHOD_1         1  '1 positional argument'
             3272  LOAD_ATTR                exclude
             3274  LOAD_STR                 ''
             3276  LOAD_CONST               ('gene_name',)
             3278  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             3280  LOAD_ATTR                annotate
             3282  LOAD_GLOBAL              Count
             3284  LOAD_STR                 'gene_name'
             3286  CALL_FUNCTION_1       1  '1 positional argument'
             3288  LOAD_CONST               ('count',)
             3290  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             3292  LOAD_METHOD              distinct
             3294  CALL_METHOD_0         0  '0 positional arguments'
             3296  STORE_FAST               'individual_genes'

 L. 746      3298  LOAD_GLOBAL              print
             3300  LOAD_GLOBAL              len
             3302  LOAD_FAST                'individual_genes'
             3304  CALL_FUNCTION_1       1  '1 positional argument'
             3306  CALL_FUNCTION_1       1  '1 positional argument'
             3308  POP_TOP          

 L. 747      3310  LOAD_GLOBAL              print
             3312  LOAD_STR                 'len individual genes'
             3314  CALL_FUNCTION_1       1  '1 positional argument'
             3316  POP_TOP          

 L. 748      3318  LOAD_FAST                'variants_per_gene_option'
             3320  LOAD_STR                 '>'
             3322  COMPARE_OP               ==
         3324_3326  POP_JUMP_IF_FALSE  3374  'to 3374'

 L. 749      3328  SETUP_LOOP         3484  'to 3484'
             3330  LOAD_FAST                'individual_genes'
             3332  GET_ITER         
           3334_0  COME_FROM          3348  '3348'
             3334  FOR_ITER           3370  'to 3370'
             3336  STORE_FAST               'gene'

 L. 750      3338  LOAD_FAST                'gene'
             3340  LOAD_STR                 'count'
             3342  BINARY_SUBSCR    
             3344  LOAD_FAST                'variants_per_gene'
             3346  COMPARE_OP               <
         3348_3350  POP_JUMP_IF_FALSE  3334  'to 3334'

 L. 751      3352  LOAD_FAST                'genes_exclude_list'
             3354  LOAD_METHOD              append
             3356  LOAD_FAST                'gene'
             3358  LOAD_STR                 'gene_name'
             3360  BINARY_SUBSCR    
             3362  CALL_METHOD_1         1  '1 positional argument'
             3364  POP_TOP          
         3366_3368  JUMP_BACK          3334  'to 3334'
             3370  POP_BLOCK        
             3372  JUMP_BACK          3234  'to 3234'
           3374_0  COME_FROM          3324  '3324'

 L. 752      3374  LOAD_FAST                'variants_per_gene_option'
             3376  LOAD_STR                 '<'
             3378  COMPARE_OP               ==
         3380_3382  POP_JUMP_IF_FALSE  3430  'to 3430'

 L. 753      3384  SETUP_LOOP         3484  'to 3484'
             3386  LOAD_FAST                'individual_genes'
             3388  GET_ITER         
           3390_0  COME_FROM          3404  '3404'
             3390  FOR_ITER           3426  'to 3426'
             3392  STORE_FAST               'gene'

 L. 754      3394  LOAD_FAST                'gene'
             3396  LOAD_STR                 'count'
             3398  BINARY_SUBSCR    
             3400  LOAD_FAST                'variants_per_gene'
             3402  COMPARE_OP               >
         3404_3406  POP_JUMP_IF_FALSE  3390  'to 3390'

 L. 755      3408  LOAD_FAST                'genes_exclude_list'
             3410  LOAD_METHOD              append
             3412  LOAD_FAST                'gene'
             3414  LOAD_STR                 'gene_name'
             3416  BINARY_SUBSCR    
             3418  CALL_METHOD_1         1  '1 positional argument'
             3420  POP_TOP          
         3422_3424  JUMP_BACK          3390  'to 3390'
             3426  POP_BLOCK        
             3428  JUMP_BACK          3234  'to 3234'
           3430_0  COME_FROM          3380  '3380'

 L. 756      3430  LOAD_FAST                'variants_per_gene_option'
             3432  LOAD_STR                 '='
             3434  COMPARE_OP               ==
         3436_3438  POP_JUMP_IF_FALSE  3234  'to 3234'

 L. 757      3440  SETUP_LOOP         3484  'to 3484'
             3442  LOAD_FAST                'individual_genes'
             3444  GET_ITER         
           3446_0  COME_FROM          3460  '3460'
             3446  FOR_ITER           3482  'to 3482'
             3448  STORE_FAST               'gene'

 L. 758      3450  LOAD_FAST                'gene'
             3452  LOAD_STR                 'count'
             3454  BINARY_SUBSCR    
             3456  LOAD_FAST                'variants_per_gene'
             3458  COMPARE_OP               !=
         3460_3462  POP_JUMP_IF_FALSE  3446  'to 3446'

 L. 759      3464  LOAD_FAST                'genes_exclude_list'
             3466  LOAD_METHOD              append
             3468  LOAD_FAST                'gene'
             3470  LOAD_STR                 'gene_name'
             3472  BINARY_SUBSCR    
             3474  CALL_METHOD_1         1  '1 positional argument'
             3476  POP_TOP          
         3478_3480  JUMP_BACK          3446  'to 3446'
             3482  POP_BLOCK        
           3484_0  COME_FROM_LOOP     3440  '3440'
           3484_1  COME_FROM_LOOP     3384  '3384'
           3484_2  COME_FROM_LOOP     3328  '3328'
         3484_3486  JUMP_BACK          3234  'to 3234'
             3488  POP_BLOCK        
           3490_0  COME_FROM_LOOP     3226  '3226'

 L. 761      3490  LOAD_FAST                'genes_exclude_list'
             3492  LOAD_METHOD              append
             3494  LOAD_STR                 ''
             3496  CALL_METHOD_1         1  '1 positional argument'
             3498  POP_TOP          

 L. 763      3500  LOAD_STR                 'gene_name__in'
             3502  LOAD_FAST                'exclude'
             3504  COMPARE_OP               in
         3506_3508  POP_JUMP_IF_FALSE  3528  'to 3528'

 L. 764      3510  LOAD_FAST                'exclude'
             3512  LOAD_STR                 'gene_name__in'
             3514  BINARY_SUBSCR    
             3516  LOAD_FAST                'genes_exclude_list'
             3518  BINARY_ADD       
             3520  LOAD_FAST                'exclude'
             3522  LOAD_STR                 'gene_name__in'
             3524  STORE_SUBSCR     
             3526  JUMP_FORWARD       3536  'to 3536'
           3528_0  COME_FROM          3506  '3506'

 L. 766      3528  LOAD_FAST                'genes_exclude_list'
             3530  LOAD_FAST                'exclude'
             3532  LOAD_STR                 'gene_name__in'
             3534  STORE_SUBSCR     
           3536_0  COME_FROM          3526  '3526'
           3536_1  COME_FROM          3188  '3188'

 L. 769      3536  LOAD_FAST                'request'
             3538  LOAD_ATTR                GET
             3540  LOAD_METHOD              get
             3542  LOAD_STR                 'genes_in_common'
             3544  LOAD_STR                 ''
             3546  CALL_METHOD_2         2  '2 positional arguments'
             3548  STORE_FAST               'genes_in_common'

 L. 770      3550  LOAD_FAST                'genes_in_common'
             3552  LOAD_STR                 'on'
             3554  COMPARE_OP               ==
         3556_3558  POP_JUMP_IF_FALSE  3672  'to 3672'

 L. 773      3560  BUILD_LIST_0          0 
             3562  STORE_FAST               'individual_gene_list'

 L. 774      3564  SETUP_LOOP         3654  'to 3654'
             3566  LOAD_FAST                'individuals_list'
             3568  GET_ITER         
             3570  FOR_ITER           3652  'to 3652'
             3572  STORE_FAST               'individual'

 L. 776      3574  LOAD_GLOBAL              Variant
             3576  LOAD_ATTR                objects
             3578  LOAD_ATTR                filter
             3580  LOAD_FAST                'args'
             3582  LOAD_STR                 'individual__id'
             3584  LOAD_FAST                'individual'
             3586  BUILD_MAP_1           1 
             3588  LOAD_FAST                'query'
             3590  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             3592  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             3594  LOAD_ATTR                exclude
             3596  BUILD_TUPLE_0         0 
             3598  LOAD_FAST                'exclude'
             3600  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             3602  LOAD_ATTR                values_list
             3604  LOAD_STR                 'gene_name'
             3606  LOAD_CONST               True
             3608  LOAD_CONST               ('flat',)
             3610  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3612  LOAD_ATTR                exclude
             3614  LOAD_STR                 ''
             3616  LOAD_CONST               ('gene_name',)
             3618  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             3620  LOAD_METHOD              distinct
             3622  CALL_METHOD_0         0  '0 positional arguments'
             3624  STORE_FAST               'individual_genes'

 L. 777      3626  LOAD_GLOBAL              set
             3628  LOAD_GLOBAL              list
             3630  LOAD_FAST                'individual_genes'
             3632  CALL_FUNCTION_1       1  '1 positional argument'
             3634  CALL_FUNCTION_1       1  '1 positional argument'
             3636  STORE_FAST               'individual_genes'

 L. 778      3638  LOAD_FAST                'individual_gene_list'
             3640  LOAD_METHOD              append
             3642  LOAD_FAST                'individual_genes'
             3644  CALL_METHOD_1         1  '1 positional argument'
             3646  POP_TOP          
         3648_3650  JUMP_BACK          3570  'to 3570'
             3652  POP_BLOCK        
           3654_0  COME_FROM_LOOP     3564  '3564'

 L. 780      3654  LOAD_GLOBAL              set
             3656  LOAD_ATTR                intersection
             3658  LOAD_FAST                'individual_gene_list'
             3660  CALL_FUNCTION_EX      0  'positional arguments only'
             3662  STORE_FAST               'genes_in_common_list'

 L. 781      3664  LOAD_FAST                'genes_in_common_list'
             3666  LOAD_FAST                'query'
             3668  LOAD_STR                 'gene_name__in'
             3670  STORE_SUBSCR     
           3672_0  COME_FROM          3556  '3556'
           3672_1  COME_FROM          2894  '2894'

 L. 790      3672  LOAD_GLOBAL              Variant
             3674  LOAD_ATTR                objects
             3676  LOAD_ATTR                filter
             3678  LOAD_FAST                'args'
             3680  LOAD_FAST                'query'
             3682  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             3684  LOAD_ATTR                exclude
             3686  BUILD_TUPLE_0         0 
             3688  LOAD_FAST                'exclude'
             3690  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             3692  LOAD_METHOD              order_by
             3694  LOAD_STR                 'gene_name'
             3696  LOAD_STR                 'individual'
             3698  CALL_METHOD_2         2  '2 positional arguments'
             3700  STORE_FAST               'variants'

 L. 791      3702  LOAD_GLOBAL              print
             3704  LOAD_GLOBAL              len
             3706  LOAD_FAST                'variants'
             3708  CALL_FUNCTION_1       1  '1 positional argument'
             3710  CALL_FUNCTION_1       1  '1 positional argument'
             3712  POP_TOP          

 L. 794      3714  SETUP_LOOP         3876  'to 3876'
             3716  LOAD_FAST                'variants'
             3718  GET_ITER         
           3720_0  COME_FROM          3836  '3836'
           3720_1  COME_FROM          3818  '3818'
             3720  FOR_ITER           3874  'to 3874'
             3722  STORE_FAST               'variant'

 L. 795      3724  LOAD_STR                 '%s-%s'
             3726  LOAD_FAST                'variant'
             3728  LOAD_ATTR                chromossome
             3730  LOAD_FAST                'variant'
             3732  LOAD_ATTR                pos
             3734  BUILD_TUPLE_2         2 
             3736  BINARY_MODULO    
             3738  STORE_FAST               'id'

 L. 796      3740  LOAD_FAST                'variant'
             3742  LOAD_ATTR                gene_name
             3744  STORE_FAST               'gene'

 L. 797      3746  LOAD_FAST                'gene'
             3748  LOAD_FAST                'parents_variants'
             3750  LOAD_STR                 'father'
             3752  BINARY_SUBSCR    
             3754  COMPARE_OP               in
         3756_3758  POP_JUMP_IF_FALSE  3808  'to 3808'

 L. 798      3760  LOAD_FAST                'id'
             3762  LOAD_FAST                'parents_variants'
             3764  LOAD_STR                 'father'
             3766  BINARY_SUBSCR    
             3768  LOAD_FAST                'gene'
             3770  BINARY_SUBSCR    
             3772  COMPARE_OP               in
         3774_3776  POP_JUMP_IF_FALSE  3808  'to 3808'

 L. 799      3778  LOAD_GLOBAL              list
             3780  LOAD_FAST                'parents_variants'
             3782  LOAD_STR                 'father'
             3784  BINARY_SUBSCR    
             3786  LOAD_FAST                'gene'
             3788  BINARY_SUBSCR    
             3790  LOAD_FAST                'id'
             3792  BINARY_SUBSCR    
             3794  LOAD_METHOD              keys
             3796  CALL_METHOD_0         0  '0 positional arguments'
             3798  CALL_FUNCTION_1       1  '1 positional argument'
             3800  LOAD_CONST               0
             3802  BINARY_SUBSCR    
             3804  LOAD_FAST                'variant'
             3806  STORE_ATTR               father
           3808_0  COME_FROM          3774  '3774'
           3808_1  COME_FROM          3756  '3756'

 L. 800      3808  LOAD_FAST                'gene'
             3810  LOAD_FAST                'parents_variants'
             3812  LOAD_STR                 'mother'
             3814  BINARY_SUBSCR    
             3816  COMPARE_OP               in
         3818_3820  POP_JUMP_IF_FALSE  3720  'to 3720'

 L. 801      3822  LOAD_FAST                'id'
             3824  LOAD_FAST                'parents_variants'
             3826  LOAD_STR                 'mother'
             3828  BINARY_SUBSCR    
             3830  LOAD_FAST                'gene'
             3832  BINARY_SUBSCR    
             3834  COMPARE_OP               in
         3836_3838  POP_JUMP_IF_FALSE  3720  'to 3720'

 L. 802      3840  LOAD_GLOBAL              list
             3842  LOAD_FAST                'parents_variants'
             3844  LOAD_STR                 'mother'
             3846  BINARY_SUBSCR    
             3848  LOAD_FAST                'gene'
             3850  BINARY_SUBSCR    
             3852  LOAD_FAST                'id'
             3854  BINARY_SUBSCR    
             3856  LOAD_METHOD              keys
             3858  CALL_METHOD_0         0  '0 positional arguments'
             3860  CALL_FUNCTION_1       1  '1 positional argument'
             3862  LOAD_CONST               0
             3864  BINARY_SUBSCR    
             3866  LOAD_FAST                'variant'
             3868  STORE_ATTR               mother
         3870_3872  JUMP_BACK          3720  'to 3720'
             3874  POP_BLOCK        
           3876_0  COME_FROM_LOOP     3714  '3714'

 L. 805      3876  LOAD_FAST                'variants'
             3878  LOAD_METHOD              count
             3880  CALL_METHOD_0         0  '0 positional arguments'
             3882  LOAD_FAST                'summary'
             3884  LOAD_STR                 'n_variants'
             3886  STORE_SUBSCR     

 L. 806      3888  LOAD_FAST                'variants'
             3890  LOAD_METHOD              values
             3892  LOAD_STR                 'gene_name'
             3894  CALL_METHOD_1         1  '1 positional argument'
             3896  LOAD_ATTR                exclude
             3898  LOAD_STR                 ''
             3900  LOAD_CONST               ('gene_name',)
             3902  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             3904  LOAD_METHOD              distinct
             3906  CALL_METHOD_0         0  '0 positional arguments'
             3908  LOAD_METHOD              count
             3910  CALL_METHOD_0         0  '0 positional arguments'
             3912  LOAD_FAST                'summary'
             3914  LOAD_STR                 'n_genes'
             3916  STORE_SUBSCR     

 L. 807      3918  LOAD_FAST                'variants'
             3920  LOAD_ATTR                values_list
             3922  LOAD_STR                 'gene_name'
             3924  LOAD_CONST               True
             3926  LOAD_CONST               ('flat',)
             3928  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3930  LOAD_ATTR                exclude
             3932  LOAD_STR                 ''
             3934  LOAD_CONST               ('gene_name',)
             3936  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             3938  LOAD_METHOD              distinct
             3940  CALL_METHOD_0         0  '0 positional arguments'
             3942  LOAD_FAST                'summary'
             3944  LOAD_STR                 'genes'
             3946  STORE_SUBSCR     

 L. 808      3948  LOAD_GLOBAL              sorted
             3950  LOAD_GLOBAL              list
             3952  LOAD_GLOBAL              set
             3954  LOAD_FAST                'summary'
             3956  LOAD_STR                 'genes'
             3958  BINARY_SUBSCR    
             3960  CALL_FUNCTION_1       1  '1 positional argument'
             3962  CALL_FUNCTION_1       1  '1 positional argument'
             3964  CALL_FUNCTION_1       1  '1 positional argument'
             3966  LOAD_FAST                'summary'
             3968  LOAD_STR                 'genes'
             3970  STORE_SUBSCR     

 L. 811      3972  LOAD_GLOBAL              print
             3974  LOAD_STR                 'summary genes'
             3976  CALL_FUNCTION_1       1  '1 positional argument'
             3978  POP_TOP          

 L. 812      3980  LOAD_GLOBAL              print
             3982  LOAD_FAST                'summary'
             3984  LOAD_STR                 'genes'
             3986  BINARY_SUBSCR    
             3988  CALL_FUNCTION_1       1  '1 positional argument'
             3990  POP_TOP          

 L. 819      3992  LOAD_GLOBAL              Paginator
             3994  LOAD_FAST                'variants'
             3996  LOAD_CONST               100
             3998  CALL_FUNCTION_2       2  '2 positional arguments'
             4000  STORE_FAST               'paginator'

 L. 821      4002  SETUP_EXCEPT       4026  'to 4026'

 L. 822      4004  LOAD_GLOBAL              int
             4006  LOAD_FAST                'request'
             4008  LOAD_ATTR                GET
             4010  LOAD_METHOD              get
             4012  LOAD_STR                 'page'
             4014  LOAD_STR                 '1'
             4016  CALL_METHOD_2         2  '2 positional arguments'
             4018  CALL_FUNCTION_1       1  '1 positional argument'
             4020  STORE_FAST               'page'
             4022  POP_BLOCK        
             4024  JUMP_FORWARD       4052  'to 4052'
           4026_0  COME_FROM_EXCEPT   4002  '4002'

 L. 823      4026  DUP_TOP          
             4028  LOAD_GLOBAL              ValueError
             4030  COMPARE_OP               exception-match
         4032_4034  POP_JUMP_IF_FALSE  4050  'to 4050'
             4036  POP_TOP          
             4038  POP_TOP          
             4040  POP_TOP          

 L. 824      4042  LOAD_CONST               1
             4044  STORE_FAST               'page'
             4046  POP_EXCEPT       
             4048  JUMP_FORWARD       4052  'to 4052'
           4050_0  COME_FROM          4032  '4032'
             4050  END_FINALLY      
           4052_0  COME_FROM          4048  '4048'
           4052_1  COME_FROM          4024  '4024'

 L. 825      4052  SETUP_EXCEPT       4068  'to 4068'

 L. 826      4054  LOAD_FAST                'paginator'
             4056  LOAD_METHOD              page
             4058  LOAD_FAST                'page'
             4060  CALL_METHOD_1         1  '1 positional argument'
             4062  STORE_FAST               'variants'
             4064  POP_BLOCK        
             4066  JUMP_FORWARD       4132  'to 4132'
           4068_0  COME_FROM_EXCEPT   4052  '4052'

 L. 827      4068  DUP_TOP          
             4070  LOAD_GLOBAL              PageNotAnInteger
             4072  COMPARE_OP               exception-match
         4074_4076  POP_JUMP_IF_FALSE  4098  'to 4098'
             4078  POP_TOP          
             4080  POP_TOP          
             4082  POP_TOP          

 L. 829      4084  LOAD_FAST                'paginator'
             4086  LOAD_METHOD              page
             4088  LOAD_CONST               1
             4090  CALL_METHOD_1         1  '1 positional argument'
             4092  STORE_FAST               'variants'
             4094  POP_EXCEPT       
             4096  JUMP_FORWARD       4132  'to 4132'
           4098_0  COME_FROM          4074  '4074'

 L. 830      4098  DUP_TOP          
             4100  LOAD_GLOBAL              EmptyPage
             4102  COMPARE_OP               exception-match
         4104_4106  POP_JUMP_IF_FALSE  4130  'to 4130'
             4108  POP_TOP          
             4110  POP_TOP          
             4112  POP_TOP          

 L. 832      4114  LOAD_FAST                'paginator'
             4116  LOAD_METHOD              page
             4118  LOAD_FAST                'paginator'
             4120  LOAD_ATTR                num_pages
             4122  CALL_METHOD_1         1  '1 positional argument'
             4124  STORE_FAST               'variants'
             4126  POP_EXCEPT       
             4128  JUMP_FORWARD       4132  'to 4132'
           4130_0  COME_FROM          4104  '4104'
             4130  END_FINALLY      
           4132_0  COME_FROM          4128  '4128'
           4132_1  COME_FROM          4096  '4096'
           4132_2  COME_FROM          4066  '4066'

 L. 835      4132  LOAD_GLOBAL              FamilyAnalysisForm
             4134  LOAD_FAST                'request'
             4136  LOAD_ATTR                GET
             4138  CALL_FUNCTION_1       1  '1 positional argument'
             4140  STORE_FAST               'form'
             4142  JUMP_FORWARD       4158  'to 4158'
           4144_0  COME_FROM           134  '134'
           4144_1  COME_FROM           124  '124'

 L. 839      4144  BUILD_LIST_0          0 
             4146  STORE_FAST               'variants'

 L. 840      4148  BUILD_LIST_0          0 
             4150  STORE_FAST               'summary'

 L. 841      4152  LOAD_GLOBAL              FamilyAnalysisForm
             4154  CALL_FUNCTION_0       0  '0 positional arguments'
             4156  STORE_FAST               'form'
           4158_0  COME_FROM          4142  '4142'
           4158_1  COME_FROM           146  '146'

 L. 843      4158  LOAD_FAST                'request'
             4160  LOAD_ATTR                GET
             4162  LOAD_METHOD              get
             4164  LOAD_STR                 'export'
             4166  LOAD_STR                 ''
             4168  CALL_METHOD_2         2  '2 positional arguments'
             4170  STORE_FAST               'export'

 L. 844      4172  LOAD_FAST                'export'
             4174  LOAD_STR                 ''
             4176  COMPARE_OP               !=
         4178_4180  POP_JUMP_IF_FALSE  4498  'to 4498'

 L. 845      4182  LOAD_GLOBAL              Variant
             4184  LOAD_ATTR                objects
             4186  LOAD_ATTR                filter
             4188  LOAD_FAST                'args'
             4190  LOAD_FAST                'query'
             4192  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             4194  LOAD_ATTR                exclude
             4196  BUILD_TUPLE_0         0 
             4198  LOAD_FAST                'exclude'
             4200  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             4202  LOAD_METHOD              order_by
             4204  LOAD_STR                 'gene_name'
             4206  CALL_METHOD_1         1  '1 positional argument'
             4208  STORE_FAST               'variants'

 L. 848      4210  LOAD_FAST                'export'
             4212  LOAD_STR                 'csv'
             4214  COMPARE_OP               ==
         4216_4218  POP_JUMP_IF_FALSE  4250  'to 4250'

 L. 849      4220  LOAD_GLOBAL              HttpResponse
             4222  LOAD_STR                 'text/csv'
             4224  LOAD_CONST               ('mimetype',)
             4226  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4228  STORE_FAST               'response'

 L. 850      4230  LOAD_STR                 'attachment; filename=Variants_from_Mendel_MD.csv'
             4232  LOAD_FAST                'response'
             4234  LOAD_STR                 'Content-Disposition'
             4236  STORE_SUBSCR     

 L. 851      4238  LOAD_GLOBAL              csv
             4240  LOAD_METHOD              writer
             4242  LOAD_FAST                'response'
             4244  CALL_METHOD_1         1  '1 positional argument'
             4246  STORE_FAST               'writer'
             4248  JUMP_FORWARD       4296  'to 4296'
           4250_0  COME_FROM          4216  '4216'

 L. 853      4250  LOAD_FAST                'export'
             4252  LOAD_STR                 'txt'
             4254  COMPARE_OP               ==
         4256_4258  POP_JUMP_IF_FALSE  4296  'to 4296'

 L. 854      4260  LOAD_GLOBAL              HttpResponse
             4262  LOAD_STR                 'text/plain'
             4264  LOAD_CONST               ('mimetype',)
             4266  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4268  STORE_FAST               'response'

 L. 855      4270  LOAD_STR                 'attachment; filename=Variants_from_Mendel_MD.txt'
             4272  LOAD_FAST                'response'
             4274  LOAD_STR                 'Content-Disposition'
             4276  STORE_SUBSCR     

 L. 856      4278  LOAD_GLOBAL              csv
             4280  LOAD_ATTR                writer
             4282  LOAD_FAST                'response'
             4284  LOAD_STR                 '\t'
             4286  LOAD_GLOBAL              csv
             4288  LOAD_ATTR                QUOTE_NONE
             4290  LOAD_CONST               ('delimiter', 'quoting')
             4292  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4294  STORE_FAST               'writer'
           4296_0  COME_FROM          4256  '4256'
           4296_1  COME_FROM          4248  '4248'

 L. 858      4296  LOAD_FAST                'writer'
             4298  LOAD_METHOD              writerow
             4300  LOAD_STR                 'Individual'

 L. 859      4302  LOAD_STR                 'Chromossome'
             4304  LOAD_STR                 'Variant Id'
             4306  LOAD_STR                 'Pos'
             4308  LOAD_STR                 'Qual'
             4310  LOAD_STR                 'Ref'
             4312  LOAD_STR                 'Alt'
             4314  LOAD_STR                 'Genotype'

 L. 860      4316  LOAD_STR                 'Genotype Info'
             4318  LOAD_STR                 'Read Depth'
             4320  LOAD_STR                 'Snpe Eff'
             4322  LOAD_STR                 'Functional Class'
             4324  LOAD_STR                 'Gene'

 L. 861      4326  LOAD_STR                 'Impact'
             4328  LOAD_STR                 'Variant is Clinical'
             4330  LOAD_STR                 '100Genomes Frequency'
             4332  LOAD_STR                 'dbSNP135 Frequency'

 L. 862      4334  LOAD_STR                 'ESP5400 Frequency'
             4336  LOAD_STR                 'ESP5400 EA/AA/ALL'
             4338  LOAD_STR                 'ESP5400 Total Allele Count'

 L. 863      4340  LOAD_STR                 'SIFT'
             4342  LOAD_STR                 'Polyphen2'
             4344  LOAD_STR                 'dbSNP Build'
             4346  LOAD_STR                 'Amino Acid Change'

 L. 864      4348  LOAD_STR                 'Cdna Position'
             4350  LOAD_STR                 'Granthamscore'
             4352  LOAD_STR                 'Protein Position'
             4354  BUILD_LIST_27        27 
             4356  CALL_METHOD_1         1  '1 positional argument'
             4358  POP_TOP          

 L. 865      4360  SETUP_LOOP         4494  'to 4494'
             4362  LOAD_FAST                'variants'
             4364  GET_ITER         
             4366  FOR_ITER           4492  'to 4492'
             4368  STORE_FAST               'variant'

 L. 866      4370  LOAD_FAST                'writer'
             4372  LOAD_METHOD              writerow
             4374  LOAD_FAST                'variant'
             4376  LOAD_ATTR                individual
             4378  LOAD_FAST                'variant'
             4380  LOAD_ATTR                chromossome

 L. 867      4382  LOAD_FAST                'variant'
             4384  LOAD_ATTR                variant_id
             4386  LOAD_FAST                'variant'
             4388  LOAD_ATTR                pos
             4390  LOAD_FAST                'variant'
             4392  LOAD_ATTR                qual
             4394  LOAD_FAST                'variant'
             4396  LOAD_ATTR                ref

 L. 868      4398  LOAD_FAST                'variant'
             4400  LOAD_ATTR                alt
             4402  LOAD_FAST                'variant'
             4404  LOAD_ATTR                genotype
             4406  LOAD_FAST                'variant'
             4408  LOAD_ATTR                genotype_info

 L. 869      4410  LOAD_FAST                'variant'
             4412  LOAD_ATTR                read_depth
             4414  LOAD_FAST                'variant'
             4416  LOAD_ATTR                snp_eff

 L. 870      4418  LOAD_FAST                'variant'
             4420  LOAD_ATTR                snp_eff_functional_class
             4422  LOAD_FAST                'variant'
             4424  LOAD_ATTR                gene_name
             4426  LOAD_FAST                'variant'
             4428  LOAD_ATTR                impact

 L. 871      4430  LOAD_FAST                'variant'
             4432  LOAD_ATTR                dbsnp_pm
             4434  LOAD_FAST                'variant'
             4436  LOAD_ATTR                genomes1k_maf
             4438  LOAD_FAST                'variant'
             4440  LOAD_ATTR                dbsnp_gmaf

 L. 872      4442  LOAD_FAST                'variant'
             4444  LOAD_ATTR                esp_maf_total
             4446  LOAD_FAST                'variant'
             4448  LOAD_ATTR                ann_esp_maf
             4450  LOAD_FAST                'variant'
             4452  LOAD_ATTR                tac

 L. 873      4454  LOAD_FAST                'variant'
             4456  LOAD_ATTR                sift
             4458  LOAD_FAST                'variant'
             4460  LOAD_ATTR                polyphen
             4462  LOAD_FAST                'variant'
             4464  LOAD_ATTR                dbsnp_build

 L. 874      4466  LOAD_FAST                'variant'
             4468  LOAD_ATTR                amino_acid_change
             4470  LOAD_FAST                'variant'
             4472  LOAD_ATTR                cdna_position

 L. 875      4474  LOAD_FAST                'variant'
             4476  LOAD_ATTR                granthamscore
             4478  LOAD_FAST                'variant'
             4480  LOAD_ATTR                protein_position
             4482  BUILD_LIST_27        27 
             4484  CALL_METHOD_1         1  '1 positional argument'
             4486  POP_TOP          
         4488_4490  JUMP_BACK          4366  'to 4366'
             4492  POP_BLOCK        
           4494_0  COME_FROM_LOOP     4360  '4360'

 L. 877      4494  LOAD_FAST                'response'
             4496  RETURN_VALUE     
           4498_0  COME_FROM          4178  '4178'

 L. 881      4498  LOAD_GLOBAL              Disease
             4500  LOAD_ATTR                objects
             4502  LOAD_METHOD              distinct
             4504  CALL_METHOD_0         0  '0 positional arguments'
             4506  LOAD_METHOD              order_by
             4508  LOAD_STR                 'name'
             4510  CALL_METHOD_1         1  '1 positional argument'
             4512  LOAD_CONST               None
             4514  LOAD_CONST               5
             4516  BUILD_SLICE_2         2 
             4518  BINARY_SUBSCR    
             4520  STORE_FAST               'diseases'

 L. 883      4522  LOAD_GLOBAL              serializers
             4524  LOAD_METHOD              serialize
             4526  LOAD_STR                 'json'
             4528  LOAD_FAST                'diseases'
             4530  CALL_METHOD_2         2  '2 positional arguments'
             4532  STORE_FAST               'diseases'

 L. 886      4534  LOAD_GLOBAL              render
             4536  LOAD_FAST                'request'
             4538  LOAD_STR                 'filter_analysis/family_analysis.html'
             4540  LOAD_FAST                'variants'
             4542  LOAD_FAST                'form'
             4544  LOAD_FAST                'summary'
             4546  LOAD_FAST                'query_string'
             4548  LOAD_FAST                'diseases'
             4550  LOAD_FAST                'filteranalysis'
             4552  LOAD_FAST                'filterconfigs'
             4554  LOAD_CONST               ('variants', 'form', 'summary', 'query_string', 'diseases', 'filteranalysis', 'filterconfigs')
             4556  BUILD_CONST_KEY_MAP_7     7 
             4558  CALL_FUNCTION_3       3  '3 positional arguments'
             4560  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 3484_1


class FilterWizard(SessionWizardView):

    def get_template(self, step):
        if step == 0:
            return 'forms/step0.html'
        if step == 1:
            return 'forms/step1.html'
        if step == 2:
            return 'forms/step2.html'


@login_required
def oneclick(request):
    form = FilterAnalysisForm
    if request.method == 'GET':
        print('Entrando no GET')
        query_string = request.META['QUERY_STRING']
        print(query_string)
        if query_string != '':
            print('LIMPANDO')
            new_query_string = []
            query_string = query_string.split'&'
            for item in query_string:
                if not item.startswith'csrfmiddlewaretoken':
                    item.startswith'hash' or item.startswith'wizard' or new_query_string.appenditem

            filterstring = '&'.joinnew_query_string
            return redirect(reverse('filter_analysis') + '?' + filterstring)
    return render(request, 'filter_analysis/oneclick.html', {'form': form})


@login_required
def wizard(request):
    form = FilterWizard([FilterWiZardForm1, FilterWiZardForm2, FilterWiZardForm3])
    if request.method == 'GET':
        print('CHECK HERE')
        query_string = request.META['QUERY_STRING']
        if query_string != '':
            print('LIMPANDO')
            new_query_string = []
            query_string = query_string.split'&'
            for item in query_string:
                if not item.startswith'csrfmiddlewaretoken':
                    item = item.startswith'hash' or item.startswith'wizard' or '-'.joinitem.split'-'2[1:]
                    new_query_string.appenditem

            filterstring = '&'.joinnew_query_string
            return redirect(reverse('filter_analysis') + '?' + filterstring)
    return form(context=(RequestContext(request)), request=request)


class FilterAnalysisUpdateView(UpdateView):
    model = FilterAnalysis

    def get_success_url(self):
        return reverse('filter_analysis')


class FilterAnalysisDeleteView(DeleteView):
    model = FilterAnalysis

    def get_success_url(self):
        return reverse('filter_analysis')


class FilterConfigUpdateView(UpdateView):
    model = FilterConfig
    template_name = 'filter_analysis/filteranalysis_form.html'

    def get_success_url(self):
        return reverse('filter_analysis')


class FilterConfigDeleteView(DeleteView):
    model = FilterConfig
    template_name = 'filter_analysis/filteranalysis_confirm_delete.html'

    def get_success_url(self):
        return reverse('filter_analysis')


@login_required
def create(request):
    print('Hello')
    filterstring = request.META['QUERY_STRING']
    print(filterstring)
    if request.method == 'POST':
        form = Filter(request.POST)
        if form.is_valid:
            filter = FilterAnalysis.objects.create(user=(request.user))
            filter.name = request.POST['name']
            filter.filterstring = form.cleaned_data['filterstring']
            filter.save
            return redirect(reverse('filter_analysis') + '?' + filter.filterstring)
    else:
        form = Filter(initial={'filterstring': filterstring})
    return render(request, 'filter_analysis/createfilter.html', {'form': form})


@login_required
def family_analysis_create_filter(request):
    print('Hello')
    filterstring = request.META['QUERY_STRING']
    print(filterstring)
    if request.method == 'POST':
        form = FamilyFilter(request.POST)
        if form.is_valid:
            filter = FamilyFilterAnalysis.objects.create(user=(request.user))
            filter.name = request.POST['name']
            filter.filterstring = form.cleaned_data['filterstring']
            filter.save
            return redirect(reverse('family_analysis') + '?' + filter.filterstring)
    else:
        form = FamilyFilter(initial={'filterstring': filterstring})
    return render(request, 'filter_analysis/createfilter.html', {'form': form})


@login_required
def createconfig(request):
    print('Hello Config')
    query_string = request.META['QUERY_STRING']
    new_query_string = []
    for item in query_string.split'&':
        if not item.startswith'individuals':
            new_query_string.appenditem

    query_string = '&'.joinnew_query_string
    filterstring = query_string
    if request.method == 'POST':
        form = Filter(request.POST)
        if form.is_valid:
            filterconfig = FilterConfig.objects.create(user=(request.user))
            filterconfig.name = request.POST['name']
            filterconfig.filterstring = form.cleaned_data['filterstring']
            filterconfig.save
            return redirect(reverse('filter_analysis') + '?' + filterconfig.filterstring)
    else:
        form = Filter(initial={'filterstring': filterstring})
    return render(request, 'filter_analysis/createfilter.html', {'form': form})