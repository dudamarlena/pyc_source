# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/filter_analysis/filter_options.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 37331 bytes
from django.db.models import Q
from diseases.models import *
import diseases.models as GeneDisease
from genes.models import *
from individuals.models import *
from variants.models import *
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
import csv, pickle
from databases.models import VariSNP

def filter_individuals_variants(request, query, args, exclude):
    individuals = request.GET.getlist('individuals')
    groups = request.GET.getlist('groups')
    individuals_list = []
    if len(groups) > 0:
        for group_id in groups:
            group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
            for individual in group_individuals:
                individuals_list.append(str(str(individual)))

            print(individuals_list)

    individuals_list = individuals_list + individuals
    print('individuals_list', individuals_list)
    exclude_individuals = request.GET.getlist('exclude_individuals')
    exclude_groups = request.GET.getlist('exclude_groups')
    exclude_individuals_list = []
    if len(exclude_groups) > 0:
        for group_id in exclude_groups:
            group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
            for individual in group_individuals:
                if str(str(individual)) not in individuals_list:
                    exclude_individuals_list.append(str(str(individual)))

    print('exclude_individuals_list', exclude_individuals_list)
    exclude_individuals_list = exclude_individuals_list + exclude_individuals
    exclude_individuals_variants = {}
    if len(exclude_individuals_list) > 0:
        exclude_indexes = ((Variant.objects.filter)(args, individual__id__in=exclude_individuals_list, **query).exclude)(**exclude).values_list('index', flat=True)
        exclude['index__in'] = exclude_indexes
    return individuals_list


def filter_variants_per_gene--- This code section failed: ---

 L.  65         0  LOAD_FAST                'request'
                2  LOAD_ATTR                GET
                4  LOAD_METHOD              get
                6  LOAD_STR                 'variants_per_gene'
                8  LOAD_STR                 ''
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  STORE_FAST               'variants_per_gene'

 L.  67        14  LOAD_GLOBAL              print
               16  LOAD_STR                 'variants per gene'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  POP_TOP          

 L.  68        22  LOAD_GLOBAL              print
               24  LOAD_FAST                'variants_per_gene'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  POP_TOP          

 L.  69        30  LOAD_FAST                'variants_per_gene'
               32  LOAD_STR                 ''
               34  COMPARE_OP               !=
            36_38  POP_JUMP_IF_FALSE   438  'to 438'

 L.  71        40  LOAD_GLOBAL              int
               42  LOAD_FAST                'variants_per_gene'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'variants_per_gene'

 L.  72        48  LOAD_FAST                'request'
               50  LOAD_ATTR                GET
               52  LOAD_METHOD              get
               54  LOAD_STR                 'variants_per_gene_option'
               56  LOAD_STR                 ''
               58  CALL_METHOD_2         2  '2 positional arguments'
               60  STORE_FAST               'variants_per_gene_option'

 L.  74        62  LOAD_GLOBAL              print
               64  LOAD_STR                 'Debugging'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  POP_TOP          

 L.  75        70  LOAD_GLOBAL              print
               72  LOAD_FAST                'variants_per_gene'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  POP_TOP          

 L.  76        78  LOAD_GLOBAL              print
               80  LOAD_FAST                'variants_per_gene_option'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  POP_TOP          

 L.  78        86  BUILD_LIST_0          0 
               88  STORE_FAST               'genes_exclude_list'

 L.  79        90  BUILD_LIST_0          0 
               92  STORE_FAST               'genes_only_list'

 L.  81     94_96  SETUP_LOOP          404  'to 404'
               98  LOAD_FAST                'query'
              100  LOAD_STR                 'individual_id__in'
              102  BINARY_SUBSCR    
              104  GET_ITER         
            106_0  COME_FROM           338  '338'
          106_108  FOR_ITER            402  'to 402'
              110  STORE_FAST               'individual'

 L.  85       112  LOAD_GLOBAL              print
              114  LOAD_STR                 'get list of all genes for each individual'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  POP_TOP          

 L.  86       120  LOAD_GLOBAL              Variant
              122  LOAD_ATTR                objects
              124  LOAD_ATTR                filter
              126  LOAD_FAST                'args'
              128  LOAD_STR                 'individual__id'
              130  LOAD_FAST                'individual'
              132  BUILD_MAP_1           1 
              134  LOAD_FAST                'query'
              136  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              138  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              140  LOAD_ATTR                exclude
              142  BUILD_TUPLE_0         0 
              144  LOAD_FAST                'exclude'
              146  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              148  LOAD_METHOD              values
              150  LOAD_STR                 'gene'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  LOAD_ATTR                exclude
              156  LOAD_STR                 ''
              158  LOAD_CONST               ('gene',)
              160  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              162  LOAD_ATTR                annotate
              164  LOAD_GLOBAL              Count
              166  LOAD_STR                 'gene'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  LOAD_CONST               ('count',)
              172  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              174  LOAD_METHOD              distinct
              176  CALL_METHOD_0         0  '0 positional arguments'
              178  STORE_FAST               'individual_genes'

 L.  87       180  LOAD_GLOBAL              print
              182  LOAD_GLOBAL              len
              184  LOAD_FAST                'individual_genes'
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  POP_TOP          

 L.  88       192  LOAD_FAST                'variants_per_gene_option'
              194  LOAD_STR                 '>'
              196  COMPARE_OP               ==
          198_200  POP_JUMP_IF_FALSE   260  'to 260'

 L.  89       202  SETUP_LOOP          400  'to 400'
              204  LOAD_FAST                'individual_genes'
              206  GET_ITER         
              208  FOR_ITER            256  'to 256'
              210  STORE_FAST               'gene'

 L.  90       212  LOAD_FAST                'gene'
              214  LOAD_STR                 'count'
              216  BINARY_SUBSCR    
              218  LOAD_FAST                'variants_per_gene'
              220  COMPARE_OP               >=
              222  POP_JUMP_IF_FALSE   240  'to 240'

 L.  91       224  LOAD_FAST                'genes_only_list'
              226  LOAD_METHOD              append
              228  LOAD_FAST                'gene'
              230  LOAD_STR                 'gene'
              232  BINARY_SUBSCR    
              234  CALL_METHOD_1         1  '1 positional argument'
              236  POP_TOP          
              238  JUMP_BACK           208  'to 208'
            240_0  COME_FROM           222  '222'

 L.  94       240  LOAD_FAST                'genes_exclude_list'
              242  LOAD_METHOD              append
              244  LOAD_FAST                'gene'
              246  LOAD_STR                 'gene'
              248  BINARY_SUBSCR    
              250  CALL_METHOD_1         1  '1 positional argument'
              252  POP_TOP          
              254  JUMP_BACK           208  'to 208'
              256  POP_BLOCK        
              258  JUMP_BACK           106  'to 106'
            260_0  COME_FROM           198  '198'

 L.  96       260  LOAD_FAST                'variants_per_gene_option'
              262  LOAD_STR                 '<'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   332  'to 332'

 L.  97       270  SETUP_LOOP          400  'to 400'
              272  LOAD_FAST                'individual_genes'
              274  GET_ITER         
              276  FOR_ITER            328  'to 328'
              278  STORE_FAST               'gene'

 L.  98       280  LOAD_FAST                'gene'
              282  LOAD_STR                 'count'
              284  BINARY_SUBSCR    
              286  LOAD_FAST                'variants_per_gene'
              288  COMPARE_OP               <=
          290_292  POP_JUMP_IF_FALSE   310  'to 310'

 L.  99       294  LOAD_FAST                'genes_only_list'
              296  LOAD_METHOD              append
              298  LOAD_FAST                'gene'
              300  LOAD_STR                 'gene'
              302  BINARY_SUBSCR    
              304  CALL_METHOD_1         1  '1 positional argument'
              306  POP_TOP          
              308  JUMP_BACK           276  'to 276'
            310_0  COME_FROM           290  '290'

 L. 102       310  LOAD_FAST                'genes_exclude_list'
              312  LOAD_METHOD              append
              314  LOAD_FAST                'gene'
              316  LOAD_STR                 'gene'
              318  BINARY_SUBSCR    
              320  CALL_METHOD_1         1  '1 positional argument'
              322  POP_TOP          
          324_326  JUMP_BACK           276  'to 276'
              328  POP_BLOCK        
              330  JUMP_BACK           106  'to 106'
            332_0  COME_FROM           266  '266'

 L. 103       332  LOAD_FAST                'variants_per_gene_option'
              334  LOAD_STR                 '='
              336  COMPARE_OP               ==
              338  POP_JUMP_IF_FALSE   106  'to 106'

 L. 104       340  SETUP_LOOP          400  'to 400'
              342  LOAD_FAST                'individual_genes'
              344  GET_ITER         
              346  FOR_ITER            398  'to 398'
              348  STORE_FAST               'gene'

 L. 105       350  LOAD_FAST                'gene'
              352  LOAD_STR                 'count'
              354  BINARY_SUBSCR    
              356  LOAD_FAST                'variants_per_gene'
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   380  'to 380'

 L. 106       364  LOAD_FAST                'genes_only_list'
              366  LOAD_METHOD              append
              368  LOAD_FAST                'gene'
              370  LOAD_STR                 'gene'
              372  BINARY_SUBSCR    
              374  CALL_METHOD_1         1  '1 positional argument'
              376  POP_TOP          
              378  JUMP_BACK           346  'to 346'
            380_0  COME_FROM           360  '360'

 L. 109       380  LOAD_FAST                'genes_exclude_list'
              382  LOAD_METHOD              append
              384  LOAD_FAST                'gene'
              386  LOAD_STR                 'gene'
              388  BINARY_SUBSCR    
              390  CALL_METHOD_1         1  '1 positional argument'
              392  POP_TOP          
          394_396  JUMP_BACK           346  'to 346'
              398  POP_BLOCK        
            400_0  COME_FROM_LOOP      340  '340'
            400_1  COME_FROM_LOOP      270  '270'
            400_2  COME_FROM_LOOP      202  '202'
              400  JUMP_BACK           106  'to 106'
              402  POP_BLOCK        
            404_0  COME_FROM_LOOP       94  '94'

 L. 111       404  LOAD_FAST                'args'
              406  LOAD_METHOD              append
              408  LOAD_GLOBAL              Q
              410  LOAD_FAST                'genes_only_list'
              412  LOAD_CONST               ('gene__in',)
              414  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          

 L. 112       420  LOAD_FAST                'args'
              422  LOAD_METHOD              append
              424  LOAD_GLOBAL              Q
              426  LOAD_FAST                'genes_exclude_list'
              428  LOAD_CONST               ('gene__in',)
              430  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              432  UNARY_INVERT     
              434  CALL_METHOD_1         1  '1 positional argument'
              436  POP_TOP          
            438_0  COME_FROM            36  '36'

