# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/parameter.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 16593 bytes
__doc__ = '\nThis module implements the Parameter() class, which is used to store\nvalues, units, uncertainties, and reference data for various quantities\nused throughout pyEQL.\n\n:copyright: 2013-2020 by Ryan S. Kingsbury\n:license: LGPL, see LICENSE for more details.\n\n'
import logging, os
from pint import UnitRegistry
from pyEQL.logging_system import Unique
logger = logging.getLogger(__name__)
unique = Unique()
logger.addFilter(unique)
ch = logging.StreamHandler()
formatter = logging.Formatter('(%(name)s) - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
unit = UnitRegistry()
unit.autoconvert_offset_to_baseunit = True
directory = os.path.dirname(__file__)
unit.load_definitions(directory + '/pint_custom_units.txt')
unit.enable_contexts('chem')
unit.default_format = 'P~'

def testfunc--- This code section failed: ---

 L.  56         0  BUILD_LIST_0          0 
                2  STORE_FAST               'list'

 L.  57         4  SETUP_FINALLY        34  'to 34'

 L.  58         6  LOAD_FAST                'list'
                8  LOAD_METHOD              append
               10  LOAD_GLOBAL              float
               12  LOAD_FAST                'val'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_GLOBAL              unit
               18  LOAD_STR                 ''
               20  CALL_FUNCTION_1       1  ''
               22  BINARY_MULTIPLY  
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.  59        28  LOAD_FAST                'list'
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY     4  '4'

 L.  60        34  DUP_TOP          
               36  LOAD_GLOBAL              ValueError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    62  'to 62'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  61        48  LOAD_GLOBAL              print
               50  LOAD_STR                 'Value Error'
               52  CALL_FUNCTION_1       1  ''
               54  POP_TOP          

 L.  62        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            40  '40'
               62  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 30


class Parameter:
    """Parameter"""

    def __init__--- This code section failed: ---

 L. 161         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               name

 L. 162         6  LOAD_STR                 ''
                8  STORE_FAST               'use_units'

 L. 166        10  LOAD_FAST                'units'
               12  LOAD_STR                 'None'
               14  COMPARE_OP               ==

 L. 165        16  POP_JUMP_IF_TRUE     42  'to 42'

 L. 167        18  LOAD_FAST                'units'
               20  LOAD_STR                 'none'
               22  COMPARE_OP               ==

 L. 165        24  POP_JUMP_IF_TRUE     42  'to 42'

 L. 168        26  LOAD_FAST                'units'
               28  LOAD_STR                 ''
               30  COMPARE_OP               ==

 L. 165        32  POP_JUMP_IF_TRUE     42  'to 42'

 L. 169        34  LOAD_FAST                'units'
               36  LOAD_STR                 'dimensionless'
               38  COMPARE_OP               ==

 L. 165        40  POP_JUMP_IF_FALSE    48  'to 48'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM            24  '24'
             42_2  COME_FROM            16  '16'

 L. 171        42  LOAD_STR                 'dimensionless'
               44  STORE_FAST               'use_units'
               46  JUMP_FORWARD         52  'to 52'
             48_0  COME_FROM            40  '40'

 L. 173        48  LOAD_FAST                'units'
               50  STORE_FAST               'use_units'
             52_0  COME_FROM            46  '46'

 L. 177        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                'magnitude'
               56  LOAD_GLOBAL              tuple
               58  LOAD_GLOBAL              list
               60  BUILD_TUPLE_2         2 
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE   184  'to 184'

 L. 179        66  BUILD_LIST_0          0 
               68  STORE_FAST               'temp_list'

 L. 180        70  LOAD_FAST                'magnitude'
               72  GET_ITER         
               74  FOR_ITER            172  'to 172'
               76  STORE_FAST               'item'

 L. 181        78  SETUP_FINALLY       106  'to 106'

 L. 182        80  LOAD_FAST                'temp_list'
               82  LOAD_METHOD              append
               84  LOAD_GLOBAL              float
               86  LOAD_FAST                'item'
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_GLOBAL              unit
               92  LOAD_FAST                'use_units'
               94  CALL_FUNCTION_1       1  ''
               96  BINARY_MULTIPLY  
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  POP_BLOCK        
              104  JUMP_BACK            74  'to 74'
            106_0  COME_FROM_FINALLY    78  '78'

 L. 183       106  DUP_TOP          
              108  LOAD_GLOBAL              ValueError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   168  'to 168'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 184       120  LOAD_GLOBAL              print
              122  LOAD_STR                 'Value Error on %s'
              124  LOAD_FAST                'item'
              126  BINARY_MODULO    
              128  CALL_FUNCTION_1       1  ''
              130  POP_TOP          

 L. 186       132  LOAD_FAST                'use_units'
              134  LOAD_STR                 'dimensionless'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_TRUE    154  'to 154'

 L. 187       140  LOAD_GLOBAL              logger
              142  LOAD_METHOD              error

 L. 188       144  LOAD_STR                 'A non-numeric parameter cannot have units, but units of %s were specified'

 L. 189       146  LOAD_FAST                'units'

 L. 188       148  BINARY_MODULO    

 L. 187       150  CALL_METHOD_1         1  ''
              152  POP_TOP          
            154_0  COME_FROM           138  '138'

 L. 191       154  LOAD_FAST                'temp_list'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'item'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  POP_EXCEPT       
              166  JUMP_BACK            74  'to 74'
            168_0  COME_FROM           112  '112'
              168  END_FINALLY      
              170  JUMP_BACK            74  'to 74'

 L. 194       172  LOAD_GLOBAL              tuple
              174  LOAD_FAST                'temp_list'
              176  CALL_FUNCTION_1       1  ''
              178  LOAD_FAST                'self'
              180  STORE_ATTR               value
              182  JUMP_FORWARD        256  'to 256'
            184_0  COME_FROM            64  '64'

 L. 199       184  SETUP_FINALLY       208  'to 208'

 L. 200       186  LOAD_GLOBAL              float
              188  LOAD_FAST                'magnitude'
              190  CALL_FUNCTION_1       1  ''
              192  LOAD_GLOBAL              unit
              194  LOAD_FAST                'use_units'
              196  CALL_FUNCTION_1       1  ''
              198  BINARY_MULTIPLY  
              200  LOAD_FAST                'self'
              202  STORE_ATTR               value
              204  POP_BLOCK        
              206  JUMP_FORWARD        256  'to 256'
            208_0  COME_FROM_FINALLY   184  '184'

 L. 201       208  DUP_TOP          
              210  LOAD_GLOBAL              ValueError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   254  'to 254'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 203       222  LOAD_FAST                'use_units'
              224  LOAD_STR                 'dimensionless'
              226  COMPARE_OP               ==
              228  POP_JUMP_IF_TRUE    244  'to 244'

 L. 204       230  LOAD_GLOBAL              logger
              232  LOAD_METHOD              error

 L. 205       234  LOAD_STR                 'A non-numeric parameter cannot have units, but units of %s were specified'

 L. 206       236  LOAD_FAST                'units'

 L. 205       238  BINARY_MODULO    

 L. 204       240  CALL_METHOD_1         1  ''
              242  POP_TOP          
            244_0  COME_FROM           228  '228'

 L. 209       244  LOAD_FAST                'magnitude'
              246  LOAD_FAST                'self'
              248  STORE_ATTR               value
              250  POP_EXCEPT       
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           214  '214'
              254  END_FINALLY      
            256_0  COME_FROM           252  '252'
            256_1  COME_FROM           206  '206'
            256_2  COME_FROM           182  '182'

 L. 212       256  LOAD_STR                 'Not specified'
              258  LOAD_FAST                'self'
              260  STORE_ATTR               base_temperature

 L. 213       262  LOAD_STR                 'Not specified'
              264  LOAD_FAST                'self'
              266  STORE_ATTR               base_pressure

 L. 214       268  LOAD_STR                 'Not specified'
              270  LOAD_FAST                'self'
              272  STORE_ATTR               base_ionic_strength

 L. 216       274  LOAD_STR                 'temperature'
              276  LOAD_FAST                'kwargs'
              278  COMPARE_OP               in
          280_282  POP_JUMP_IF_FALSE   318  'to 318'
              284  LOAD_FAST                'kwargs'
              286  LOAD_STR                 'temperature'
              288  BINARY_SUBSCR    
              290  LOAD_STR                 ''
              292  COMPARE_OP               !=
          294_296  POP_JUMP_IF_FALSE   318  'to 318'

 L. 217       298  LOAD_CONST               True
              300  LOAD_FAST                'self'
              302  STORE_ATTR               temperature_set

 L. 218       304  LOAD_GLOBAL              unit
              306  LOAD_FAST                'kwargs'
              308  LOAD_STR                 'temperature'
              310  BINARY_SUBSCR    
              312  CALL_FUNCTION_1       1  ''
              314  LOAD_FAST                'self'
              316  STORE_ATTR               base_temperature
            318_0  COME_FROM           294  '294'
            318_1  COME_FROM           280  '280'

 L. 219       318  LOAD_STR                 'pressure'
              320  LOAD_FAST                'kwargs'
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   362  'to 362'
              328  LOAD_FAST                'kwargs'
              330  LOAD_STR                 'pressure'
              332  BINARY_SUBSCR    
              334  LOAD_STR                 ''
              336  COMPARE_OP               !=
          338_340  POP_JUMP_IF_FALSE   362  'to 362'

 L. 220       342  LOAD_CONST               True
              344  LOAD_FAST                'self'
              346  STORE_ATTR               pressure_set

 L. 221       348  LOAD_GLOBAL              unit
              350  LOAD_FAST                'kwargs'
              352  LOAD_STR                 'pressure'
              354  BINARY_SUBSCR    
              356  CALL_FUNCTION_1       1  ''
              358  LOAD_FAST                'self'
              360  STORE_ATTR               base_pressure
            362_0  COME_FROM           338  '338'
            362_1  COME_FROM           324  '324'

 L. 222       362  LOAD_STR                 'ionic_strength'
              364  LOAD_FAST                'kwargs'
              366  COMPARE_OP               in
          368_370  POP_JUMP_IF_FALSE   406  'to 406'
              372  LOAD_FAST                'kwargs'
              374  LOAD_STR                 'ionic_strength'
              376  BINARY_SUBSCR    
              378  LOAD_STR                 ''
              380  COMPARE_OP               !=
          382_384  POP_JUMP_IF_FALSE   406  'to 406'

 L. 223       386  LOAD_CONST               True
              388  LOAD_FAST                'self'
              390  STORE_ATTR               ionic_strength_set

 L. 224       392  LOAD_GLOBAL              unit
              394  LOAD_FAST                'kwargs'
              396  LOAD_STR                 'ionic_strength'
              398  BINARY_SUBSCR    
              400  CALL_FUNCTION_1       1  ''
              402  LOAD_FAST                'self'
              404  STORE_ATTR               base_ionic_strength
            406_0  COME_FROM           382  '382'
            406_1  COME_FROM           368  '368'

 L. 227       406  LOAD_STR                 'Not specified'
              408  LOAD_FAST                'self'
              410  STORE_ATTR               reference

 L. 228       412  LOAD_STR                 ''
              414  LOAD_FAST                'self'
              416  STORE_ATTR               description

 L. 229       418  LOAD_STR                 ''
              420  LOAD_FAST                'self'
              422  STORE_ATTR               comment

 L. 231       424  LOAD_STR                 'reference'
              426  LOAD_FAST                'kwargs'
              428  COMPARE_OP               in
          430_432  POP_JUMP_IF_FALSE   444  'to 444'

 L. 232       434  LOAD_FAST                'kwargs'
              436  LOAD_STR                 'reference'
              438  BINARY_SUBSCR    
              440  LOAD_FAST                'self'
              442  STORE_ATTR               reference
            444_0  COME_FROM           430  '430'

 L. 233       444  LOAD_STR                 'description'
              446  LOAD_FAST                'kwargs'
              448  COMPARE_OP               in
          450_452  POP_JUMP_IF_FALSE   464  'to 464'

 L. 234       454  LOAD_FAST                'kwargs'
              456  LOAD_STR                 'description'
              458  BINARY_SUBSCR    
              460  LOAD_FAST                'self'
              462  STORE_ATTR               description
            464_0  COME_FROM           450  '450'

 L. 235       464  LOAD_STR                 'comment'
              466  LOAD_FAST                'kwargs'
              468  COMPARE_OP               in
          470_472  POP_JUMP_IF_FALSE   484  'to 484'

 L. 236       474  LOAD_FAST                'kwargs'
              476  LOAD_STR                 'comment'
              478  BINARY_SUBSCR    
              480  LOAD_FAST                'self'
              482  STORE_ATTR               comment
            484_0  COME_FROM           470  '470'

Parse error at or near `JUMP_FORWARD' instruction at offset 46

    def get_name(self):
        """
        Return the name of the parameter.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The name of the parameter
        """
        return self.name

    def get_value(self, temperature=None, pressure=None, ionic_strength=None):
        """
        Return the value of a parameter at the specified conditions.

        Parameters
        ----------
        temperature : str, optional
                    The temperature at which 'magnitude' was measured in degrees Celsius.
                    Specify the temperature as a string containing the magnitude and
                    a unit, e.g. '25 degC', '32 degF', '298 kelvin', and '500 degR'
        pressure : str, optional
                    The pressure at which 'magnitude' was measured in Pascals
                    Specify the pressure as a string containing the magnitude and a
                    unit. e.g. '101 kPa'.
                    Typical valid units are 'Pa', 'atm', or 'torr'.
        ionic_strength : str, optional
                    The ionic strength of the solution in which 'magnitude' was measured. Specify
                    the ionic strength as a string containing the magnitude and a unit. e.g. '2 mol/kg'

        Returns
        -------
        Quantity
            The value of the parameter at the specified conditions.

        """
        if temperature is None:
            temperature = self.base_temperature
            logger.info('Temperature not specified for ' + str(self.name) + '. Returning value at ' + str(temperature) + '.')
        else:
            temperature = unit(temperature)
        if pressure is None:
            pressure = self.base_pressure
            logger.info('Pressure not specified for ' + str(self.name) + '. Returning value at ' + str(pressure) + '.')
        else:
            pressure = unit(pressure)
        if ionic_strength is None:
            ionic_strength = self.base_ionic_strength
            logger.info('Ionic Strength not specified for ' + str(self.name) + '. Returning value at ' + str(ionic_strength) + '.')
        else:
            ionic_strength = unit(ionic_strength)
        if temperature != self.base_temperature:
            logger.warning('Requested temperature for ' + str(self.name) + ' (' + str(temperature) + ') differs from measurement conditions.' + 'Returning value at ' + str(self.base_temperature))
        if pressure != self.base_pressure:
            logger.warning('Requested pressure for ' + str(self.name) + ' (' + str(pressure) + ') differs from measurement conditions.' + 'Returning value at ' + str(self.base_pressure))
        if ionic_strength != self.base_ionic_strength:
            logger.warning('Requested ionic strength for ' + str(self.name) + ' (' + str(ionic_strength) + ') differs from measurement conditions.' + 'Returning value at ' + str(self.base_ionic_strength))
        return self.value

    def get_magnitude(self, temperature=None, pressure=None, ionic_strength=None):
        """
        Return the magnitude of a parameter at the specified conditions.

        Parameters
        ----------
        temperature : str, optional
                    The temperature at which 'magnitude' was measured in degrees Celsius.
                    Specify the temperature as a string containing the magnitude and
                    a unit, e.g. '25 degC', '32 degF', '298 kelvin', and '500 degR'
        pressure : str, optional
                    The pressure at which 'magnitude' was measured in Pascals
                    Specify the pressure as a string containing the magnitude and a
                    unit. e.g. '101 kPa'.
                    Typical valid units are 'Pa', 'atm', or 'torr'.
        ionic_strength : str, optional
                    The ionic strength of the solution in which 'magnitude' was measured. Specify
                    the ionic strength as a string containing the magnitude and a unit. e.g. '2 mol/kg'

        Returns
        -------
        Number
            The magnitude of the parameter at the specified conditions.

        """
        return self.get_value(temperature, pressure, ionic_strength).magnitude

    def get_units(self):
        """
        Return the units of a parameter
        """
        return self.get_value().units

    def get_dimensions(self):
        """
        Return the dimensions of the parameter.
        """
        return self.get_value().dimensionality

    def __str__(self):
        """
        Set the output of the print() statement for a parameter value
        """
        return '\n----------------------------------------------------------------------------\nParameter ' + str(self.name) + '\n\n' + str(self.description) + '\nValue: ' + str(self.get_value()) + '\n' + 'Conditions (T,P,Ionic Strength): ' + str(self.base_temperature) + ', ' + str(self.base_pressure) + ', ' + str(self.base_ionic_strength) + '\n' + 'Notes: ' + str(self.comment) + '\n' + 'Reference: ' + str(self.reference) + '\n' + '--------------------------------------------------------------------------------------' + '\n'