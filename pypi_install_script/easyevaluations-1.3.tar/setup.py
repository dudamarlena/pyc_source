from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
   name='easyevaluations',
   version='1.3',
   description='Easily evaluate the predictions of machine learning algorithms',
   license='MIT',
   long_description=long_description,
   author='Leo Ko',
   author_email='33845@novasbe.pt',
   url = 'https://github.com/leo9226/easy_evaluations',
   download_url = 'https://github.com/leo9226/easy_evaluations/archive/v1.1.tar.gz',
   packages=['easyevaluations']
)