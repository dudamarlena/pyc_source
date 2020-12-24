# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/BioClients/lincs/cmap_query.py
# Compiled at: 2020-03-30 12:51:55
# Size of source mod 2**32: 15449 bytes
import sys, os, re, argparse, json, logging, yaml, urllib.parse
from ..util import rest_utils
N_CHUNK = 200

def ListDatatypes(base_url, params):
    headers = {'Accept':'application/json', 
     'user_key':params['user_key']}
    url = base_url + '/dataTypes'
    response = rest_utils.GetURL(url, headers=headers, parse_json=True)
    logging.debug(json.dumps(response, indent=2))


def ListDatasets(base_url, params):
    headers = {'Accept':'application/json', 
     'user_key':params['user_key']}
    url = base_url + '/datasets'
    response = rest_utils.GetURL(url, headers=headers, parse_json=True)
    logging.debug(json.dumps(response, indent=2))


def ListPerturbagenClasses(base_url, params, fout):
    headers = {'user_key': params['user_key']}
    url = base_url + '/pcls'
    pcls = rest_utils.GetURL(url, headers=headers, parse_json=True)
    tags = None
    n_pcl = 0
    for pcl in pcls:
        n_pcl += 1
        if not tags:
            tags = pcl.keys()
            fout.write('\t'.join(tags) + '\n')
        vals = []
        for tag in tags:
            if tag not in pcl:
                vals.append('')
            else:
                vals.append(str(pcl[tag]))
        else:
            fout.write('\t'.join(vals) + '\n')

    else:
        logging.info('pcls: %d' % n_pcl)


def GetGenes(base_url, params, ids, id_type, fout):
    url_base = base_url + '/genes?user_key=' + params['user_key']
    tags = None
    n_gene = 0
    for id_this in ids:
        n_gene_this = 0
        logging.info('id: %s' % id_this)
        i_chunk = 0
        while True:
            qry = '{"where":{"%s":"%s"},"skip":%d,"limit":%d}' % (
             id_type, urllib.parse.quote(id_this), i_chunk * N_CHUNK, N_CHUNK)
            url = url_base + '&filter=%s' % qry
            try:
                genes = rest_utils.GetURL(url, parse_json=True)
            except:
                break
            else:
                if not genes:
                    break
            for gene in genes:
                n_gene_this += 1
                if not tags:
                    tags = gene.keys()
                    fout.write('\t'.join(tags) + '\n')
                vals = []
                for tag in tags:
                    if tag not in gene:
                        vals.append('')
                    elif type(gene[tag]) in (list, tuple):
                        vals.append(';'.join([str(x) for x in gene[tag]]))
                    else:
                        vals.append(str(gene[tag]))
                else:
                    fout.write('\t'.join(vals) + '\n')

            else:
                i_chunk += 1

        logging.info('\tgenes: %d' % n_gene_this)
        n_gene += n_gene_this
    else:
        logging.info('genes: %d' % n_gene)


def ListGenes_Landmark(base_url, params, fout):
    GetGenes(base_url, params, ['landmark'], 'l1000_type', fout)


def ListGenes(base_url, params, fout):
    GetGenes(base_url, params, ['landmark', 'inferred', 'best inferred', 'not inferred'], 'l1000_type', fout)


