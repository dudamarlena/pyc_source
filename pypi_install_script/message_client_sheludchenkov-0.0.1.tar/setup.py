from setuptools import setup, find_packages

setup(name="message_client_sheludchenkov",
      version="0.0.1",
      description="Message Client Sheludchenkov",
      author="Aleksey Sheludchenkov",
      author_email="aleshkashell@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
