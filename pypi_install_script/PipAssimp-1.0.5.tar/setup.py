from setuptools import setup, find_packages
setup(
    name = 'PipAssimp',         # How you named your package folder (MyLib)
    packages = ['PipAssimp'],   # Chose the same as "name"
    version = '1.0.5',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Conveniece pkg for install assimp/pyassimp from requirements.txt',   # Give a short description about your library
    author = 'James Ford',                   # Type in your name
    author_email = 'jameslford8@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/jameslford/PipAssimp',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/jameslford/PipAssimp/archive/v0.0.1.tar.gz',    # I explain this later on
    keywords = ['3D', 'File Conversion', 'gltf', 'glb', 'obj'],   # Keywords that define your package best
    install_requires=['numpy'],
    # # package_data = {'': ['libassimp.so.5.0.1']},
    # data_files = [('', 'libassimp.so.5.0.1')],
    # include_package_data=True,
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