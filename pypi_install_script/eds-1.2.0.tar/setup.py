# Copyright 2020 Rockabox Media Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

with open('README.md', 'r') as fd:
    long_description = fd.read()

setup(
    name='eds',
    version='1.2.0',
    license='Apache 2.0',
    description='A series of high-level utilities on top of the google-cloud-python libraries.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rockabox/eds',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only'
    ],
    author='The Scoota Engineering Team',
    author_email='engineering@scoota.com',
    python_requires='>=3.6',
    install_requires=[
        'arrow>=0.15',
        'Click<8',
        'colorama',
        'pyyaml',
        'rfc3339',
    ],
    extras_require={
        'eds': [
            'google-cloud-bigquery>=1.24.0',
            'google-cloud-datastore>=1.11.0',
            # Explicitly put grpcio in requirements.txt to mitigate
            # https://github.com/googleapis/google-cloud-python/issues/6259
            'grpcio>=1.2.0',
        ],
        'mysql': [
            'PyMySQL',
            'sqlalchemy>=1.3,<1.4',
        ],
        'storage': [
            'google-cloud-storage==1.23',
        ],
        'tests': [
            'Flask==1.1.1',
        ],
    },
    packages=find_packages(),
    zip_safe=True
)
