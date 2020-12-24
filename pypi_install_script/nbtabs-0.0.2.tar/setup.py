from setuptools import setup, find_packages

# parse version ---------------------------------------------------------------

import re
import ast
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('nbtabs/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# setup -----------------------------------------------------------------------

setup(
    name='nbtabs',
    packages=['nbtabs'],
    version=version,
    description='Generate jupyter notebooks with tabbed code blocks',
    author='Michael Chow',
    license='MIT',
    author_email='mc_al_gh@fastmail.com',
    url='https://github.com/machow/nbtabs',
    keywords=['package', ],
    entry_points={
        "console_scripts": [
            "nbtabs = nbtabs:main",
        ],
    },
    install_requires=[
        "argh",
        "jupytext",
        "jinja2",
    ],
    include_package_data=True,
    python_requires=">=3.0",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
