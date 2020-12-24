# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/accounting/accounting.py
# Compiled at: 2016-02-29 16:10:37
"""Base Project Module.

The MIT License (MIT)

Copyright (c) 2016 Ojengwa Bernard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re
from .utils import is_str, check_type, is_num

class Accounting(object):
    """docstring for Accounting.

    Attributes:
        settings (dict): The library's settings configuration object. Contains
         default parameters for currency and number formatting
    """

    def __init__(self, options={}):
        """
        Summary.

        Args:
            options (dict, optional): settings configuration object.
        """
        settings = {'currency': {'symbol': '$', 
                        'format': '%s%v', 
                        'decimal': '.', 
                        'thousand': ',', 
                        'precision': 2, 
                        'grouping': 3}, 
           'number': {'precision': 0, 
                      'grouping': 3, 
                      'thousand': ',', 
                      'decimal': '.'}}
        if options:
            settings.update(options)
        self.settings = settings

    def _check_currency_format(self, format=None):
        """
        Summary.

        Args:
            format (TYPE, optional): Description

        Returns:
            name (TYPE): Description
        """
        defaults = self.settings['currency']['format']
        if hasattr(format, '__call__'):
            format = format()
        if is_str(format) and re.match('%v', format):
            return {'pos': format, 
               'neg': format.replace('-', '').replace('%v', '-%v'), 
               'zero': format}
        if not format or not format['por'] or not re.match('%v', format['pos']):
            self.settings['currency']['format'] = {'pos': defaults, 'neg': defaults.replace('%v', '-%v'), 
               'zero': defaults}
            return self.settings
        return format

    def _check_precision(self, val, base=0):
        """
        Check and normalise the value of precision (must be positive integer).

        Args:
            val (INT): must be positive integer
            base (INT): Description

        Returns:
            VAL (INT): Description
        """
        if not isinstance(val, int):
            raise TypeError('The first argument must be an integer.')
        val = round(abs(val))
        val = (lambda num: base if is_num(num) else num)(val)
        return val

    def parse(self, value, decimal=None):
        """
        Summary.

         Takes a string/array of strings, removes all formatting/cruft and
         returns the raw float value

         Decimal must be included in the regular expression to match floats
          (defaults to Accounting.settings.number.decimal),
          so if the number uses a non-standard decimal
         separator, provide it as the second argument.
         *
         Also matches bracketed negatives (eg. "$ (1.99)" => -1.99)

         Doesn't throw any errors (`None`s become 0) but this may change

        Args:
            value (TYPE): Description
            decimal (TYPE): Description

        Returns:
            name (TYPE): Description
        """
        value = value or 0
        if check_type(value, 'list'):
            return map(lambda val: self.parse(val, decimal))
        if check_type(value, 'int') or check_type(value, 'float'):
            return value
        decimal = decimal or self.settings.number.decimal
        regex = re.compile('[^0-9-' + decimal + ']')
        unformatted = str(value)
        unformatted = re.sub('/\\((.*)\\)/', '-$1', unformatted)
        unformatted = re.sub(regex, '', unformatted)
        unformatted = unformatted.replace('.', decimal)
        formatted = (lambda val: unformatted if val else 0)(is_num(unformatted))
        return formatted

    def to_fixed(self, value, precision):
        """Implementation that treats floats more like decimals.

        Fixes binary rounding issues (eg. (0.615).toFixed(2) === "0.61")
        that present problems for accounting and finance-related software.

        """
        precision = self._check_precision(precision, self.settings['number']['precision'])
        power = pow(10, precision)
        power = round(self.parse(value) * power) / power
        return ('{0} {1}.{2}f').format(value, precision, precision)

    def format(self, number, **kwargs):
        """Format a given number.

        Format a number, with comma-separated thousands and
        custom precision/decimal places

        Localise by overriding the precision and thousand / decimal separators
        2nd parameter `precision` can be an object matching `settings.number`

        Args:
            number (TYPE): Description
            precision (TYPE): Description
            thousand (TYPE): Description
            decimal (TYPE): Description

        Returns:
            name (TYPE): Description
        """
        if check_type(number, 'list'):
            return map(lambda val: self.format(val, **kwargs))
        number = self.parse(number)
        if check_type(kwargs, 'dict'):
            options = self.settings['number'].update(kwargs)
        precision = self._check_precision(options['precision'])
        negative = (lambda num: '-' if num < 0 else '')(number)
        base = str(int(self.to_fixed(abs(number) or 0, precision)), 10)
        mod = (lambda num: len(num) % 3 if len(num) > 3 else 0)(base)
        num = negative + (lambda num: base[0:num] if num else '')(mod)
        num += re.sub('/(\\d{3})(?=\\d)/g', '$1' + options['thousand'], base[mod:])
        num += (lambda val: options['decimal'] + self.to_fixed(abs(number), precision).split('.')[1] if val else '')(precision)
        return num

    def as_money(self, number, **options):
        """Format a number into currency.

        Usage: accounting.formatMoney(number, symbol, precision, thousandsSep,
                                      decimalSep, format)
        defaults: (0, "$", 2, ",", ".", "%s%v")
        Localise by overriding the symbol, precision,
        thousand / decimal separators and format
        Second param can be an object matching `settings.currency`
        which is the easiest way.

        Args:
            number (TYPE): Description
            precision (TYPE): Description
            thousand (TYPE): Description
            decimal (TYPE): Description

        Returns:
            name (TYPE): Description
        """
        if isinstance(number, list):
            return map(lambda val: self.as_money(val, **options))
        decimal = options.get('decimal')
        number = self.parse(number, decimal)
        if check_type(options, 'dict'):
            options = self.settings['currency'].update(options)
        formats = self._check_currency_format(options['format'])
        use_format = (--- This code section failed: ---

 L. 262         0  LOAD_FAST             0  'num'
                3  LOAD_CONST               0
                6  COMPARE_OP            4  >
                9  POP_JUMP_IF_FALSE    20  'to 20'
               12  LOAD_DEREF            0  'formats'
               15  LOAD_CONST               'pos'
               18  BINARY_SUBSCR    
               19  RETURN_END_IF_LAMBDA
             20_0  COME_FROM             9  '9'

 L. 263        20  LOAD_FAST             0  'num'
               23  LOAD_CONST               0
               26  COMPARE_OP            0  <
               29  POP_JUMP_IF_FALSE    40  'to 40'
               32  LOAD_DEREF            0  'formats'
               35  LOAD_CONST               'neg'
               38  BINARY_SUBSCR    
               39  RETURN_END_IF_LAMBDA
             40_0  COME_FROM            29  '29'
               40  LOAD_DEREF            0  'formats'
               43  LOAD_CONST               'zero'
               46  BINARY_SUBSCR    
               47  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `RETURN_END_IF_LAMBDA' instruction at offset 39
)(number)
        precision = self._check_precision(number, options['precision'])
        thousands = options['thousand']
        decimal = options['decimal']
        formater = self.format(abs(number), precision, thousands, decimal)
        amount = use_format.replace('%s', options['symbol']).replace('%v', formater)
        return amount