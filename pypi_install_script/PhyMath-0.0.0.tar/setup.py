from distutils.core import Extension, setup

def main():
    setup(name='PhyMath',
          ext_modules=[Extension('PhyMath', ['main.c'])])

if __name__ == '__main__':
    main()