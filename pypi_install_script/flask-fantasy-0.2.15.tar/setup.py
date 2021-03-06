from setuptools import find_packages, setup

version = "0.2.15"

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

requirements_list = [
    'python-dateutil',
    'xmltodict',
    'dicttoxml',
    'gunicorn',
    'redis',
    'requests',
    'raven',
    'blinker',
    'celery',
    'webargs',
    'mongoengine',
    'pymysql',
    'cryptography',
    'bcrypt',
    'pycrypto',
    'sqlalchemy-utils',
    'flask',
    'flask-sqlalchemy',
    'flask-caching',
    'flask-migrate',
    'flask-admin',
    'flask-security',
    'flask-mongoengine',
    'flask-socketio',
    'gevent',
    'gevent-websocket'
]

setup(
    name='flask-fantasy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements_list,
    version=version,
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/wangwenpei/fantasy',
    download_url='https://github.com/wangwenpei/fantasy/tarball/master',
    license='MIT',
    author='WANG WENPEI',
    zip_safe=False,
    test_suite="tests",
    author_email='stormxx@1024.engineer',
    description='A bootstrap tool for Flask APP',
    keywords='fantasy,flask',
)