Parse error at or near `COME_FROM_LOOP' instruction at offset 400_1


def filter_genes_in_common(request, query, args, exclude):
    print('genes in common')
    genes_in_common = request.GET.get'genes_in_common'''
    if genes_in_common == 'on':
        individual_gene_list = []
        for individual in query['individual_id__in']:
            individual_genes = ((Variant.objects.filter)(args, individual__id=individual, **query).exclude)(**exclude).values_list('gene', flat=True).exclude(gene='').distinct
            individual_genes = set(list(individual_genes))
            individual_gene_list.append(individual_genes)

        genes_in_common_list = (set.intersection)(*individual_gene_list)
        query['gene__in'] = genes_in_common_list


def filter_positions_in_common(request, query, args, exclude):
    print('positions in common')
    positions_in_common = request.GET.get'positions_in_common'''
    if positions_in_common == 'on':
        individual_positions_list = []
        for individual in query['individual_id__in']:
            individual_positions = ((Variant.objects.filter)(args, individual__id=individual, **query).exclude)(**exclude).values_list('pos', flat=True).distinct
            individual_positions = set(list(individual_positions))
            individual_positions_list.append(individual_positions)

        positions_in_common_list = (set.intersection)(*individual_positions_list)
        query['pos__in'] = positions_in_common_list


def filter_chr(request, query):
    chr = request.GET.get'chr'''
    if chr != '':
        query['chr'] = chr


def filter_pos(request, query):
    pos = request.GET.get'pos'''
    if pos != '':
        pos = pos.split('-')
        if len(pos) == 2:
            query['pos__range'] = (
             pos[0], pos[1])
        else:
            query['pos'] = pos[0]


def filter_snp_list(request, query, exclude):
    snp_list = request.GET.get'snp_list'''
    snp_list = snp_list.split('\r\n')
    if snp_list[0] != '':
        safe_snp_list = []
        for row in snp_list:
            row = row.split(',')
            for item in row:
                safe_snp_list.append(item.strip)

        query['variant_id__in'] = safe_snp_list
    exclude_snp_list = request.GET.get'exclude_snp_list'''
    exclude_snp_list = exclude_snp_list.split('\r\n')
    if exclude_snp_list[0] != '':
        safe_exclude_snp_list = []
        for row in exclude_snp_list:
            row = row.split(',')
            for item in row:
                safe_exclude_snp_list.append(item.strip)

        exclude['variant_id__in'] = safe_exclude_snp_list


def filter_gene_list(request, query, args):
    gene_list = request.GET.get'gene_list'''
    gene_list = gene_list.split('\r\n')
    if gene_list[0] != '':
        safe_gene_list = []
        for row in gene_list:
            row = row.split(',')
            for item in row:
                safe_gene_list.append(item.strip.upper)

        print(safe_gene_list)
        query['gene__in'] = safe_gene_list
    exclude_gene_list = request.GET.get'exclude_gene_list'''
    exclude_gene_list = exclude_gene_list.split('\r\n')
    if exclude_gene_list[0] != '':
        safe_gene_list = []
        for row in exclude_gene_list:
            row = row.split(',')
            for item in row:
                safe_gene_list.append(item.strip.upper)

        print(safe_gene_list)
        args.append(~Q(gene__in=safe_gene_list))


def filter_mutation_type(request, args):
    genotype = request.GET.get'genotype'''
    if genotype != '':
        print('genotype', genotype)
        args.append(Q(genotype=genotype))
    else:
        mutation_type = request.GET.get'mutation_type'''
        if mutation_type == 'homozygous':
            args.append(Q(mutation_type='HOM'))
        else:
            if mutation_type == 'heterozygous':
                args.append(Q(mutation_type='HET'))


def filter_effect(request, query):
    effect = request.GET.getlist('effect')
    if len(effect) > 0:
        print('effect', effect)
        query['snpeff_effect__in'] = effect


def filter_dbsnp(request, query):
    dbsnp = request.GET.get'dbsnp'''
    if dbsnp == 'on':
        query['variant_id'] = '.'


def filter_varisnp(request, query, exclude):
    exclude_varisnp = request.GET.get'exclude_varisnp'''
    if exclude_varisnp == 'on':
        snp_list = VariSNP.objects.all.values_list('dbsnp_id', flat=True)
        if 'variant_id__in' in exclude:
            exclude['variant_id__in'].extend(safe_snp_list)
        else:
            exclude['variant_id__in'] = safe_snp_list


def filter_by_1000g(request, args):
    genomes1000_exclude = request.GET.get'genomes1000_exclude'''
    if genomes1000_exclude == 'on':
        args.append(Q(genomes1k_maf__isnull=True))
    else:
        genomes1000 = request.GET.get'genomes1000'''
        if genomes1000 != '':
            genomes1000 = genomes1000.split(' - ')
            if len(genomes1000) == 2:
                min = float(genomes1000[0])
                max = float(genomes1000[1])
                args.append(Q(genomes1k_maf__lte=max) & Q(genomes1k_maf__gte=min) | Q(genomes1k_maf__isnull=True))
            if len(genomes1000) == 1:
                max = float(genomes1000[0])
                args.append(Q(genomes1k_maf__lte=max) & Q(genomes1k_maf__gte=0) | Q(genomes1k_maf__isnull=True))


def filter_by_dbsnp(request, args):
    dbsnp_exclude = request.GET.get'dbsnp_exclude'''
    if dbsnp_exclude == 'on':
        args.append(Q(dbsnp_maf__isnull=True))
    else:
        dbsnp = request.GET.get'dbsnp_frequency'''
        if dbsnp != '':
            dbsnp = dbsnp.split(' - ')
            if len(dbsnp) == 2:
                min = float(dbsnp[0])
                max = float(dbsnp[1])
                args.append(Q(dbsnp_maf__lte=max) & Q(dbsnp_maf__gte=min) | Q(dbsnp_maf__isnull=True))
            if len(dbsnp) == 1:
                max = float(dbsnp[0])
                args.append(Q(dbsnp_maf__lte=max) & Q(dbsnp_maf__gte=0) | Q(dbsnp_maf__isnull=True))


def filter_by_esp(request, args):
    esp_exclude = request.GET.get'esp_exclude'''
    if esp_exclude == 'on':
        args.append(Q(esp_maf__isnull=True))
    else:
        esp = request.GET.get'esp_frequency'''
        if esp != '':
            esp = esp.split(' - ')
            min = float(esp[0])
            max = float(esp[1])
            args.append(Q(esp_maf__lte=max) & Q(esp_maf__gte=min) | Q(esp_maf__isnull=True))


def filter_by_individuals--- This code section failed: ---

 L. 339         0  LOAD_FAST                'request'
                2  LOAD_ATTR                GET
                4  LOAD_METHOD              getlist
                6  LOAD_STR                 'individuals'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               'individuals'

 L. 341        12  LOAD_FAST                'request'
               14  LOAD_ATTR                GET
               16  LOAD_METHOD              getlist
               18  LOAD_STR                 'groups'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  STORE_FAST               'groups'

 L. 343        24  BUILD_LIST_0          0 
               26  STORE_FAST               'individuals_list'

 L. 344        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'groups'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  LOAD_CONST               0
               36  COMPARE_OP               >
               38  POP_JUMP_IF_FALSE   118  'to 118'

 L. 345        40  SETUP_LOOP          118  'to 118'
               42  LOAD_FAST                'groups'
               44  GET_ITER         
               46  FOR_ITER            116  'to 116'
               48  STORE_FAST               'group_id'

 L. 346        50  LOAD_GLOBAL              get_object_or_404
               52  LOAD_GLOBAL              Group
               54  LOAD_FAST                'group_id'
               56  LOAD_CONST               ('pk',)
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  LOAD_ATTR                members
               62  LOAD_ATTR                values_list
               64  LOAD_STR                 'id'
               66  LOAD_CONST               True
               68  LOAD_CONST               ('flat',)
               70  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               72  STORE_FAST               'group_individuals'

 L. 347        74  SETUP_LOOP          106  'to 106'
               76  LOAD_FAST                'group_individuals'
               78  GET_ITER         
               80  FOR_ITER            104  'to 104'
               82  STORE_FAST               'individual'

 L. 348        84  LOAD_FAST                'individuals_list'
               86  LOAD_METHOD              append
               88  LOAD_GLOBAL              str
               90  LOAD_GLOBAL              str
               92  LOAD_FAST                'individual'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  POP_TOP          
              102  JUMP_BACK            80  'to 80'
              104  POP_BLOCK        
            106_0  COME_FROM_LOOP       74  '74'

 L. 349       106  LOAD_GLOBAL              print
              108  LOAD_FAST                'individuals_list'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  POP_TOP          
              114  JUMP_BACK            46  'to 46'
              116  POP_BLOCK        
            118_0  COME_FROM_LOOP       40  '40'
            118_1  COME_FROM            38  '38'

 L. 350       118  LOAD_FAST                'individuals_list'
              120  LOAD_FAST                'individuals'
              122  BINARY_ADD       
              124  STORE_FAST               'individuals_list'

 L. 351       126  LOAD_GLOBAL              print
              128  LOAD_STR                 'individuals_list'
              130  LOAD_FAST                'individuals_list'
              132  CALL_FUNCTION_2       2  '2 positional arguments'
              134  POP_TOP          

 L. 355       136  LOAD_FAST                'request'
              138  LOAD_ATTR                GET
              140  LOAD_METHOD              getlist
              142  LOAD_STR                 'exclude_individuals'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  STORE_FAST               'exclude_individuals'

 L. 359       148  LOAD_FAST                'request'
              150  LOAD_ATTR                GET
              152  LOAD_METHOD              getlist
              154  LOAD_STR                 'exclude_groups'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  STORE_FAST               'exclude_groups'

 L. 361       160  BUILD_LIST_0          0 
              162  STORE_FAST               'exclude_individuals_list'

 L. 362       164  LOAD_GLOBAL              len
              166  LOAD_FAST                'exclude_groups'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  LOAD_CONST               0
              172  COMPARE_OP               >
          174_176  POP_JUMP_IF_FALSE   264  'to 264'

 L. 363       178  SETUP_LOOP          264  'to 264'
              180  LOAD_FAST                'exclude_groups'
              182  GET_ITER         
              184  FOR_ITER            262  'to 262'
              186  STORE_FAST               'group_id'

 L. 364       188  LOAD_GLOBAL              get_object_or_404
              190  LOAD_GLOBAL              Group
              192  LOAD_FAST                'group_id'
              194  LOAD_CONST               ('pk',)
              196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              198  LOAD_ATTR                members
              200  LOAD_ATTR                values_list
              202  LOAD_STR                 'id'
              204  LOAD_CONST               True
              206  LOAD_CONST               ('flat',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  STORE_FAST               'group_individuals'

 L. 365       212  SETUP_LOOP          260  'to 260'
              214  LOAD_FAST                'group_individuals'
              216  GET_ITER         
            218_0  COME_FROM           236  '236'
              218  FOR_ITER            258  'to 258'
              220  STORE_FAST               'individual'

 L. 366       222  LOAD_GLOBAL              str
              224  LOAD_GLOBAL              str
              226  LOAD_FAST                'individual'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  LOAD_FAST                'individuals_list'
              234  COMPARE_OP               not-in
              236  POP_JUMP_IF_FALSE   218  'to 218'

 L. 367       238  LOAD_FAST                'exclude_individuals_list'
              240  LOAD_METHOD              append
              242  LOAD_GLOBAL              str
              244  LOAD_GLOBAL              str
              246  LOAD_FAST                'individual'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  POP_TOP          
              256  JUMP_BACK           218  'to 218'
              258  POP_BLOCK        
            260_0  COME_FROM_LOOP      212  '212'
              260  JUMP_BACK           184  'to 184'
              262  POP_BLOCK        
            264_0  COME_FROM_LOOP      178  '178'
            264_1  COME_FROM           174  '174'

 L. 369       264  LOAD_GLOBAL              print
              266  LOAD_STR                 'exclude_individuals_list'
              268  LOAD_FAST                'exclude_individuals_list'
              270  CALL_FUNCTION_2       2  '2 positional arguments'
              272  POP_TOP          

 L. 371       274  LOAD_FAST                'exclude_individuals_list'
              276  LOAD_FAST                'exclude_individuals'
              278  BINARY_ADD       
              280  STORE_FAST               'exclude_individuals_list'

 L. 373       282  BUILD_MAP_0           0 
              284  STORE_FAST               'exclude_individuals_variants'

 L. 375       286  LOAD_GLOBAL              len
              288  LOAD_FAST                'exclude_individuals_list'
              290  CALL_FUNCTION_1       1  '1 positional argument'
              292  LOAD_CONST               0
              294  COMPARE_OP               >
          296_298  POP_JUMP_IF_FALSE   348  'to 348'

 L. 376       300  LOAD_GLOBAL              Variant
              302  LOAD_ATTR                objects
              304  LOAD_ATTR                filter
              306  LOAD_FAST                'args'
              308  LOAD_STR                 'individual__id__in'
              310  LOAD_FAST                'exclude_individuals_list'
              312  BUILD_MAP_1           1 
              314  LOAD_FAST                'query'
              316  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              318  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              320  LOAD_ATTR                exclude
              322  BUILD_TUPLE_0         0 
              324  LOAD_FAST                'exclude'
              326  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              328  LOAD_ATTR                values_list
              330  LOAD_STR                 'index'
              332  LOAD_CONST               True
              334  LOAD_CONST               ('flat',)
              336  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              338  STORE_FAST               'exclude_indexes'

 L. 377       340  LOAD_FAST                'exclude_indexes'
              342  LOAD_FAST                'exclude'
              344  LOAD_STR                 'index__in'
              346  STORE_SUBSCR     
            348_0  COME_FROM           296  '296'

 L. 380       348  LOAD_GLOBAL              len
              350  LOAD_FAST                'individuals_list'
              352  CALL_FUNCTION_1       1  '1 positional argument'
              354  LOAD_CONST               0
              356  COMPARE_OP               >
          358_360  POP_JUMP_IF_FALSE  1074  'to 1074'

 L. 382       362  LOAD_FAST                'individuals_list'
              364  LOAD_FAST                'query'
              366  LOAD_STR                 'individual_id__in'
              368  STORE_SUBSCR     

 L. 384       370  LOAD_FAST                'request'
              372  LOAD_ATTR                GET
              374  LOAD_METHOD              get
              376  LOAD_STR                 'variants_per_gene'
              378  CALL_METHOD_1         1  '1 positional argument'
              380  STORE_FAST               'variants_per_gene'

 L. 386       382  LOAD_FAST                'request'
              384  LOAD_ATTR                GET
              386  LOAD_METHOD              get
              388  LOAD_STR                 'genes_in_common'
              390  LOAD_STR                 ''
              392  CALL_METHOD_2         2  '2 positional arguments'
              394  STORE_FAST               'genes_in_common'

 L. 388       396  LOAD_GLOBAL              print
              398  LOAD_STR                 'variants per gene'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  POP_TOP          

 L. 389       404  LOAD_GLOBAL              print
              406  LOAD_FAST                'variants_per_gene'
              408  CALL_FUNCTION_1       1  '1 positional argument'
              410  POP_TOP          

 L. 390       412  LOAD_FAST                'variants_per_gene'
              414  LOAD_STR                 ''
              416  COMPARE_OP               !=
          418_420  POP_JUMP_IF_FALSE   824  'to 824'

 L. 392       422  LOAD_GLOBAL              int
              424  LOAD_FAST                'variants_per_gene'
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  STORE_FAST               'variants_per_gene'

 L. 394       430  LOAD_FAST                'request'
              432  LOAD_ATTR                GET
              434  LOAD_METHOD              get
              436  LOAD_STR                 'variants_per_gene_option'
              438  LOAD_STR                 ''
              440  CALL_METHOD_2         2  '2 positional arguments'
              442  STORE_FAST               'variants_per_gene_option'

 L. 396       444  LOAD_GLOBAL              print
              446  LOAD_STR                 'Debugging'
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  POP_TOP          

 L. 397       452  LOAD_GLOBAL              print
              454  LOAD_FAST                'variants_per_gene'
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  POP_TOP          

 L. 398       460  LOAD_GLOBAL              print
              462  LOAD_FAST                'variants_per_gene_option'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  POP_TOP          

 L. 400       468  BUILD_LIST_0          0 
              470  STORE_FAST               'genes_exclude_list'

 L. 401       472  BUILD_LIST_0          0 
              474  STORE_FAST               'genes_only_list'

 L. 403   476_478  SETUP_LOOP          790  'to 790'
              480  LOAD_FAST                'individuals_list'
              482  GET_ITER         
            484_0  COME_FROM           720  '720'
          484_486  FOR_ITER            788  'to 788'
              488  STORE_FAST               'individual'

 L. 407       490  LOAD_GLOBAL              print
              492  LOAD_STR                 'get list of all genes for each individual'
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  POP_TOP          

 L. 408       498  LOAD_GLOBAL              Variant
              500  LOAD_ATTR                objects
              502  LOAD_ATTR                filter
              504  LOAD_FAST                'args'
              506  LOAD_STR                 'individual__id'
              508  LOAD_FAST                'individual'
              510  BUILD_MAP_1           1 
              512  LOAD_FAST                'query'
              514  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              516  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              518  LOAD_ATTR                exclude
              520  BUILD_TUPLE_0         0 
              522  LOAD_FAST                'exclude'
              524  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              526  LOAD_METHOD              values
              528  LOAD_STR                 'gene'
              530  CALL_METHOD_1         1  '1 positional argument'
              532  LOAD_ATTR                exclude
              534  LOAD_STR                 ''
              536  LOAD_CONST               ('gene',)
              538  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              540  LOAD_ATTR                annotate
              542  LOAD_GLOBAL              Count
              544  LOAD_STR                 'gene'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  LOAD_CONST               ('count',)
              550  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              552  LOAD_METHOD              distinct
              554  CALL_METHOD_0         0  '0 positional arguments'
              556  STORE_FAST               'individual_genes'

 L. 409       558  LOAD_GLOBAL              print
              560  LOAD_GLOBAL              len
              562  LOAD_FAST                'individual_genes'
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  CALL_FUNCTION_1       1  '1 positional argument'
              568  POP_TOP          

 L. 410       570  LOAD_FAST                'variants_per_gene_option'
              572  LOAD_STR                 '>'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   642  'to 642'

 L. 411       580  SETUP_LOOP          784  'to 784'
              582  LOAD_FAST                'individual_genes'
              584  GET_ITER         
              586  FOR_ITER            638  'to 638'
              588  STORE_FAST               'gene'

 L. 412       590  LOAD_FAST                'gene'
              592  LOAD_STR                 'count'
              594  BINARY_SUBSCR    
              596  LOAD_FAST                'variants_per_gene'
              598  COMPARE_OP               >=
          600_602  POP_JUMP_IF_FALSE   620  'to 620'

 L. 413       604  LOAD_FAST                'genes_only_list'
              606  LOAD_METHOD              append
              608  LOAD_FAST                'gene'
              610  LOAD_STR                 'gene'
              612  BINARY_SUBSCR    
              614  CALL_METHOD_1         1  '1 positional argument'
              616  POP_TOP          
              618  JUMP_BACK           586  'to 586'
            620_0  COME_FROM           600  '600'

 L. 416       620  LOAD_FAST                'genes_exclude_list'
              622  LOAD_METHOD              append
              624  LOAD_FAST                'gene'
              626  LOAD_STR                 'gene'
              628  BINARY_SUBSCR    
              630  CALL_METHOD_1         1  '1 positional argument'
              632  POP_TOP          
          634_636  JUMP_BACK           586  'to 586'
              638  POP_BLOCK        
              640  JUMP_BACK           484  'to 484'
            642_0  COME_FROM           576  '576'

 L. 418       642  LOAD_FAST                'variants_per_gene_option'
              644  LOAD_STR                 '<'
              646  COMPARE_OP               ==
          648_650  POP_JUMP_IF_FALSE   714  'to 714'

 L. 419       652  SETUP_LOOP          784  'to 784'
              654  LOAD_FAST                'individual_genes'
              656  GET_ITER         
              658  FOR_ITER            710  'to 710'
              660  STORE_FAST               'gene'

 L. 420       662  LOAD_FAST                'gene'
              664  LOAD_STR                 'count'
              666  BINARY_SUBSCR    
              668  LOAD_FAST                'variants_per_gene'
              670  COMPARE_OP               <=
          672_674  POP_JUMP_IF_FALSE   692  'to 692'

 L. 421       676  LOAD_FAST                'genes_only_list'
              678  LOAD_METHOD              append
              680  LOAD_FAST                'gene'
              682  LOAD_STR                 'gene'
              684  BINARY_SUBSCR    
              686  CALL_METHOD_1         1  '1 positional argument'
              688  POP_TOP          
              690  JUMP_BACK           658  'to 658'
            692_0  COME_FROM           672  '672'

 L. 424       692  LOAD_FAST                'genes_exclude_list'
              694  LOAD_METHOD              append
              696  LOAD_FAST                'gene'
              698  LOAD_STR                 'gene'
              700  BINARY_SUBSCR    
              702  CALL_METHOD_1         1  '1 positional argument'
              704  POP_TOP          
          706_708  JUMP_BACK           658  'to 658'
              710  POP_BLOCK        
              712  JUMP_BACK           484  'to 484'
            714_0  COME_FROM           648  '648'

 L. 425       714  LOAD_FAST                'variants_per_gene_option'
              716  LOAD_STR                 '='
              718  COMPARE_OP               ==
          720_722  POP_JUMP_IF_FALSE   484  'to 484'

 L. 426       724  SETUP_LOOP          784  'to 784'
              726  LOAD_FAST                'individual_genes'
              728  GET_ITER         
              730  FOR_ITER            782  'to 782'
              732  STORE_FAST               'gene'

 L. 427       734  LOAD_FAST                'gene'
              736  LOAD_STR                 'count'
              738  BINARY_SUBSCR    
              740  LOAD_FAST                'variants_per_gene'
              742  COMPARE_OP               ==
          744_746  POP_JUMP_IF_FALSE   764  'to 764'

 L. 428       748  LOAD_FAST                'genes_only_list'
              750  LOAD_METHOD              append
              752  LOAD_FAST                'gene'
              754  LOAD_STR                 'gene'
              756  BINARY_SUBSCR    
              758  CALL_METHOD_1         1  '1 positional argument'
              760  POP_TOP          
              762  JUMP_BACK           730  'to 730'
            764_0  COME_FROM           744  '744'

 L. 431       764  LOAD_FAST                'genes_exclude_list'
              766  LOAD_METHOD              append
              768  LOAD_FAST                'gene'
              770  LOAD_STR                 'gene'
              772  BINARY_SUBSCR    
              774  CALL_METHOD_1         1  '1 positional argument'
              776  POP_TOP          
          778_780  JUMP_BACK           730  'to 730'
              782  POP_BLOCK        
            784_0  COME_FROM_LOOP      724  '724'
            784_1  COME_FROM_LOOP      652  '652'
            784_2  COME_FROM_LOOP      580  '580'
          784_786  JUMP_BACK           484  'to 484'
              788  POP_BLOCK        
            790_0  COME_FROM_LOOP      476  '476'

 L. 433       790  LOAD_FAST                'args'
              792  LOAD_METHOD              append
              794  LOAD_GLOBAL              Q
              796  LOAD_FAST                'genes_only_list'
              798  LOAD_CONST               ('gene__in',)
              800  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              802  CALL_METHOD_1         1  '1 positional argument'
              804  POP_TOP          

 L. 434       806  LOAD_FAST                'args'
              808  LOAD_METHOD              append
              810  LOAD_GLOBAL              Q
              812  LOAD_FAST                'genes_exclude_list'
              814  LOAD_CONST               ('gene__in',)
              816  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              818  UNARY_INVERT     
              820  CALL_METHOD_1         1  '1 positional argument'
              822  POP_TOP          
            824_0  COME_FROM           418  '418'

 L. 436       824  LOAD_FAST                'genes_in_common'
              826  LOAD_STR                 'on'
              828  COMPARE_OP               ==
          830_832  POP_JUMP_IF_FALSE   946  'to 946'

 L. 438       834  BUILD_LIST_0          0 
              836  STORE_FAST               'individual_gene_list'

 L. 439       838  SETUP_LOOP          928  'to 928'
              840  LOAD_FAST                'individuals_list'
              842  GET_ITER         
              844  FOR_ITER            926  'to 926'
              846  STORE_FAST               'individual'

 L. 440       848  LOAD_GLOBAL              Variant
              850  LOAD_ATTR                objects
              852  LOAD_ATTR                filter
              854  LOAD_FAST                'args'
              856  LOAD_STR                 'individual__id'
              858  LOAD_FAST                'individual'
              860  BUILD_MAP_1           1 
              862  LOAD_FAST                'query'
              864  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              866  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              868  LOAD_ATTR                exclude
              870  BUILD_TUPLE_0         0 
              872  LOAD_FAST                'exclude'
              874  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              876  LOAD_ATTR                values_list
              878  LOAD_STR                 'gene'
              880  LOAD_CONST               True
              882  LOAD_CONST               ('flat',)
              884  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              886  LOAD_ATTR                exclude
              888  LOAD_STR                 ''
              890  LOAD_CONST               ('gene',)
              892  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              894  LOAD_METHOD              distinct
              896  CALL_METHOD_0         0  '0 positional arguments'
              898  STORE_FAST               'individual_genes'

 L. 441       900  LOAD_GLOBAL              set
              902  LOAD_GLOBAL              list
              904  LOAD_FAST                'individual_genes'
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  CALL_FUNCTION_1       1  '1 positional argument'
              910  STORE_FAST               'individual_genes'

 L. 442       912  LOAD_FAST                'individual_gene_list'
              914  LOAD_METHOD              append
              916  LOAD_FAST                'individual_genes'
              918  CALL_METHOD_1         1  '1 positional argument'
              920  POP_TOP          
          922_924  JUMP_BACK           844  'to 844'
              926  POP_BLOCK        
            928_0  COME_FROM_LOOP      838  '838'

 L. 443       928  LOAD_GLOBAL              set
              930  LOAD_ATTR                intersection
              932  LOAD_FAST                'individual_gene_list'
              934  CALL_FUNCTION_EX      0  'positional arguments only'
              936  STORE_FAST               'genes_in_common_list'

 L. 444       938  LOAD_FAST                'genes_in_common_list'
              940  LOAD_FAST                'query'
              942  LOAD_STR                 'gene__in'
              944  STORE_SUBSCR     
            946_0  COME_FROM           830  '830'

 L. 447       946  LOAD_FAST                'request'
              948  LOAD_ATTR                GET
              950  LOAD_METHOD              get
              952  LOAD_STR                 'positions_in_common'
              954  LOAD_STR                 ''
              956  CALL_METHOD_2         2  '2 positional arguments'
              958  STORE_FAST               'positions_in_common'

 L. 448       960  LOAD_FAST                'positions_in_common'
              962  LOAD_STR                 'on'
              964  COMPARE_OP               ==
          966_968  POP_JUMP_IF_FALSE  1074  'to 1074'

 L. 450       970  BUILD_LIST_0          0 
              972  STORE_FAST               'individual_positions_list'

 L. 451       974  SETUP_LOOP         1056  'to 1056'
              976  LOAD_FAST                'individuals_list'
              978  GET_ITER         
              980  FOR_ITER           1054  'to 1054'
              982  STORE_FAST               'individual'

 L. 453       984  LOAD_GLOBAL              Variant
              986  LOAD_ATTR                objects
              988  LOAD_ATTR                filter
              990  LOAD_FAST                'args'
              992  LOAD_STR                 'individual__id'
              994  LOAD_FAST                'individual'
              996  BUILD_MAP_1           1 
              998  LOAD_FAST                'query'
             1000  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1002  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1004  LOAD_ATTR                exclude
             1006  BUILD_TUPLE_0         0 
             1008  LOAD_FAST                'exclude'
             1010  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1012  LOAD_ATTR                values_list
             1014  LOAD_STR                 'pos'
             1016  LOAD_CONST               True
             1018  LOAD_CONST               ('flat',)
             1020  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1022  LOAD_METHOD              distinct
             1024  CALL_METHOD_0         0  '0 positional arguments'
             1026  STORE_FAST               'individual_positions'

 L. 454      1028  LOAD_GLOBAL              set
             1030  LOAD_GLOBAL              list
             1032  LOAD_FAST                'individual_positions'
             1034  CALL_FUNCTION_1       1  '1 positional argument'
             1036  CALL_FUNCTION_1       1  '1 positional argument'
             1038  STORE_FAST               'individual_positions'

 L. 455      1040  LOAD_FAST                'individual_positions_list'
             1042  LOAD_METHOD              append
             1044  LOAD_FAST                'individual_positions'
             1046  CALL_METHOD_1         1  '1 positional argument'
             1048  POP_TOP          
         1050_1052  JUMP_BACK           980  'to 980'
             1054  POP_BLOCK        
           1056_0  COME_FROM_LOOP      974  '974'

 L. 456      1056  LOAD_GLOBAL              set
             1058  LOAD_ATTR                intersection
             1060  LOAD_FAST                'individual_positions_list'
             1062  CALL_FUNCTION_EX      0  'positional arguments only'
             1064  STORE_FAST               'positions_in_common_list'

 L. 457      1066  LOAD_FAST                'positions_in_common_list'
             1068  LOAD_FAST                'query'
             1070  LOAD_STR                 'pos__in'
             1072  STORE_SUBSCR     
           1074_0  COME_FROM           966  '966'
           1074_1  COME_FROM           358  '358'

Parse error at or near `COME_FROM_LOOP' instruction at offset 784_1


