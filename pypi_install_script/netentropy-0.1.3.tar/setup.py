from distutils.core import setup
setup(
  name = 'netentropy',
  packages = ['netentropy'],   
  version = '0.1.3',      
  license='MIT',        
  description = 'Simple library for calculating information theoretic quantities in networks. Current version calculates efficiently the modified mutual information between two labelings of nodes into communities.',
  author = 'Gaston Maffei',                   
  author_email = 'gastonmaffei@gmail.com',
  url = 'https://github.com/Popeyef5/Netentropy',
  download_url = 'https://github.com/Popeyef5/Netentropy/archive/v_01_3.tar.gz',
  keywords = ['networks', 'entropy', 'information'],
  install_requires=[
          'ortools',
          'scikit-learn',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Physics',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)