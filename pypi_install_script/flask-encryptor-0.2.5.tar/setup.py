"""
Flask Encryptor
===============

Installation::

    pip install flask-encryptor

For documentation, check the github repository (https://github.com/Querdos/Flask-Encryptor).
"""

from setuptools import setup

setup(
    name                    = 'flask-encryptor',
    version                 = '0.2.5',
    url                     = 'https://github.com/Querdos/Flask-Encryptor',
    license                 = 'BSD',
    author                  = 'Hamza ESSAYEGH',
    author_email            = 'hamza.essayegh@protonmail.com',
    description             = 'Flask extension helping encrypting users personal files',
    long_description        = __doc__,
    packages                = ['flask_encryptor'],
    zip_safe                = False,
    include_package_data    = True,
    platforms               ='any',
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'pycrypto'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