def filter_qual(request, args):
    qual = request.GET.get'qual'''
    if qual != '':
        qual_option = request.GET.get'qual_option'''
        if qual_option == '<':
            args.append(Q(qual__lte=(float(qual))))
        else:
            if qual_option == '>':
                args.append(Q(qual__gte=(float(qual))))
            else:
                if qual_option == '=':
                    args.append(Q(qual=(float(qual))))


def filter_filter(request, query):
    filter = request.GET.getlist('filter')
    if len(filter) > 0:
        query['filter__in'] = filter


def filter_by_sift(request, args):
    sift = request.GET.get'sift'''
    if sift != '':
        sift_exclude = request.GET.get'sift_exclude'''
        if sift_exclude == 'on':
            sift_flag = True
        else:
            sift_flag = False
        sift = sift.split(' - ')
        sift_min = float(sift[0])
        sift_max = float(sift[1])
        if sift_flag:
            args.append(Q(sift__lte=sift_max) & Q(sift__gte=sift_min))
        else:
            args.append(Q(sift__lte=sift_max) & Q(sift__gte=sift_min) | Q(sift__isnull=True))


def filter_by_cadd(request, args):
    cadd = request.GET.get'cadd'''
    if cadd != '':
        cadd_exclude = request.GET.get'cadd_exclude'''
        if cadd_exclude == 'on':
            cadd_flag = True
        else:
            cadd_flag = False
        cadd = cadd.split(' - ')
        cadd_min = float(cadd[0])
        cadd_max = float(cadd[1])
        if cadd_flag:
            args.append(Q(cadd__lte=cadd_max) & Q(cadd__gte=cadd_min))
        else:
            args.append(Q(cadd__lte=cadd_max) & Q(cadd__gte=cadd_min) | Q(cadd__isnull=True))


