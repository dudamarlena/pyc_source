from setuptools import find_packages, setup

setup(
    name='django-bootstrap-sass',
    packages=find_packages(),
    include_package_data=True,
    version='1.0.0',
    author='Kevin Etienne',
    author_email='etienne.kevin@gmail.com',
    url='http://github.com/ekevin/django-bootstrap-sass',
    license='Apache licence, see LICENCE',
    description='Bootstrap sass file for django',
    long_description=open('README.rst').read(),
)
