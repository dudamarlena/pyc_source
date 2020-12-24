from distutils.core import setup

setup(
  name = 'timer_decorator',         
  packages = ['timer_decorator'],
  version = '1.2',     
  license='MIT', 
  description = 'Decorator to measure function runtimes easily',
  author = 'ValeKnappich',                   
  author_email = 'valentin.knappich@web.de',    
  url = 'https://github.com/ValeKnappich/timer-decorator.git',   
  download_url = 'https://github.com/ValeKnappich/timer-decorator/archive/master.zip', 
  keywords = ['timer', 'decorator'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)