def filter_by_mcap(request, args):
    mcap = request.GET.get'mcap'''
    if mcap != '':
        mcap_exclude = request.GET.get'mcap_exclude'''
        if mcap_exclude == 'on':
            mcap_flag = True
        else:
            mcap_flag = False
        mcap = mcap.split(' - ')
        mcap_min = float(mcap[0])
        mcap_max = float(mcap[1])
        if mcap_flag:
            args.append(Q(mcap_score__lte=mcap_max) & Q(mcap_score__gte=mcap_min))
        else:
            args.append(Q(mcap_score__lte=mcap_max) & Q(mcap_score__gte=mcap_min) | Q(mcap_score__isnull=True))


def filter_by_rf_score(request, args):
    rf_score = request.GET.get'rf_score'''
    if rf_score != '':
        rf_exclude = request.GET.get'rf_exclude'''
        if rf_exclude == 'on':
            rf_flag = True
        else:
            rf_flag = False
        rf = rf_score.split(' - ')
        rf_min = float(rf[0])
        rf_max = float(rf[1])
        if rf_flag:
            args.append(Q(rf_score__lte=rf_max) & Q(rf_score__gte=rf_min))
        else:
            args.append(Q(rf_score__lte=rf_max) & Q(rf_score__gte=rf_min) | Q(rf_score__isnull=True))


