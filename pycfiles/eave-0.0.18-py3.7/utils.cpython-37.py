# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\eave\utils.py
# Compiled at: 2020-03-20 06:10:02
# Size of source mod 2**32: 11509 bytes
import json, re, requests, os
from eave import *
import yaml
__all__ = [
 'raml2eave', 'auto_drf_apis']

def _find_resources(data, base_uri):
    for key, value in data.items():
        if not key.startswith('/'):
            continue
        if not isinstance(value, dict):
            continue
        for method in ('get', 'post', 'put', 'patch', 'delete'):
            if method in value:
                resource = value
                resource['uri'] = base_uri + key
                yield resource
                break


def _find_target--- This code section failed: ---

 L.  27         0  LOAD_FAST                'excludes'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_LIST_0          0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'excludes'

 L.  28         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'data'
               12  LOAD_GLOBAL              list
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE    64  'to 64'

 L.  29        18  SETUP_LOOP          142  'to 142'
               20  LOAD_FAST                'data'
               22  GET_ITER         
             24_0  COME_FROM            52  '52'
               24  FOR_ITER             60  'to 60'
               26  STORE_FAST               'item'

 L.  30        28  LOAD_FAST                'item'
               30  LOAD_FAST                'excludes'
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    38  'to 38'

 L.  31        36  CONTINUE             24  'to 24'
             38_0  COME_FROM            34  '34'

 L.  32        38  LOAD_GLOBAL              _find_target
               40  LOAD_FAST                'item'
               42  LOAD_FAST                'target'
               44  LOAD_FAST                'excludes'
               46  CALL_FUNCTION_3       3  '3 positional arguments'
               48  STORE_FAST               'r'

 L.  33        50  LOAD_FAST                'r'
               52  POP_JUMP_IF_FALSE    24  'to 24'

 L.  34        54  LOAD_FAST                'r'
               56  RETURN_VALUE     
               58  JUMP_BACK            24  'to 24'
               60  POP_BLOCK        
               62  JUMP_FORWARD        142  'to 142'
             64_0  COME_FROM            16  '16'

 L.  35        64  LOAD_GLOBAL              isinstance
               66  LOAD_FAST                'data'
               68  LOAD_GLOBAL              dict
               70  CALL_FUNCTION_2       2  '2 positional arguments'
               72  POP_JUMP_IF_FALSE   142  'to 142'

 L.  36        74  LOAD_FAST                'target'
               76  LOAD_FAST                'data'
               78  COMPARE_OP               in
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L.  37        82  LOAD_FAST                'data'
               84  LOAD_FAST                'target'
               86  BINARY_SUBSCR    
               88  RETURN_VALUE     
             90_0  COME_FROM            80  '80'

 L.  39        90  SETUP_LOOP          142  'to 142'
               92  LOAD_FAST                'data'
               94  LOAD_METHOD              items
               96  CALL_METHOD_0         0  '0 positional arguments'
               98  GET_ITER         
            100_0  COME_FROM           132  '132'
              100  FOR_ITER            140  'to 140'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'key'
              106  STORE_FAST               'value'

 L.  40       108  LOAD_FAST                'key'
              110  LOAD_FAST                'excludes'
              112  COMPARE_OP               in
              114  POP_JUMP_IF_FALSE   118  'to 118'

 L.  41       116  CONTINUE            100  'to 100'
            118_0  COME_FROM           114  '114'

 L.  42       118  LOAD_GLOBAL              _find_target
              120  LOAD_FAST                'value'
              122  LOAD_FAST                'target'
              124  LOAD_FAST                'excludes'
              126  CALL_FUNCTION_3       3  '3 positional arguments'
              128  STORE_FAST               'r'

 L.  43       130  LOAD_FAST                'r'
              132  POP_JUMP_IF_FALSE   100  'to 100'

 L.  44       134  LOAD_FAST                'r'
              136  RETURN_VALUE     
              138  JUMP_BACK           100  'to 100'
              140  POP_BLOCK        
            142_0  COME_FROM_LOOP       90  '90'
            142_1  COME_FROM            72  '72'
            142_2  COME_FROM            62  '62'
            142_3  COME_FROM_LOOP       18  '18'

