from setuptools import setup
import os


current_path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_path, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

subpackages = []
parent = 'edpy'
subpackages_path = os.path.join(current_path, 'edpy')
for subdir, _, _ in os.walk(subpackages_path):
    subdirs = subdir.split(os.sep)
    parent_index = subdirs.index(parent) + 1
    subpackages.append('.'.join(subdirs[parent_index:]))

setup(
    name='edpy',
    version='0.0.0',
    description='',
    long_description=long_description,
    url='https://github.com/monzita/edpy',
    author='Monika Ilieva',
    author_email='example@hidden.com',
    license='MIT License',
    keywords='edpy',
    packages=[*subpackages],
    package_data={},
    py_modules=['edpy'],
    install_requires=['n'],
    entry_points = {
      'console_scripts': [],
    },
    classifiers=[
        
   ],
    zip_safe=True)