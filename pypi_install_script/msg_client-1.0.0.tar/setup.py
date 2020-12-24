from setuptools import setup, find_packages

setup(name="msg_client",
      version="1.0.0",
      description="msg_client",
      author="Boris Ostroumov",
      author_email="borisostroumov@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodomex']
      )