import setuptools

package = dict(
    
    name         = 'autocompleter',
    version      = '0.1.0',

    license      = 'MIT',
    author       = 'Dan Gittik',
    author_email = 'dan.gittik@gmail.com',
    url          = 'https://github.com/dan-gittik/autocompleter',

    py_modules   = ['autocompleter'],

)

if __name__ == '__main__':
    setuptools.setup(**package)
