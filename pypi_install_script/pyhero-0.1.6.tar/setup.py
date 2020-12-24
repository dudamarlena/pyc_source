from distutils.core import setup
from types import SimpleNamespace

cls = list()
cls.append('Development Status :: 5 - Production/Stable')
cls.append('Intended Audience :: Developers')
cls.append('License :: OSI Approved :: GNU General Public License v3 (GPLv3)')
cls.append('Operating System :: OS Independent')
cls.append('Programming Language :: Python')
cls.append('Programming Language :: Python :: 3.6')
cls.append('Programming Language :: Python :: 3.7')
cls.append('Programming Language :: Python :: 3.8')
cls.append('Topic :: Software Development :: Build Tools')

ext = list()
ext.append('pymysql==0.9.3')
ext.append('bcrypt==3.1.7')
ext.append('google-auth-oauthlib==0.4.1')
ext.append('google-api-python-client==1.7.11')

settings = SimpleNamespace()
settings.name = 'pyhero'
settings.packages = ['pyhero']
settings.version = '0.1.6'
settings.license = 'GNU General Public License v3 (GPLv3)'
settings.description = 'PyHero is a set of packages, that can be easily use into any Python project.'
settings.author = 'Joumaico Maulas'
settings.author_email = 'maulasjoumaico@gmail.com'
settings.url = 'https://github.com/maulasjoumaico/PyHero'
settings.download_url = 'https://github.com/maulasjoumaico/PyHero/archive/0.1.6.tar.gz'
settings.install_requires = ext
settings.classifiers = cls

setup(**settings.__dict__)
