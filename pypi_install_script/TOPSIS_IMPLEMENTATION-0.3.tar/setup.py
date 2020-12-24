from distutils.core import setup

def readme():
	with open('README.md') as f:
		README = f.read()
		return README

setup(
  name = 'TOPSIS IMPLEMENTATION',         # How you named your package folder (MyLib)
  packages = ['TOPSIS IMPLEMENTATION'],   # Chose the same as "name"
  include_packages_data = True,
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Topsis',   # Give a short description about your library
  long_description = readme(),
  long_description_content_type = "text/markdown",
  author = 'DHRUV GOYAL',                  
  author_email = 'dhruvgoyal200@gmail.com',
  url = 'https://github.com/dhruvgoyal200/Topsis-implementation',
  install_requires=[
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