def GetPerturbagens--- This code section failed: ---

 L. 114         0  LOAD_STR                 'application/json'
                2  LOAD_FAST                'params'
                4  LOAD_STR                 'user_key'
                6  BINARY_SUBSCR    
                8  LOAD_CONST               ('Accept', 'user_key')
               10  BUILD_CONST_KEY_MAP_2     2 
               12  STORE_FAST               'headers'

 L. 115        14  LOAD_FAST                'base_url'
               16  LOAD_STR                 '/perts'
               18  BINARY_ADD       
               20  STORE_FAST               'url_base'

 L. 116        22  LOAD_CONST               None
               24  STORE_FAST               'tags'

 L. 117        26  LOAD_STR                 'pert_id'
               28  LOAD_STR                 'pert_iname'
               30  LOAD_STR                 'pert_type'
               32  LOAD_STR                 'pert_vendor'
               34  LOAD_STR                 'pert_url'
               36  LOAD_STR                 'id'
               38  LOAD_STR                 'pubchem_cid'
               40  LOAD_STR                 'entrez_geneId'
               42  LOAD_STR                 'vector_id'
               44  LOAD_STR                 'clone_name'
               46  LOAD_STR                 'oligo_seq'
               48  LOAD_STR                 'description'
               50  LOAD_STR                 'target'
               52  LOAD_STR                 'structure_url'
               54  LOAD_STR                 'moa'
               56  LOAD_STR                 'pcl_membership'
               58  LOAD_STR                 'tas'
               60  LOAD_STR                 'num_sig'
               62  LOAD_STR                 'status'
               64  BUILD_LIST_19        19 
               66  STORE_FAST               'fields'

 L. 118        68  LOAD_CONST               0
               70  STORE_FAST               'n_pert'

 L. 119        72  LOAD_FAST                'ids'
               74  GET_ITER         
            76_78  FOR_ITER            444  'to 444'
               80  STORE_FAST               'id_this'

 L. 120        82  LOAD_CONST               0
               84  STORE_FAST               'n_pert_this'

 L. 121        86  LOAD_GLOBAL              logging
               88  LOAD_METHOD              info
               90  LOAD_STR                 'id: %s'
               92  LOAD_FAST                'id_this'
               94  BINARY_MODULO    
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 122       100  LOAD_CONST               0
              102  STORE_FAST               'i_chunk'

 L. 124       104  LOAD_STR                 '{"where":{"%s":"%s"},"fields":[%s],"skip":%d,"limit":%d}'

 L. 125       106  LOAD_FAST                'id_type'

 L. 125       108  LOAD_GLOBAL              urllib
              110  LOAD_ATTR                parse
              112  LOAD_METHOD              quote
              114  LOAD_FAST                'id_this'
              116  CALL_METHOD_1         1  ''

 L. 126       118  LOAD_STR                 ','
              120  LOAD_METHOD              join
              122  LOAD_LISTCOMP            '<code_object <listcomp>>'
              124  LOAD_STR                 'GetPerturbagens.<locals>.<listcomp>'
              126  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              128  LOAD_FAST                'fields'
              130  GET_ITER         
              132  CALL_FUNCTION_1       1  ''
              134  CALL_METHOD_1         1  ''

 L. 127       136  LOAD_FAST                'i_chunk'
              138  LOAD_GLOBAL              N_CHUNK
              140  BINARY_MULTIPLY  

 L. 127       142  LOAD_GLOBAL              N_CHUNK

 L. 124       144  BUILD_TUPLE_5         5 
              146  BINARY_MODULO    
              148  STORE_FAST               'qry'

 L. 128       150  LOAD_FAST                'url_base'
              152  LOAD_STR                 '?filter=%s'
              154  LOAD_FAST                'qry'
              156  BINARY_MODULO    
              158  BINARY_ADD       
              160  STORE_FAST               'url'

 L. 129       162  SETUP_FINALLY       184  'to 184'

 L. 130       164  LOAD_GLOBAL              rest_utils
              166  LOAD_ATTR                GetURL
              168  LOAD_FAST                'url'
              170  LOAD_FAST                'headers'
              172  LOAD_CONST               True
              174  LOAD_CONST               ('headers', 'parse_json')
              176  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              178  STORE_FAST               'perts'
              180  POP_BLOCK        
              182  JUMP_FORWARD        200  'to 200'
            184_0  COME_FROM_FINALLY   162  '162'

 L. 131       184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 132       190  POP_EXCEPT       
              192  JUMP_BACK           104  'to 104'
              194  POP_EXCEPT       
              196  JUMP_FORWARD        200  'to 200'
              198  END_FINALLY      
            200_0  COME_FROM           196  '196'
            200_1  COME_FROM           182  '182'

 L. 133       200  LOAD_FAST                'perts'
              202  POP_JUMP_IF_TRUE    208  'to 208'

 L. 134   204_206  BREAK_LOOP          420  'to 420'
            208_0  COME_FROM           202  '202'

 L. 135       208  LOAD_GLOBAL              logging
              210  LOAD_METHOD              debug
              212  LOAD_GLOBAL              json
              214  LOAD_ATTR                dumps
              216  LOAD_FAST                'perts'
              218  LOAD_CONST               2
              220  LOAD_CONST               ('indent',)
              222  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          

 L. 136       228  LOAD_FAST                'perts'
              230  GET_ITER         
              232  FOR_ITER            410  'to 410'
              234  STORE_FAST               'pert'

 L. 137       236  LOAD_FAST                'n_pert_this'
              238  LOAD_CONST               1
              240  INPLACE_ADD      
              242  STORE_FAST               'n_pert_this'

 L. 138       244  LOAD_FAST                'tags'
          246_248  POP_JUMP_IF_TRUE    278  'to 278'

 L. 139       250  LOAD_FAST                'pert'
              252  LOAD_METHOD              keys
              254  CALL_METHOD_0         0  ''
              256  STORE_FAST               'tags'

 L. 140       258  LOAD_FAST                'fout'
              260  LOAD_METHOD              write
              262  LOAD_STR                 '\t'
              264  LOAD_METHOD              join
              266  LOAD_FAST                'tags'
              268  CALL_METHOD_1         1  ''
              270  LOAD_STR                 '\n'
              272  BINARY_ADD       
              274  CALL_METHOD_1         1  ''
              276  POP_TOP          
            278_0  COME_FROM           246  '246'

 L. 141       278  BUILD_LIST_0          0 
              280  STORE_FAST               'vals'

 L. 142       282  LOAD_FAST                'tags'
              284  GET_ITER         
              286  FOR_ITER            388  'to 388'
              288  STORE_FAST               'tag'

 L. 143       290  LOAD_FAST                'tag'
              292  LOAD_FAST                'pert'
              294  COMPARE_OP               not-in
          296_298  POP_JUMP_IF_FALSE   312  'to 312'

 L. 144       300  LOAD_FAST                'vals'
              302  LOAD_METHOD              append
              304  LOAD_STR                 ''
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          
              310  JUMP_BACK           286  'to 286'
            312_0  COME_FROM           296  '296'

 L. 145       312  LOAD_GLOBAL              type
              314  LOAD_FAST                'pert'
              316  LOAD_FAST                'tag'
              318  BINARY_SUBSCR    
              320  CALL_FUNCTION_1       1  ''
              322  LOAD_GLOBAL              list
              324  LOAD_GLOBAL              tuple
              326  BUILD_TUPLE_2         2 
              328  COMPARE_OP               in
          330_332  POP_JUMP_IF_FALSE   366  'to 366'

 L. 146       334  LOAD_FAST                'vals'
              336  LOAD_METHOD              append
              338  LOAD_STR                 ';'
              340  LOAD_METHOD              join
              342  LOAD_LISTCOMP            '<code_object <listcomp>>'
              344  LOAD_STR                 'GetPerturbagens.<locals>.<listcomp>'
              346  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              348  LOAD_FAST                'pert'
              350  LOAD_FAST                'tag'
              352  BINARY_SUBSCR    
              354  GET_ITER         
              356  CALL_FUNCTION_1       1  ''
              358  CALL_METHOD_1         1  ''
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          
              364  JUMP_BACK           286  'to 286'
            366_0  COME_FROM           330  '330'

 L. 148       366  LOAD_FAST                'vals'
              368  LOAD_METHOD              append
              370  LOAD_GLOBAL              str
              372  LOAD_FAST                'pert'
              374  LOAD_FAST                'tag'
              376  BINARY_SUBSCR    
              378  CALL_FUNCTION_1       1  ''
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          
          384_386  JUMP_BACK           286  'to 286'

 L. 149       388  LOAD_FAST                'fout'
              390  LOAD_METHOD              write
              392  LOAD_STR                 '\t'
              394  LOAD_METHOD              join
              396  LOAD_FAST                'vals'
              398  CALL_METHOD_1         1  ''
              400  LOAD_STR                 '\n'
              402  BINARY_ADD       
              404  CALL_METHOD_1         1  ''
              406  POP_TOP          
              408  JUMP_BACK           232  'to 232'

 L. 150       410  LOAD_FAST                'i_chunk'
              412  LOAD_CONST               1
              414  INPLACE_ADD      
              416  STORE_FAST               'i_chunk'
              418  JUMP_BACK           104  'to 104'

 L. 151       420  LOAD_GLOBAL              logging
              422  LOAD_METHOD              info
              424  LOAD_STR                 '\tperturbagens: %d'
              426  LOAD_FAST                'n_pert_this'
              428  BINARY_MODULO    
              430  CALL_METHOD_1         1  ''
              432  POP_TOP          

 L. 152       434  LOAD_FAST                'n_pert'
              436  LOAD_FAST                'n_pert_this'
              438  INPLACE_ADD      
              440  STORE_FAST               'n_pert'
              442  JUMP_BACK            76  'to 76'

 L. 153       444  LOAD_GLOBAL              logging
              446  LOAD_METHOD              info
              448  LOAD_STR                 'perturbagens: %d'
              450  LOAD_FAST                'n_pert'
              452  BINARY_MODULO    
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 194


