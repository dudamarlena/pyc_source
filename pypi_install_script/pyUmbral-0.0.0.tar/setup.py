from distutils.core import setup
from wheel.bdist_wheel import bdist_wheel

setup(name='pyUmbral',
      version='0.0.0',
      description='Umbral: Proxy re-encryption scheme (placeholder only!)',
      long_description='Umbral: Proxy re-encryption scheme (placeholder only!)',
      packages=[],
      cmdclass={
          'bdist_wheel': bdist_wheel})
