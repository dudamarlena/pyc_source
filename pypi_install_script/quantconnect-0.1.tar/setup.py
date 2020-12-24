from setuptools import setup, find_packages

setup(
     name='quantconnect',
     version='0.1',
     description = 'QuantConnect API',
     url='https://www.quantconnect.com/',
     author = 'QuantConnect Python Team',
     author_email = 'support@quantconnect.com',
     packages = find_packages(),
     install_requires=['requests']
     )