def ListPerturbagens(base_url, params, fout):
    pert_types = [
     'trt_cp', 'trt_lig', 'trt_sh', 'trt_sh.cgs', 'trt_oe', 'trt_oe.mut', 'trt_xpr', 'trt_sh.css', 'ctl_vehicle.cns', 'ctl_vehicle', 'ctl_vector', 'ctl_vector.cns', 'ctl_untrt.cns', 'ctl_untrt']
    GetPerturbagens(base_url, params, pert_types, 'pert_type', fout)


def ListDrugs--- This code section failed: ---

 L. 162         0  LOAD_STR                 'application/json'
                2  LOAD_FAST                'params'
                4  LOAD_STR                 'user_key'
                6  BINARY_SUBSCR    
                8  LOAD_CONST               ('Accept', 'user_key')
               10  BUILD_CONST_KEY_MAP_2     2 
               12  STORE_FAST               'headers'

 L. 163        14  LOAD_FAST                'base_url'
               16  LOAD_STR                 '/rep_drugs'
               18  BINARY_ADD       
               20  STORE_FAST               'url_base'

 L. 164        22  LOAD_CONST               None
               24  STORE_FAST               'tags'

 L. 165        26  LOAD_CONST               0
               28  STORE_FAST               'n_drug'

 L. 165        30  LOAD_CONST               0
               32  STORE_FAST               'i_chunk'

 L. 167        34  LOAD_STR                 '{"skip":%d,"limit":%d}'
               36  LOAD_FAST                'i_chunk'
               38  LOAD_GLOBAL              N_CHUNK
               40  BINARY_MULTIPLY  
               42  LOAD_GLOBAL              N_CHUNK
               44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  STORE_FAST               'qry'

 L. 168        50  LOAD_FAST                'url_base'
               52  LOAD_STR                 '?filter=%s'
               54  LOAD_FAST                'qry'
               56  BINARY_MODULO    
               58  BINARY_ADD       
               60  STORE_FAST               'url'

 L. 169        62  SETUP_FINALLY        84  'to 84'

 L. 170        64  LOAD_GLOBAL              rest_utils
               66  LOAD_ATTR                GetURL
               68  LOAD_FAST                'url'
               70  LOAD_FAST                'headers'
               72  LOAD_CONST               True
               74  LOAD_CONST               ('headers', 'parse_json')
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               'drugs'
               80  POP_BLOCK        
               82  JUMP_FORWARD        140  'to 140'
             84_0  COME_FROM_FINALLY    62  '62'

 L. 171        84  DUP_TOP          
               86  LOAD_GLOBAL              Exception
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   138  'to 138'
               92  POP_TOP          
               94  STORE_FAST               'e'
               96  POP_TOP          
               98  SETUP_FINALLY       126  'to 126'

 L. 172       100  LOAD_GLOBAL              logging
              102  LOAD_METHOD              error
              104  LOAD_STR                 'Exception: %s'
              106  LOAD_FAST                'e'
              108  BINARY_MODULO    
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 173       114  POP_BLOCK        
              116  POP_EXCEPT       
              118  CALL_FINALLY        126  'to 126'
              120  JUMP_BACK            34  'to 34'
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM           118  '118'
            126_1  COME_FROM_FINALLY    98  '98'
              126  LOAD_CONST               None
              128  STORE_FAST               'e'
              130  DELETE_FAST              'e'
              132  END_FINALLY      
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM            90  '90'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM            82  '82'

 L. 174       140  LOAD_FAST                'drugs'
              142  POP_JUMP_IF_TRUE    148  'to 148'

 L. 175   144_146  BREAK_LOOP          334  'to 334'
            148_0  COME_FROM           142  '142'

 L. 176       148  LOAD_FAST                'drugs'
              150  GET_ITER         
              152  FOR_ITER            324  'to 324'
              154  STORE_FAST               'drug'

 L. 177       156  LOAD_FAST                'n_drug'
              158  LOAD_CONST               1
              160  INPLACE_ADD      
              162  STORE_FAST               'n_drug'

 L. 178       164  LOAD_FAST                'tags'
              166  POP_JUMP_IF_TRUE    196  'to 196'

 L. 179       168  LOAD_FAST                'drug'
              170  LOAD_METHOD              keys
              172  CALL_METHOD_0         0  ''
              174  STORE_FAST               'tags'

 L. 180       176  LOAD_FAST                'fout'
              178  LOAD_METHOD              write
              180  LOAD_STR                 '\t'
              182  LOAD_METHOD              join
              184  LOAD_FAST                'tags'
              186  CALL_METHOD_1         1  ''
              188  LOAD_STR                 '\n'
              190  BINARY_ADD       
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
            196_0  COME_FROM           166  '166'

 L. 181       196  BUILD_LIST_0          0 
              198  STORE_FAST               'vals'

 L. 182       200  LOAD_FAST                'tags'
              202  GET_ITER         
              204  FOR_ITER            302  'to 302'
              206  STORE_FAST               'tag'

 L. 183       208  LOAD_FAST                'tag'
              210  LOAD_FAST                'drug'
              212  COMPARE_OP               not-in
              214  POP_JUMP_IF_FALSE   228  'to 228'

 L. 184       216  LOAD_FAST                'vals'
              218  LOAD_METHOD              append
              220  LOAD_STR                 ''
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
              226  JUMP_BACK           204  'to 204'
            228_0  COME_FROM           214  '214'

 L. 185       228  LOAD_GLOBAL              type
              230  LOAD_FAST                'drug'
              232  LOAD_FAST                'tag'
              234  BINARY_SUBSCR    
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_GLOBAL              list
              240  LOAD_GLOBAL              tuple
              242  BUILD_TUPLE_2         2 
              244  COMPARE_OP               in
          246_248  POP_JUMP_IF_FALSE   282  'to 282'

 L. 186       250  LOAD_FAST                'vals'
              252  LOAD_METHOD              append
              254  LOAD_STR                 ';'
              256  LOAD_METHOD              join
              258  LOAD_LISTCOMP            '<code_object <listcomp>>'
              260  LOAD_STR                 'ListDrugs.<locals>.<listcomp>'
              262  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              264  LOAD_FAST                'drug'
              266  LOAD_FAST                'tag'
              268  BINARY_SUBSCR    
              270  GET_ITER         
              272  CALL_FUNCTION_1       1  ''
              274  CALL_METHOD_1         1  ''
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
              280  JUMP_BACK           204  'to 204'
            282_0  COME_FROM           246  '246'

 L. 188       282  LOAD_FAST                'vals'
              284  LOAD_METHOD              append
              286  LOAD_GLOBAL              str
              288  LOAD_FAST                'drug'
              290  LOAD_FAST                'tag'
              292  BINARY_SUBSCR    
              294  CALL_FUNCTION_1       1  ''
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
              300  JUMP_BACK           204  'to 204'

 L. 189       302  LOAD_FAST                'fout'
              304  LOAD_METHOD              write
              306  LOAD_STR                 '\t'
              308  LOAD_METHOD              join
              310  LOAD_FAST                'vals'
              312  CALL_METHOD_1         1  ''
              314  LOAD_STR                 '\n'
              316  BINARY_ADD       
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          
              322  JUMP_BACK           152  'to 152'

 L. 190       324  LOAD_FAST                'i_chunk'
              326  LOAD_CONST               1
              328  INPLACE_ADD      
              330  STORE_FAST               'i_chunk'
              332  JUMP_BACK            34  'to 34'

 L. 191       334  LOAD_GLOBAL              logging
              336  LOAD_METHOD              info
              338  LOAD_STR                 'drugs: %d'
              340  LOAD_FAST                'n_drug'
              342  BINARY_MODULO    
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 118


