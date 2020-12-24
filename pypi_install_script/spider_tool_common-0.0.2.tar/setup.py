from distutils.core import setup

setup(
    name='spider_tool_common',
    version='0.0.2',
    description='spidertool',
    author='yhl',
    author_email='yyqq188@foxmail.com',
    packages=['spider_tool_common',
              'spider_tool_common.deploy_template',
              'spider_tool_common.item_template',
              'spider_tool_common.main_template',
              'spider_tool_common.pipeline_template',
              'spider_tool_common.settings_template',
              'spider_tool_common.spider_template']
)
