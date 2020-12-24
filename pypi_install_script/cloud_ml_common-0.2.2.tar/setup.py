try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(name="cloud_ml_common",
      version="0.2.2",
      author="Xiaomi",
      license="Apache License",
      description="Xiaomi Cloud-ml Common",
      install_requires=["requests>=2.6.0"],
      packages=["cloud_ml_common", "cloud_ml_common.auth"])
