from setuptools import setup, find_packages

setup(name='unictelecomes',
      version='1.6.4',
      url='https://github.com/SamirWardak/sendmessageunictelecome',
      license='MIT',
      author='Wardak Ahmad Samir',
      author_email='wardag.as@gmail.com',
      description='Send sms from unictelecome.',
      packages=find_packages(exclude=['tests']),
      download_url = 'https://github.com/SamirWardak/sendmessageunictelecome',
      long_description=open('README.md').read(),
      install_requires=[
            'requests',
        ],
      zip_safe=False)