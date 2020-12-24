import setuptools

setuptools.setup(
  name = 'pykitut',         # How you named your package folder (MyLib)
  packages = ['pykitut'],   # Chose the same as "name"
  version = '0.1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'unittest util',   # Give a short description about your library
  author = 'Zhang Yanpo',                   # Type in your name
  author_email = 'drdr.xp@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/drmingdrmer/pykitut',   # Provide either the link to your github or to your website
  # download_url = 'https://github.com/drmingdrmer/pykitut/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['unittest'],   # Keywords that define your package best
  install_requires=[],
  python_requires='>=2.7,!=3.0.*,!=3.1.*',
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries', 
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
