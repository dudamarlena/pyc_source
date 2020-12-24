# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Matemáticas\Calib.py
# Compiled at: 2017-11-08 10:00:34
# Size of source mod 2**32: 11419 bytes
import numpy as np, pymc
from tikon.Matemáticas.Incert import trazas_a_dists

class ModBayes(object):
    __doc__ = '\n    Esta clase merece una descripción detallada. Al final, un Modelo es lo que trae junto simulación, observaciones y\n    parámetros para calibrar estos últimos por medio de inferencia Bayesiana (usando el módulo de Python PyMC).\n    Si no conoces bien la inferencia Bayesiana, ahora sería una buena cosa para leer antes de intentar entender lo\n    que sigue. Si hacia yo me confundo yo mismo en mi propio código, no lo vas a entender si no entiendes bien\n    el concepto de la inferencia Bayesiana con método de Monte Carlo.\n\n    '

    def __init__--- This code section failed: ---

 L.  84         0  LOAD_FAST                'lista_d_paráms'
                2  LOAD_FAST                'símismo'
                4  STORE_ATTR               lista_parám

 L.  85         6  LOAD_FAST                'id_calib'
                8  LOAD_FAST                'símismo'
               10  STORE_ATTR               id

 L.  86        12  LOAD_CONST               0
               14  LOAD_FAST                'símismo'
               16  STORE_ATTR               n_iter

 L.  91        18  LOAD_GLOBAL              trazas_a_dists
               20  LOAD_FAST                'símismo'
               22  LOAD_ATTR                id
               24  LOAD_FAST                'lista_d_paráms'
               26  LOAD_FAST                'lista_líms'

 L.  92        28  LOAD_FAST                'aprioris'
               30  LOAD_STR                 'calib'
               32  LOAD_CONST               False
               34  LOAD_CONST               ('id_simul', 'l_d_pm', 'l_lms', 'l_trazas', 'formato', 'comunes')
               36  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               38  STORE_FAST               'l_var_paráms'

 L.  95        40  LOAD_LISTCOMP            '<code_object <listcomp>>'
               42  LOAD_STR                 'ModBayes.__init__.<locals>.<listcomp>'
               44  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               46  LOAD_FAST                'l_var_paráms'
               48  GET_ITER         
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  STORE_FAST               'l_var_paráms'

 L. 102        54  SETUP_LOOP           96  'to 96'
               56  LOAD_FAST                'l_var_paráms'
               58  GET_ITER         
               60  FOR_ITER             94  'to 94'
               62  STORE_FAST               'parám'

 L. 103        64  LOAD_GLOBAL              isinstance
               66  LOAD_FAST                'parám'
               68  LOAD_GLOBAL              pymc
               70  LOAD_ATTR                Deterministic
               72  CALL_FUNCTION_2       2  '2 positional arguments'
               74  POP_JUMP_IF_FALSE    60  'to 60'

 L. 104        76  LOAD_FAST                'l_var_paráms'
               78  LOAD_ATTR                append
               80  LOAD_GLOBAL              min
               82  LOAD_FAST                'parám'
               84  LOAD_ATTR                extended_parents
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  POP_TOP          
               92  JUMP_BACK            60  'to 60'
               94  POP_BLOCK        
             96_0  COME_FROM_LOOP       54  '54'

 L. 107        96  LOAD_FAST                'función_llenar_coefs'
               98  LOAD_FAST                'id_calib'
              100  LOAD_CONST               1
              102  LOAD_CONST               False
              104  LOAD_CONST               ('nombre_simul', 'n_rep_parám', 'dib_dists')
              106  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              108  POP_TOP          

 L. 113       110  LOAD_GLOBAL              pymc
              112  LOAD_ATTR                deterministic
              114  LOAD_CONST               False
              116  LOAD_CONST               ('trace',)
              118  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 114       120  LOAD_FAST                'l_var_paráms'
              122  BUILD_TUPLE_1         1 
              124  LOAD_CLOSURE             'dic_argums'
              126  LOAD_CLOSURE             'función'
              128  BUILD_TUPLE_2         2 
              130  LOAD_CODE                <code_object simul>
              132  LOAD_STR                 'ModBayes.__init__.<locals>.simul'
              134  MAKE_FUNCTION_9          'default, closure'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  STORE_FAST               'simul'

 L. 118       140  BUILD_LIST_0          0 
              142  STORE_FAST               'l_var_obs'

 L. 119       144  SETUP_LOOP          362  'to 362'
              146  LOAD_FAST                'd_obs'
              148  LOAD_ATTR                items
              150  CALL_FUNCTION_0       0  '0 positional arguments'
              152  GET_ITER         
              154  FOR_ITER            360  'to 360'
              156  UNPACK_SEQUENCE_2     2 
              158  STORE_FAST               'tipo'
              160  STORE_FAST               'm_obs'

 L. 123       162  LOAD_FAST                'tipo'
              164  LOAD_STR                 'Gamma'
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   228  'to 228'

 L. 127       170  LOAD_GLOBAL              pymc
              172  LOAD_ATTR                Gamma
              174  LOAD_STR                 'obs_{}'
              176  LOAD_ATTR                format
              178  LOAD_FAST                'tipo'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  LOAD_FAST                'simul'
              184  LOAD_STR                 'Gamma'
              186  BINARY_SUBSCR    
              188  LOAD_STR                 'alpha'
              190  BINARY_SUBSCR    
              192  LOAD_FAST                'simul'
              194  LOAD_STR                 'Gamma'
              196  BINARY_SUBSCR    
              198  LOAD_STR                 'beta'
              200  BINARY_SUBSCR    

 L. 128       202  LOAD_FAST                'm_obs'
              204  LOAD_CONST               True
              206  LOAD_CONST               False
              208  LOAD_CONST               ('alpha', 'beta', 'value', 'observed', 'trace')
              210  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              212  STORE_FAST               'var_obs'

 L. 131       214  LOAD_FAST                'l_var_obs'
              216  LOAD_ATTR                extend
              218  LOAD_FAST                'var_obs'
              220  BUILD_LIST_1          1 
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  POP_TOP          
              226  JUMP_BACK           154  'to 154'
              228  ELSE                     '358'

 L. 133       228  LOAD_FAST                'tipo'
              230  LOAD_STR                 'Normal'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   354  'to 354'

 L. 135       238  LOAD_FAST                'simul'
              240  LOAD_STR                 'Normal'
              242  BINARY_SUBSCR    
              244  LOAD_STR                 'sigma'
              246  BINARY_SUBSCR    
              248  LOAD_CONST               -2
              250  BINARY_POWER     
              252  STORE_FAST               'tau'

 L. 136       254  LOAD_GLOBAL              pymc
              256  LOAD_ATTR                Normal
              258  LOAD_STR                 'obs_{}'
              260  LOAD_ATTR                format
              262  LOAD_FAST                'tipo'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  LOAD_FAST                'simul'
              268  LOAD_STR                 'Normal'
              270  BINARY_SUBSCR    
              272  LOAD_STR                 'mu'
              274  BINARY_SUBSCR    
              276  LOAD_FAST                'tau'

 L. 137       278  LOAD_FAST                'm_obs'
              280  LOAD_CONST               True
              282  LOAD_CONST               False
              284  LOAD_CONST               ('mu', 'tau', 'value', 'observed', 'trace')
              286  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              288  STORE_FAST               'var_obs'

 L. 138       290  LOAD_FAST                'var_obs'
              292  LOAD_FAST                'tau'
              294  LOAD_FAST                'var_obs'
              296  LOAD_ATTR                parents
              298  LOAD_STR                 'mu'
              300  BINARY_SUBSCR    
              302  LOAD_FAST                'var_obs'
              304  LOAD_ATTR                parents
              306  LOAD_STR                 'mu'
              308  BINARY_SUBSCR    
              310  LOAD_ATTR                parents
              312  LOAD_STR                 'self'
              314  BINARY_SUBSCR    

 L. 139       316  LOAD_FAST                'tau'
              318  LOAD_ATTR                parents
              320  LOAD_STR                 'a'
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'tau'
              326  LOAD_ATTR                parents
              328  LOAD_STR                 'a'
              330  BINARY_SUBSCR    
              332  LOAD_ATTR                parents
              334  LOAD_STR                 'self'
              336  BINARY_SUBSCR    
              338  BUILD_LIST_6          6 
              340  STORE_FAST               'nuevos'

 L. 140       342  LOAD_FAST                'l_var_obs'
              344  LOAD_ATTR                extend
              346  LOAD_FAST                'nuevos'
              348  CALL_FUNCTION_1       1  '1 positional argument'
              350  POP_TOP          
              352  JUMP_BACK           154  'to 154'
              354  ELSE                     '358'

 L. 142       354  LOAD_GLOBAL              ValueError
              356  RAISE_VARARGS_1       1  'exception'
              358  JUMP_BACK           154  'to 154'
              360  POP_BLOCK        
            362_0  COME_FROM_LOOP      144  '144'

 L. 145       362  LOAD_GLOBAL              pymc
              364  LOAD_ATTR                MCMC
              366  LOAD_FAST                'simul'
              368  BUILD_SET_1           1 
              370  LOAD_FAST                'l_var_paráms'
              372  LOAD_FAST                'l_var_obs'
              374  BUILD_SET_UNPACK_3     3 
              376  LOAD_STR                 'sqlite'
              378  LOAD_FAST                'símismo'
              380  LOAD_ATTR                id
              382  LOAD_CONST               ('db', 'dbname')
              384  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              386  LOAD_FAST                'símismo'
              388  STORE_ATTR               MCMC

