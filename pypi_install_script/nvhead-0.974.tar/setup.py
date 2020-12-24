from setuptools import setup, find_packages
setup(
      name="nvhead",
      version = "0.974",
      description="convinient APIs for http headers",
      author="dapeli",
      url="https://github.com/ihgazni2/nvhead",
      author_email='terryinzaghi@163.com', 
      license="MIT",
      long_description = "refer to .md files in https://github.com/ihgazni2/nvhead",
      classifiers=[
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          ],
      packages= find_packages(),
      py_modules=['nvhead'], 
      )


# python3 setup.py bdist --formats=tar
# python3 setup.py sdist

