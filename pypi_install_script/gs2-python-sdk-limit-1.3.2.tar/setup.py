import os

from setuptools import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gs2-python-sdk-limit',
    version='1.3.2',
    package_dir={'': 'src'},
    packages=[
        "",
        "gs2_limit_client",
        "gs2_limit_client.control",
        "gs2_limit_client.model",
    ],
    install_requires=[
        'gs2-python-sdk-core >= 1.3.0',
    ],
    tests_require=[],
    license='Apache License 2.0',
    description='GS2-Limit SDK for Python.',
    url='https://gs2.io/',
    author='Game Server Services Co., LTD',
    author_email='admin@gs2.io',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)