from setuptools import setup, find_packages

setup(name="MegaMess_server",
      version="0.8.5",
      description="Mega messenger server",
      author="Maria Afanaseva",
      author_email="mashenkachukina@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodomex']
      )
