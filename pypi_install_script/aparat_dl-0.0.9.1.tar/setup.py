from distutils.core import setup
setup(
	name = 'aparat_dl',         
	packages = ['aparat_dl'],   
	version = '0.0.9.1',      
	license='GNU3',       
	description = 'a handy tools to deal with aparat',   
	author = 'mehdi gudy',                 
	author_email = 'thisismrmehdi@gmail.com',    
	url = 'https://github.com/mehdigudy/aparat-dl',   
	download_url = 'https://github.com/mehdigudy/aparat-dl/archive/0.6.tar.gz',  
	keywords = ['aparat', 'aparat_dl', 'apart-dl'],  
	install_requires=[           
			"beautifulsoup4",
			"certifi",
			"chardet",
			"idna",
			"requests",
			"soupsieve",
			"urllib3",
			"youtube-dl",
			"lxml"
			],
	classifiers=[
		'Development Status :: 5 - Production/Stable',     
		'Intended Audience :: Developers',     
		'Intended Audience :: End Users/Desktop',
		'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
    entry_points={
        'console_scripts': [
            'aparat_dl=aparat_dl.aparat_Api:main'
        ]
    }
)