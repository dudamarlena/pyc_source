from setuptools import setup,find_packages

setup(name='hsgconv',
	packages=['hsgconv'],
    version='1.1.0',
    description='Pure Python converter for Highways England Local Grid to British National Grid - OSBG36, EPSG:27700',
    long_description=open('README.md').read(),
    author='Claudio Campanile',
    author_email='ccampanile@brydenwood.co.uk',
    download_url='https://github.com/ccampanile/hsgconv/',
	url='https://github.com/ccampanile/hsgconv/',
    py_modules=['hsgconv','hsgconv/data'],
	include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords=['geographic', 'coordinates', 'highwaysengland', 'localgrid', 'osbg36'],
    classifiers=[])
