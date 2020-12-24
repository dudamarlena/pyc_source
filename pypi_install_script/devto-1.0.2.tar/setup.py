from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name="devto",
    version="1.0.2",
    description="Unoffical Dev.To Python Wrapper",
    author="BTaskaya",
    packages=find_packages(),
    long_description=readme,
    install_requires=["requests"],
    author_email='batuhanosmantaskaya@gmail.com',
    url='https://github.com/btaskaya/pydevto',
)
