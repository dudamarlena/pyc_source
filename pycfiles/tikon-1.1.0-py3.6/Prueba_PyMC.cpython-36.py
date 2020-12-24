# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Matemáticas\Prueba_PyMC.py
# Compiled at: 2017-11-07 14:50:22
# Size of source mod 2**32: 7682 bytes
import matplotlib.pyplot as dib, numpy as np, pymc
from Matemáticas.Incert import trazas_a_dists
i = 0
adaptivo = True
emp = 0
fin = 60
print(emp, fin)
n_iter = 5000

class ModBayes(object):

    def __init__--- This code section failed: ---

 L.  18         0  LOAD_FAST                'id_calib'
                2  LOAD_FAST                'símismo'
                4  STORE_ATTR               id

 L.  20         6  LOAD_GLOBAL              trazas_a_dists
                8  LOAD_FAST                'símismo'
               10  LOAD_ATTR                id
               12  LOAD_FAST                'lista_d_paráms'
               14  LOAD_FAST                'lista_líms'

 L.  21        16  LOAD_FAST                'aprioris'
               18  LOAD_STR                 'calib'
               20  LOAD_CONST               False
               22  LOAD_CONST               ('id_simul', 'l_d_pm', 'l_lms', 'l_trazas', 'formato', 'comunes')
               24  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               26  STORE_FAST               'l_var_paráms'

 L.  25        28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 'ModBayes.__init__.<locals>.<listcomp>'
               32  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               34  LOAD_FAST                'l_var_paráms'
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  STORE_FAST               'l_var_paráms'

 L.  30        42  LOAD_FAST                'l_var_paráms'
               44  LOAD_GLOBAL              emp
               46  LOAD_GLOBAL              fin
               48  BUILD_SLICE_2         2 
               50  BINARY_SUBSCR    
               52  STORE_FAST               'l_var_paráms'

 L.  32        54  SETUP_LOOP           96  'to 96'
               56  LOAD_FAST                'l_var_paráms'
               58  GET_ITER         
               60  FOR_ITER             94  'to 94'
               62  STORE_FAST               'parám'

 L.  33        64  LOAD_GLOBAL              isinstance
               66  LOAD_FAST                'parám'
               68  LOAD_GLOBAL              pymc
               70  LOAD_ATTR                Deterministic
               72  CALL_FUNCTION_2       2  '2 positional arguments'
               74  POP_JUMP_IF_FALSE    60  'to 60'

 L.  34        76  LOAD_FAST                'l_var_paráms'
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

 L.  39        96  LOAD_FAST                'función_llenar_coefs'
               98  LOAD_FAST                'id_calib'
              100  LOAD_CONST               1
              102  LOAD_CONST               False
              104  LOAD_CONST               ('nombre_simul', 'n_rep_parám', 'dib_dists')
              106  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              108  POP_TOP          

 L.  41       110  LOAD_CLOSURE             'función'
              112  BUILD_TUPLE_1         1 
              114  LOAD_CODE                <code_object fun>
              116  LOAD_STR                 'ModBayes.__init__.<locals>.fun'
              118  MAKE_FUNCTION_8          'closure'
              120  STORE_DEREF              'fun'

 L.  50       122  LOAD_GLOBAL              pymc
              124  LOAD_ATTR                deterministic
              126  LOAD_CONST               True
              128  LOAD_CONST               ('trace',)
              130  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  51       132  LOAD_FAST                'l_var_paráms'
              134  BUILD_TUPLE_1         1 
              136  LOAD_CLOSURE             'dic_argums'
              138  LOAD_CLOSURE             'fun'
              140  BUILD_TUPLE_2         2 
              142  LOAD_CODE                <code_object simul>
              144  LOAD_STR                 'ModBayes.__init__.<locals>.simul'
              146  MAKE_FUNCTION_9          'default, closure'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  STORE_FAST               'simul'

 L.  54       152  BUILD_LIST_0          0 
              154  STORE_FAST               'l_var_obs'

 L.  56       156  SETUP_LOOP          240  'to 240'
              158  LOAD_FAST                'd_obs'
              160  LOAD_ATTR                items
              162  CALL_FUNCTION_0       0  '0 positional arguments'
              164  GET_ITER         
              166  FOR_ITER            238  'to 238'
              168  UNPACK_SEQUENCE_2     2 
              170  STORE_FAST               'tipo'
              172  STORE_FAST               'obs'

 L.  57       174  LOAD_FAST                'tipo'
              176  LOAD_STR                 'Normal'
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   166  'to 166'

 L.  58       182  LOAD_CONST               1
              184  LOAD_FAST                'simul'
              186  LOAD_STR                 'sigma'
              188  BINARY_SUBSCR    
              190  LOAD_CONST               2
              192  BINARY_POWER     
              194  BINARY_TRUE_DIVIDE
              196  STORE_FAST               'tau'

 L.  59       198  LOAD_GLOBAL              pymc
              200  LOAD_ATTR                Normal
              202  LOAD_STR                 'obs'
              204  LOAD_FAST                'simul'
              206  LOAD_STR                 'mu'
              208  BINARY_SUBSCR    
              210  LOAD_FAST                'tau'
              212  LOAD_FAST                'obs'
              214  LOAD_CONST               True
              216  LOAD_CONST               ('mu', 'tau', 'value', 'observed')
              218  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              220  STORE_FAST               'var_obs'

 L.  60       222  LOAD_FAST                'l_var_obs'
              224  LOAD_ATTR                extend
              226  LOAD_FAST                'var_obs'
              228  LOAD_FAST                'tau'
              230  BUILD_LIST_2          2 
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  POP_TOP          
              236  JUMP_BACK           166  'to 166'
              238  POP_BLOCK        
            240_0  COME_FROM_LOOP      156  '156'

 L.  62       240  LOAD_GLOBAL              pymc
              242  LOAD_ATTR                MCMC
              244  LOAD_FAST                'simul'
              246  BUILD_SET_1           1 
              248  LOAD_FAST                'l_var_paráms'
              250  LOAD_FAST                'l_var_obs'
              252  BUILD_SET_UNPACK_3     3 
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  LOAD_FAST                'símismo'
              258  STORE_ATTR               MCMC

