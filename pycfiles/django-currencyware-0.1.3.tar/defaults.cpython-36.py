# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.venv/trade/lib/python3.6/site-packages/currencyware/defaults.py
# Compiled at: 2018-09-08 19:43:00
# Size of source mod 2**32: 2308 bytes
from django.conf import settings
DEFAULT_CURRENY_LANGUAGE_CODE = getattr(settings, 'DEFAULT_CURRENY_LANGUAGE_CODE', 'en')
ALL_CURRENCY_CODES = getattr(settings, 'ALL_CURRENCY_CODES', [
 'AED', 'AFN', 'ALL', 'AMD', 'AOA', 'ARS',
 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT',
 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB',
 'BRL', 'BSD', 'BTN', 'BWP', 'BYR', 'BZD',
 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP',
 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK',
 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR',
 'FJD', 'FKP', 'GBP', 'GEL', 'GHS', 'GIP',
 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL',
 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'INR',
 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY',
 'KES', 'KGS', 'KHR', 'KPW', 'KRW', 'KWD',
 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD',
 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD',
 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR',
 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN',
 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB',
 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG',
 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR',
 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP',
 'SLL', 'SOS', 'SRD', 'STD', 'SYP', 'SZL',
 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY',
 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD',
 'UYU', 'UZS', 'VEF', 'VND', 'VUV', 'WST',
 'XAF', 'XCD', 'XPF', 'YER', 'ZAR', 'ZMW'])
PRIORITY_CURRENCY_CODES = getattr(settings, 'PRIORITY_CURRENCY_CODES', [
 'USD', 'CAD', 'EUR', 'AUD', 'GBP', 'HKD', 'JPY', 'CNY', 'CHF'])
BASE_CURRENY_CODE = getattr(settings, 'BASE_CURRENY_CODE', 'USD')
OPEN_EXCHANGE_RATES_URL = 'https://openexchangerates.org/api/'
OPEN_EXCHANGE_RATES_URL = getattr(settings, 'OPEN_EXCHANGE_RATES_URL', OPEN_EXCHANGE_RATES_URL)
OPEN_EXCHANGE_RATES_API_KEY = getattr(settings, 'OPEN_EXCHANGE_RATES_API_KEY', None)
OPEN_EXCHANGE_RATES_API_CALLS_PER_SECONDS = 1
GOOGLE_API_KEY = getattr(settings, 'GOOGLE_API_KEY', None)
GOOGLE_TRANSLATE_URL = 'https://www.googleapis.com/language/translate/v2'