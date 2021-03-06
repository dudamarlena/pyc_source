import setuptools
import re
import os

here = os.path.abspath(os.path.dirname(__file__))
release_tag_pattern = re.compile('^v[0-9]+\\.[0-9]+\\.[0-9]+-release$')

with open(os.path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

if (release_tag_pattern.match(version)):
    current_version = version[1:][:-8]
else:
    current_version = version


setuptools.setup(
    name='mc_server_manager',
    version=current_version,
    description='Manages Servers on AWS',
    url='https://github.com/bwilliam0/mc-server-manager',
    author='bwilliam0',
    author_email='dev@mycodeiscompiling.com',
    license='Apache License 2.0',
    packages=setuptools.find_packages(exclude=('scripts',)),
    entry_points={
        'console_scripts': [
            'mc-manager = mc_server_manager.mc_server_manager:main'
        ]
    },
    install_requires=[
        "boto3>=1.9.188"
        "botocore>=1.12.188"
        "docutils>=0.14"
        "jmespath>=0.9.4"
        "python-dateutil>=2.8.0"
        "s3transfer>=0.2.1"
        "six>=1.12.0"
        "urllib3>=1.25.3"
    ],
    zip_safe=False
)