Parse error at or near `COME_FROM' instruction at offset 142_2


def _append_resource(doc, data, base_uri=''):
    for resource in _find_resources(data, base_uri):
        api_uri = resource['uri']
        secured_by = resource.get('securedBy')
        for method_name, method_data in resource.items():
            if method_name not in ('get', 'post', 'put', 'patch', 'delete'):
                continue
            api = Api()
            name1 = resource.get('displayName', '')
            name2 = method_data.get('description', '')
            if name1 in name2:
                name1 = ''
            api.title = f"{name1} {name2}".strip()
            api.uri = api_uri
            api.method = method_name
            secured_by = method_data.get('securedBy', secured_by)
            if secured_by:
                api.description = f"Secured By: **{secured_by}**"
            ups = re.findall('\\{(.+)\\}', api.uri)
            for up in ups:
                api.uri_params.append(UP(name=up))

            queryparameters = method_data.get('queryParameters', {})
            for p_name, p_data in queryparameters.items():
                p_data = p_data or {}
                p_data['name'] = p_name
                api.query_params.append(QP(p_data))

            properties = _find_target(method_data.get('body'), 'properties') or {}
            for p_name, p_data in properties.items():
                p_data = p_data or {}
                p_data['name'] = p_name
                api.body_params.append(BP(p_data))

            api.body_example = _find_targetmethod_data.get('body')'example'['properties'] or ''
            api.response_example = _find_target(method_data.get('responses'), 'example') or ''
            api.content_types = []
            doc.apis.append(api)

        _append_resourcedocresourceapi_uri


def raml2eave(raml_file, silence=True):
    """
    raml2eave('tiadmin.raml').build('tiadmin.html', 'zh')
    raml2eave('grs.raml').build('grs.html', 'zh')
    """
    raml_content = open(raml_file, encoding='utf8').read()
    data = yaml.safe_load(raml_content)
    if not silence:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    doc = Doc()
    doc.title = data.get('title', '')
    doc.version = data.get('version', '')
    doc.host = data.get('baseUri', '')
    doc.description = data.get('description', '')
    for note in data.get('documentation', []):
        doc.add_note(note)

    security_schemes = data.get('securitySchemes')
    for name, scheme in security_schemes.items():
        content = scheme.get('description', '')
        doc.add_note(title=name, content=content)

    _append_resourcedocdata''
    return doc


def _get_request(url, testhost=''):
    print('get:', testhost + url)
    if os.path.exists('eave_cache.json'):
        cache = open('eave_cache.json', encoding='utf8').read()
        cache = json.loads(cache)
    else:
        cache = {}
    if testhost:
        data = requests.get(testhost + url).json()
        cache[url] = data
        open('eave_cache.json', 'w', encoding='utf8').write(json.dumps(cache, indent=4))
        print('save cache')
    else:
        if url in cache:
            data = cache[url]
            print('use cache')
        else:
            data = {}
            print('default empty')
    return data


def _action_description_handle(func):
    description = func.kwargs['description'] or ''
    assert description, f"{func.url_path} 接口缺少描述！请至少在 `__doc__` 中添加至少一行内容，作为接口名称。"
    method = list(func.mapping.keys())[0].upper()
    lines = description.strip().splitlines()
    title = lines[0].strip()
    result = {'title':title, 
     'description':'', 
     'query_params':[],  'body_params':[],  'response_description':''}
    target = 'description'
    for line in lines[1:]:
        line = line.strip()
        if line in ('GET', 'POST', 'PUT', 'PATCH', 'PARAMS'):
            if method == 'GET':
                target = 'query_params'
            else:
                target = 'body_params'
                continue
        elif line == 'RESPONSE':
            target = 'response_description'
            continue
        if isinstance(result[target], str):
            result[target] += line + '\n\n'
        elif isinstance(result[target], list):
            name, description = line.split(':', 1)
            name = name.strip()
            description = description.strip()
            required = False
            default = ''
            if name.startswith('*'):
                name = name[1:]
                required = True
            if description.count('=>') == 1:
                description, default = description.split('=>')
            if target == 'query_params':
                item = QP(name=name, description=description, required=required, default=default)
            else:
                if target == 'body_params':
                    item = BP(name=name, description=description, required=required, default=default)
                else:
                    assert False
                    result[target].append(item)

    return result


def auto_drf_apis(res_name, uri, view_set, testhost='http://127.0.0.1:8000'):
    """
    # todo: 加强这块文档和示例，写进 eave 主页介绍
    api_list, api_post, api_detail, actions = auto_drf_apis('用户', '/api/users/', UserViewSet)
    doc.add_apis(api_list, api_post, api_detail, *actions)
    """
    api_list = Api()
    api_list.title = res_name + '列表'
    api_list.uri = uri
    api_list.method = 'GET'
    api_list.query_params = []
    if hasattr(view_set, 'filter_class'):
        filter_fields = view_set.filter_class.Meta.fields
        for field_name, kinds in filter_fields.items():
            for kind in kinds:
                query_name = f"{field_name}__{kind}"
                kind_zh = '筛选'
                if kind == 'exact':
                    kind_zh = '指定'
                    query_name = field_name
                else:
                    if kind in ('icontains', 'contains'):
                        kind_zh = '匹配'
                    else:
                        if kind == 'in':
                            kind_zh = '命中'
                        else:
                            f = field_name.split('__')
                            if len(f) == 1:
                                field_zh = view_set.serializer_class.Meta.model._meta.get_field(f[0]).verbose_name
                            else:
                                q_model = view_set.serializer_class.Meta.model
                                for k in f[0:-1]:
                                    q_model = q_model._meta.get_field(k).related_model

                            field_zh = q_model._meta.get_field(f[(-1)]).verbose_name
                        description = kind_zh + field_zh
                        api_list.query_params.append(QP(name=query_name, description=description))

    url = api_list.uri
    data = _get_request(url, testhost)
    if len(data['results']) > 2:
        data['results'] = [
         data['results'][0]]
    api_list.response_example = json.dumps(data, ensure_ascii=False, indent=4)
    api_post = Api()
    api_post.title = '创建' + res_name
    api_post.uri = uri
    api_post.method = 'POST'
    serializer = view_set.serializer_class()
    api_post.body_params = []
    for field_name, field in serializer.fields.items():
        if field.read_only:
            continue
        type = 'string'
        field_type = str(field.__class__)
        if 'IntegerField' in field_type:
            type = 'int'
        else:
            if 'FloatField' in field_type:
                type = 'float'
            else:
                if 'DecimalField' in field_type:
                    type = 'decimal'
                else:
                    if 'BooleanField' in field_type:
                        type = 'bool'
                    else:
                        description = field.label
                        if field.help_text:
                            description += f" [{field.help_text}]"
                        required = field.required
                        default = field.default
                        try:
                            if 'empty' in str(default.__class__):
                                default = view_set.serializer_class.Meta.model._meta.get_field(field_name).default
                        except:
                            pass

                    api_post.body_params.append(BP(name=field_name, type=type, description=description, required=required, default=default))

    if data['results']:
        api_post.response_example = json.dumps((data['results'][0]), ensure_ascii=False, indent=4)
    api_detail = Api()
    api_detail.title = res_name + '详情'
    api_detail.uri = f"{uri.rstrip('/')}/<id>/"
    api_detail.method = 'GET'
    api_detail.uri_params = [UP(name='id', description=f"{res_name} ID", example=1)]
    data = _get_request(url, testhost)
    if data['results']:
        res_id = data['results'][0].get('id')
        if res_id:
            url = f"{uri.rstrip('/')}/{res_id}/"
        else:
            url = data['results'][0].get('url')
            items = url.split('/')[3:]
            url = '/' + '/'.join(items)
        data2 = _get_request(url, testhost)
        api_detail.response_example = json.dumps(data2, ensure_ascii=False, indent=4)
    actions = []
    for item in dir(view_set):
        func = getattr(view_set, item)
        if not all([hasattr(func, 'detail'), hasattr(func, 'url_path'), hasattr(func, 'kwargs')]):
            continue
        else:
            detail = func.detail
            url_path = func.url_path
            description = func.kwargs['description']
            method = list(func.mapping.keys())[0].upper()
            result = _action_description_handle(func)
            if detail:
                action_uri = f"{uri.rstrip('/')}/<id>/{url_path}/"
            else:
                action_uri = f"{uri.rstrip('/')}/{url_path}/"
        api_action = Api(uri=action_uri, method=method, **result)
        actions.append(api_action)

    return (
     api_list, api_post, api_detail, actions)