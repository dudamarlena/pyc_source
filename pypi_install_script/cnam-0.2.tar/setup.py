from setuptools import setup


setup(

    # Basic package information.
    name = 'cnam',
    version = '0.2',
    scripts = ['cnam'],

    # Packaging options.
    zip_safe = False,
    include_package_data = True,

    # Package dependencies.
    install_requires = ['requests>=0.10.1'],
    tests_require = ['fudge>=1.0.3', 'nose>=1.1.2'],

    # Metadata for PyPI.
    author = 'Randall Degges',
    author_email = 'rdegges@gmail.com',
    license = 'UNLICENSE',
    url = 'http://www.opencnam.com',
    keywords = 'voip http api rest caller id name cid cnam telephony telephone',
    description = 'A simple CLI program that spits out caller ID name ' \
            'information given a phone number.',
    long_description = open('README.md').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Telecommunications Industry',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Communications',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Communications :: Telephony',
        'Topic :: Internet',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],

)