Parse error at or near `BUILD_SET_UNPACK_3' instruction at offset 252

    def calib(símismo, rep, quema, extraer, **kwargs):
        if adaptivo:
            símismo.MCMC.use_step_method(pymc.AdaptiveMetropolis, símismo.MCMC.stochastics)
        símismo.MCMC.sample(iter=rep, burn=quema, thin=extraer, verbose=1)
        for v in símismo.MCMC.variables:
            try:
                print('{}\n\t'.format(v.__name__), símismo.MCMC.trace(v.__name__)[:])
                print('************')
            except (TypeError, KeyError):
                pass


líms = [
 [
  0.006143547954646662, 0.004143547954646662], [0.02641613017892241, 0.02561613017892241], [3.6560851733914808, 3.2560851733914804], [1.9650416697683102, 1.36504166976831], [1.0043484484635446e-08, 8.905226359823514e-09], [5.2344154421948645e-17, 3.584930542917252e-17], [0.01, 0.008424049215276837], [0.05278370675938784, 0.034783706759387835], [8.344156186512684, 7.544156186512684], [1.859969480435551, 1.259969480435551], [8.408452689594336e-09, 7.270194564782404e-09], [7.937490983672413e-17, 6.288006084394801e-17], [0.009822133533670865, 0.007822133533670866], [0.02360183840006633, 0.012018505066732996], [6.735045441220312, 6.335045441220312], [2.935368687970388, 2.3353686879703885], [6.767427175972795e-09, 5.629169051160862e-09], [3.5942494909704755e-17, 1.9447645916928642e-17], [0.0010892446260036938, 0.0], [0.06456888904570236, 0.052985555712369035], [7.993218921346308, 7.593218921346308], [3.805551951662424, 3.2055519516624242], [9.473954656090874e-09, 8.335696531278942e-09], [6.156900521985185e-17, 4.507415622707573e-17], [0.0017283406835598317, 0.0], [0.125, 0.1132149097879174], [6.0, 5.630711932400921], [2.6814139049624686, 2.081413904962469], [5.2171445961448266e-09, 4.4000086539813725e-09], [8.532503690773825e-17, 6.883018791496213e-17], [0.005909086460391245, 0.003909086460391245], [0.08149692925899343, 0.06499187875394291], [11.0, 10.70688092264144], [1.4300829767935785, 1.0], [0.0067909413050695555, 0.0047909413050695555], [0.024449742955003222, 0.008862441367701635], [7.81351465785079, 7.41351465785079], [3.9871155195555192, 3.3871155195555196], [0.0041580911542028875, 0.002158091154202888], [3.408383637925069, 3.0083836379250686], [92.78184230132567, 73.48184230132566], [1.667745375005944, 1.467745375005944], [7.454915463070574, 6.2949154630705735], [3.1526724082578497, 2.55267240825785], [0.0076823064053704575, 0.0056823064053704575], [9.866900929997412, 8.066900929997411], [10.061451653132691, 9.661451653132692], [0.6, 0.5839890199595302], [1.3450794438657239, 1.0950794438657239], [0.7643829171197258, 0.5143829171197258], [0.48207860410886627, 0.25], [290743531.36023504, 110743531.36023504], [279281018.73310006, 100000000.0], [585476626.0580845, 405476626.0580845], [0.006723886177260551, 0.004723886177260551], [18.586660304562358, 16.586660304562358], [8.043619184444477, 7.043619184444478], [0.003894993948127248, 0.001894993948127248], [5.186734565996787, 3.3867345659967865], [7.994937321302886, 7.5949373213028855], [0.589093500637263, 0.5690935006372629], [0.8656415159401634, 0.6156415159401634], [490321.97721997125, 100000.0], [0.01, 0.008765390303566392], [14.580562059315994, 12.580562059315994], [8.428071586548748, 7.428071586548748], [0.1, 0.0]]
if __name__ == '__main__':
    for l in líms:
        i = 0
        print(l)
        dic_paráms = {'sigma':None, 
         'mu':None}

        def fun0():
            s = np.zeros(5)
            m = np.zeros(5)
            s[:] = dic_paráms['sigma']
            m[:] = dic_paráms['mu']
            return {'Normal': {'sigma':s,  'mu':m}}


        def f(**kwargs):
            for i, ll in enumerate(sorted(dic_paráms)):
                dic_paráms[ll] = l_d_paráms[i]['prueba']


        d_args = {}
        datos = np.array([4.1, 3.9, 4.2, 3.8, 4])
        d_obs = {'Normal': datos}
        l_d_paráms = [
         {'a': 'Uniforme~({}, {})'.format(l[0], l[1])}, {'a': 'Gamma~(1, 0, 1)'}]
        l_líms = [
         (
          -np.inf, np.inf), (0, np.inf)]
        m = ModBayes(función=fun0, dic_argums=d_args, d_obs=d_obs, lista_d_paráms=l_d_paráms, aprioris=[
         [
          'a'], ['a']],
          lista_líms=l_líms,
          id_calib='prueba',
          función_llenar_coefs=f)
        m.calib(rep=n_iter, quema=0, extraer=1)

    input()
    var_mu = pymc.Uniform('parám_0', 0, 10)
    var_s = pymc.Gamma('parám_1', 1, 1)
    obs = pymc.Normal('obs', mu=var_mu, tau=(1 / var_s ** 2), value=datos, trace=True, observed=True)
    mod_prueba = pymc.MCMC((var_mu, var_s, obs))
    if adaptivo:
        mod_prueba.use_step_method(pymc.AdaptiveMetropolis, mod_prueba.stochastics)
    mod_prueba.sample(iter=n_iter, burn=0, thin=1, verbose=1)
    for v in mod_prueba.variables:
        try:
            dib.plot(mod_prueba.trace(v.__name__)[:])
            dib.title(v.__name__)
            dib.show()
        except (TypeError, KeyError):
            pass

        try:
            print('{}\n\t'.format(v.__name__), mod_prueba.trace(v.__name__)[:])
            print('************')
        except (TypeError, KeyError):
            pass

# global i ## Warning: Unused global