from setuptools import setup


setup(
    name             = 'Torrelque',
    version          = '0.2.0',
    author           = 'saaj',
    author_email     = 'mail@saaj.me',
    packages         = ['torrelque'],
    url              = 'https://heptapod.host/saajns/torrelque',
    license          = 'LGPL-3.0-only',
    description      = 'Asynchronous Redis-based reliable queue package',
    long_description = open('README.rst', 'rb').read().decode('utf-8'),
    platforms        = ['Any'],
    keywords         = 'python redis asynchronous reliable-queue work-queue',
    classifiers      = [
        'Topic :: Software Development :: Libraries',
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers'
        ],
    install_requires = ['aredis >= 1.1, < 2'],
    extras_require   = {'test': ['asynctest < 0.14']},
)