def filter_by_ada_score(request, args):
    ada_score = request.GET.get'ada_score'''
    if ada_score != '':
        ada_exclude = request.GET.get'ada_exclude'''
        if ada_exclude == 'on':
            ada_flag = True
        else:
            ada_flag = False
        ada = ada_score.split(' - ')
        ada_min = float(ada[0])
        ada_max = float(ada[1])
        if ada_flag:
            args.append(Q(ada_score__lte=ada_max) & Q(ada_score__gte=ada_min))
        else:
            args.append(Q(ada_score__lte=ada_max) & Q(ada_score__gte=ada_min) | Q(ada_score__isnull=True))


def filter_by_pp2(request, args):
    polyphen = request.GET.get'polyphen'''
    if polyphen != '':
        polyphen_exclude = request.GET.get'polyphen_exclude'''
        if polyphen_exclude == 'on':
            polyphen_flag = True
        else:
            polyphen_flag = False
        polyphen = polyphen.split(' - ')
        polyphen_min = float(polyphen[0])
        polyphen_max = float(polyphen[1])
        if polyphen_flag:
            args.append(Q(polyphen2__lte=polyphen_max) & Q(polyphen2__gte=polyphen_min))
        else:
            args.append(Q(polyphen2__lte=polyphen_max) & Q(polyphen2__gte=polyphen_min) | Q(polyphen2__isnull=True))


