from setuptools import setup, find_packages

setup(name="msg_serv",
      version="1.0.0",
      description="msg_serv",
      author="Boris Ostroumov",
      author_email="borisostroumov@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodomex']
      )