from distutils.core import setup


setup(
    # Application info:
    name='nmap_parser',
    version='0.0.0',
    author='Ramces Chirino',
    author_email='ramces@chirinosky.com',
    url='https://github.com/chirinosky/nmap_parser',
    description='Nmap XML parser',
    long_description='Nmap XML parser',

    packages=['nmap_parser'],

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Other Audience',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    # What does the project relate to?
    keywords='nmap pentest security',
)
