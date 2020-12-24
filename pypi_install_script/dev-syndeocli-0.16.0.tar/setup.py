from setuptools import setup

setup(
    name='dev-syndeocli',
    version='0.16.0',
    py_modules=['syndeocli'],
    install_requires=[
        'Click',
        'pyyaml==3.12',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        syndeocli=syndeocli:cli
    ''',
)
