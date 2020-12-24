from setuptools import setup, find_packages
from os.path import join, dirname
import ks_django_response

setup(
    name='ks_django_response',
    version=ks_django_response.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=['django', 'ks-response'],
    author='Yurii Chudakov',
    author_email='kappa@ksprojects.ru',
    description='KS library for api response for Django',
    license='Apache2',
)
