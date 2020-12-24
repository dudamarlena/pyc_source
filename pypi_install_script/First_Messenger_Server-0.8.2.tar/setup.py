from setuptools import setup, find_packages

setup(name="First_Messenger_Server",
      version="0.8.2",
      description="Messenger_Server",
      author="Pavel Dudkov",
      author_email="paveldudkov003@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
