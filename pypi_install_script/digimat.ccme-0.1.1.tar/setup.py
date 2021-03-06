from setuptools import setup, find_packages

setup(
    name='digimat.ccme',
    version='0.1.1',
    description='Digimat CCME',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
