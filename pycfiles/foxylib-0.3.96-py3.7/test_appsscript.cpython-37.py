# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/googleapi/tests/test_appsscript.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 6663 bytes
from foxylib.tools.googleapi.appsscript import AppsscriptToolkit
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
from googleapiclient import errors
from foxylib.tools.jinja2.jinja2_tool import tmplt_file2str

class AppsScript:
    SAMPLE_CODE = '\nfunction helloWorld() {\n  console.log("Hello, world!");\n}\n'.strip()
    SAMPLE_MANIFEST = '\n{\n  "timeZone": "America/New_York",\n  "exceptionLogging": "CLOUD"\n}\n'.strip()

    @classmethod
    def test(cls):
        return cls.test_03()

    @classmethod
    def test_01(cls):
        filepath = 'config/google/api/foxytrixy.bot.credentials.json'
        creds = username_scope2creds(filepath, 'foxytrixy.bot', cls.SCOPE_PROJECT)
        service = build('script', 'v1', http=(creds.authorize(Http())))
        try:
            request = {'title': 'My Script'}
            response = service.projects().create(body=request).execute()
            request = {'files': [
                       {'name':'hello', 
                        'type':'SERVER_JS', 
                        'source':cls.SAMPLE_CODE},
                       {'name':'appsscript', 
                        'type':'JSON', 
                        'source':cls.SAMPLE_MANIFEST}]}
            response = service.projects().updateContent(body=request,
              scriptId=(response['scriptId'])).execute()
            print('https://script.google.com/d/' + response['scriptId'] + '/edit')
        except errors.HttpError as error:
            try:
                print(error.content)
            finally:
                error = None
                del error

    @classmethod
    def test_02(cls):
        filepath = 'config/google/api/foxytrixy.bot.credentials.json'
        creds = username_scope2creds(filepath, 'foxytrixy.bot', cls.SCOPE_PROJECT)
        service = build('script', 'v1', http=(creds.authorize(Http())))
        gsheet_id = '15K2PThxUL6YQhJBoQ5GYEgtNUsH132lUZDGYGxQDn40'
        str_JS = tmplt_file2str('foxyos/spreadsheet.isPartOfMerge.part.js', {'googlespreadsheet_id': gsheet_id})
        str_JSON_MANIFEST = tmplt_file2str('foxyos/manifest.sample.part.json')
        try:
            h_PROJECT = {'title':'Google Spreadsheet', 
             'parentId':gsheet_id}
            response = service.projects().create(body=h_PROJECT).execute()
            script_id = response['scriptId']
            print(script_id)
            h_BODY = {'files': [
                       {'name':'zz_code', 
                        'type':'SERVER_JS', 
                        'source':str_JS},
                       {'name':'appsscript', 
                        'type':'JSON', 
                        'source':cls.SAMPLE_MANIFEST}]}
            response = (service.projects().updateContent)(body=h_BODY, scriptId=script_id).execute()
            print('https://script.google.com/d/' + response['scriptId'] + '/edit')
        except errors.HttpError as error:
            try:
                print(error.content)
            finally:
                error = None
                del error

    @classmethod
    def test_03(cls):
        filepath = 'config/google/api/foxytrixy.bot.credentials.json'
        script_id = 'MiPzz27QS2ea2WtmtlLsLxAl12BWE2MQs'
        from foxylib.tools.googleapi.gsheet_tool import GSSTool
        creds = username_scope2creds(filepath, 'foxytrixy.bot', GSSTool.SCOPE_READWRITE)
        service = build('script', 'v1', http=(creds.authorize(Http())))
        gsheet_id = '15K2PThxUL6YQhJBoQ5GYEgtNUsH132lUZDGYGxQDn40'
        request = {'function':'run',  'parameters':[
          gsheet_id, 'field',
          gsheet_id, 'field_UNMERGED']}
        try:
            response = service.scripts().run(body=request, scriptId=script_id).execute()
            print(response)
            if 'error' in response:
                raise Exception()
        except errors.HttpError as error:
            try:
                print(error.content)
            finally:
                error = None
                del error

    @classmethod
    def test_RAW(cls):
        """Calls the Apps Script API.
        """
        username_GOOGLE = 'foxytrixy.bot'
        filepath_credentials_json = username2filepath_credentials_json(username_GOOGLE)
        filepath_token_json = username_scope2filepath_token_json(username_GOOGLE, AppsscriptToolkit.SCOPE_PROJECT)
        store = file.Storage(filepath_token_json)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(filepath_credentials_json, scope_str2url(AppsscriptToolkit.SCOPE_PROJECT))
            creds = tools.run_flow(flow, store)
        service = build('script', 'v1', http=(creds.authorize(Http())))
        try:
            request = {'title': 'My Script'}
            response = service.projects().create(body=request).execute()
            request = {'files': [
                       {'name':'hello', 
                        'type':'SERVER_JS', 
                        'source':cls.SAMPLE_CODE},
                       {'name':'appsscript', 
                        'type':'JSON', 
                        'source':cls.SAMPLE_MANIFEST}]}
            response = service.projects().updateContent(body=request,
              scriptId=(response['scriptId'])).execute()
            print('https://script.google.com/d/' + response['scriptId'] + '/edit')
        except errors.HttpError as error:
            try:
                print(error.content)
            finally:
                error = None
                del error