def filter_by_segdup(request, args):
    exclude_segdup = request.GET.get'exclude_segdup'''
    if exclude_segdup == 'on':
        args.append(Q(segdup=''))


def filter_cgd(request, args):
    cgdmanifestation = request.GET.getlist('cgdmanifestation')
    conditions = request.GET.getlist('cgd')
    if len(cgdmanifestation) > 0:
        if cgdmanifestation[0] != '':
            cgdentries = CGDEntry.objects.filter(MANIFESTATION_CATEGORIES__in=cgdmanifestation)
            gene_list = []
            for gene in cgdentries:
                gene_list.append(gene.GENE)

            args.append(Q(gene__in=gene_list))
    if len(conditions) > 0:
        if conditions[0] != '':
            cgdentries = CGDEntry.objects.filter(CONDITIONS__in=conditions)
            gene_list = []
            for gene in cgdentries:
                gene_list.append(gene.GENE)

            args.append(Q(gene__in=gene_list))


def filter_omim(request, args):
    omim = request.GET.getlist('omim')
    print('omim', omim)
    print('FILTER OMIM')
    if len(omim) > 0:
        if omim[0] != '':
            omimentries = Disease.objects.filter(id__in=omim)
            gene_list = []
            print('omimentries', omimentries)
            genes = GeneDisease.objects.filter(diseases__in=omimentries)
            print('omimgenes', genes)
            for gene in genes:
                gene_list.append(gene.official_name)

            args.append(Q(gene__in=gene_list))