def GetCells(base_url, params, ids, id_type, fout):
    headers = {'Accept':'application/json', 
     'user_key':params['user_key']}
    url_base = base_url + '/cells'
    tags = None
    n_cell = 0
    for id_this in ids:
        n_cell_this = 0
        logging.info('id: %s' % id_this)
        i_chunk = 0
        while True:
            qry = '{"where":{"%s":"%s"},"skip":%d,"limit":%d}' % (
             id_type, urllib.parse.quote(id_this),
             i_chunk * N_CHUNK, N_CHUNK)
            url = url_base + '?filter=%s' % qry
            try:
                cells = rest_utils.GetURL(url, headers=headers, parse_json=True)
            except:
                break
            else:
                if not cells:
                    break
                logging.debug(json.dumps(cells, indent=2))
            for cell in cells:
                n_cell_this += 1
                if not tags:
                    tags = cell.keys()
                    fout.write('\t'.join(tags) + '\n')
                vals = []
                for tag in tags:
                    if tag not in cell:
                        vals.append('')
                    elif type(cell[tag]) in (list, tuple):
                        vals.append(';'.join([str(x) for x in cell[tag]]))
                    else:
                        vals.append(str(cell[tag]))
                else:
                    fout.write('\t'.join(vals) + '\n')

            else:
                i_chunk += 1

        logging.info('\tcells: %d' % n_cell_this)
        n_cell += n_cell_this
    else:
        logging.info('cells: %d' % n_cell)


