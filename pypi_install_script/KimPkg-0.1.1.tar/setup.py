from setuptools import setup

setup(name='KimPkg',
      version='0.1.1',
      description='Kim Package',
      url='http://github.com/hgkmail/KimPkg',
      author='Kim Huang',
      author_email='hgkformap@gmail.com',
      license='MIT',
      packages=['KimPkg'],
      install_requires=[
            'tornado'
      ],
      zip_safe=False)
