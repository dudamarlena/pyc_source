from distutils.core import setup
setup(
  name = 'changeCalculatorWithDenominalsPackage',
  packages = ['change_calculator_denominals'],  
  version = '0.3',      
  license='MIT',        
  description = 'calculates minimum amount of coins for change. If you want to use the program, pip install and then call calculateChange ',  
  author = 'Rokas Alechnavicius',                  
  author_email = 'rokasalech@gmail.com',      
  url = 'https://gitlab.com/rokasalech/topkek',   
  download_url = 'https://gitlab.com/rokasalech/topkek/-/archive/REL3/topkek-REL3.tar.gz',
  keywords = ['test'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  entry_points={
    "console_scripts": [
        "calculateChange=change_calculator_denominals.progrem:main",
        ]
    },
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
