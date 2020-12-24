# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/controller/ajax.py
# Compiled at: 2019-09-26 11:32:58
# Size of source mod 2**32: 6907 bytes
from ..main import application
from .helper import load_pipe

@application.route('/pipeline/<storage>/<name>/outer_fold/<outer_fold>/config/<config_index>/inner_fold/<inner_fold>/load')
def load_tested_config_for_inner_fold(storage, name, outer_fold, config_index, inner_fold):
    pipe = load_pipe(storage, name)
    config_index = int(config_index)
    outer_fold_index = int(int(outer_fold) - 1)
    inner_fold_index = int(int(inner_fold) - 1)
    inner_fold_object = pipe.outer_folds[outer_fold_index].tested_config_list[config_index].inner_folds[inner_fold_index]
    train_y_prediction = ','.join(map(str, inner_fold_object.training.y_pred))
    train_x_prediction = ','.join(map(str, list(range(1, len(inner_fold_object.training.y_pred)))))
    train_y_true = ','.join(map(str, inner_fold_object.training.y_true))
    train_x_true = ','.join(map(str, list(range(1, len(inner_fold_object.training.y_true)))))
    val_y_prediction = ','.join(map(str, inner_fold_object.training.y_pred))
    val_x_prediction = ','.join(map(str, list(range(1, len(inner_fold_object.training.y_pred)))))
    val_y_true = ','.join(map(str, inner_fold_object.training.y_true))
    val_x_true = ','.join(map(str, list(range(1, len(inner_fold_object.training.y_true)))))
    result = "<div class='tab-pane' id='config_" + str(config_index) + '_fold_' + str(inner_fold) + "'>"
    result += "<div class='row'>"
    result += "<div class='col-md-12'><div id='config_" + str(config_index) + '_fold_' + str(inner_fold) + "_training'></div>"
    result += '<script>'
    result += 'var trace1 = {x: [' + train_x_true + '],'
    result += 'y: [' + train_y_true + '],'
    result += " name: 'true',"
    result += " mode: 'markers'};"
    result += 'var trace2 = {'
    result += 'x: [' + train_x_prediction + '],'
    result += 'y: [' + train_y_prediction + '],'
    result += " name: 'prediction',"
    result += " mode: 'markers'};"
    result += 'var data = [ trace1, trace2 ];'
    result += "var layout = {title:'True/Predict for training set', width: 1600};"
    result += "Plotly.newPlot('config_" + str(config_index) + '_fold_' + str(inner_fold) + "_training', data, layout);"
    result += '</script></div>'
    result += "<div class='col-md-12'><div id='config_" + str(config_index) + '_fold_' + str(inner_fold) + "_validation'></div>"
    result += '<script>'
    result += 'var trace1 = {x: [' + val_x_true + '],'
    result += 'y: [' + val_y_true + '],'
    result += " name: 'true',"
    result += " mode: 'markers'};"
    result += 'var trace2 = {'
    result += 'x: [' + val_x_prediction + '],'
    result += 'y: [' + val_y_prediction + '],'
    result += " name: 'prediction',"
    result += " mode: 'markers'};"
    result += 'var data = [ trace1, trace2 ];'
    result += "var layout = {title:'True/Predict for validation set', width: 1600};"
    result += "Plotly.newPlot('config_" + str(config_index) + '_fold_' + str(inner_fold) + "_validation', data, layout);"
    result += '</script></div>'
    result += '</div>'
    result += '</div>'
    return result


