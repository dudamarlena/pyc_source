# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/esl/eslgenerator.py
# Compiled at: 2016-04-10 11:34:51
import commands, urllib
from jinja2 import Template
from eslast import QueryStringNode, HeaderNode, BodyNode, ValueNode, ShellNode

class ESLGenerator(object):

    def __init__(self, ast):
        self.ast = ast

    def to_curl(self):
        url = self.ast.left.url
        method = self.ast.method.name
        params = {}
        headers = {}
        body = {}
        for option in self.ast.right.options if self.ast.right else []:
            if isinstance(option.key, QueryStringNode):
                if isinstance(option.value, ValueNode):
                    params[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    params[option.key.key] = commands.getstatusoutput(option.value.value)[1]
            elif isinstance(option.key, HeaderNode):
                if isinstance(option.value, ValueNode):
                    headers[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    headers[option.key.key] = commands.getstatusoutput(option.value.value)[1]
            elif isinstance(option.key, BodyNode):
                if isinstance(option.value, ValueNode):
                    body[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    body[option.key.key] = commands.getstatusoutput(option.value.value)[1]

        if '?' in url:
            url = url + urllib.urlencode(params)
        else:
            url = url + '?' + urllib.urlencode(params)
        headers = [ ('-H "{k}: {v}"').format(k=k, v=v) for k, v in headers.items() ]
        body = [ ('-d "{k}={v}"').format(k=k, v=v) for k, v in body.items() ]
        return ('\n        curl -X {method} {headers} {data} "{url}"\n        ').format(url=url, method=method, headers=(' ').join(headers), data=(' ').join(body))

    def to_go(self):
        url = self.ast.left.url
        method = self.ast.method.name
        params = {}
        headers = {}
        body = {}
        for option in self.ast.right.options if self.ast.right else []:
            if isinstance(option.key, QueryStringNode):
                if isinstance(option.value, ValueNode):
                    params[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    params[option.key.key] = commands.getstatusoutput(option.value.value)[1]
            elif isinstance(option.key, HeaderNode):
                if isinstance(option.value, ValueNode):
                    headers[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    headers[option.key.key] = commands.getstatusoutput(option.value.value)[1]
            elif isinstance(option.key, BodyNode):
                if isinstance(option.value, ValueNode):
                    body[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    body[option.key.key] = commands.getstatusoutput(option.value.value)[1]

        if '?' in url:
            url = url + urllib.urlencode(params)
        else:
            url = url + '?' + urllib.urlencode(params)
        template = Template('\n            url = "{{ url }}"\n            form := url.Values{}\n            {% for k,v in headers.items() -%}\n            form.Add("{{k}}", "{{v}}")\n            {% endfor -%}\n            client := &http.Client{}\n            req, err := http.NewRequest("{{ method }}", url, strings.NewReader(form.Encode()))\n            if err != nil {\n                fmt.Println(err)\n                return\n            }\n            {% for k,v in headers.items() %}\n            req.Header.Add("{{k}}", "{{v}}")\n            {% endfor -%}\n            resp, err := client.Do(req)\n        ')
        return template.render(url=url, headers=headers, method=method)

    def to_python(self):
        url = self.ast.left.url
        method = self.ast.method.name
        params = {}
        headers = {}
        body = {}
        for option in self.ast.right.options if self.ast.right else []:
            if isinstance(option.key, QueryStringNode):
                if isinstance(option.value, ValueNode):
                    params[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    params[option.key.key] = commands.getstatusoutput(option.value.value)[1]
            elif isinstance(option.key, HeaderNode):
                headers[option.key.key] = option.value.value
            elif isinstance(option.key, BodyNode):
                body[option.key.key] = option.value.value

        template = Template('Hello {{ name }}!')
        template.render(name='John Doe')
        return ("\n    params = {params}\n    data = {data}\n    headers = {headers}\n    requests.{method}('{url}', params=params, data=data, body=body, headers=headers)\n        ").format(url=url, method=method.lower(), params=params, data=body, headers=headers)