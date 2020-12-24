import jiracall
from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='jiracall',
    version=jiracall.__version__,
    packages=['jiracall'],
    url='https://github.com/CoolCoderCarl/JAPI',
    license='MIT Licensse',
    author='Kir',
    author_email='123qwekir2wl@gmail.com',
    description=long_description,
    python_requires='>=3.7',
    install_requires=[
    'configparser==4.0.2',
    'jira==2.0.0'
    ]
)
