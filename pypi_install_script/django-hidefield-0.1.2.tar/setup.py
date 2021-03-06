from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, RuntimeError):
    long_description = ''

setup(
    name='django-hidefield',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    version='0.1.2',
    description='hide fields in django admin',
    long_description=long_description,
    author='Joerg Breitbart',
    author_email='j.breitbart@netzkolchose.de',
    url='https://github.com/jerch/django-hidefield',
    download_url='https://github.com/jerch/django-hidefield/archive/0.1.2.tar.gz',
    keywords=['django', 'widget', 'admin', 'field', 'hide'],
    classifiers=[],
)
