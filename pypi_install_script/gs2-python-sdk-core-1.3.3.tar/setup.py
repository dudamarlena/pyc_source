import os

from setuptools import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gs2-python-sdk-core',
    version='1.3.3',
    package_dir={'': 'src'},
    packages=[
        "",
        "gs2_core_client",
        "gs2_core_client.fast_requests",
        "gs2_core_client.model",
        "gs2_core_client.exception",
    ],
    install_requires=[
        'pycrypto >= 2.6.1',
    ],
    tests_require=[],
    license='Apache License 2.0',
    description='GS2 SDK for Python - Core Library.',
    url='https://gs2.io/',
    author='Game Server Services Co., LTD',
    author_email='admin@gs2.io',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)