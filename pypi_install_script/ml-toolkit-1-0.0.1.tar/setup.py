from setuptools import setup, find_packages

setup(
    name='ml-toolkit-1',
    version='0.0.1',
    url='https://github.com/prajit/ml-toolkit',
    author='Prajit Nadkarni',
    author_email='prajit.24@gmail.com',
    description='ML Toolkit',
    packages=find_packages(),
    long_description=open('README.md').read(),
    zip_safe=False
)
