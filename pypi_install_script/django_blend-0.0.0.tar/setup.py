import setuptools

import django_blend as project


# setup.cfg is a new-ish standard, so we need to check this for now
if int(setuptools.__version__.split('.', 1)[0]) < 38:
    raise EnvironmentError(
        'Please upgrade setuptools. This package uses setup.cfg, which requires '
        'setuptools version 38 or higher. If you use pip, for instance, you can '
        'upgrade easily with ` pip install -U setuptools `'
    )


setuptools.setup(
    description=project.short_description(),
    long_description=project.long_description(),
    name=project.name(),
    version=project.version_string(),
)