Parse error at or near `BUILD_SET_UNPACK_3' instruction at offset 374

    def calib(símismo, rep, quema, extraer):
        """
        Esta función sirve para llamar a las funcionalidades de calibración de PyMC.

        :param rep: El número de repeticiones para la calibración.
        :type rep: int

        :param quema: El número de repeticiones iniciales a cortar de los resultados. Esto evita que los resultados
        estén muy influenciados por los valores iniciales (y posiblemente erróneos) que toman los parámetros al
        principio de la calibración.
        :type quema: int

        :param extraer: Cada cuántas repeticiones hay que guardar para los resultados. Por ejemplo, con `extraer`=10,
        cada 10 repeticiones se guardará, así que, con `rep`=10000, `quema`=100 y `extraer`=10, quedaremos con trazas
        de (10000 - 100) / 10 = 990 datos para aproximar la destribución de cada parámetro.

        """
        símismo.n_iter += rep
        símismo.MCMC.use_step_methodpymc.AdaptiveMetropolissímismo.MCMC.stochastics
        símismo.MCMC.sample(iter=rep, burn=quema, thin=extraer, verbose=1)

    def guardar(símismo, nombre=None):
        """
        Esta función guarda las trazas de los parámetros generadas por la calibración en el diccionario del parámetro
        como una nueva calibración.

        """
        id_calib = strsímismo.id
        bd = pymc.database.sqlite.loadid_calib
        bd.connect_modelsímismo.MCMC
        if nombre is None:
            nombre = símismo.id
        else:
            símismo.id = nombre
        for d_parám in símismo.lista_parám:
            try:
                vec_np = d_parám[id_calib].trace(chain=None)[:]
            except AttributeError:
                vec_np = np.zerossímismo.n_iter
                vec_np[:] = d_parám[id_calib].value

            d_parám.popid_calib
            d_parám[nombre] = vec_np

        símismo.MCMC.db.close