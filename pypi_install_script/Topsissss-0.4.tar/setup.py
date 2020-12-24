from distutils.core import setup

def readme():
	with open('README.md') as f:
		README = f.read()
		return README

setup(
  name = 'Topsissss',         # How you named your package folder (MyLib)
  packages = ['Topsissss'],   # Chose the same as "name"
  include_packages_data = True,
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Topsis code',   # Give a short description about your library
  long_description = readme(),
  long_description_content_type = "text/markdown",
  author = 'Deepak Gupta',                   # Type in your name
  author_email = 'deepakgupta221999@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/deepak199922/Topsisss',   # Provide either the link to your github or to your website
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)