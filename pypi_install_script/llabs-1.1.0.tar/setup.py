from distutils.core import setup
import os,llabs.__init__
from glob import glob

def get_data_names(root):
    '''
    Return list of all filenames (not directories) under root.
    '''
    temp = [root+'/*']
    for dirpath, dirnames, filenames in os.walk(root):
        temp.extend((os.path.join(dirpath, d, '*') for d in dirnames))
    names = []
    for path in temp:
        if any(os.path.isfile(f) for f in glob(path)):
            names.append(path.replace('llabs/',''))
    return names

package_data = {'llabs' : get_data_names('llabs/data')}

setup(
    name="llabs",
    version=llabs.__version__,
    author="Vincent Dumont",
    author_email="vincentdumont@gmail.com",
    packages=["llabs"],
    requires=["numpy","matplotlib","scipy","pandas"],
    package_data = package_data,
    include_package_data=True,
    scripts = glob('bin/*'),
    url="https://gitlab.com/astroquasar/programs/llabs",
    description="LLabs - Automatic DLA finder algorithm for D/H candidates",
    install_requires=[]
)
