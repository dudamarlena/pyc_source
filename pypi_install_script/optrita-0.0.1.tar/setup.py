from setuptools import setup

requires = ['numpy', 'matplotlib.pyplot', 'pandas',  'sympy']

packages = [
	'optrita',
	'optrita.linesearch'
]

package_dir = {'optrita' : 'optrita'}
package_data = {'optrita' : []}

setup(
	name = 'optrita',
	packages = packages,
	version = '0.0.1',
	license = 'MIT',
	description = 'Optimization and Machine Learning from 0',
	author = '3omni',
	author_email = 'rita.geleta@jediupc.com',
	url = 'https://github.com/margaritageleta/optrita',
	download_url = 'https://github.com/margaritageleta/optrita/archive/0.0.1.tar.gz',
	keywords = ['python', 'optimization'],
	install_requires = requires,
	classifiers=[
    		'Development Status :: 3 - Alpha',     
    		'Intended Audience :: Developers',     
    		'Topic :: Software Development :: Build Tools',
    		'License :: OSI Approved :: MIT License',   
    		'Programming Language :: Python :: 3',     
    		'Programming Language :: Python :: 3.4',
    		'Programming Language :: Python :: 3.5',
    		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
  	],
	package_data = package_data,
	package_dir = package_dir,
)

__author__ = {'3omni' : 'rita.geleta@jediupc.com'}
__version__ = '0.0.1'
