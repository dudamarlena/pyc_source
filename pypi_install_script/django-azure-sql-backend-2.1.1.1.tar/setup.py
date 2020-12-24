try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: BSD License",
    "Framework :: Django",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Internet :: WWW/HTTP",
]

setup(
    name="django-azure-sql-backend",
    version="2.1.1.1",
    description="Django backend for Microsoft SQL Server and Azure SQL Database using pyodbc",
    long_description=open("README.rst").read(),
    author="Elmar Langholz",
    author_email="langholz@gmail.com",
    url="https://github.com/langholz/django-azure-sql-backend",
    license="BSD",
    packages=["sql_server", "sql_server.pyodbc"],
    install_requires=["Django>=2.1.0,<2.2", "pyodbc>=3.0", "msal>=1.2.0"],
    classifiers=CLASSIFIERS,
    keywords="azure django",
)
