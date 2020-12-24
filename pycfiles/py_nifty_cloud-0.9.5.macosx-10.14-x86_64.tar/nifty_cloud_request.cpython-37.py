# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/petitviolet/.anyenv/envs/pyenv/versions/3.7.3/lib/python3.7/site-packages/py_nifty_cloud/nifty_cloud_request.py
# Compiled at: 2019-09-28 10:29:57
# Size of source mod 2**32: 7253 bytes
import yaml, requests
from datetime import datetime
try:
    from urllib.parse import quote
except:
    from urllib import quote

import hmac, hashlib, base64, json

class NiftyCloudRequest(object):
    __doc__ = ' ニフティクラウド mobile backendのREST APIへのリクエスト用モジュール\n    APPLICATION_KEYとCLIENT_KEYはyamlファイルとして\n    ```\n    APPLICATION_KEY: "app_key"\n    CLIENT_KEY: "client_key"\n    ```\n    と書く\n    defaultでは~/.nifty.ymlを読み込む\n    '
    API_PROTOCOL = 'https'
    API_DOMAIN = 'mbaas.api.nifcloud.com'
    API_VERSION = '2013-09-01'
    CHARSET = 'UTF-8'
    SIGNATURE_METHOD = 'HmacSHA256'
    SIGNATURE_VERSION = '2'

    def __init__(self, config_file='~/.nifty.yml'):
        """ KEYの設定
        Args:
            config_file: APPLICATION_KEYとCLIENT_KEYを書いたyamlファイル
        """
        config = yaml.load(open(config_file, 'r').read())
        self.APP_KEY = config['APPLICATION_KEY']
        self.CLIENT_KEY = config['CLIENT_KEY']

    def get(self, path, query, **kwargs):
        """ getのalias
        requestを参照
        """
        return (self.request)(path, query, 'GET', **kwargs)

    def post(self, path, query, **kwargs):
        """ postのalias
        requestを参照
        """
        return (self.request)(path, query, 'POST', **kwargs)

    def put(self, path, query, **kwargs):
        """ putのalias
        requestを参照
        """
        return (self.request)(path, query, 'PUT', **kwargs)

    def delete(self, path, query, **kwargs):
        """ deleteのalias
        requestを参照
        """
        return (self.request)(path, query, 'DELETE', **kwargs)

    def request(self, path, query, method, **kwargs):
        """ niftyのmbaasにrequestを送る
        Reference:
            http://mb.cloud.nifty.com/doc/rest/common/format.html
        Args:
            path: 叩くAPIのpath(eg. /classes/TestClass)
            query: 辞書形式のクエリ(eg. {'where': {'key': 'value'}})
            method: 'get' or 'post'
            kwargs: requests.request に追加で渡すパラメータ
        Return:
            response: requestに対するresponse
        """
        if not type(query) is dict:
            raise AssertionError
        else:
            method = method.upper()
            signature = self._NiftyCloudRequest__make_signature(path=path, query=query, method=method)
            headers = self._NiftyCloudRequest__make_headers(signature)
            url = self._NiftyCloudRequest__make_url(path)
            kwargs['headers'] = headers
            if method.upper() == 'GET':
                url += '?' + self._NiftyCloudRequest__query(query)
            else:
                kwargs['data'] = json.dumps(query)
        response = (requests.request)(method, url, **kwargs)
        return response

    def __make_headers(self, signature):
        """ ヘッダ作成
        """
        assert self.timestamp is not None
        return {'X-NCMB-Application-Key':self.APP_KEY, 
         'X-NCMB-Signature':signature, 
         'X-NCMB-Timestamp':self.timestamp, 
         'Content-Type':'application/json'}

    def __timestamp(self):
        """ iso8601形式のtimestampを作成する
        """
        self.timestamp = datetime.utcnow().isoformat()
        return self.timestamp

    def __make_url(self, path):
        """ pathを使ってurlを構成する
        """
        return '{protocol}://{domain}/{version}{path}'.format(protocol=(self.API_PROTOCOL),
          domain=(self.API_DOMAIN),
          version=(self.API_VERSION),
          path=path)

    def __path(self, path):
        """ ヘッダで必要なpathの形式にする
        """
        return '/{api_version}{path}'.format(api_version=(self.API_VERSION),
          path=path)

    def __query(self, dict_query):
        """ 辞書形式のqueryをシグネチャ作成に必要な形に変換する
        urlエンコードしたkey=valueを&でつなぐ
        """
        encoded_query = self._NiftyCloudRequest__encode_query(dict_query)
        return self._NiftyCloudRequest__join_query(encoded_query)

    def __join_query(self, encoded_dict_query):
        """ key=valueにして&でつなぐ
        シグネチャ生成で使うためsortしておく
        """
        return '&'.join(('='.join(e) for e in sorted(encoded_dict_query.items())))

    def __encode_query(self, dict_query):
        """ 辞書をurlエンコードする
        valueがdictの場合はjson文字列に変換してから行う
        """
        q = lambda x: quote(str(x))
        qj = lambda x: q(json.dumps(x).replace(': ', ':'))
        result = {}
        for k, v in dict_query.items():
            if type(v) is dict:
                result[q(k)] = qj(v)
            else:
                result[q(k)] = q(v)

        return result

    def __make_signature_str(self, path, query, method='GET'):
        """ niftyのAPIへrequest送る時に必要なシグネチャの元となる
        文字列を生成する
        Args:
            path: データの保存場所へのpath
            query: 問い合わせ内容のdict
            method: 'GET'とか'POST'
        Return:
            シグネチャ生成元となるstr型
        """
        signature_list = [
         method, self.API_DOMAIN, self._NiftyCloudRequest__path(path)]
        signature_dict = {'SignatureMethod':self.SIGNATURE_METHOD, 
         'SignatureVersion':self.SIGNATURE_VERSION, 
         'X-NCMB-Application-Key':self.APP_KEY, 
         'X-NCMB-Timestamp':self._NiftyCloudRequest__timestamp()}
        signature_list.append('&'.join(['='.join(_sd) for _sd in sorted(signature_dict.items())]))
        if query:
            if method == 'GET':
                signature_list[(-1)] += '&' + self._NiftyCloudRequest__query(query).strip()
        return '\n'.join(signature_list).strip()

    def __encode_signature(self, signature_str):
        """ HmacSHA256アルゴリズムでハッシュ文字列を生成する
        秘密鍵としてCLIENT_KEYを使用する
        Args:
            signature_str: シグネチャ用の文字列
        Return:
            bytes型のシグネチャ
        """
        return base64.b64encode(hmac.new(self.CLIENT_KEY.encode(self.CHARSET), signature_str.encode(self.CHARSET), hashlib.sha256).digest())

    def __make_signature(self, path, query, method):
        """ requestする情報を使って認証用のシグネチャを作成する
        """
        signature_str = self._NiftyCloudRequest__make_signature_str(path, query, method)
        signature = self._NiftyCloudRequest__encode_signature(signature_str)
        return signature.decode(self.CHARSET)