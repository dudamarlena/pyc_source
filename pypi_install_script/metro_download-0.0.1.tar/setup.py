from setuptools import setup

setup(
    name='metro_download',
    version='0.0.1',
    description='Downloads Brazilian Metro newspaper',
    author='Marcelo Subtil Marcal',
    author_email='marcelo@smarcal.com',
    license='MIT',
    py_modules=['metro'],
    install_requires=[
        'datetime',
        'Click',
        'requests',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        metro_download=metro_download:cli
    ''',
)
