from os import path
from setuptools import setup, find_packages, Extension

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

# TODO: remove this, we're not using it
"""spellfix_module = Extension(
    'simon.extension.spellfix',
    sources=[
        'simon/extension/spellfix.c'
    ],
    include_dirs=[
        'build/sqlite/',
        'build/sqlite/ext/misc'
    ]
)"""

setup(
    name='simonbot',
    version='0.0.2',
    description='yugioh card search bot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vonas/simon',
    author='Jonas van den Berg',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Board Games',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='yugioh discord bot simon',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'peewee~=3.13',
        'discord.py~=1.3',
        'python-dotenv~=0.13'
    ],
    ext_modules=[
        # spellfix_module
    ],
    entry_points={
        'console_scripts': [
            'simon=simon.__main__:main',
        ]
    },
    project_urls={
        'Bug Reports': 'https://github.com/vonas/simon/issues',
        'Source': 'https://github.com/vonas/simon',
    }
)
