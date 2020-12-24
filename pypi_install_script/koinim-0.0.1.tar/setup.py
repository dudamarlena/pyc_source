import koinim
from setuptools import setup

def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()


setup(
    name=koinim.__name__,
    version=koinim.__version__,
    url=koinim.__url__,
    author=koinim.__author__,
    author_email=koinim.__author_email__,
    description=koinim.__description__,
    long_description=fread('README.md'),
    license='MIT',
    py_modules=['koinim'],
    platforms='windows',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
