from setuptools import setup, find_packages
import re

with open('pyrunehistory/__init__.py') as version_file:
    version = re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                        version_file.read()).group('version')

github = 'https://github.com/runehistory/pyrunehistory'

setup(
    name='pyrunehistory',
    packages=find_packages(),
    version=version,
    license='MIT',
    python_requires='>=3.6, <4',
    description='RuneHistory API client',
    author='Jim Wright',
    author_email='jmwri93@gmail.com',
    url=github,
    download_url='{github}/archive/{version}.tar.gz'.format(
        github=github, version=version
    ),
    keywords=['runehistory', 'api', 'client'],
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
        'simplejwt>=2.0.0,<3',
    ],
    tests_require=[
        'python-dateutil>=2.6.1,<3', 'pytest',
    ],
    extras_require={
        'test': [
            'coverage', 'tox', 'pytest', 'pytest-runner',
            'python-dateutil>=2.6.1,<3'
        ]
    }
)
