from setuptools import setup

setup(
        name='jidoka',
        version='0.1.3',
        author = "Johannes Daniel Nuemm",
        author_email = "daniel.nuemm@gmail.com",
        description = ("Simple build tool for sass, coffescript and many more..."),
        license = "MIT",
        url = "https://github.com/monocult/jidoka",
        py_modules=['jidoka'],
        install_requires=[
            'CoffeeScript',
            'click',
            'jsmin',
            'jsonschema',
            'libsass',
            'watchdog',
            'csscompressor',
            'htmlmin',
            'Markdown'
            ],
        entry_points='''
            [console_scripts]
            jidoka=jidoka:cli
        ''',
)
