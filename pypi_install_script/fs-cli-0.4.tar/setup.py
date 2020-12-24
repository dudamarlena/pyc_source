import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="fs-cli",
    version="0.4",
    author="Dmitry Kotov",
    author_email="dmitrii.kotov@fogstream.com",
    description="Fogstream CLI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url='https://github.com/fogstream/fs-cli',
    entry_points={
        'console_scripts': ['fs-cli=fs_cli.cli:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    install_requires=[
        'GitPython==2.1.11',
        'Jinja2==2.10',
        'Click==7.0'
    ]
)