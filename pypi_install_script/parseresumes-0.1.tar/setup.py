import setuptools
from distutils.core import setup
setup(
  name = 'parseresumes',
  packages =setuptools.find_packages(),
  version = '0.1',
  license='MIT',
  description = 'Parse resumes and generate scores',
  author = 'Subodh Shakya',
  author_email = 'subodh.shakya@infodevelopers.com.np',
  url = 'https://gitlab.com/SubodhShakya/resumescoringdep1.0.git',
  download_url = 'https://gitlab.com/SubodhShakya/resumescoringdep1.0/-/archive/v1.0.0.0/resumescoringdep1.0-v1.0.0.0.tar.gz',
  keywords = ['resumeparser', 'resumescorer', 'resumematcher'],
  extras_require = {
  'dev': ['check-manifest'],
  'test': ['coverage'],
  },
  install_requires=[
          'docx2txt',
          'blis',
          'cymem',
          'keras',
          'nltk',
          'numpy',
          'matplotlib',
          'pytesseract',
          'requests',
          'scikit-learn',
          'sklearn',
          'scipy',
          'tensorflow',
          'tika',
          'urllib3',
          'wasabi',
          'wrapt',
          'pillow',
          'wasabi',
          'gensim',
          'spacy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
