"""
Setup the package.
"""
from setuptools import find_packages, setup

with open('README.md', 'r') as read_me:
    long_description = read_me.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    version='0.1.1',
    name='pattern_recognition_cli',
    description='The command-line interface (CLI) that provides a set of commands '
                'for pattern recognition by interacting with the server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Alladin9393/Pattern-recognition',
    license='MIT',
    author='Alladin9393',
    author_email='ember.toon@protonmail.com',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pattern_recognition = cli.entrypoint:cli',
        ]
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
