#! usr/bin/python
# -*- coding: utf-8 *-* 

from distutils.core import setup
setup(
    name = 'caspertools',
    packages = ['caspertools'],
    version = '1.0',
    description = 'Tools used for hidden navigation',
    author = 'José Fº Queija',
    author_email = 'pepekiko@gmail.com',
    url = 'https://github.com/jfqueija/caspertools',
    download_url = 'https://github.com/jfqueija/caspertools/tarball/0.1',
    keywords = ['hidden', 'navigation', 'tor','privoxy'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    project_urls={ 
        'Bug Reports': 'https://github.com/jfqueija/caspertools/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'https://github.com/jfqueija/caspertools/stargazers',
        'Source': 'https://github.com/jfqueija/caspertools',
    },
    classifiers = [  
        # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    
)