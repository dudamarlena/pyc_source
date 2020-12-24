# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/currency.py
# Compiled at: 2015-07-18 19:38:10
__doc__ = '$id$'
__version__ = '$Revision$'[11:-2]
import types, re, string
currency_match = re.compile('^\\s*([\\(\\+\\-])?\\s*([A-Za-z][A-Za-z][A-Za-z])?(\\s*)([-+]?[\\d\\.\\, ]+)?\\s*([\\)])?\\s*$')
_CURRENCY_META = {'Afghanistan': 'AFA', 
   'Albania': 'ALL', 
   'Algeria': 'DZD', 
   'American Samoa': 'USD', 
   'Andorra': 'EUR', 
   'Angola': 'AOA', 
   'Anguilla': 'XCD', 
   'Antigua and Barbuda': 'XCD', 
   'Argentina': 'ARS', 
   'Armenia': 'AMD', 
   'Aruba': 'AWG', 
   'Australia': 'AUD', 
   'Austria': 'EUR', 
   'Azerbaijan': 'AZM', 
   'Bahamas, The': 'BSD', 
   'Bahrain': 'BHD', 
   'Bangladesh': 'BDT', 
   'Barbados': 'BBD', 
   'Belarus': 'BYR', 
   'Belgium': 'EUR', 
   'Benin': 'XOF', 
   'Bermuda': 'BMD', 
   'Bhutan': 'BTN; INR', 
   'Bolivia': 'BOB', 
   'Bosnia and Herzegovina': 'BAM', 
   'Botswana': 'BWP', 
   'Brazil': 'BRL', 
   'British Virgin Islands': 'USD', 
   'Brunei': 'BND', 
   'Bulgaria': 'BGL', 
   'Burkina Faso': 'XOF', 
   'Burma': 'MMK', 
   'Burundi': 'BIF', 
   'Cambodia': 'KHR', 
   'Cameroon': 'XAF', 
   'Canada': 'CAD', 
   'Cape Verde': 'CVE', 
   'Cayman Islands': 'KYD', 
   'Central African Republic': 'XAF', 
   'Chad': 'XAF', 
   'Chile': 'CLP', 
   'China': 'CNY', 
   'Christmas Island': 'AUD', 
   'Cocos (Keeling) Islands': 'AUD', 
   'Colombia': 'COP', 
   'Comoros': 'KMF', 
   'Congo, Democratic Republic of the': 'CDF', 
   'Congo, Republic of the': 'XAF', 
   'Cook Islands': 'NZD', 
   'Costa Rica': 'CRC', 
   'Cote dIvoire': 'XOF', 
   'Croatia': 'HRK', 
   'Cuba': 'CUP', 
   'Cyprus': 'CYP; TRL', 
   'Czech Republic': 'CZK', 
   'Denmark': 'DKK', 
   'Djibouti': 'DJF', 
   'Dominica': 'XCD', 
   'Dominican Republic': 'DOP', 
   'East Timor': 'USD', 
   'Ecuador': 'USD', 
   'Egypt': 'EGP', 
   'El Salvador': 'SVC; USD', 
   'Equatorial Guinea': 'XAF', 
   'Eritrea': 'ERN', 
   'Estonia': 'EEK', 
   'Ethiopia': 'ETB', 
   'Falkland Islands (Islas Malvinas)': 'FKP', 
   'Faroe Islands': 'DKK', 
   'Fiji': 'FJD', 
   'Finland': 'FIM; EUR', 
   'France': 'EUR', 
   'French Guiana': 'EUR', 
   'French Polynesia': 'XPF', 
   'Gabon': 'XAF', 
   'Gambia, The': 'GMD', 
   'Gaza Strip': 'ILS', 
   'Georgia': 'GEL', 
   'Germany': 'EUR', 
   'Ghana': 'GHC', 
   'Gibraltar': 'GIP', 
   'Greece': 'EUR; GRD', 
   'Greenland': 'DKK', 
   'Grenada': 'XCD', 
   'Guadeloupe': 'EUR', 
   'Guam': 'USD', 
   'Guatemala': 'GTQ; USD', 
   'Guernsey': 'GBP', 
   'Guinea': 'GNF', 
   'Guinea-Bissau': 'XOF; GWP', 
   'Guyana': 'GYD', 
   'Haiti': 'HTG', 
   'Holy See (Vatican City)': 'EUR', 
   'Honduras': 'HNL', 
   'Hong Kong': 'HKD', 
   'Hungary': 'HUF', 
   'Iceland': 'ISK', 
   'India': 'INR', 
   'Indonesia': 'IDR', 
   'Iran': 'IRR', 
   'Iraq': 'IQD', 
   'Ireland': 'EUR', 
   'Israel': 'ILS', 
   'Italy': 'EUR', 
   'Jamaica': 'JMD', 
   'Japan': 'JPY', 
   'Jersey': 'GBP', 
   'Jordan': 'JOD', 
   'Kazakhstan': 'KZT', 
   'Kenya': 'KES', 
   'Kiribati': 'AUD', 
   'Korea, North': 'KPW', 
   'Korea, South': 'KRW', 
   'Kuwait': 'KWD', 
   'Kyrgyzstan': 'KGS', 
   'Laos': 'LAK', 
   'Latvia': 'LVL', 
   'Lebanon': 'LBP', 
   'Lesotho': 'LSL; ZAR', 
   'Liberia': 'LRD', 
   'Libya': 'LYD', 
   'Liechtenstein': 'CHF', 
   'Lithuania': 'LTL', 
   'Luxembourg': 'EUR', 
   'Macau': 'MOP', 
   'Macedonia, The Former Yugoslav Republic of': 'MKD', 
   'Madagascar': 'MGF', 
   'Malawi': 'MWK', 
   'Malaysia': 'MYR', 
   'Maldives': 'MVR', 
   'Mali': 'XOF', 
   'Malta': 'MTL', 
   'Man, Isle of': 'GBP', 
   'Marshall Islands': 'USD', 
   'Martinique': 'EUR', 
   'Mauritania': 'MRO', 
   'Mauritius': 'MUR', 
   'Mayotte': 'EUR', 
   'Mexico': 'MXN', 
   'Micronesia, Federated States of': 'USD', 
   'Moldova': 'MDL', 
   'Monaco': 'EUR', 
   'Mongolia': 'MNT', 
   'Montserrat': 'XCD', 
   'Morocco': 'MAD', 
   'Mozambique': 'MZM', 
   'Namibia': 'NAD; ZAR', 
   'Nauru': 'AUD', 
   'Nepal': 'NPR', 
   'Netherlands': 'EUR', 
   'Netherlands Antilles': 'ANG', 
   'New Caledonia': 'XPF', 
   'New Zealand': 'NZD', 
   'Nicaragua': 'NIO', 
   'Niger': 'XOF', 
   'Nigeria': 'NGN', 
   'Niue': 'NZD', 
   'Norfolk Island': 'AUD', 
   'Northern Mariana Islands': 'USD', 
   'Norway': 'NOK', 
   'Oman': 'OMR', 
   'Pakistan': 'PKR', 
   'Palau': 'USD', 
   'Panama': 'PAB; USD', 
   'Papua New Guinea': 'PGK', 
   'Paraguay': 'PYG', 
   'Peru': 'PEN', 
   'Philippines': 'PHP', 
   'Pitcairn Islands': 'NZD', 
   'Poland': 'PLN', 
   'Portugal': 'EUR', 
   'Puerto Rico': 'USD', 
   'Qatar': 'QAR', 
   'Reunion': 'EUR', 
   'Romania': 'ROL', 
   'Russia': 'RUR', 
   'Rwanda': 'RWF', 
   'Saint Helena': 'SHP', 
   'Saint Kitts and Nevis': 'XCD', 
   'Saint Lucia': 'XCD', 
   'Saint Pierre and Miquelon': 'EUR', 
   'Saint Vincent and the Grenadines': 'XCD', 
   'Samoa': 'WST', 
   'San Marino': 'EUR', 
   'Sao Tome and Principe': 'STD', 
   'Saudi Arabia': 'SAR', 
   'Senegal': 'XOF', 
   'Seychelles': 'SCR', 
   'Sierra Leone': 'SLL', 
   'Singapore': 'SGD', 
   'Slovakia': 'SKK', 
   'Slovenia': 'SIT', 
   'Solomon Islands': 'SBD', 
   'Somalia': 'SOS', 
   'South Africa': 'ZAR', 
   'Spain': 'EUR', 
   'Sri Lanka': 'LKR', 
   'Sudan': 'SDD', 
   'Suriname': 'SRG', 
   'Svalbard': 'NOK', 
   'Swaziland': 'SZL', 
   'Sweden': 'SEK', 
   'Switzerland': 'CHF', 
   'Syria': 'SYP', 
   'Taiwan': 'TWD', 
   'Tajikistan': 'SM', 
   'Tanzania': 'TZS', 
   'Thailand': 'THB', 
   'Togo': 'XOF', 
   'Tokelau': 'NZD', 
   'Tonga': 'TOP', 
   'Trinidad and Tobago': 'TTD', 
   'Tunisia': 'TND', 
   'Turkey': 'TRL', 
   'Turkmenistan': 'TMM', 
   'Turks and Caicos Islands': 'USD', 
   'Tuvalu': 'AUD', 
   'Uganda': 'UGX', 
   'Ukraine': 'UAH', 
   'United Arab Emirates': 'AED', 
   'United Kingdom': 'GBP', 
   'United States': 'USD', 
   'Uruguay': 'UYU', 
   'Uzbekistan': 'UZS', 
   'Vanuatu': 'VUV', 
   'Venezuela': 'VEB', 
   'Vietnam': 'VND', 
   'Virgin Islands': 'USD', 
   'Wallis and Futuna': 'XPF', 
   'West Bank': 'ILS; JOD', 
   'Western Sahara': 'MAD', 
   'Yemen': 'YER', 
   'Yugoslavia': 'YUM', 
   'Zambia': 'ZMK', 
   'Zimbabwe': 'ZWD'}
