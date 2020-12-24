# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/salt_ion_match.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 10757 bytes
__doc__ = '\npyEQL salt matching library\n\nThis file contains functions that allow a pyEQL Solution object composed of\nindividual species (usually ions) to be mapped to a solution of one or more\nsalts. This mapping is necessary because some parameters (such as activity\ncoefficient data) can only be determined for salts (e.g. NaCl) and not individual\nspecies (e.g. Na+)\n\n:copyright: 2013-2020 by Ryan S. Kingsbury\n:license: LGPL, see LICENSE for more details.\n\n'
import logging
from pyEQL.logging_system import Unique
import pyEQL.chemical_formula as chem
logger = logging.getLogger(__name__)
unique = Unique()
logger.addFilter(unique)
ch = logging.StreamHandler()
formatter = logging.Formatter('(%(name)s) - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Salt:
    """Salt"""

    def __init__(self, cation, anion):
        self.cation = cation
        self.anion = anion
        self.z_cation = chem.get_formal_charge(cation)
        self.z_anion = chem.get_formal_charge(anion)
        self.nu_cation = abs(self.z_anion)
        self.nu_anion = abs(self.z_cation)
        if self.nu_cation == self.nu_anion:
            self.nu_cation = 1
            self.nu_anion = 1
        else:
            salt_formula = ''
            if self.nu_cation > 1:
                if len(chem.get_elements(cation)) > 1:
                    salt_formula += '('
                    salt_formula += _trim_formal_charge(cation)
                    salt_formula += ')'
                else:
                    salt_formula += _trim_formal_charge(cation)
                salt_formula += str(self.nu_cation)
            else:
                salt_formula += _trim_formal_charge(cation)
            if self.nu_anion > 1:
                if len(chem.get_elements(anion)) > 1:
                    salt_formula += '('
                    salt_formula += _trim_formal_charge(anion)
                    salt_formula += ')'
                else:
                    salt_formula += _trim_formal_charge(anion)
                salt_formula += str(self.nu_anion)
            else:
                salt_formula += _trim_formal_charge(anion)
        self.formula = salt_formula

    def get_effective_molality(self, ionic_strength):
        r""" Calculate the effective molality according to [#]_

        .. math:: 2 I \over (\nu_+ z_+^2 + \nu_- z_- ^2)

        Parameters
        ----------
        ionic_strength: Quantity
                        The ionic strength of the parent solution, mol/kg

        Returns
        -------
        Quantity: the effective molality of the salt in the parent solution

        References
        ----------
        .. [#] Mistry, K. H.; Hunter, H. a.; Lienhard V, J. H. Effect of         composition and nonideal solution behavior on desalination calculations         for mixed electrolyte solutions with comparison to seawater.         Desalination 2013, 318, 34–47.
        """
        m_effective = 2 * ionic_strength / (self.nu_cation * self.z_cation ** 2 + self.nu_anion * self.z_anion ** 2)
        return m_effective.to('mol/kg')


def _sort_components(Solution, type='all'):
    """
    Sort the components of a solution in descending order (by mol).

    Parameters:
    ----------
    Solution : Solution object
    type     : The type of component to be sorted. Defaults to 'all' for all
                solutes. Other valid arguments are 'cations' and 'anions' which
                return sorted lists of cations and anions, respectively.

    Returns:
    -------
    A list whose keys are the component names (formulas) and whose
    values are the component objects themselves
    
    
    """
    formula_list = []
    for item in Solution.components:
        if type == 'all':
            formula_list.append(item)
        elif type == 'cations':
            if Solution.get_solute(item).get_formal_charge() > 0:
                formula_list.append(item)
        elif type == 'anions' and Solution.get_solute(item).get_formal_charge() < 0:
            formula_list.append(item)
        else:
            mol_list = {}
            for item in formula_list:
                mol_list.update({item: Solution.get_amount(item, 'mol')})

            return sorted(formula_list, key=(mol_list.__getitem__), reverse=True)


def identify_salt(Solution):
    """
    Analyze the components of a solution and identify the salt that most closely
    approximates it.
    (e.g., if a solution contains 0.5 mol/kg of Na+ and Cl-, plus traces of H+
    and OH-, the matched salt is 0.5 mol/kg NaCl)
    
    Create a Salt object for this salt.
    
    Returns:
    -------
    A Salt object.
    """
    sort_list = _sort_components(Solution)
    cation = 'H+'
    anion = 'OH-'
    if len(sort_list) < 3:
        if sort_list[0] == 'H2O':
            logger.info('Salt matching aborted because there are not enough solutes.')
            return Salt(cation, anion)
    if sort_list[0] != 'H2O':
        logger.warning('H2O is not the most prominent component')
    for item in sort_list:
        if chem.get_formal_charge(item) > 0 and cation == 'H+':
            cation = item
        else:
            if chem.get_formal_charge(item) < 0 and anion == 'OH-':
                anion = item
                continue
            return Salt(cation, anion)


def generate_salt_list--- This code section failed: ---

 L. 232         0  BUILD_MAP_0           0 
                2  STORE_FAST               'salt_list'

 L. 235         4  LOAD_GLOBAL              _sort_components
                6  LOAD_FAST                'Solution'
                8  LOAD_STR                 'cations'
               10  LOAD_CONST               ('type',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_FAST               'cation_list'

 L. 236        16  LOAD_GLOBAL              _sort_components
               18  LOAD_FAST                'Solution'
               20  LOAD_STR                 'anions'
               22  LOAD_CONST               ('type',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  STORE_FAST               'anion_list'

 L. 241        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'cation_list'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'len_cat'

 L. 242        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'anion_list'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'len_an'

 L. 245        44  LOAD_CONST               0
               46  STORE_FAST               'index_cat'

 L. 246        48  LOAD_CONST               0
               50  STORE_FAST               'index_an'

 L. 249        52  LOAD_FAST                'Solution'
               54  LOAD_METHOD              get_amount
               56  LOAD_FAST                'cation_list'
               58  LOAD_FAST                'index_cat'
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'unit'
               64  CALL_METHOD_2         2  ''
               66  LOAD_GLOBAL              chem
               68  LOAD_METHOD              get_formal_charge

 L. 250        70  LOAD_FAST                'cation_list'
               72  LOAD_FAST                'index_cat'
               74  BINARY_SUBSCR    

 L. 249        76  CALL_METHOD_1         1  ''
               78  BINARY_MULTIPLY  
               80  STORE_FAST               'c1'

 L. 252        82  LOAD_FAST                'Solution'
               84  LOAD_METHOD              get_amount
               86  LOAD_FAST                'anion_list'
               88  LOAD_FAST                'index_an'
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'unit'
               94  CALL_METHOD_2         2  ''
               96  LOAD_GLOBAL              abs

 L. 253        98  LOAD_GLOBAL              chem
              100  LOAD_METHOD              get_formal_charge
              102  LOAD_FAST                'anion_list'
              104  LOAD_FAST                'index_an'
              106  BINARY_SUBSCR    
              108  CALL_METHOD_1         1  ''

 L. 252       110  CALL_FUNCTION_1       1  ''
              112  BINARY_MULTIPLY  
              114  STORE_FAST               'a1'
            116_0  COME_FROM           410  '410'

 L. 256       116  LOAD_FAST                'index_cat'
              118  LOAD_FAST                'len_cat'
              120  COMPARE_OP               <
          122_124  POP_JUMP_IF_FALSE   568  'to 568'
              126  LOAD_FAST                'index_an'
              128  LOAD_FAST                'len_an'
              130  COMPARE_OP               <
          132_134  POP_JUMP_IF_FALSE   568  'to 568'

 L. 258       136  LOAD_FAST                'c1'
              138  LOAD_FAST                'a1'
              140  COMPARE_OP               >
          142_144  POP_JUMP_IF_FALSE   274  'to 274'

 L. 260       146  LOAD_GLOBAL              Salt
              148  LOAD_FAST                'cation_list'
              150  LOAD_FAST                'index_cat'
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'anion_list'
              156  LOAD_FAST                'index_an'
              158  BINARY_SUBSCR    
              160  CALL_FUNCTION_2       2  ''
              162  STORE_FAST               'x'

 L. 262       164  LOAD_FAST                'a1'
              166  LOAD_GLOBAL              abs
              168  LOAD_FAST                'x'
              170  LOAD_ATTR                z_anion
              172  CALL_FUNCTION_1       1  ''
              174  BINARY_TRUE_DIVIDE
              176  STORE_FAST               'amount'

 L. 264       178  LOAD_FAST                'salt_list'
              180  LOAD_METHOD              update
              182  LOAD_FAST                'x'
              184  LOAD_FAST                'amount'
              186  BUILD_MAP_1           1 
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 266       192  LOAD_FAST                'c1'
              194  LOAD_FAST                'a1'
              196  BINARY_SUBTRACT  
              198  STORE_FAST               'c1'

 L. 268       200  LOAD_FAST                'index_an'
              202  LOAD_CONST               1
              204  INPLACE_ADD      
              206  STORE_FAST               'index_an'

 L. 269       208  SETUP_FINALLY       248  'to 248'

 L. 270       210  LOAD_FAST                'Solution'
              212  LOAD_METHOD              get_amount
              214  LOAD_FAST                'anion_list'
              216  LOAD_FAST                'index_an'
              218  BINARY_SUBSCR    
              220  LOAD_FAST                'unit'
              222  CALL_METHOD_2         2  ''
              224  LOAD_GLOBAL              abs

 L. 271       226  LOAD_GLOBAL              chem
              228  LOAD_METHOD              get_formal_charge
              230  LOAD_FAST                'anion_list'
              232  LOAD_FAST                'index_an'
              234  BINARY_SUBSCR    
              236  CALL_METHOD_1         1  ''

 L. 270       238  CALL_FUNCTION_1       1  ''
              240  BINARY_MULTIPLY  
              242  STORE_FAST               'a1'
              244  POP_BLOCK        
              246  JUMP_FORWARD        274  'to 274'
            248_0  COME_FROM_FINALLY   208  '208'

 L. 273       248  DUP_TOP          
              250  LOAD_GLOBAL              IndexError
              252  COMPARE_OP               exception-match
          254_256  POP_JUMP_IF_FALSE   272  'to 272'
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 274       264  POP_EXCEPT       
              266  JUMP_BACK           116  'to 116'
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           254  '254'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           246  '246'
            274_2  COME_FROM           142  '142'

 L. 276       274  LOAD_FAST                'c1'
              276  LOAD_FAST                'a1'
              278  COMPARE_OP               <
          280_282  POP_JUMP_IF_FALSE   404  'to 404'

 L. 278       284  LOAD_GLOBAL              Salt
              286  LOAD_FAST                'cation_list'
              288  LOAD_FAST                'index_cat'
              290  BINARY_SUBSCR    
              292  LOAD_FAST                'anion_list'
              294  LOAD_FAST                'index_an'
              296  BINARY_SUBSCR    
              298  CALL_FUNCTION_2       2  ''
              300  STORE_FAST               'x'

 L. 280       302  LOAD_FAST                'c1'
              304  LOAD_FAST                'x'
              306  LOAD_ATTR                z_cation
              308  BINARY_TRUE_DIVIDE
              310  STORE_FAST               'amount'

 L. 282       312  LOAD_FAST                'salt_list'
              314  LOAD_METHOD              update
              316  LOAD_FAST                'x'
              318  LOAD_FAST                'amount'
              320  BUILD_MAP_1           1 
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          

 L. 284       326  LOAD_FAST                'a1'
              328  LOAD_FAST                'c1'
              330  BINARY_SUBTRACT  
              332  STORE_FAST               'a1'

 L. 286       334  LOAD_FAST                'index_cat'
              336  LOAD_CONST               1
              338  INPLACE_ADD      
              340  STORE_FAST               'index_cat'

 L. 287       342  SETUP_FINALLY       378  'to 378'

 L. 288       344  LOAD_FAST                'Solution'
              346  LOAD_METHOD              get_amount

 L. 289       348  LOAD_FAST                'cation_list'
              350  LOAD_FAST                'index_cat'
              352  BINARY_SUBSCR    

 L. 289       354  LOAD_FAST                'unit'

 L. 288       356  CALL_METHOD_2         2  ''

 L. 290       358  LOAD_GLOBAL              chem
              360  LOAD_METHOD              get_formal_charge
              362  LOAD_FAST                'cation_list'
              364  LOAD_FAST                'index_cat'
              366  BINARY_SUBSCR    
              368  CALL_METHOD_1         1  ''

 L. 288       370  BINARY_MULTIPLY  
              372  STORE_FAST               'c1'
              374  POP_BLOCK        
              376  JUMP_FORWARD        404  'to 404'
            378_0  COME_FROM_FINALLY   342  '342'

 L. 291       378  DUP_TOP          
              380  LOAD_GLOBAL              IndexError
              382  COMPARE_OP               exception-match
          384_386  POP_JUMP_IF_FALSE   402  'to 402'
              388  POP_TOP          
              390  POP_TOP          
              392  POP_TOP          

 L. 292       394  POP_EXCEPT       
              396  JUMP_BACK           116  'to 116'
              398  POP_EXCEPT       
              400  JUMP_FORWARD        404  'to 404'
            402_0  COME_FROM           384  '384'
              402  END_FINALLY      
            404_0  COME_FROM           400  '400'
            404_1  COME_FROM           376  '376'
            404_2  COME_FROM           280  '280'

 L. 293       404  LOAD_FAST                'c1'
              406  LOAD_FAST                'a1'
              408  COMPARE_OP               ==
              410  POP_JUMP_IF_FALSE   116  'to 116'

 L. 295       412  LOAD_GLOBAL              Salt
              414  LOAD_FAST                'cation_list'
              416  LOAD_FAST                'index_cat'
              418  BINARY_SUBSCR    
              420  LOAD_FAST                'anion_list'
              422  LOAD_FAST                'index_an'
              424  BINARY_SUBSCR    
              426  CALL_FUNCTION_2       2  ''
              428  STORE_FAST               'x'

 L. 297       430  LOAD_FAST                'c1'
              432  LOAD_FAST                'x'
              434  LOAD_ATTR                z_cation
              436  BINARY_TRUE_DIVIDE
              438  STORE_FAST               'amount'

 L. 299       440  LOAD_FAST                'salt_list'
              442  LOAD_METHOD              update
              444  LOAD_FAST                'x'
              446  LOAD_FAST                'amount'
              448  BUILD_MAP_1           1 
              450  CALL_METHOD_1         1  ''
              452  POP_TOP          

 L. 301       454  LOAD_FAST                'index_an'
              456  LOAD_CONST               1
              458  INPLACE_ADD      
              460  STORE_FAST               'index_an'

 L. 302       462  LOAD_FAST                'index_cat'
              464  LOAD_CONST               1
              466  INPLACE_ADD      
              468  STORE_FAST               'index_cat'

 L. 303       470  SETUP_FINALLY       540  'to 540'

 L. 304       472  LOAD_FAST                'Solution'
              474  LOAD_METHOD              get_amount

 L. 305       476  LOAD_FAST                'cation_list'
              478  LOAD_FAST                'index_cat'
              480  BINARY_SUBSCR    

 L. 305       482  LOAD_FAST                'unit'

 L. 304       484  CALL_METHOD_2         2  ''

 L. 306       486  LOAD_GLOBAL              chem
              488  LOAD_METHOD              get_formal_charge
              490  LOAD_FAST                'cation_list'
              492  LOAD_FAST                'index_cat'
              494  BINARY_SUBSCR    
              496  CALL_METHOD_1         1  ''

 L. 304       498  BINARY_MULTIPLY  
              500  STORE_FAST               'c1'

 L. 307       502  LOAD_FAST                'Solution'
              504  LOAD_METHOD              get_amount
              506  LOAD_FAST                'anion_list'
              508  LOAD_FAST                'index_an'
              510  BINARY_SUBSCR    
              512  LOAD_FAST                'unit'
              514  CALL_METHOD_2         2  ''
              516  LOAD_GLOBAL              abs

 L. 308       518  LOAD_GLOBAL              chem
              520  LOAD_METHOD              get_formal_charge
              522  LOAD_FAST                'anion_list'
              524  LOAD_FAST                'index_an'
              526  BINARY_SUBSCR    
              528  CALL_METHOD_1         1  ''

 L. 307       530  CALL_FUNCTION_1       1  ''
              532  BINARY_MULTIPLY  
              534  STORE_FAST               'a1'
              536  POP_BLOCK        
              538  JUMP_BACK           116  'to 116'
            540_0  COME_FROM_FINALLY   470  '470'

 L. 310       540  DUP_TOP          
              542  LOAD_GLOBAL              IndexError
              544  COMPARE_OP               exception-match
          546_548  POP_JUMP_IF_FALSE   564  'to 564'
              550  POP_TOP          
              552  POP_TOP          
              554  POP_TOP          

 L. 311       556  POP_EXCEPT       
              558  JUMP_BACK           116  'to 116'
              560  POP_EXCEPT       
              562  JUMP_BACK           116  'to 116'
            564_0  COME_FROM           546  '546'
              564  END_FINALLY      
              566  JUMP_BACK           116  'to 116'
            568_0  COME_FROM           132  '132'
            568_1  COME_FROM           122  '122'

 L. 313       568  LOAD_FAST                'salt_list'
              570  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 268


def _trim_formal_charge(formula):
    """
    remove the formal charge from a chemical formula
    
    Examples:
    --------
    >>> _trim_formal_charge('Fe+++')
    'Fe'
    >>> _trim_formal_charge('SO4-2')
    'SO4'
    >>> _trim_formal_charge('Na+')
    'Na'
    
    """
    charge = chem.get_formal_charge(formula)
    output = ''
    if charge > 0:
        output = formula.split('+')[0]
    elif charge < 0:
        output = formula.split('-')[0]
    return output