# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\appli\Documents\GitHub\alphaVantageAPI Project\alphaVantageAPI\alphavantage.py
# Compiled at: 2020-04-21 13:59:13
# Size of source mod 2**32: 25594 bytes
import os, sys, time, json, re, math, requests, pprint
from pathlib import Path, PurePath
from functools import wraps
from pandas import DataFrame
from .utils import is_home
from .validate_parameters import _validate_parameters
try:
    import openpyxl
    _EXCEL_ = True
except ImportError:
    _EXCEL_ = False

MISSING_API_KEY = '\n[X] The AlphaVantage API key must be provided.\n\nGet a free key from the alphavantage website:\nhttps://www.alphavantage.co/support/#api-key\nUse: api_key to set your AV API key\nOR\nSet your environment variable AV_API_KEY to your AV API key\n'

class AlphaVantage(object):
    __doc__ = "AlphaVantage Class\n\n    A Class to handle Python 3.6 calls to the AlphaVantage API.  It requires Pandas\n    module to simplify some operations.  All requests are 'json' requests to\n    AlphaVantage's REST API and converted into Pandas DataFrames.\n\n    Parameters\n    ----------\n    api_key: str = None\n    premium: bool = False\n    output_size: str = 'compact'\n    datatype: str = 'json'\n    export: bool = False\n    export_path: str = '~/av_data'\n    output: str = 'csv'\n    clean: bool = False\n    proxy: dict = dict()\n    \n    Examples\n    --------\n    >>> from alphaVantageAPI.alphavantage import AlphaVantage\n    >>> av = AlphaVantage(api_key='your API key')"
    API_NAME = 'AlphaVantage'
    END_POINT = 'https://www.alphavantage.co/query'
    DEBUG = False

    def __init__(self, api_key: str=None, premium: bool=False, export: bool=False, export_path: str='~/av_data', output: str='csv', datatype: str='json', output_size: str='compact', clean: bool=False, proxy: dict={}) -> None:
        api_file = Path(PurePath(__file__).parent / 'data/api.json')
        self._load_api(api_file)
        self.api_key = api_key
        self.premium = premium
        self.export = export
        self.export_path = export_path
        self.output = output
        self.datatype = datatype
        self.output_size = output_size
        self.proxy = proxy
        self.clean = clean
        self._requests_session = requests.session()
        self._response_history = []
        self._api_call_count = 0

    def _init_export_path(self) -> str:
        """Create the export_path directory if it does not exist."""
        if self.export:
            try:
                if not self.export_path.exists():
                    self.export_path.mkdir(parents=True)
            except OSError as ex:
                try:
                    raise
                finally:
                    ex = None
                    del ex

            except PermissionError as ex:
                try:
                    raise
                finally:
                    ex = None
                    del ex

    def _load_api(self, api_file: Path) -> None:
        """Load API from a JSON file."""
        if api_file.exists():
            with api_file.open('r') as (content):
                api = json.load(content)
            content.close()
            self._AlphaVantage__api = api
            self._api_lists()
        else:
            raise ValueError(f"{api_file} does not exist.")

    def _api_lists(self) -> None:
        """Initialize lists based on API."""
        self.series = [x for x in self._AlphaVantage__api['series']]
        self._AlphaVantage__api_series = [x['function'] for x in self.series]
        self._AlphaVantage__api_function = {x['alias']:x['function'] for x in self._AlphaVantage__api['series']}
        self._AlphaVantage__api_function_inv = {v:k for k, v in self._AlphaVantage__api_function.items()}
        self._AlphaVantage__api_datatype = self._AlphaVantage__api['datatype']
        self._AlphaVantage__api_outputsize = self._AlphaVantage__api['outputsize']
        self._AlphaVantage__api_series_interval = self._AlphaVantage__api['series_interval']
        self.indicators = [x for x in self._AlphaVantage__api['indicator']]
        self._AlphaVantage__api_indicator = [x['function'] for x in self.indicators]
        self._AlphaVantage__api_indicator_matype = self._AlphaVantage__api['matype']

    def _function_alias(self, function: str) -> str:
        """Returns the function alias for the given 'function'."""
        if function in self._AlphaVantage__api_function_inv:
            return self._AlphaVantage__api_function_inv[function]
        return function

    def _parameters(self, function: str, kind: str) -> list:
        """Returns 'required' or 'optional' parameters for a 'function'."""
        result = []
        if kind in ('required', 'optional'):
            try:
                all_functions = self.series + self.indicators
                result = [x[kind] for x in all_functions if kind in x if function == x['function']].pop()
            except IndexError as ex:
                try:
                    pass
                finally:
                    ex = None
                    del ex

        return result

    def _av_api_call(self, parameters: dict, timeout: int=60, **kwargs) -> DataFrame or json or None:
        """Main method to handle AlphaVantage API call request and response."""
        proxies = kwargs['proxies'] if 'proxies' in kwargs else self.proxy
        parameters['apikey'] = self.api_key
        if not self.premium:
            if self._api_call_count > 0:
                time.sleep(15.01)
        else:
            try:
                try:
                    response = requests.get((AlphaVantage.END_POINT),
                      params=parameters,
                      timeout=timeout,
                      proxies=proxies)
                except requests.exceptions.RequestException as ex:
                    try:
                        print(f"[X] response.get() exception: {ex}\n    parameters: {parameters}")
                    finally:
                        ex = None
                        del ex

            finally:
                response.close()

            if response.status_code != 200:
                print(f"[X] Request Failed: {response.status_code}.\nText:\n{response.text}\n{parameters['function']}")
            if self.datatype == 'json':
                response = response.json()
            else:
                response = response.text
        self._response_history.append(parameters)
        if self.datatype == 'json':
            response = self._to_dataframe(parameters['function'], response)
        if self._api_call_count < 1:
            self._api_call_count += 1
        return response

    def _save_df(self, function: str, df: DataFrame) -> None:
        """Save Pandas DataFrame to a file type given a 'function'."""
        short_function = self._function_alias(function)
        parameters = self.last()
        if function == 'CURRENCY_EXCHANGE_RATE':
            path = f"{self.export_path}/{parameters['from_currency']}{parameters['to_currency']}"
        else:
            if function == 'SECTOR':
                path = f"{self.export_path}/sectors"
            else:
                if function == 'CRYPTO_RATING':
                    path = f"{self.export_path}/{parameters['symbol']}_RATING"
                else:
                    if function == 'TIME_SERIES_INTRADAY':
                        path = f"{self.export_path}/{parameters['symbol']}_{parameters['interval']}"
                    else:
                        if short_function.startswith('C') and len(short_function) == 2:
                            path = f"{self.export_path}/{parameters['symbol']}{parameters['market']}"
                        else:
                            if function in self._AlphaVantage__api_indicator:
                                path = f"{self.export_path}/{parameters['symbol']}_{parameters['interval'][0].upper()}_{short_function}"
                                if 'series_type' in parameters:
                                    path += f"_{parameters['series_type'][0].upper()}"
                                elif 'time_period' in parameters:
                                    path += f"_{parameters['time_period']}"
                                else:
                                    path = f"{self.export_path}/{parameters['symbol']}_{short_function}"
                            else:
                                path += f".{self.output}"
                                if self.output == 'csv':
                                    df.to_csv(path)
                                else:
                                    if self.output == 'json':
                                        df.to_json(path)
                                    else:
                                        if self.output == 'pkl':
                                            df.to_pickle(path)
                                        else:
                                            if self.output == 'html':
                                                df.to_html(path)
                                            else:
                                                if self.output == 'txt':
                                                    Path(path).write_text(df.to_string())
                                                else:
                                                    if _EXCEL_:
                                                        if self.output == 'xlsx':
                                                            df.to_excel(path, sheet_name=(parameters['function']))

    def _to_dataframe(self, function: str, response: dict) -> DataFrame:
        """Converts json response into a Pandas DataFrame given a 'function'"""
        try:
            json_keys = response.keys()
            key = [x for x in json_keys if not x.startswith('Meta Data')].pop()
        except IndexError as ie:
            try:
                print(' [X] Download failed.  Check the AV documentation for correct parameters: https://www.alphavantage.co/documentation/')
                sys.exit(1)
            finally:
                ie = None
                del ie

        if function == 'CURRENCY_EXCHANGE_RATE':
            df = DataFrame.from_dict(response, orient='index')
            df.set_index('6. Last Refreshed', inplace=True)
        else:
            if function == 'GLOBAL_QUOTE':
                df = DataFrame.from_dict(response, orient='index')
                df.iloc[(0, -1)] = float(df.iloc[(0, -1)].strip('%')) / 100
            else:
                if function == 'CRYPTO_RATING':
                    df = DataFrame.from_dict(response, orient='index')
                else:
                    if function == 'SYMBOL_SEARCH':
                        if len(response[key]) < 1:
                            return
                            df = DataFrame(response[key])
                        elif function == 'SECTOR':
                            df = DataFrame.from_dict(response)
                            df.dropna(axis='index', how='any', thresh=3, inplace=True)
                            df.dropna(axis='columns', how='any', thresh=3, inplace=True)
                            df.fillna('0%', inplace=True)
                        else:
                            df = DataFrame.from_dict((response[key]), dtype=float).T
                            df.index.rename('date', inplace=True)
                    elif function == 'SYMBOL_SEARCH':
                        pass
                    elif function == 'SECTOR':
                        df = df.applymap(lambda x: float(x.strip('%')) / 100)
                    else:
                        df = df.iloc[::-1]
                        df.reset_index(inplace=True)
                    if self.clean:
                        df = self._simplify_dataframe_columns(function, df)
                    if self.export:
                        self._save_df(function, df)
                    return df

    def _simplify_dataframe_columns(self, function: str, df: DataFrame) -> DataFrame or None:
        """Simplifies DataFrame Column Names given a 'function'."""
        if function == 'CURRENCY_EXCHANGE_RATE':
            column_names = [
             'refreshed', 'from', 'from_name', 'to', 'to_name', 'rate', 'tz']
        else:
            if function == 'SECTOR':
                column_names = [
                 'RT', '1D', '5D', '1M', '3M', 'YTD', '1Y', '3Y', '5Y', '10Y']
            else:
                if function == 'CRYPTO_RATING':
                    column_names = [re.sub('\\d+(|\\w). ', '', name) for name in df.columns]
                else:
                    if function == 'SYMBOL_SEARCH':
                        column_names = [
                         'symbol', 'name', 'type', 'region', 'market_open', 'market_close', 'tz', 'currency', 'match']
                    else:
                        column_names = [re.sub('\\d+(|\\w). ', '', name) for name in df.columns]
                        column_names = [re.sub(' amount', '', name) for name in column_names]
                        column_names = [re.sub('adjusted', 'adj', name) for name in column_names]
                        column_names = [re.sub(' ', '_', name) for name in column_names]
        df.columns = column_names
        return df

    def _saved_symbols(self, kind: str=None) -> list:
        """Returns a list of saved symbols beginning with: 'ticker_interval'"""
        if kind and isinstance(kind, str):
            files = Path(self.export_path).glob(f"*.{kind}")
        else:
            files = Path(self.export_path).glob(f"*.{self.output}")
        saved_files = sorted(files)
        symbols = set()
        for file in saved_files:
            file_stem_desc = file.stem.split('_')
            if len(file_stem_desc) == 2:
                symbols.add(f"{file_stem_desc[0]}_{file_stem_desc[1]}")

        return list(symbols)

    def fxrate(self, from_currency: str, to_currency: str='USD', **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for currency requests."""
        parameters = {'function':'CURRENCY_EXCHANGE_RATE', 
         'from_currency':from_currency.upper(), 
         'to_currency':to_currency.upper()}
        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def fx(self, function: str, from_symbol: str='EUR', to_symbol: str='USD', **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for currency requests."""
        if function.upper() not in ('FXD', 'FXI', 'FXM', 'FXW', 'FX_DAILY', 'FX_INTRADAY',
                                    'FX_MONTHLY', 'FX_WEEKLY'):
            return
            function = self._AlphaVantage__api_function[function]
            parameters = {'function':function.upper(), 
             'from_symbol':from_symbol.upper(), 
             'to_symbol':to_symbol.upper()}
            interval = kwargs.pop('interval', None)
            if interval is not None:
                if isinstance(interval, str) and interval in self._AlphaVantage__api_series_interval:
                    parameters['interval'] = interval
        elif isinstance(interval, int) and interval in [int(re.sub('min', '', x)) for x in self._AlphaVantage__api_series_interval]:
            parameters['interval'] = '{}min'.format(interval)
        else:
            return
        if function not in self._AlphaVantage__api_indicator:
            parameters['datatype'] = self.datatype
            parameters['outputsize'] = self.output_size
        required_parameters = self._parameters(parameters['function'], 'required')
        for required in required_parameters:
            if required in kwargs:
                parameters[required] = kwargs[required]

        optional_parameters = self._parameters(parameters['function'], 'optional')
        for option in optional_parameters:
            if option in kwargs:
                _validate_parameters((self._AlphaVantage__api_indicator_matype), option, parameters, **kwargs)

        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def global_quote(self, symbol: str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for global_quote requests."""
        parameters = {'function':'GLOBAL_QUOTE', 
         'symbol':symbol.upper()}
        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def search(self, keywords: str, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for search requests."""
        parameters = {'function':'SYMBOL_SEARCH', 
         'keywords':keywords}
        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def sectors(self, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method to request sector performances."""
        parameters = {'function': 'SECTOR'}
        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def digital(self, symbol: str, market: str='USD', function: str='CD', **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for digital currency requests."""
        parameters = {'function':self._AlphaVantage__api_function[function.upper()], 
         'symbol':symbol.upper(), 
         'market':market.upper()}
        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def crypto_rating(self, symbol: str, function: str='CR', **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for digital currency rating requests."""
        parameters = {'function':self._AlphaVantage__api_function[function.upper()], 
         'symbol':symbol.upper()}
        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def intraday(self, symbol: str, interval=5, **kwargs) -> DataFrame or None:
        """Simple wrapper to _av_api_call method for intraday requests."""
        parameters = {'function':'TIME_SERIES_INTRADAY', 
         'symbol':symbol.upper(), 
         'datatype':self.datatype, 
         'outputsize':self.output_size}
        if isinstance(interval, str) and interval in self._AlphaVantage__api_series_interval:
            parameters['interval'] = interval
        else:
            if isinstance(interval, int) and interval in [int(re.sub('min', '', x)) for x in self._AlphaVantage__api_series_interval]:
                parameters['interval'] = '{}min'.format(interval)
            else:
                return
        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def data(self, function: str, symbol: str=None, **kwargs) -> DataFrame or list or None:
        """Simple wrapper to _av_api_call method for an equity or indicator."""
        if isinstance(symbol, list):
            if len(symbol) > 1:
                symbols = list(map(str.upper, symbol))
                return [(self.data)(function, ticker, **kwargs) for ticker in symbols]
        try:
            symbol = symbol.upper()
        except AttributeError:
            pass

        function = function.upper()
        try:
            function = self._AlphaVantage__api_function[function] if function not in self._AlphaVantage__api_indicator else function
        except KeyError:
            print(f"[X] Perhaps 'function' and 'symbol' are interchanged!? function={function} and symbol={symbol}")
            function, symbol = symbol, function
            (self.data)(function, symbol, **kwargs)

        parameters = {'function':function, 
         'symbol':symbol}
        if function not in self._AlphaVantage__api_indicator:
            parameters['datatype'] = self.datatype
            parameters['outputsize'] = self.output_size
        required_parameters = self._parameters(parameters['function'], 'required')
        for required in required_parameters:
            if required in kwargs:
                parameters[required] = kwargs[required]

        optional_parameters = self._parameters(parameters['function'], 'optional')
        for option in optional_parameters:
            if option in kwargs:
                _validate_parameters((self._AlphaVantage__api_indicator_matype), option, parameters, **kwargs)

        download = (self._av_api_call)(parameters, **kwargs)
        if download is not None:
            return download

    def help(self, keyword: str=None) -> None:
        """Simple help system to print 'required' or 'optional' parameters based on a keyword."""

        def _functions():
            print(f"   Functions:\n    {', '.join(self._AlphaVantage__api_series)}")

        def _indicators():
            print(f"  Indicators:\n    {', '.join(self._AlphaVantage__api_indicator)}")

        def _aliases():
            pprint.pprint((self._AlphaVantage__api_function), indent=4)

        if keyword is None:
            print(f"{AlphaVantage.__name__} Help: Input a function name for more infomation on 'required'\nAvailable Functions:\n")
            _functions()
            _indicators()
        else:
            if keyword == 'aliases':
                print('Aliases:')
                _aliases()
            else:
                if keyword == 'functions':
                    _functions()
                else:
                    if keyword == 'indicators':
                        _indicators()
                    else:
                        keyword = keyword.upper()
                        required = self._parameters(keyword, 'required')
                        optional = self._parameters(keyword, 'optional')
                        description = [x for x in self.series + self.indicators if x['function'] == keyword][0]['description']
                        print(f"\n   Function: {keyword}")
                        print(f"Description: {description}")
                        print(f"   Required: {', '.join(required)}")
                        print(f"   Optional: {', '.join(optional)}") if optional else None

    def call_history(self) -> list:
        """Returns a history of successful response calls."""
        return self._response_history

    def last(self, n: int=1) -> str:
        """Returns the last 'n' calls as a list."""
        if n > 0:
            return self.call_history()[(-n)]
        return []

    @property
    def api_key(self) -> str:
        return self._AlphaVantage__apikey

    @api_key.setter
    def api_key(self, value: str) -> None:
        if value is None:
            self._AlphaVantage__apikey = os.getenv('AV_API_KEY')
        else:
            if isinstance(value, str) and value:
                self._AlphaVantage__apikey = value
            else:
                self._AlphaVantage__apikey = None
                print(MISSING_API_KEY)
                sys.exit(1)

    @property
    def export(self) -> bool:
        return self._AlphaVantage__export

    @export.setter
    def export(self, value: bool) -> None:
        if value is not None and isinstance(value, bool):
            self._AlphaVantage__export = value
        else:
            self._AlphaVantage__export = False

    @property
    def export_path(self) -> str:
        return self._AlphaVantage__export_path

    @export_path.setter
    def export_path(self, value: str) -> None:
        if value is not None:
            if isinstance(value, str):
                path = Path(value)
                if is_home(path):
                    user_subdir = '/'.join(path.parts[1:])
                    self._AlphaVantage__export_path = Path.home().joinpath(user_subdir)
                else:
                    self._AlphaVantage__export_path = path
                self._init_export_path()

    @property
    def output_size(self) -> str:
        return self._AlphaVantage__output_size

    @output_size.setter
    def output_size(self, value: str) -> None:
        if value is not None and value.lower() in self._AlphaVantage__api_outputsize:
            self._AlphaVantage__output_size = value.lower()
        else:
            self._AlphaVantage__output_size = self._AlphaVantage__api_outputsize[0]

    @property
    def output(self) -> str:
        return self._AlphaVantage__output

    @output.setter
    def output(self, value: str) -> None:
        output_type = ['csv', 'json', 'pkl', 'html', 'txt']
        output_type.append('xlsx') if _EXCEL_ else None
        if value is not None and value.lower() in output_type:
            self._AlphaVantage__output = value.lower()
        else:
            self._AlphaVantage__output = output_type[0]

    @property
    def datatype(self) -> str:
        return self._AlphaVantage__datatype

    @datatype.setter
    def datatype(self, value: str) -> None:
        if value is not None and value.lower() in self._AlphaVantage__api_datatype:
            self._AlphaVantage__datatype = value.lower()
        else:
            self._AlphaVantage__datatype = self._AlphaVantage__api_datatype[0]

    @property
    def proxy(self) -> dict:
        return self._AlphaVantage__proxy

    @proxy.setter
    def proxy(self, value: dict) -> None:
        if value is not None and isinstance(value, dict):
            self._AlphaVantage__proxy = value
        else:
            self._AlphaVantage__proxy = dict()

    @property
    def clean(self) -> bool:
        return self._AlphaVantage__clean

    @clean.setter
    def clean(self, value: bool) -> None:
        if value is not None and isinstance(value, bool):
            self._AlphaVantage__clean = value
        else:
            self._AlphaVantage__clean = False

    @property
    def premium(self) -> bool:
        return self._AlphaVantage__premium

    @premium.setter
    def premium(self, value: bool) -> None:
        if value is not None and isinstance(value, bool):
            self._AlphaVantage__premium = value
        else:
            self._AlphaVantage__premium = False

    def __repr__(self) -> str:
        s = f"{AlphaVantage.API_NAME}(\n  end_point:str = {AlphaVantage.END_POINT},\n"
        s += f"  api_key:str = {self.api_key},\n  export:bool = {self.export},\n"
        s += f"  export_path:str = {self.export_path},\n  output_size:str = {self.output_size},\n"
        s += f"  output:str = {self.output},\n  datatype:str = {self.datatype},\n"
        s += f"  clean:bool = {self.clean},\n  proxy:dict = {self.proxy}\n)"
        return s

    def __str__(self) -> str:
        s = f"{AlphaVantage.API_NAME}(\n  end_point:str = {AlphaVantage.END_POINT},\n"
        s += f"  api_key:str = {self.api_key},\n  export:bool = {self.export},\n"
        s += f"  export_path:str = {self.export_path},\n  output_size:str = {self.output_size},\n"
        s += f"  output:str = {self.output},\n  datatype:str = {self.datatype},\n"
        s += f"  clean:bool = {self.clean},\n  proxy:dict = {self.proxy}\n)"
        return s