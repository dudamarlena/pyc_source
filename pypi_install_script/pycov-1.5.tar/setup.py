from setuptools import setup

setup(name='pycov',
      version='1.5',
      description='A library getting how many people are now ill with coronavirus',
      packages=['pycov'],
      author_email='kewldanil1@gmail.com',
	author="kewldan",
	url="https://pypi.org/project/pycov/",
      zip_safe=False,
	python_requires='>=3',
	python_version=">=3",
	classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
		  'Programming Language :: Python :: 3.5',
		  'Programming Language :: Python :: 3.6',
		  'Programming Language :: Python :: 3.7',
		  'Programming Language :: Python :: 3.8'
      ],
	install_requires=[
	  "requsts",
	  "lxml",
	  "bs4",
	"python_version<'3.4'"
	  ]
)