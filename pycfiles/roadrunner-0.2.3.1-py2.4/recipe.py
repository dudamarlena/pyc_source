# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/roadrunner/recipe.py
# Compiled at: 2009-06-16 00:05:39
import os, fnmatch, shutil
from zc.recipe.egg.egg import Scripts

class RoadrunnerRecipe(Scripts):
    """
    generic options:
    packages_under_test = list of regex packages
    preload_packages = list of packages
    """
    __module__ = __name__

    def __init__(self, buildout, name, options):
        super(RoadrunnerRecipe, self).__init__(buildout, name, options)
        self.instance_part = buildout[options.get('zope2-instance', 'instance')]
        self.part_dir = self.buildout['buildout']['directory'] + '/parts/' + self.name
        self.packages_under_test = options.get('packages-under-test', '').split()

    def install(self):
        """
        emulate this sort of thing:
        [roadrunner]
        recipe = zc.recipe.egg
        eggs =
            ${instance:eggs}
            roadrunner
        extra-paths = 
        initialization =
            conf_file = "${instance:location}/etc/zope-roadrunner.conf"
        arguments = conf_file, "${instance:zope2-location}", "${buildout:directory}"
        """
        options = self.options
        vars = dict(instance_location=self.instance_part['location'], zope2_location=self.instance_part['zope2-location'], preload_modules=options.get('preload-modules', ''), packages_under_test=self.packages_under_test, buildout_home=self.buildout['buildout']['directory'], part_dir=self.part_dir)
        options['eggs'] = ('\n').join(options.get('eggs', '').split() + self.instance_part['eggs'].split() + ['roadrunner'])
        options['initialization'] = 'zope_conf = \'%(part_dir)s/etc/zope.conf\'\npreload_modules = \'%(preload_modules)s\'\npackages_under_test = %(packages_under_test)s\nzope2_location = \'%(zope2_location)s\'\nbuildout_home = \'%(buildout_home)s\'\npart_dir = \'%(part_dir)s\'\nsys.path.append(zope2_location + "/lib/python")\n' % vars
        options['arguments'] = 'zope_conf, preload_modules, packages_under_test, zope2_location, buildout_home, part_dir'
        options['extra_paths'] = '%(zope2_location)s/lib/python' % vars
        options['scripts'] = 'rrplone=' + self.name
        return super(RoadrunnerRecipe, self).install()

    def update(self):
        return self.install()


class RoadrunnerPloneRecipe(RoadrunnerRecipe):
    """
    zope recipe options:
    
    zope_instance
    """
    __module__ = __name__

    def is_package_under_test(self, filepath):
        for pattern in self.packages_under_test:
            if fnmatch.fnmatch(filepath, '*' + pattern + '*'):
                return True

        return False

    def configure_roadrunner_instance(self):
        """
        copy a zope instance to work with roadrunner packages under test
        """
        if os.path.exists(self.part_dir):
            shutil.rmtree(self.part_dir)
        instance = self.instance_part['location']
        shutil.copytree(instance, self.part_dir)
        zcml_dest = self.part_dir + '/etc/package-includes'
        for (dirpath, dirnames, filenames) in os.walk(zcml_dest):
            for filename in filenames:
                if self.is_package_under_test(filename):
                    path = dirpath + '/' + filename
                    os.remove(path)

        zopeconf_dest = '%s/etc/zope.conf' % self.part_dir
        zopeconf = file(zopeconf_dest).read()
        zopeconf = zopeconf.replace(instance, self.part_dir)
        file(zopeconf_dest, 'w').write(zopeconf)

    def install(self):
        self.configure_roadrunner_instance()
        return super(RoadrunnerPloneRecipe, self).install() + [self.part_dir]