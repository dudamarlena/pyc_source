# -*- coding: utf-8 -*-

import os
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

if __name__ == '__main__':
    from distutils.core import setup
    extra_files = package_files('pyZiagn')
    setup(name='pyZiagn',
          version='0.1.5',
          description='Python librarY for material characteriZation based on experImental dAta for lightweiGht desigN',
          author='E. J. Wehrle',
          url='https://github.com/e-dub/pyZiagn',
          package_data={'': extra_files},
          license='gpl-3.0',
          packages=['pyZiagn'],
          install_requires=['numpy',
                            'matplotlib',
                            'matplotlib2tikz',
                            'pandas'])