@application.route('/pipeline/<storage>/<name>/outer_fold/<outer_fold>/config/<config_index>/load')
def load_inner_fold_data_for_config--- This code section failed: ---

 L.  71         0  LOAD_GLOBAL              load_pipe
                2  LOAD_FAST                'storage'
                4  LOAD_FAST                'name'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'pipe'

 L.  73        10  LOAD_GLOBAL              int
               12  LOAD_FAST                'config_index'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  STORE_FAST               'config_index'

 L.  74        18  LOAD_GLOBAL              int
               20  LOAD_GLOBAL              int
               22  LOAD_FAST                'outer_fold'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_CONST               1
               28  BINARY_SUBTRACT  
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  STORE_FAST               'outer_fold_index'

 L.  76        34  LOAD_STR                 ''
               36  STORE_FAST               'result'

 L.  77        38  LOAD_GLOBAL              int
               40  LOAD_CONST               0
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  STORE_FAST               'count'

 L.  79     46_48  SETUP_LOOP          858  'to 858'
               50  LOAD_FAST                'pipe'
               52  LOAD_ATTR                outer_folds
               54  LOAD_FAST                'outer_fold_index'
               56  BINARY_SUBSCR    
               58  LOAD_ATTR                tested_config_list
               60  LOAD_FAST                'config_index'
               62  BINARY_SUBSCR    
               64  LOAD_ATTR                inner_folds
               66  GET_ITER         
             68_0  COME_FROM           386  '386'
            68_70  FOR_ITER            856  'to 856'
               72  STORE_FAST               'inner_fold'

 L.  81        74  LOAD_FAST                'count'
               76  LOAD_GLOBAL              int
               78  LOAD_CONST               1
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  INPLACE_ADD      
               84  STORE_FAST               'count'

 L.  82        86  LOAD_GLOBAL              int
               88  LOAD_GLOBAL              int
               90  LOAD_FAST                'inner_fold'
               92  LOAD_ATTR                fold_nr
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_CONST               1
               98  BINARY_SUBTRACT  
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  STORE_FAST               'inner_fold_index'

 L.  84       104  LOAD_FAST                'pipe'
              106  LOAD_ATTR                outer_folds
              108  LOAD_FAST                'outer_fold_index'
              110  BINARY_SUBSCR    
              112  LOAD_ATTR                tested_config_list
              114  LOAD_FAST                'config_index'
              116  BINARY_SUBSCR    
              118  LOAD_ATTR                inner_folds
              120  LOAD_FAST                'inner_fold_index'
              122  BINARY_SUBSCR    
              124  STORE_FAST               'inner_fold_object'

 L.  86       126  LOAD_STR                 ','
              128  LOAD_METHOD              join
              130  LOAD_GLOBAL              map
              132  LOAD_GLOBAL              str
              134  LOAD_FAST                'inner_fold_object'
              136  LOAD_ATTR                training
              138  LOAD_ATTR                y_pred
              140  CALL_FUNCTION_2       2  '2 positional arguments'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  STORE_FAST               'train_y_prediction'

 L.  87       146  LOAD_STR                 ','
              148  LOAD_METHOD              join
              150  LOAD_GLOBAL              map
              152  LOAD_GLOBAL              str
              154  LOAD_GLOBAL              list
              156  LOAD_GLOBAL              range
              158  LOAD_CONST               1
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                'inner_fold_object'
              164  LOAD_ATTR                training
              166  LOAD_ATTR                y_pred
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  CALL_FUNCTION_2       2  '2 positional arguments'
              176  CALL_METHOD_1         1  '1 positional argument'
              178  STORE_FAST               'train_x_prediction'

 L.  88       180  LOAD_STR                 ','
              182  LOAD_METHOD              join
              184  LOAD_GLOBAL              map
              186  LOAD_GLOBAL              str
              188  LOAD_FAST                'inner_fold_object'
              190  LOAD_ATTR                training
              192  LOAD_ATTR                y_true
              194  CALL_FUNCTION_2       2  '2 positional arguments'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  STORE_FAST               'train_y_true'

 L.  89       200  LOAD_STR                 ','
              202  LOAD_METHOD              join
              204  LOAD_GLOBAL              map
              206  LOAD_GLOBAL              str
              208  LOAD_GLOBAL              list
              210  LOAD_GLOBAL              range
              212  LOAD_CONST               1
              214  LOAD_GLOBAL              len
              216  LOAD_FAST                'inner_fold_object'
              218  LOAD_ATTR                training
              220  LOAD_ATTR                y_true
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  CALL_FUNCTION_2       2  '2 positional arguments'
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  CALL_METHOD_1         1  '1 positional argument'
              232  STORE_FAST               'train_x_true'

 L.  91       234  LOAD_STR                 ','
              236  LOAD_METHOD              join
              238  LOAD_GLOBAL              map
              240  LOAD_GLOBAL              str
              242  LOAD_FAST                'inner_fold_object'
              244  LOAD_ATTR                training
              246  LOAD_ATTR                y_pred
              248  CALL_FUNCTION_2       2  '2 positional arguments'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  STORE_FAST               'val_y_prediction'

 L.  92       254  LOAD_STR                 ','
              256  LOAD_METHOD              join
              258  LOAD_GLOBAL              map
              260  LOAD_GLOBAL              str
              262  LOAD_GLOBAL              list
              264  LOAD_GLOBAL              range
              266  LOAD_CONST               1
              268  LOAD_GLOBAL              len
              270  LOAD_FAST                'inner_fold_object'
              272  LOAD_ATTR                training
              274  LOAD_ATTR                y_pred
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  CALL_FUNCTION_2       2  '2 positional arguments'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  CALL_FUNCTION_2       2  '2 positional arguments'
              284  CALL_METHOD_1         1  '1 positional argument'
              286  STORE_FAST               'val_x_prediction'

 L.  93       288  LOAD_STR                 ','
              290  LOAD_METHOD              join
              292  LOAD_GLOBAL              map
              294  LOAD_GLOBAL              str
              296  LOAD_FAST                'inner_fold_object'
              298  LOAD_ATTR                training
              300  LOAD_ATTR                y_true
              302  CALL_FUNCTION_2       2  '2 positional arguments'
              304  CALL_METHOD_1         1  '1 positional argument'
              306  STORE_FAST               'val_y_true'

 L.  94       308  LOAD_STR                 ','
              310  LOAD_METHOD              join
              312  LOAD_GLOBAL              map
              314  LOAD_GLOBAL              str
              316  LOAD_GLOBAL              list
              318  LOAD_GLOBAL              range
              320  LOAD_CONST               1
              322  LOAD_GLOBAL              len
              324  LOAD_FAST                'inner_fold_object'
              326  LOAD_ATTR                training
              328  LOAD_ATTR                y_true
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  CALL_FUNCTION_2       2  '2 positional arguments'
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  CALL_FUNCTION_2       2  '2 positional arguments'
              338  CALL_METHOD_1         1  '1 positional argument'
              340  STORE_FAST               'val_x_true'

 L.  96       342  LOAD_FAST                'train_x_true'
          344_346  POP_JUMP_IF_TRUE    388  'to 388'
              348  LOAD_FAST                'train_y_true'
          350_352  POP_JUMP_IF_TRUE    388  'to 388'
              354  LOAD_FAST                'train_x_prediction'
          356_358  POP_JUMP_IF_TRUE    388  'to 388'
              360  LOAD_FAST                'train_y_prediction'
          362_364  POP_JUMP_IF_TRUE    388  'to 388'
              366  LOAD_FAST                'val_x_true'
          368_370  POP_JUMP_IF_TRUE    388  'to 388'
              372  LOAD_FAST                'val_y_true'
          374_376  POP_JUMP_IF_TRUE    388  'to 388'
              378  LOAD_FAST                'val_x_prediction'
          380_382  POP_JUMP_IF_TRUE    388  'to 388'
              384  LOAD_FAST                'val_y_prediction'
              386  POP_JUMP_IF_FALSE    68  'to 68'
            388_0  COME_FROM           380  '380'
            388_1  COME_FROM           374  '374'
            388_2  COME_FROM           368  '368'
            388_3  COME_FROM           362  '362'
            388_4  COME_FROM           356  '356'
            388_5  COME_FROM           350  '350'
            388_6  COME_FROM           344  '344'

 L.  98       388  LOAD_FAST                'result'
              390  LOAD_STR                 "<div class='tab-pane' id='config_"
              392  LOAD_GLOBAL              str
              394  LOAD_FAST                'config_index'
              396  CALL_FUNCTION_1       1  '1 positional argument'
              398  BINARY_ADD       
              400  LOAD_STR                 '_fold_'
              402  BINARY_ADD       
              404  LOAD_GLOBAL              str
              406  LOAD_FAST                'inner_fold'
              408  LOAD_ATTR                fold_nr
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  BINARY_ADD       
              414  LOAD_STR                 "'>"
              416  BINARY_ADD       
              418  INPLACE_ADD      
              420  STORE_FAST               'result'

 L.  99       422  LOAD_FAST                'result'
              424  LOAD_STR                 "<div class='row'>"
              426  INPLACE_ADD      
              428  STORE_FAST               'result'

 L. 103       430  LOAD_FAST                'result'
              432  LOAD_STR                 "<div class='col-md-12'><div id='config_"
              434  LOAD_GLOBAL              str
              436  LOAD_FAST                'config_index'
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  BINARY_ADD       
              442  LOAD_STR                 '_fold_'
              444  BINARY_ADD       
              446  LOAD_GLOBAL              str
              448  LOAD_FAST                'inner_fold'
              450  LOAD_ATTR                fold_nr
              452  CALL_FUNCTION_1       1  '1 positional argument'
              454  BINARY_ADD       
              456  LOAD_STR                 "_training'></div>"
              458  BINARY_ADD       
              460  INPLACE_ADD      
              462  STORE_FAST               'result'

 L. 104       464  LOAD_FAST                'result'
              466  LOAD_STR                 '<script>'
              468  INPLACE_ADD      
              470  STORE_FAST               'result'

 L. 105       472  LOAD_FAST                'result'
              474  LOAD_STR                 'var trace1 = {x: ['
              476  LOAD_FAST                'train_x_true'
              478  BINARY_ADD       
              480  LOAD_STR                 '],'
              482  BINARY_ADD       
              484  INPLACE_ADD      
              486  STORE_FAST               'result'

 L. 106       488  LOAD_FAST                'result'
              490  LOAD_STR                 'y: ['
              492  LOAD_FAST                'train_y_true'
              494  BINARY_ADD       
              496  LOAD_STR                 '],'
              498  BINARY_ADD       
              500  INPLACE_ADD      
              502  STORE_FAST               'result'

 L. 107       504  LOAD_FAST                'result'
              506  LOAD_STR                 " name: 'true',"
              508  INPLACE_ADD      
              510  STORE_FAST               'result'

 L. 108       512  LOAD_FAST                'result'
              514  LOAD_STR                 " mode: 'markers'};"
              516  INPLACE_ADD      
              518  STORE_FAST               'result'

 L. 109       520  LOAD_FAST                'result'
              522  LOAD_STR                 'var trace2 = {'
              524  INPLACE_ADD      
              526  STORE_FAST               'result'

 L. 110       528  LOAD_FAST                'result'
              530  LOAD_STR                 'x: ['
              532  LOAD_FAST                'train_x_prediction'
              534  BINARY_ADD       
              536  LOAD_STR                 '],'
              538  BINARY_ADD       
              540  INPLACE_ADD      
              542  STORE_FAST               'result'

 L. 111       544  LOAD_FAST                'result'
              546  LOAD_STR                 'y: ['
              548  LOAD_FAST                'train_y_prediction'
              550  BINARY_ADD       
              552  LOAD_STR                 '],'
              554  BINARY_ADD       
              556  INPLACE_ADD      
              558  STORE_FAST               'result'

 L. 112       560  LOAD_FAST                'result'
              562  LOAD_STR                 " name: 'prediction',"
              564  INPLACE_ADD      
              566  STORE_FAST               'result'

 L. 113       568  LOAD_FAST                'result'
              570  LOAD_STR                 " mode: 'markers'};"
              572  INPLACE_ADD      
              574  STORE_FAST               'result'

 L. 114       576  LOAD_FAST                'result'
              578  LOAD_STR                 'var data = [ trace1, trace2 ];'
              580  INPLACE_ADD      
              582  STORE_FAST               'result'

 L. 115       584  LOAD_FAST                'result'
              586  LOAD_STR                 "var layout = {title:'True/Predict for training set', width: 1600};"
              588  INPLACE_ADD      
              590  STORE_FAST               'result'

 L. 116       592  LOAD_FAST                'result'
              594  LOAD_STR                 "Plotly.newPlot('config_"
              596  LOAD_GLOBAL              str
              598  LOAD_FAST                'config_index'
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  BINARY_ADD       
              604  LOAD_STR                 '_fold_'
              606  BINARY_ADD       
              608  LOAD_GLOBAL              str
              610  LOAD_FAST                'inner_fold'
              612  LOAD_ATTR                fold_nr
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  BINARY_ADD       
              618  LOAD_STR                 "_training', data, layout);"
              620  BINARY_ADD       
              622  INPLACE_ADD      
              624  STORE_FAST               'result'

 L. 117       626  LOAD_FAST                'result'
              628  LOAD_STR                 '</script></div>'
              630  INPLACE_ADD      
              632  STORE_FAST               'result'

 L. 121       634  LOAD_FAST                'result'
              636  LOAD_STR                 "<div class='col-md-12'><div id='config_"
              638  LOAD_GLOBAL              str
              640  LOAD_FAST                'config_index'
              642  CALL_FUNCTION_1       1  '1 positional argument'
              644  BINARY_ADD       
              646  LOAD_STR                 '_fold_'
              648  BINARY_ADD       
              650  LOAD_GLOBAL              str
              652  LOAD_FAST                'inner_fold'
              654  LOAD_ATTR                fold_nr
              656  CALL_FUNCTION_1       1  '1 positional argument'
              658  BINARY_ADD       
              660  LOAD_STR                 "_validation'></div>"
              662  BINARY_ADD       
              664  INPLACE_ADD      
              666  STORE_FAST               'result'

 L. 122       668  LOAD_FAST                'result'
              670  LOAD_STR                 '<script>'
              672  INPLACE_ADD      
              674  STORE_FAST               'result'

 L. 123       676  LOAD_FAST                'result'
              678  LOAD_STR                 'var trace1 = {x: ['
              680  LOAD_FAST                'val_x_true'
              682  BINARY_ADD       
              684  LOAD_STR                 '],'
              686  BINARY_ADD       
              688  INPLACE_ADD      
              690  STORE_FAST               'result'

 L. 124       692  LOAD_FAST                'result'
              694  LOAD_STR                 'y: ['
              696  LOAD_FAST                'val_y_true'
              698  BINARY_ADD       
              700  LOAD_STR                 '],'
              702  BINARY_ADD       
              704  INPLACE_ADD      
              706  STORE_FAST               'result'

 L. 125       708  LOAD_FAST                'result'
              710  LOAD_STR                 " name: 'true',"
              712  INPLACE_ADD      
              714  STORE_FAST               'result'

 L. 126       716  LOAD_FAST                'result'
              718  LOAD_STR                 " mode: 'markers'};"
              720  INPLACE_ADD      
              722  STORE_FAST               'result'

 L. 127       724  LOAD_FAST                'result'
              726  LOAD_STR                 'var trace2 = {'
              728  INPLACE_ADD      
              730  STORE_FAST               'result'

 L. 128       732  LOAD_FAST                'result'
              734  LOAD_STR                 'x: ['
              736  LOAD_FAST                'val_x_prediction'
              738  BINARY_ADD       
              740  LOAD_STR                 '],'
              742  BINARY_ADD       
              744  INPLACE_ADD      
              746  STORE_FAST               'result'

 L. 129       748  LOAD_FAST                'result'
              750  LOAD_STR                 'y: ['
              752  LOAD_FAST                'val_y_prediction'
              754  BINARY_ADD       
              756  LOAD_STR                 '],'
              758  BINARY_ADD       
              760  INPLACE_ADD      
              762  STORE_FAST               'result'

 L. 130       764  LOAD_FAST                'result'
              766  LOAD_STR                 " name: 'prediction',"
              768  INPLACE_ADD      
              770  STORE_FAST               'result'

 L. 131       772  LOAD_FAST                'result'
              774  LOAD_STR                 " mode: 'markers'};"
              776  INPLACE_ADD      
              778  STORE_FAST               'result'

 L. 132       780  LOAD_FAST                'result'
              782  LOAD_STR                 'var data = [ trace1, trace2 ];'
              784  INPLACE_ADD      
              786  STORE_FAST               'result'

 L. 133       788  LOAD_FAST                'result'
              790  LOAD_STR                 "var layout = {title:'True/Predict for validation set', width: 1600};"
              792  INPLACE_ADD      
              794  STORE_FAST               'result'

 L. 134       796  LOAD_FAST                'result'
              798  LOAD_STR                 "Plotly.newPlot('config_"
              800  LOAD_GLOBAL              str
              802  LOAD_FAST                'config_index'
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  BINARY_ADD       
              808  LOAD_STR                 '_fold_'
              810  BINARY_ADD       
              812  LOAD_GLOBAL              str
              814  LOAD_FAST                'inner_fold'
              816  LOAD_ATTR                fold_nr
              818  CALL_FUNCTION_1       1  '1 positional argument'
              820  BINARY_ADD       
              822  LOAD_STR                 "_validation', data, layout);"
              824  BINARY_ADD       
              826  INPLACE_ADD      
              828  STORE_FAST               'result'

 L. 135       830  LOAD_FAST                'result'
              832  LOAD_STR                 '</script></div>'
              834  INPLACE_ADD      
              836  STORE_FAST               'result'

 L. 136       838  LOAD_FAST                'result'
              840  LOAD_STR                 '</div>'
              842  INPLACE_ADD      
              844  STORE_FAST               'result'

 L. 137       846  LOAD_FAST                'result'
              848  LOAD_STR                 '</div>'
              850  INPLACE_ADD      
              852  STORE_FAST               'result'
              854  JUMP_BACK            68  'to 68'
              856  POP_BLOCK        
            858_0  COME_FROM_LOOP       46  '46'

 L. 139       858  LOAD_FAST                'result'
              860  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 856