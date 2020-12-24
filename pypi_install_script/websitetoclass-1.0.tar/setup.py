from setuptools import setup

def readme():
    with open('README.rst', 'r') as fo:
        return fo.read()

setup(name='websitetoclass',
      version='1.0',
      description='Converting html into classes',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Code Generators',
      ],
      keywords='class website html css converter generator',
      url='http://github.com/enchant97/Website_To_Class',
      author='enchant97',
      author_email='contact@enchantedcode.co.uk',
      license='mit',
      packages=['website_to_class'],
      include_package_data=True,
      zip_safe=False)
