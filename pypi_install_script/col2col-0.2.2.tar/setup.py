"""Setup.py file."""

from setuptools import setup, find_packages


# README.md file
# ==============
def readme():
    """Load readme file."""
    with open('README.md') as f:
        return f.read()


# LICENSE file
# ============
def license():
    """Load license file."""
    with open('LICENSE.md') as f:
        return f.read()


# requirements.txt file
# =====================
def requirements():
    """Load requirements file."""
    with open('requirements.txt') as f:
        return f.read()


# Description
# ===========
description = """Python package to convert units by column in XLSX files"""

# setup
# =====
setup(
    name='col2col',
    version='0.2.2',
    author='Diego Rodriguez, Gabriel Capeans',
    author_email='diego.cacheiras@gmail.com, gabriel23cg@gmail.com',
    description=description,
    url='https://github.com/gabriel23cg/col2col',
    download_url='https://github.com/gabriel23cg/col2col/archive/v0.2.2.tar.gz',
    classifiers=['Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6'
                 'Programming Language :: Python :: 3.7'],
    long_description=readme(),
    packages=find_packages(),
    install_requires=requirements(),
    include_package_data=True,
    license=license(),
    entry_points={
        'console_scripts': ['col2col=col2col.main:main']}
)
