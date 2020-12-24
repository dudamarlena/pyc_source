from setuptools import setup, find_packages

github = 'https://github.com/runehistory/runehistory-cli'
version = '0.2.0'

setup(
    name='runehistory-cli',
    packages=find_packages(),
    version=version,
    license='MIT',
    python_requires='>=3.6, <4',
    description='RuneHistory CLI',
    author='Jim Wright',
    author_email='jmwri93@gmail.com',
    url=github,
    download_url='{github}/archive/{version}.tar.gz'.format(
        github=github, version=version
    ),
    keywords=['runehistory'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    setup_requires=['pytest-runner'],
    install_requires=[
        'typing',
        'requests>=2.18,<3',
        'click>=6.7,<7',
        'ioccontainer>=1.0.5,<2',
        'pyrunehistory>=1.0.4,<2',
    ],
    tests_require=[
        'pytest',
    ],
    extras_require={
        'test': [
            'coverage', 'tox'
        ]
    },
    entry_points={
        'console_scripts': [
            'runehistory=runehistory_cli.cli:run'
        ],
    },
)
