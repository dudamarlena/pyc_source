from setuptools import setup, find_packages

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

with open('README.rst', 'r') as f:
    readme = f.read()

setup(name='dispam',
      author='xanthe1337 & Fweak',
      url='https://github.com/xanthe1337/Spammer.py',
      version=2.8,
      packages=find_packages(),
      license='MIT',
      description="A small but powerfull package to help making discord raidbots easier",
      long_description=readme,
      long_description_content_type="text/x-rst",
      include_package_data=True,
      install_requires=requirements,
      python_requires='>=3.5.3',
)