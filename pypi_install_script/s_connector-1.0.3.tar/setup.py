from setuptools import setup, find_packages
from os.path import join, dirname
import s_connector as connector


setup(
    name='s_connector',
    version=connector.__version__,
    author="Kiseev Nikolay",
    author_email="kiseev.nikolay@gmail.com",
    description='S_Connector',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nkiseev/S_Connector",
    install_requires=[
        'mysqlclient',
        'psycopg2',
        'PyYAML',
        'S-Logger',
    ],
)

