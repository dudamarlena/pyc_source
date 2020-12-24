"""Package setup."""
from setuptools import setup, find_packages

setup(
    name="cmtimeout",
    version="1.0.3",
    description="Python ContextManager timeout handler library.",
    long_description=open("README.rst").read(),
    author="Morteza Nourelahi Alamdari",
    author_email="me@mortezana.com",
    keywords=["context-manager", "timeout"],
    license="GPLv3.0",
    url="https://github.com/mortezaipo/cmtimeout",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=2',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
    ])
