from setuptools import setup, find_packages

setup(name='rotcaesarcipher',
      version='0.5',
      description='ROT-n encrypt and decrypt',
      url='https://github.com/andersongomes001/CaesarCipher',
      author='Anderson Gomes',
      author_email='comprasgomes@hotmail.com',
      license='GNU GPL v3',
      include_package_data=True,
      packages=find_packages(),
      zip_safe=False)