def filter_hgmd(request, args):
    hgmd = request.GET.getlist('hgmd')
    if len(hgmd) > 0:
        if hgmd[0] != '':
            hgmdentries = HGMDPhenotype.objects.filter(id__in=hgmd)
            gene_list = []
            genes = HGMDGene.objects.filter(diseases__in=hgmdentries)
            for gene in genes:
                gene_list.append(gene.symbol)

            args.append(Q(gene__in=gene_list))


def filter_genelists(request, query, args, exclude):
    genelists = request.GET.getlist('genelists')
    safe_gene_list = []
    if len(genelists) > 0:
        for genelist_id in genelists:
            genelist_obj = GeneList.objects.get(pk=genelist_id)
            gene_list = genelist_obj.genes.split(',')
            for gene in gene_list:
                if gene not in safe_gene_list:
                    safe_gene_list.append(gene.upper)

        query['gene__in'] = safe_gene_list
    exclude_genelists = request.GET.getlist('exclude_genelists')
    if len(exclude_genelists) > 0:
        exclude_safe_gene_list = []
        for genelist_id in exclude_genelists:
            genelist_obj = GeneList.objects.get(pk=genelist_id)
            gene_list = genelist_obj.genes.split(',')
            for gene in gene_list:
                if gene not in safe_gene_list and gene not in exclude_safe_gene_list:
                    exclude_safe_gene_list.append(gene)

        if len(exclude_safe_gene_list) > 0:
            exclude['gene__in'] = exclude_safe_gene_list


