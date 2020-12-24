'''
Python package setup script.
'''

import setuptools

DESC = '''
Sonte (Stephen's Objective Note-Taking Engine) is a command-line
note-taking application created by Stephen Malone.

See https://bitbucket.org/stvmln/sonte for more information.
'''

setuptools.setup(
    # Basic details.
    name             = 'sonte',
    description      = "Stephen's Objective Note-Taking Engine",
    license          = 'BSD-3',
    long_description = DESC,
    url              = 'https://bitbucket.org/stvmln/sonte',
    version          = '0.2.0',

    # Author details.
    author       = 'Stephen Malone',
    author_email = 'private@example.com',

    # Package metadata.
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Terminals',
    ],

    entry_points     = {'console_scripts': ['sonte=sonte.__main__:main']},
    extras_require   = {'test': ['py.test']},
    install_requires = ['toml'],
    keywords         = 'command-line notes note-taking writing',
    packages         = setuptools.find_packages(exclude=['tests']),
)
