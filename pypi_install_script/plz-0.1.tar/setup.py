from setuptools import setup, find_packages


setup(
    name='plz',
    version='0.1',
    description='command-line calculator and unit conversion utility',
    author='Nazar Kanaev',
    author_email='nkanaev@live.com',
    url='https://github.com/nkanaev/plz',
    licence='MIT',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['plz=plz.cli:main']
    },
)
