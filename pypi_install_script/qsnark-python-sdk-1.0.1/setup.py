"""
Detail see: https://github.com/pypa/sampleproject/blob/master/setup.py
"""
from setuptools import setup, find_packages

LONG_DESCRIPTION = 'Document see https://github.com/hyperchaincn/qsnark-python-sdk'

setup(
    name='qsnark-python-sdk',
    version='1.0.1',
    keywords='Qsnark, SDK',
    description='Qsnark SDK for Python',
    long_description=LONG_DESCRIPTION,
    license='MIT License',
    url='https://github.com/hyperchaincn/qsnark-python-sdk',
    author='hyperchaincn',
    author_email='support.dev@hyperchain.cn',
    packages=find_packages(exclude=['dist']),
    install_requires=[
        'requests>=v2.19.0,<3'
    ],
    python_requires='>=3.*',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent"
    ],
)
