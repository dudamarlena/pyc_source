

from setuptools import setup, find_packages
from core import version
setup(
    name='matches-cli',
    version=version.__version__,
    packages=find_packages(),
    include_package_data=True,
    author='tiny',
    author_email='tiny.hoooooo@gmail.com',
    url='https://github.com/Tiny-hoooooo',
    install_requires=[
        'click',
        'requests',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        matches=core.main:matches
    ''',
)