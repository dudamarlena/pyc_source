from distutils.core import setup, Extension

module = Extension('fdir',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    sources = ['src/_fdir_.c'])



setup(
    name="fdir",
    version="0.1.0",
    description = 'Module For Iterating through OS Directories',
    url="https://github.com/m-zayan/fdir",
    download_url = 'https://github.com/m-zayan/fdir/archive/v0.1.0-alpha.tar.gz',
    author = 'Mohamed Zayan',
    author_email="zayanm410@gmail.com",
    license ='MIT',
    keywords = ['Files', 'Directories', 'OS'],  
    classifiers=[
    'Development Status :: 3 - Alpha',            
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
    ext_modules = [module]
)

