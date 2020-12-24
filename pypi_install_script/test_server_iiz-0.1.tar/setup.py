from setuptools import setup, find_packages

setup(name="test_server_iiz",
      version="0.1",
      description="Alfa test client chat",
      author="Ilya Zakharov",
      author_email="axe-ska@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