CURRENCIES = []
_CURRENCY_DECIMALS = {'BHD': 3, 
   'BIF': 0, 'BYR': 0, 'CLP': 0, 'DJF': 0, 'GNF': 0, 'IQD': 3, 'JOD': 3, 
   'JPY': 0, 'KMF': 0, 'KRW': 0, 'KWD': 3, 'LYD': 3, 'OMR': 3, 'PYG': 0, 
   'RWF': 0, 'TND': 3, 'VUV': 0, 'XAF': 0, 'XDR': 5, 
   'XOF': 0, 
   'XPF': 0}
for code in _CURRENCY_META.values():
    if code.find(';') != -1:
        for c in code.split(';'):
            c = c.strip()
            if c not in CURRENCIES:
                CURRENCIES.append(c)

    elif code not in CURRENCIES:
        CURRENCIES.append(code)
    CURRENCIES.sort()

class UnsupportedCurrency(TypeError):
    """
    An unsupported currency
    """


def valid_currency(code):
    """
    returns whether the currency code is a valid currency code
    """
    return code in CURRENCIES


def decimals(code):
    """
    returns the number of decimal places for a currency code
    """
    if not valid_currency(code):
        raise UnsupportedCurrency, code
    return _CURRENCY_DECIMALS.get(code, 2)


