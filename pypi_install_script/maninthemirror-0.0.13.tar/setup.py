with open('version', 'r') as f:
    version = f.read()

if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(
        name='maninthemirror',
        version=version,
        description='man in the mirror',
        long_description='man in the mirror',
        author='jpm',
        author_email='joepatmckenna@gmail.com',
        url='http://joepatmckenna.github.io',
        packages=['maninthemirror'])
