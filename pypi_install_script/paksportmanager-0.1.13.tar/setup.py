from setuptools import setup

setup(
    name='paksportmanager',
    version='0.1.13',
    packages=['paksportmanager', 'paksportmanager.config', 'paksportmanager.data', 'paksportmanager.helpers',
              'paksportmanager.stat'],
    url='https://pypi.org/user/Ipakeev/',
    license='MIT',
    author='Ipakeev',
    author_email='ipakeev93@gmail.com',
    description='Grab sport data through paksportgrab',
    install_requires=['paklib', 'paksportgrab', 'pakselenium', 'numpy', 'scipy', 'pyod']
)
