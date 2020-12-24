from setuptools import setup, find_packages
from diabase import __version__


long_description = """
=======
Diabase
=======

Diabase is an Asyncio-powered RPC over TCP.

We intent to try it over UDP in the future.

By now, check Bitbucket_.

.. _Bitbucket: https://bitbucket.org/cacilhas/diabase
"""


setup(
    name='diabase',
    version=__version__,
    description='Asyncio-powered RPC',
    long_description=long_description,
    author='ℛodrigo Arĥimedeς ℳontegasppa Cacilhας',
    author_email='batalema@cacilhas.info',
    url='https://bitbucket.org/cacilhas/diabase',
    packages=find_packages(),
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
    ],
)