def ListCells--- This code section failed: ---

 L. 237         0  LOAD_STR                 'application/json'
                2  LOAD_FAST                'params'
                4  LOAD_STR                 'user_key'
                6  BINARY_SUBSCR    
                8  LOAD_CONST               ('Accept', 'user_key')
               10  BUILD_CONST_KEY_MAP_2     2 
               12  STORE_FAST               'headers'

 L. 238        14  LOAD_FAST                'base_url'
               16  LOAD_STR                 '/cells'
               18  BINARY_ADD       
               20  STORE_FAST               'url_base'

 L. 239        22  LOAD_CONST               None
               24  STORE_FAST               'tags'

 L. 240        26  LOAD_CONST               0
               28  STORE_FAST               'n_cell'

 L. 240        30  LOAD_CONST               0
               32  STORE_FAST               'i_chunk'

 L. 242        34  LOAD_STR                 '{"skip":%d,"limit":%d}'
               36  LOAD_FAST                'i_chunk'
               38  LOAD_GLOBAL              N_CHUNK
               40  BINARY_MULTIPLY  
               42  LOAD_GLOBAL              N_CHUNK
               44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  STORE_FAST               'qry'

 L. 243        50  LOAD_FAST                'url_base'
               52  LOAD_STR                 '?filter=%s'
               54  LOAD_FAST                'qry'
               56  BINARY_MODULO    
               58  BINARY_ADD       
               60  STORE_FAST               'url'

 L. 244        62  SETUP_FINALLY        84  'to 84'

 L. 245        64  LOAD_GLOBAL              rest_utils
               66  LOAD_ATTR                GetURL
               68  LOAD_FAST                'url'
               70  LOAD_FAST                'headers'
               72  LOAD_CONST               True
               74  LOAD_CONST               ('headers', 'parse_json')
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               'cells'
               80  POP_BLOCK        
               82  JUMP_FORWARD        140  'to 140'
             84_0  COME_FROM_FINALLY    62  '62'

 L. 246        84  DUP_TOP          
               86  LOAD_GLOBAL              Exception
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   138  'to 138'
               92  POP_TOP          
               94  STORE_FAST               'e'
               96  POP_TOP          
               98  SETUP_FINALLY       126  'to 126'

 L. 247       100  LOAD_GLOBAL              logging
              102  LOAD_METHOD              error
              104  LOAD_STR                 'Exception: %s'
              106  LOAD_FAST                'e'
              108  BINARY_MODULO    
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 248       114  POP_BLOCK        
              116  POP_EXCEPT       
              118  CALL_FINALLY        126  'to 126'
              120  JUMP_BACK            34  'to 34'
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM           118  '118'
            126_1  COME_FROM_FINALLY    98  '98'
              126  LOAD_CONST               None
              128  STORE_FAST               'e'
              130  DELETE_FAST              'e'
              132  END_FINALLY      
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM            90  '90'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM            82  '82'

 L. 249       140  LOAD_FAST                'cells'
              142  POP_JUMP_IF_TRUE    148  'to 148'

 L. 250   144_146  BREAK_LOOP          334  'to 334'
            148_0  COME_FROM           142  '142'

 L. 251       148  LOAD_FAST                'cells'
              150  GET_ITER         
              152  FOR_ITER            324  'to 324'
              154  STORE_FAST               'cell'

 L. 252       156  LOAD_FAST                'n_cell'
              158  LOAD_CONST               1
              160  INPLACE_ADD      
              162  STORE_FAST               'n_cell'

 L. 253       164  LOAD_FAST                'tags'
              166  POP_JUMP_IF_TRUE    196  'to 196'

 L. 254       168  LOAD_FAST                'cell'
              170  LOAD_METHOD              keys
              172  CALL_METHOD_0         0  ''
              174  STORE_FAST               'tags'

 L. 255       176  LOAD_FAST                'fout'
              178  LOAD_METHOD              write
              180  LOAD_STR                 '\t'
              182  LOAD_METHOD              join
              184  LOAD_FAST                'tags'
              186  CALL_METHOD_1         1  ''
              188  LOAD_STR                 '\n'
              190  BINARY_ADD       
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
            196_0  COME_FROM           166  '166'

 L. 256       196  BUILD_LIST_0          0 
              198  STORE_FAST               'vals'

 L. 257       200  LOAD_FAST                'tags'
              202  GET_ITER         
              204  FOR_ITER            302  'to 302'
              206  STORE_FAST               'tag'

 L. 258       208  LOAD_FAST                'tag'
              210  LOAD_FAST                'cell'
              212  COMPARE_OP               not-in
              214  POP_JUMP_IF_FALSE   228  'to 228'

 L. 259       216  LOAD_FAST                'vals'
              218  LOAD_METHOD              append
              220  LOAD_STR                 ''
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
              226  JUMP_BACK           204  'to 204'
            228_0  COME_FROM           214  '214'

 L. 260       228  LOAD_GLOBAL              type
              230  LOAD_FAST                'cell'
              232  LOAD_FAST                'tag'
              234  BINARY_SUBSCR    
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_GLOBAL              list
              240  LOAD_GLOBAL              tuple
              242  BUILD_TUPLE_2         2 
              244  COMPARE_OP               in
          246_248  POP_JUMP_IF_FALSE   282  'to 282'

 L. 261       250  LOAD_FAST                'vals'
              252  LOAD_METHOD              append
              254  LOAD_STR                 ';'
              256  LOAD_METHOD              join
              258  LOAD_LISTCOMP            '<code_object <listcomp>>'
              260  LOAD_STR                 'ListCells.<locals>.<listcomp>'
              262  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              264  LOAD_FAST                'cell'
              266  LOAD_FAST                'tag'
              268  BINARY_SUBSCR    
              270  GET_ITER         
              272  CALL_FUNCTION_1       1  ''
              274  CALL_METHOD_1         1  ''
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
              280  JUMP_BACK           204  'to 204'
            282_0  COME_FROM           246  '246'

 L. 263       282  LOAD_FAST                'vals'
              284  LOAD_METHOD              append
              286  LOAD_GLOBAL              str
              288  LOAD_FAST                'cell'
              290  LOAD_FAST                'tag'
              292  BINARY_SUBSCR    
              294  CALL_FUNCTION_1       1  ''
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
              300  JUMP_BACK           204  'to 204'

 L. 264       302  LOAD_FAST                'fout'
              304  LOAD_METHOD              write
              306  LOAD_STR                 '\t'
              308  LOAD_METHOD              join
              310  LOAD_FAST                'vals'
              312  CALL_METHOD_1         1  ''
              314  LOAD_STR                 '\n'
              316  BINARY_ADD       
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          
              322  JUMP_BACK           152  'to 152'

 L. 265       324  LOAD_FAST                'i_chunk'
              326  LOAD_CONST               1
              328  INPLACE_ADD      
              330  STORE_FAST               'i_chunk'
              332  JUMP_BACK            34  'to 34'

 L. 266       334  LOAD_GLOBAL              logging
              336  LOAD_METHOD              info
              338  LOAD_STR                 'cells: %d'
              340  LOAD_FAST                'n_cell'
              342  BINARY_MODULO    
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 118


