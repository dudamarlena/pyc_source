from distutils.core import setup
setup(
  name = 'codemate',         # How you named your package folder (MyLib)
  packages = ['codemate'],   # Chose the same as "name"
  version = '0.1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Useful data structures such as Stacks, and Queues',   # Give a short description about your library
  author = 'Joseph Mpo Yeti',                   # Type in your name
  author_email = 'josephmpo@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/joseph-mpo-yeti/codemate',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/joseph-mpo-yeti/datastruct/archive/v1.0.3-alpha.tar.gz',    # I explain this later on
  keywords = ['data', 'structure', 'stack', 'queue', 'bst', 'linked', 'list', 'package'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3'      #Specify which pyhton versions that you want to support
  ],
)