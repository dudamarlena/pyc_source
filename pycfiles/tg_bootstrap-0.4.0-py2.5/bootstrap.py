# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tg_bootstrap\bootstrap.py
# Compiled at: 2008-01-12 18:05:23
import virtualenv, textwrap
__all__ = [
 'create_scripts']
version = '0.4.0'

def create_scripts(src_repository, proj, release_version):
    _do_create_script(src_repository, proj, None)
    _do_create_script(src_repository, proj, repr(release_version))
    return


def _do_create_script(src_repository, proj, release_version):
    boostrap_version = version
    escaped_substiution = '%s'
    escaped_percent = '%'
    recipe_ = _recipe % locals()
    open('%s-%s.py' % (proj, ['release', 'devel'][(release_version is None)]), 'w').write(virtualenv.create_bootstrap_script(recipe_))
    return


_recipe = textwrap.dedent('\nimport os, subprocess, sys\n\nsrc_repository_ = \'%(src_repository)s\'\nproj_ = \'%(proj)s\'\nrelease_version_ = %(release_version)s\n\nwin32 = """\nWe require Python 2.5.1. You can download it here:\n\nhttp://www.python.org/ftp/python/2.5.1/python-2.5.1.msi\n"""\n\ndarwin = """\nWe require Python 2.5.1. You can download a Universal build here:\n\nhttp://www.python.org/ftp/python/2.5.1/python-2.5.1-macosx.dmg \n"""\n\nother = """\nWe require Python 2.5.1. This version of Python is often available in\nyour operating system\'s native package format (via apt-get or yum, for\ninstance). You can also easily build Python from source on Unix-like\nsystems. Here is the source download link for Python:\n\nhttp://www.python.org/ftp/python/2.5.1/Python-2.5.1.tar.bz2\n"""\n\ndef extend_parser(parser):\n\tparser.add_option(\n\t\t\'--with-global-site-packages\',\n\t\tdest=\'no_site_packages\',\n\t\taction=\'store_false\',\n\t\thelp="Copy the contents of the global site-packages dir to the "\n\t\t\t"non-root site-packages")\n\tparser.set_default(\'no_site_packages\', True)\n\tparser.remove_option(\'--no-site-packages\')\n\ndef locate_installed_script(script_base_name):\n\tif sys.platform == \'win32\':\n\t\treturn os.path.join(bin_dir, script_base_name + \'-script.py\')\n\telse:\n\t\treturn os.path.join(bin_dir, script_base_name)\n\ndef set_bin_dir(home_dir):\n\tglobal bin_dir\n\tif sys.platform == \'win32\':\n\t\tbin_dir = os.path.join(home_dir, \'Scripts\')\n\telse:\n\t\tbin_dir = os.path.join(home_dir, \'bin\')\n\ndef run_bin_executable(prog, *args):\n\tcmd = [os.path.join(bin_dir, prog)]\n\tcmd.extend(args)\n\tsubprocess.call(cmd)\n\ndef run_py_script(*args):\n\trun_bin_executable(\'python\', *args)\n\ndef inst_package(package, *args):\n\t# We have to run the script explicitly because easy_install sets its exe to require admin\n\t# privs on Vista. We don\'t actually need such privs, so we avoid the elevation.\n\trun_py_script(locate_installed_script(\'easy_install\'), package, *args)\n\ndef check_python():\n\tif sys.version_info < (2,5):\n\t\tif sys.platform == "darwin":\n\t\t\tprint darwin\n\t\telif sys.platform == "win32":\n\t\t\tprint win32\n\t\telse:\n\t\t\tprint other\n\t\treturn False\n\telse:\n\t\treturn True\n\ndef setup_tg_for_devel(code_root):\n\tos.chdir(code_root)\n\tif os.path.exists(\'setup.py\'):\n\t\trun_py_script(\'setup.py\', \'develop\')\n\t\trun_py_script(locate_installed_script(\'tg-admin\'), \'sql\', \'create\')\n\t\treturn True\n\ndef after_install(options, home_dir):\n\tif not check_python():\n\t\tsys.exit()\n\tset_bin_dir(home_dir)\n\tif sys.platform == "win32":\n\t\tinst_package(\'pywin32\')\n\tinst_package(\'tg_bootstrap >= %(boostrap_version)s\')\n\tif release_version_ is None:\n\t\tcode_root = os.path.join(home_dir, \'src\')\n\t\tsubprocess.call([\'svn\', \'co\', src_repository_, code_root])\n\t\tsetup_tg_for_devel(code_root) or setup_tg_for_devel(os.path.join(code_root, proj_))\n\telse:\n\t\tinst_package(\'%(escaped_substiution)s == %(escaped_substiution)s\' %(escaped_percent)s (proj_, release_version_))\n')