class currency:
    """
    A Builtin-Python Currency Type

    A Currency is described by a base and an amount.  A base is a three-letter country
    code, and the amount should probably be a float ...
    """
    decimal_places = 2
    _currency = ''

    def __init__(self, *args):
        self._amount = 0.0
        for arg in args:
            try:
                arg = round(float(arg), self.decimal_places)
            except:
                pass

            if type(arg) == types.StringType:
                if len(arg) == 3:
                    self._currency = arg.upper()
                else:
                    match = currency_match.match(arg)
                    if match:
                        self._currency = match.group(2).upper()
                        amount = match.group(4)
                        amount = amount.replace(',', '')
                        amount = amount.replace(' ', '')
                        if amount:
                            try:
                                amount = round(float(amount), self.decimal_places)
                            except:
                                raise TypeError, 'cannot coerce amount: %s' % amount

                        if match.group(1) == '+':
                            amount = abs(amount)
                        elif match.group(1) == '-' or match.group(1) == '(' and match.group(5) == ')':
                            amount = abs(amount) * -1
                        self._amount = amount
                    else:
                        raise TypeError, 'cannot coerce string to currency: %s' % arg
            elif type(arg) in (types.FloatType, types.IntType, types.LongType):
                self._amount = round(float(arg), self.decimal_places)
            elif hasattr(arg, '_currency') and hasattr(arg, '_amount'):
                self._currency = arg._currency
                self._amount = round(float(arg._amount), self.decimal_places)
            else:
                raise UnsupportedCurrency, '(%s) [%s]' % (str(arg),
                 getattr(arg, '__dict__', {}))

        if self._currency not in CURRENCIES:
            raise AttributeError, 'Invalid Currency Code: %s' % self._currency

    def __add__(self, other):
        if type(other) in (types.FloatType, types.IntType, types.LongType):
            return currency(self._currency, self._amount + other)
        if isinstance(other, currency) or hasattr(other, '_currency') and hasattr(other, '_amount'):
            if self._currency == other._currency:
                return currency(self._currency, self._amount + other._amount)
            if other._amount == 0:
                return self
            raise ArithmeticError, 'Currency Code Mismatch %s != %s' % (self, other)
        else:
            try:
                tmp = currency(other)
                return self + tmp
            except:
                raise
                raise UnsupportedCurrency, type(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __cmp__(self, other):
        """
        comparisons are a little ridiculous as these are face-value, and really should
        only be used for equality checking
        """
        if type(other) in (types.FloatType, types.IntType, types.LongType):
            return cmp(self._amount, other)
        else:
            if isinstance(other, currency) or hasattr(other, '_currency') and hasattr(other, '_amount'):
                if self._currency != other._currency and (self._amount != 0 or other._amount != 0):
                    raise UnsupportedCurrency, other.currency()
                return cmp(self._amount, other._amount)
            return -1

    def __mul__(self, other):
        if type(other) in [types.FloatType, types.IntType, types.LongType]:
            return currency(self._currency, self._amount * other)
        if isinstance(other, currency) or hasattr(other, '_currency') and hasattr(other, '_amount'):
            if self._currency != other._currency and other._amount != 0:
                raise ArithmeticError, 'cannot multiply unequal currency bases: %s, %s' % (self, other)
            return currency(self._currency, self._amount * other._amount)
        raise TypeError, 'Not supported for this type (%s)' % type(other)

    def __div__(self, other):
        if type(other) in (types.FloatType, types.IntType, types.LongType):
            return currency(self._currency, self._amount / other)
        if isinstance(other, currency) or hasattr(other, '_currency') and hasattr(other, '_amount'):
            if self._currency != other._currency:
                raise ArithmeticError, 'cannot divide unequal currency bases: %s, %s' % (self, other)
            return currency(self._currency, self._amount / other._amount)
        raise TypeError, type(other)

    def __neg__(self):
        return currency(self._currency, -self._amount)

    def __abs__(self):
        return currency(self._currency, abs(self._amount))

    def __pos__(self):
        return self

    def __len__(self):
        return 1

    def __str__(self):
        return self.strfcur()

    def __repr__(self):
        return self.strfcur()

    def __hash__(self):
        return str(self).__hash__()

    def strfcur(self, fmt='%a'):
        """
        Format a currency - of form XXX 9,999.00 ...

        %a  comma-separated with brackets representing a credit amount

        %c  the ISO 4217 currency code

        anything else is passed to sprintf to format the amount
        """
        if fmt.find('%a') != -1:
            amt = self.amount_str()
            commas = []
            length = len(amt)
            for i in xrange(0, length):
                commas.append(amt[i])
                index = length - i - 6
                if index > 0 and index % 3 == 1:
                    commas.append(',')

            if self < 0:
                return '(%s %s)' % (self._currency, string.join(commas, ''))
            return ' %s %s ' % (self._currency, string.join(commas, ''))
        if fmt.find('%c') != -1:
            result = fmt.replace('%c', self._currency)
        else:
            result = fmt
        if result.find('%') == -1:
            return result
        return result % self._amount

    def __float__(self):
        return self._amount

    def currency(self):
        return self._currency

    def amount(self):
        return self._amount

    def amount_str(self):
        return '%0.2f' % abs(self._amount)

    def decimals(self):
        """ returns the number of decimal places """
        return _CURRENCY_DECIMALS.get(self._currency, 2)

    def cents(self):
        """
        return the amount as cents (if a decimal currency)
        """
        if self.decimals() != 2:
            raise AttributeError, self._currency
        return int(self._amount * 100)