
from distutils.core import setup,Extension

module=Extension("mesibo",
        sources=["src/bind.cpp","src/notify.cpp","src/core.cpp","src/globals.cpp","src/utils.cpp"], 
        include_dirs = ['include'],
        libraries = ['mesibo64']
        )

setup(name="mesibo",
        version="0.0.6",
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3 ',
        'Programming Language :: Python :: Implementation :: CPython',
        "Operating System :: Unix"
        ],
        description="Python extension module for C/C++ mesibo API",
        ext_modules=[module]        
        )