def filter_inheritance_option(request):
    inheritance_option = request.GET.get'inheritance_option'''
    if inheritance_option == '3':
        request.GET.__setitem__'variants_per_gene''2'
        request.GET.__setitem__'variants_per_gene_option''>'
        print(request.GET)


def filter_inheritance_option_exclude_individuals(request):
    inheritance_option = request.GET.get'inheritance_option'''
    exclude_individuals = request.GET.getlist('exclude_individuals')
    father = request.GET.get'father'''
    mother = request.GET.get'mother'''
    parents = [father, mother]
    if inheritance_option == '1' or inheritance_option == '2':
        if father not in exclude_individuals:
            request.GET.appendlist'exclude_individuals'father
        if mother not in exclude_individuals:
            request.GET.appendlist'exclude_individuals'mother


def filter_inheritance_option_mutation_type(request, args):
    inheritance_option = request.GET.get'inheritance_option'''
    if inheritance_option == '1':
        genotypes = [
         '0/0', './.', '0/1', '1/0', '0/2', '2/0']
        args.append(~Q(genotype__in=genotypes))


def filter_sift(request, args):
    sift = request.GET.get'sift'''
    if sift != '':
        sift_exclude = request.GET.get'sift_exclude'''
        if sift_exclude == 'on':
            sift_flag = True
        else:
            sift_flag = False
        sift_option = request.GET.get'sift_option'''
        if sift_option == '<':
            if sift_flag:
                args.append(Q(sift__lte=(float(sift))))
        else:
            args.append(Q(sift__lte=(float(sift))) | Q(sift__isnull=True))
    else:
        if sift_option == '>':
            if sift_flag:
                args.append(Q(sift__gte=(float(sift))))
            else:
                args.append(Q(sift__gte=(float(sift))) | Q(sift__isnull=True))
        else:
            if sift_option == '=':
                if sift_flag:
                    args.append(Q(sift=(float(sift))))
                else:
                    args.append(Q(sift=(float(sift))) | Q(sift__isnull=True))


def filter_polyphen2(request, args):
    polyphen = request.GET.get'polyphen'''
    if polyphen != '':
        polyphen_exclude = request.GET.get'polyphen_exclude'''
        if polyphen_exclude == 'on':
            polyphen_flag = True
        else:
            polyphen_flag = False
        polyphen_option = request.GET.get'polyphen_option'''
        if polyphen_option == '<':
            if polyphen_flag:
                args.append(Q(polyphen2__lte=(float(polyphen))))
        else:
            args.append(Q(polyphen2__lte=(float(polyphen))) | Q(polyphen2__isnull=True))
    else:
        if polyphen_option == '>':
            if polyphen_flag:
                args.append(Q(polyphen2__gte=(float(polyphen))))
            else:
                args.append(Q(polyphen2__gte=(float(polyphen))) | Q(polyphen2__isnull=True))
        else:
            if polyphen_option == '=':
                if polyphen_flag:
                    args.append(Q(polyphen2=(float(polyphen))))
                else:
                    args.append(Q(polyphen2=(float(polyphen))) | Q(polyphen2__isnull=True))


def filter_dbsnp_build(request, args):
    dbsnp_build = request.GET.get'dbsnp_build'''
    if dbsnp_build != '':
        dbsnp_option = request.GET.get'dbsnp_option'''
        if dbsnp_option == '<':
            args.append(Q(dbsnp_build__lte=(int(dbsnp_build))) | Q(dbsnp_build__isnull=True))
        else:
            if dbsnp_option == '>':
                args.append(Q(dbsnp_build__gte=(int(dbsnp_build))) | Q(dbsnp_build__isnull=True))


def filter_read_depth(request, args):
    read_depth = request.GET.get'read_depth'''
    if read_depth != '':
        read_depth_option = request.GET.get'read_depth_option'''
        if read_depth_option == '<':
            args.append(Q(read_depth__lte=(int(read_depth))))
        else:
            if read_depth_option == '>':
                args.append(Q(read_depth__gte=(int(read_depth))))
            else:
                if read_depth_option == '=':
                    args.append(Q(read_depth=(int(read_depth))))


def filter_func_class(request, query):
    func_class = request.GET.getlist('func_class')
    if len(func_class) > 0:
        query['snpeff_func_class__in'] = func_class


def filter_impact(request, query):
    impact = request.GET.getlist('impact')
    if len(impact) > 0:
        query['snpeff_impact__in'] = impact


def filter_is_at_hgmd(request, query):
    hgmd = request.GET.get'is_at_hgmd'''
    if hgmd == 'on':
        query['is_at_hgmd'] = True


def filter_clnsig(request, query):
    clnsig = request.GET.get'clnsig'''
    if clnsig != '':
        query['clinvar_clnsig'] = clnsig


def export_to_csv(request, variants):
    export = request.GET.get'export'''
    if export != '':
        if export == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=export.csv'
            writer = csv.writer(response)
        else:
            if export == 'txt':
                response = HttpResponse(content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=export.txt'
                writer = csv.writer(response, delimiter='\t', quoting=(csv.QUOTE_NONE))
        writer.writerow(['Individual', 'Index', 'Pos_index', 'Chr', 'Pos', 'Variant_id', 'Ref', 'Alt', 'Qual', 'Filter', 'Info', 'Format', 'Genotype_col', 'Genotype', 'Read_depth', 'Gene', 'Mutation_type', 'Vartype', 'Genomes1k_maf', 'Dbsnp_maf', 'Esp_maf', 'Dbsnp_build', 'Sift', 'Sift_pred', 'Polyphen2', 'Polyphen2_pred', 'Condel', 'Condel_pred', 'DANN', 'CADD', 'Is_at_omim', 'Is_at_hgmd', 'Hgmd_entries', 'Effect', 'Impact', 'Func_class', 'Codon_change', 'Aa_change', 'Aa_len', 'Gene_name', 'Biotype', 'Gene_coding', 'Transcript_id', 'Exon_rank', 'Genotype_number', 'Allele', 'Gene', 'Feature', 'Feature_type', 'Consequence', 'Cdna_position', 'Cds_position', 'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation', 'Distance', 'Strand', 'Symbol', 'Symbol_source', 'Sift', 'Polyphen', 'Condel'])
        for variant in variants:
            writer.writerow([variant.individual, variant.index, variant.pos_index, variant.chr, variant.pos, variant.variant_id, variant.ref, variant.alt, variant.qual, variant.filter, pickle.loads(variant.info), variant.format, variant.genotype_col, variant.genotype, variant.read_depth, variant.gene, variant.mutation_type, variant.vartype, variant.genomes1k_maf, variant.dbsnp_maf, variant.esp_maf, variant.dbsnp_build, variant.sift, variant.sift_pred, variant.polyphen2, variant.polyphen2_pred, variant.condel, variant.condel_pred, variant.dann, variant.cadd, variant.is_at_omim, variant.is_at_hgmd, variant.hgmd_entries])

        return response