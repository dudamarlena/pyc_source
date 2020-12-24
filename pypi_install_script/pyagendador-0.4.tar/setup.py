from setuptools import setup, find_packages
 
setup(name='pyagendador',
      version='0.4',
      url='https://github.com/blbcava/Agendador-Python',
      license='MIT',
      author='Bruno Cavalcante',
      author_email='bruno.cavalcante2121@outlook.com.br',
      description='return a comparable value pattern of date and time from system and a date and time defined by user. The objective of this package is easier the building of projects that needs to be schedule',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.txt').read(),
      zip_safe=False)