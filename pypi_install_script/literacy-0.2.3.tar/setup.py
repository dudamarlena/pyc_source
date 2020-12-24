import os
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

folder = '~/.literacy'
download_site = 'https://raw.githubusercontent.com/holyfiddlex/literate-git-hooks/master/hooks'

with open('README.md') as f:
    long_description = f.read()

def setup_download(hook):
    print("Setting up library")
    if not(os.path.isdir(folder)):
        os.system(f'mkdir {folder}')
    print(f"Created {folder}")
    os.system(f'wget {download_site}/{hook} -O {folder}/{hook}')
    os.system(f'chmod +x {folder}/{hook}')
    print("Finished")

class LibrarySetup(install):
    def run(self):
        hooks = ['pre-commit']
        for hook in hooks:
            setup_download(hook)
        install.run(self)

setup(name='literacy',
      version='0.2.3',
      url='https://github.com/holyfiddlex/literacy',
      author='Héctor de la Rosa Prado',
      author_email='hoftherose@gmail.com',
      description='Tools for literate programming in python and jupyter notebooks, following the functionality of Fastai v2 dev https://github.com/fastai/fastai_dev',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['literacy'],
      scripts=['bin/literate-git-hooks', 'bin/git-hook'],
      cmdclass={
          'develop': LibrarySetup,
          'install': LibrarySetup
      },
      zip_safe=False)
