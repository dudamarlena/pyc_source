# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/init/templates/cookiecutter-aws-sam-hello-java-maven/tests/test_cookiecutter.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1650 bytes
"""
    Tests cookiecutter baking process and rendered content
"""

def test_project_tree(cookies):
    result = cookies.bake(extra_context={'project_name': 'hello sam'})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'hello sam'
    assert result.project.isdir()
    assert result.project.join('template.yaml').isfile()
    assert result.project.join('README.md').isfile()
    assert result.project.join('src').isdir()
    assert result.project.join('src', 'main').isdir()
    assert result.project.join('src', 'main', 'java').isdir()
    assert result.project.join('src', 'main', 'java', 'helloworld').isdir()
    assert result.project.join('src', 'main', 'java', 'helloworld', 'App.java').isfile()
    assert result.project.join('src', 'main', 'java', 'helloworld', 'GatewayResponse.java').isfile()
    assert result.project.join('src', 'test', 'java').isdir()
    assert result.project.join('src', 'test', 'java', 'helloworld').isdir()
    assert result.project.join('src', 'test', 'java', 'helloworld', 'AppTest.java').isfile()


def test_app_content(cookies):
    result = cookies.bake(extra_context={'project_name': 'my_lambda'})
    app_file = result.project.join('src', 'main', 'java', 'helloworld', 'App.java')
    app_content = app_file.readlines()
    app_content = ''.join(app_content)
    contents = ('package helloword', 'class App implements RequestHandler<Object, Object>',
                'https://checkip.amazonaws.com', 'return new GatewayResponse', 'getPageContents')
    for content in contents:
        assert content in app_content