def CountSignatures(base_url, params, args):
    headers = {'Accept':'application/json', 
     'user_key':params['user_key']}
    url_base = base_url + '/sigs/count'
    url = url_base + '?where=%s' % args.clue_where
    try:
        sigs = rest_utils.GetURL(url, headers=headers, parse_json=True)
        logging.info('signatures: %d' % len(sigs))
    except Exception as e:
        try:
            logging.error('%s' % e)
        finally:
            e = None
            del e


def GetSignatures--- This code section failed: ---

 L. 281         0  LOAD_STR                 'pert_id'
                2  LOAD_STR                 'pert_iname'
                4  LOAD_STR                 'pert_desc'
                6  LOAD_STR                 'pert_dose'
                8  LOAD_STR                 'cell_id'
               10  LOAD_STR                 'provenance_code'
               12  LOAD_STR                 'target_seq'
               14  LOAD_STR                 'target_is_lm'
               16  LOAD_STR                 'target_is_bing'
               18  LOAD_STR                 'target_zs'
               20  LOAD_STR                 'dn100_bing'
               22  LOAD_STR                 'up100_bing'
               24  BUILD_LIST_12        12 
               26  STORE_FAST               'fields'

 L. 282        28  LOAD_STR                 'application/json'
               30  LOAD_FAST                'params'
               32  LOAD_STR                 'user_key'
               34  BINARY_SUBSCR    
               36  LOAD_CONST               ('Accept', 'user_key')
               38  BUILD_CONST_KEY_MAP_2     2 
               40  STORE_FAST               'headers'

 L. 283        42  LOAD_FAST                'base_url'
               44  LOAD_STR                 '/sigs'
               46  BINARY_ADD       
               48  STORE_FAST               'url_base'

 L. 284        50  LOAD_CONST               None
               52  STORE_FAST               'tags'

 L. 284        54  LOAD_CONST               0
               56  STORE_FAST               'n_sig'

 L. 284        58  LOAD_CONST               0
               60  STORE_FAST               'i_chunk'

 L. 286        62  LOAD_STR                 '{"where":%s,"fields":[%s],"skip":%d,"limit":%d}'

 L. 287        64  LOAD_FAST                'args'
               66  LOAD_ATTR                clue_where

 L. 287        68  LOAD_STR                 ','
               70  LOAD_METHOD              join
               72  LOAD_LISTCOMP            '<code_object <listcomp>>'
               74  LOAD_STR                 'GetSignatures.<locals>.<listcomp>'
               76  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               78  LOAD_FAST                'fields'
               80  GET_ITER         
               82  CALL_FUNCTION_1       1  ''
               84  CALL_METHOD_1         1  ''

 L. 288        86  LOAD_FAST                'args'
               88  LOAD_ATTR                skip
               90  LOAD_FAST                'i_chunk'
               92  LOAD_GLOBAL              N_CHUNK
               94  BINARY_MULTIPLY  
               96  BINARY_ADD       

 L. 288        98  LOAD_GLOBAL              N_CHUNK

 L. 286       100  BUILD_TUPLE_4         4 
              102  BINARY_MODULO    
              104  STORE_FAST               'qry'

 L. 289       106  LOAD_FAST                'url_base'
              108  LOAD_STR                 '?filter=%s'
              110  LOAD_FAST                'qry'
              112  BINARY_MODULO    
              114  BINARY_ADD       
              116  STORE_FAST               'url'

 L. 290       118  SETUP_FINALLY       140  'to 140'

 L. 291       120  LOAD_GLOBAL              rest_utils
              122  LOAD_ATTR                GetURL
              124  LOAD_FAST                'url'
              126  LOAD_FAST                'headers'
              128  LOAD_CONST               True
              130  LOAD_CONST               ('headers', 'parse_json')
              132  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              134  STORE_FAST               'sigs'
              136  POP_BLOCK        
              138  JUMP_FORWARD        156  'to 156'
            140_0  COME_FROM_FINALLY   118  '118'

 L. 292       140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 293       146  POP_EXCEPT       
              148  JUMP_BACK            62  'to 62'
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
              154  END_FINALLY      
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           138  '138'

 L. 294       156  LOAD_FAST                'sigs'
              158  POP_JUMP_IF_TRUE    164  'to 164'

 L. 295   160_162  BREAK_LOOP          404  'to 404'
            164_0  COME_FROM           158  '158'

 L. 296       164  LOAD_GLOBAL              logging
              166  LOAD_METHOD              debug
              168  LOAD_GLOBAL              json
              170  LOAD_ATTR                dumps
              172  LOAD_FAST                'sigs'
              174  LOAD_CONST               2
              176  LOAD_CONST               ('indent',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 297       184  LOAD_FAST                'sigs'
              186  GET_ITER         
            188_0  COME_FROM           368  '368'
              188  FOR_ITER            378  'to 378'
              190  STORE_FAST               'sig'

 L. 298       192  LOAD_FAST                'n_sig'
              194  LOAD_CONST               1
              196  INPLACE_ADD      
              198  STORE_FAST               'n_sig'

 L. 299       200  LOAD_FAST                'tags'
              202  POP_JUMP_IF_TRUE    232  'to 232'

 L. 300       204  LOAD_FAST                'sig'
              206  LOAD_METHOD              keys
              208  CALL_METHOD_0         0  ''
              210  STORE_FAST               'tags'

 L. 301       212  LOAD_FAST                'fout'
              214  LOAD_METHOD              write
              216  LOAD_STR                 '\t'
              218  LOAD_METHOD              join
              220  LOAD_FAST                'tags'
              222  CALL_METHOD_1         1  ''
              224  LOAD_STR                 '\n'
              226  BINARY_ADD       
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
            232_0  COME_FROM           202  '202'

 L. 302       232  BUILD_LIST_0          0 
              234  STORE_FAST               'vals'

 L. 303       236  LOAD_FAST                'tags'
              238  GET_ITER         
              240  FOR_ITER            340  'to 340'
              242  STORE_FAST               'tag'

 L. 304       244  LOAD_FAST                'tag'
              246  LOAD_FAST                'sig'
              248  COMPARE_OP               not-in
          250_252  POP_JUMP_IF_FALSE   266  'to 266'

 L. 305       254  LOAD_FAST                'vals'
              256  LOAD_METHOD              append
              258  LOAD_STR                 ''
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
              264  JUMP_BACK           240  'to 240'
            266_0  COME_FROM           250  '250'

 L. 306       266  LOAD_GLOBAL              type
              268  LOAD_FAST                'sig'
              270  LOAD_FAST                'tag'
              272  BINARY_SUBSCR    
              274  CALL_FUNCTION_1       1  ''
              276  LOAD_GLOBAL              list
              278  LOAD_GLOBAL              tuple
              280  BUILD_TUPLE_2         2 
              282  COMPARE_OP               in
          284_286  POP_JUMP_IF_FALSE   320  'to 320'

 L. 307       288  LOAD_FAST                'vals'
              290  LOAD_METHOD              append
              292  LOAD_STR                 ';'
              294  LOAD_METHOD              join
              296  LOAD_LISTCOMP            '<code_object <listcomp>>'
              298  LOAD_STR                 'GetSignatures.<locals>.<listcomp>'
              300  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              302  LOAD_FAST                'sig'
              304  LOAD_FAST                'tag'
              306  BINARY_SUBSCR    
              308  GET_ITER         
              310  CALL_FUNCTION_1       1  ''
              312  CALL_METHOD_1         1  ''
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          
              318  JUMP_BACK           240  'to 240'
            320_0  COME_FROM           284  '284'

 L. 309       320  LOAD_FAST                'vals'
              322  LOAD_METHOD              append
              324  LOAD_GLOBAL              str
              326  LOAD_FAST                'sig'
              328  LOAD_FAST                'tag'
              330  BINARY_SUBSCR    
              332  CALL_FUNCTION_1       1  ''
              334  CALL_METHOD_1         1  ''
              336  POP_TOP          
              338  JUMP_BACK           240  'to 240'

 L. 310       340  LOAD_FAST                'fout'
              342  LOAD_METHOD              write
              344  LOAD_STR                 '\t'
              346  LOAD_METHOD              join
              348  LOAD_FAST                'vals'
              350  CALL_METHOD_1         1  ''
              352  LOAD_STR                 '\n'
              354  BINARY_ADD       
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          

 L. 311       360  LOAD_FAST                'n_sig'
              362  LOAD_FAST                'args'
              364  LOAD_ATTR                nmax
              366  COMPARE_OP               >=
              368  POP_JUMP_IF_FALSE   188  'to 188'

 L. 311       370  POP_TOP          
          372_374  BREAK_LOOP          378  'to 378'
              376  JUMP_BACK           188  'to 188'

 L. 312       378  LOAD_FAST                'n_sig'
              380  LOAD_FAST                'args'
              382  LOAD_ATTR                nmax
              384  COMPARE_OP               >=
          386_388  POP_JUMP_IF_FALSE   394  'to 394'

 L. 312   390_392  BREAK_LOOP          404  'to 404'
            394_0  COME_FROM           386  '386'

 L. 313       394  LOAD_FAST                'i_chunk'
              396  LOAD_CONST               1
              398  INPLACE_ADD      
              400  STORE_FAST               'i_chunk'
              402  JUMP_BACK            62  'to 62'

 L. 314       404  LOAD_GLOBAL              logging
              406  LOAD_METHOD              info
              408  LOAD_STR                 'signatures: %d'
              410  LOAD_FAST                'n_sig'
              412  BINARY_MODULO    
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 150


if __name__ == '__main__':
    API_HOST = 'api.clue.io'
    API_BASE_PATH = '/api'
    epilog = 'CMap is the project; Clue is the platform.\nhttps://clue.io/api. \nCredentials config file should be at $HOME/.clueapi.yaml.\n'
    parser = argparse.ArgumentParser(description='CLUE.IO REST API client utility', epilog=epilog)
    ops = ['getGenes', 'listGenes', 'listGenes_landmark',
     'getPerturbagens', 'listPerturbagens', 'listDrugs',
     'countSignatures', 'getSignatures',
     'getCells', 'listCells',
     'listPerturbagenClasses',
     'listDatasets', 'listDatatypes',
     'search']
    id_types = ['cell_id', 'pert_id', 'gene_symbol', 'entrez_id']
    parser.add_argument('op', choices=ops, help='operation')
    parser.add_argument('--ids', help='IDs, comma-separated')
    parser.add_argument('--i', dest='ifile', help='input file, IDs')
    parser.add_argument('--o', dest='ofile', help='output (TSV)')
    parser.add_argument('--id_type', choices=id_types, help='query ID or field type, e.g. gene_symbol')
    parser.add_argument('--clue_where', help='Clue API search where, e.g. \'{"pert_desc":"sirolimus","cell_id":"MCF7"}\'')
    parser.add_argument('--nmax', type=int, default=1000, help='max results')
    parser.add_argument('--skip', type=int, default=0, help='skip results')
    parser.add_argument('--api_host', default=API_HOST)
    parser.add_argument('--api_base_path', default=API_BASE_PATH)
    parser.add_argument('--param_file', default=(os.environ['HOME'] + '/.clueapi.yaml'))
    parser.add_argument('-v', '--verbose', dest='verbose', action='count', default=0)
    args = parser.parse_args()
    with open(args.param_file, 'r') as (fh):
        params = {}
        for param in yaml.load_all(fh, Loader=(yaml.BaseLoader)):
            for k, v in param.items():
                params[k] = v

    logging.basicConfig(format='%(levelname)s:%(message)s', level=(logging.DEBUG if args.verbose > 1 else logging.INFO))
    base_url = 'https://' + args.api_host + args.api_base_path
    if args.ofile:
        fout = open(args.ofile, 'w+')
        fout or parser.error('Cannot open: %s' % args.ofile)
    else:
        fout = sys.stdout
    if args.ifile:
        fin = open(args.ifile)
        if not fin:
            parser.error('Cannot open: %s' % args.ifile)
        ids = []
        while True:
            line = fin.readline()
            if not line:
                break
            ids.append(line.rstrip())

        fin.close()
        logging.info('input queries: %d' % len(ids))
    else:
        if args.ids:
            ids = re.split('[, ]+', args.ids.strip())
        elif args.op == 'getGenes':
            if not ids:
                parser.error('--ids or --i required.')
            GetGenes(base_url, params, ids, args.id_type, fout)
        else:
            if args.op == 'listGenes':
                ListGenes(base_url, params, fout)
            else:
                if args.op == 'listGenes_landmark':
                    ListGenes_Landmark(base_url, params, fout)
                else:
                    if args.op == 'getPerturbagens':
                        if not ids:
                            parser.error('--ids or --i required.')
                        GetPerturbagens(base_url, params, ids, args.id_type, fout)
                    else:
                        if args.op == 'listPerturbagens':
                            ListPerturbagens(base_url, params, fout)
                        else:
                            if args.op == 'listDrugs':
                                ListDrugs(base_url, params, fout)
                            else:
                                if args.op == 'getCells':
                                    if not ids:
                                        parser.error('--ids or --i required.')
                                    GetCells(base_url, params, ids, args.id_type, fout)
                                else:
                                    if args.op == 'listCells':
                                        ListCells(base_url, params, fout)
                                    else:
                                        if args.op == 'getSignatures':
                                            if not args.clue_where:
                                                parser.error('--clue_where required.')
                                            GetSignatures(base_url, params, args, fout)
                                        else:
                                            if args.op == 'countSignatures':
                                                if not args.clue_where:
                                                    parser.error('--clue_where required.')
                                                CountSignatures(base_url, params, args)
                                            else:
                                                if args.op == 'listDatasets':
                                                    ListDatasets(base_url, params)
                                                else:
                                                    if args.op == 'listDatatypes':
                                                        ListDatatypes(base_url, params)
                                                    else:
                                                        if args.op == 'listPerturbagenClasses':
                                                            ListPerturbagenClasses(base_url, params, fout)
                                                        else:
                                                            parser.error('Unsupported operation: %s' % args.op)
                                                            parser.print_help()