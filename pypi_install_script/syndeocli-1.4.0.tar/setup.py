from setuptools import setup

setup(
    name='syndeocli',
    version='1.4.0',
    py_modules=['syndeocli'],
    description='Command Line Interface to interact with Syndeo API for resource management',
    long_description='Command Line Interface to interact with Syndeo API for resource management',
    author='Nazar Topolnytskyi',
    author_email='ntopolnytskyy@edgegravity.ericsson.com',
    install_requires=[
        'Click==7.0',
        'pyyaml==5.1.2',
        'requests==2.20',
        'texttable==1.6.2'
    ],
    entry_points='''
        [console_scripts]
        syndeocli=syndeocli:cli
    ''',
    licence="proprietary",
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    package_data={'': ['LICENSE']},
)
