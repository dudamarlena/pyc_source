from setuptools import setup, find_packages

setup(
  name = 'uo_puddles',         # How you named your package folder (MyLib)
  packages = ['uo_puddles'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Data sciency functions to enhance pandas, numpy, etc.',   # Give a short description about your library
  author = 'Stephen Fickas',                   # Type in your name
  author_email = 'stephenfickas@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/fickas/uo_puddles',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/fickas/uo_puddles/archive/v0.2.tar.gz',    # I explain this later on
  keywords = ['Data science'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          #'validators',
          #'beautifulsoup4',
      ],
  #packages=find_packages(exclude=['tests']),
  long_description=open('README.md').read(),
  zip_safe=False,

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Education',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3 :: Only',
    #'Programming Language :: Python :: 3.4',
    #'Programming Language :: Python :: 3.5',
    #'Programming Language :: Python :: 3.6',
  ],
)

'''
When changing the github repository (by a git push -u origin master), you can create a new release that will be obtained with pip. Cool.
First, go to github.com and navigate to your repository. Next, click on the tab “releases” and then on “Create a new release”. Now,
define a Tag version (it is best to use the same number as you used in your setup.py version-field: v_01. Add a release title and a
description (not that important), then click on “publish release”. Now you see a new release and under Assets, there is a link to
Source Code (tar.gz). Right-click on this link and chose Copy Link Address. Paste this link-address into the download_url field
in the setup.py file. Every time you want to update your package later on, upload a new version to github, create a new release
 as we just discussed, specify a new release tag and copy-paste the link to Source into the setup.py file (do not forget to also
  increment the version number).
'''