#   Copyright 2019 Avaamo, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
Handles the building of python package
"""
from setuptools import setup
from distutils.util import convert_path

PACKAGE_NAME = 'avaamo'

main_ns = {}
version_path = convert_path(PACKAGE_NAME + '/version.py')
with open(version_path) as version_file:
        exec(version_file.read(), main_ns)

with open("README.md", "r") as fh:
    long_description = fh.read();

setup(
    name=PACKAGE_NAME,
    version=main_ns['__version__'],
    url='http://github.io/avaamo/avaamo-python',
    author='David Gwartney',
    author_email='david.gwartney@avaamo.io',
    packages=['avaamo', 'avaamo.api'],
    license='LICENSE',
    entry_points={
        'console_scripts': [
            'avaamo=avaamo.cli:main',
            'avaamo-insights=avaamo.insights_dump:main',
            'avaamo-add-doc=avaamo.add_document:main',
            'avaamo-list-docs=avaamo.list_documents:main',
            'avaamo-send-msg=avaamo.send_bot_message:main'
        ],
    },
    description='Avaamo API for Python',
    install_requires=[
        'requests >= 2.21.0',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
