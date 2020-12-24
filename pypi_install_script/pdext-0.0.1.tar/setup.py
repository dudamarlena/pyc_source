from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pdext',
      version='0.0.1',
      description='Pandas Extention python module',
      long_description=readme(),
      url='https://github.com/malneni/PdExt',
      download_url = 'https://github.com/malneni/PdExt/archive/V_001.tar.gz',
      author = 'Venkatesh Malneni',
      author_email='malneni258@gmail.com',
      license='MIT',
      py_modules = ['pdext'],
      keywords = ['pandas', 'Split Columns', 'Multiple Rows'],
      install_requires=[
          'numpy',
          'docx',
          'pandas',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License', 
          'Programming Language :: Python :: 3.7'],
      zip_safe=False,
      )
