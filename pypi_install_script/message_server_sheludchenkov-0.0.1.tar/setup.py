from setuptools import setup, find_packages

setup(name="message_server_sheludchenkov",
      version="0.0.1",
      description="Message Server Sheludchenkov",
      author="Aleksey Sheludchenkov",
      author_email="aleshkashell@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )