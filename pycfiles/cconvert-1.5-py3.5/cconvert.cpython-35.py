# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cconvert/cconvert.py
# Compiled at: 2020-02-10 12:56:10
# Size of source mod 2**32: 2085 bytes
import requests, json, sys, traceback, argparse

def main():
    url = 'https://api.ratesapi.io/api/latest'
    parser = argparse.ArgumentParser(add_help=False)
    (
     parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='USAGE : cconvert 1 usd inr'),)
    (
     parser.add_argument('VALUE:', help='Value to be converted. Eg : 1', type=str),)
    (
     parser.add_argument('BASE:', help='Base currency value. Eg : usd', type=str),)
    parser.add_argument('CONVERT:', help='Convert currency value. Eg : inr', type=str)
    args = parser.parse_args()
    try:
        baseCurrency = sys.argv[2].upper()
        convertCurrency = sys.argv[3].upper()
    except:
        print('Please enter command line arguments to proceed.')
        print(args)
        sys.exit(1)

    querystring = {'base': baseCurrency.upper()}
    headers = {'Host': 'api.ratesapi.io'}
    response = requests.request('GET', url, headers=headers, params=querystring)
    try:
        response.raise_for_status()
        jsonresp = json.loads(response.text)
        arguements = sys.argv[1]
        convertedResponse = '{:.2f}'.format(jsonresp['rates'][convertCurrency] * float(arguements))
        print(str(sys.argv[1] + ' ' + str(baseCurrency) + ' to ' + str(convertCurrency) + ' => ' + str(convertedResponse)) + ' ' + str(convertCurrency).lower())
    except:
        print('\n===================\n BRUHception occured. You got BRUHed by the service or the currency you entered! Please check the stacktrace king. \n==================\n')
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()