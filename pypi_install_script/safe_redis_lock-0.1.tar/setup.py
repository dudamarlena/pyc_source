from setuptools import setup,find_packages

with open("README.rst", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='safe_redis_lock',
      version='0.1',
      description='a safe redis lock in Single node Redis',
      long_description=long_description,
      url='https://gitee.com',
      author='liuyancong',
      author_email='lyc456789@163.com',
      license='MIT',
      install_requires=[
        "redis>=3.0.0"
    ],
      packages=find_packages(),
      )
