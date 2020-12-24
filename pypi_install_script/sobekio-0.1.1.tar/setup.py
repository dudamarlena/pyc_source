from setuptools import setup

setup(name='sobekio',
      version='0.1.1',
      description='Support reading output (.HIS) from Sobek Version 2',
      url='http://github.com/dinhquanght/sobekio_py',
      author='D. Quang Duong',
      author_email='dinhquanght@gmail.com',
      license='GPL3',
      packages=['sobekio'],
      keywords = ['Sobek', 'Sobek River', 'Deltares', 'HIS'],
	  install_requires=['pandas', 'numpy', 'configparser', 'datetime'],
      zip_safe=False)