from setuptools import setup

setup(name='pywaves-with-base58',
      version='0.8.25_03',
      description='Object-oriented library for the Waves blockchain platform',
      url='http://github.com/pywaves/pywaves',
      author='PyWaves Developers',
      author_email='dev@pywaves.org',
      license='MIT',
      packages=['pywaves'],
      keywords = ['waves', 'blockchain', 'analytics'],
      install_requires=[
            'pyblake2',
            'python-axolotl-curve25519',
            'requests'
      ]
      )


