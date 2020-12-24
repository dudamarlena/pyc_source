# -*- coding: UTF-8 -*-

import re
from os import path

from setuptools import setup, find_packages


def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(path.join(project, '__init__.py')).read())

    return result.group(1)


with open('README.md', encoding='utf-8') as readme_file:
    _long_description = readme_file.read()

setup(
    author='handy',
    author_email='cvdnn@foxmail.com',
    url='https://pypi.org/project/paddle-wrap/',

    license='Apache v2.0',
    description='paddle wrap',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    keywords=["paddle", "paddlehub"],

    name='paddle-wrap',
    version='0.0.9',

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['paddlehub', 'numpy', 'prettytable'],

    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
