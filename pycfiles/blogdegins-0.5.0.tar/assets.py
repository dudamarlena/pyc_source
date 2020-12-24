# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/blogdegins-data/www.artgins.es/htmlrendercode/assets.py
# Compiled at: 2012-08-28 06:06:10
import os.path
from webassets import Environment, Bundle
css_or_scss_content = [
 'css/libs/normalize/normalize.css',
 'css/app/page.scss',
 'css/app/content.scss',
 'css/widgets/boxlist.scss']
top_js_content = [
 'js/top/modernizr.js']
bottom_js_content = [
 'js/bottom/libs/jquery/jquery.js',
 'js/bottom/libs/plugins.js',
 'js/bottom/app/page.js',
 'js/bottom/app/content.js',
 'js/bottom/widgets/boxlist.js']

def get_assets_env(code_path, output_path, debug=False):
    """ The directory structure of assets is:
        output_path
            static
                css
                js
    """
    output_path = os.path.join(output_path, 'static')
    assets_env = Environment(output_path, 'static', debug=debug)
    assets_env.config['compass_plugins'] = ['normalize']
    assets_env.config['compass_config'] = {'additional_import_paths': os.path.join(code_path, 'scss-mixins')}
    css_list = []
    scss_list = []
    for filename in css_or_scss_content:
        ext = os.path.splitext(filename)[1]
        if ext == '.scss':
            scss_list.append(filename)
        elif ext == '.css':
            css_list.append(filename)
        else:
            raise Exception('Bad extension: is %s instead of css/scss' % ext)

    css_bundle = Bundle(*css_list)
    scss_bundle = []
    for scss_file in scss_list:
        x = Bundle(scss_file, filters='compass', output=scss_file + '.css')
        scss_bundle.append(x)

    css = Bundle(css_bundle, filters='yui_css', output='css/packed.css', *scss_bundle)
    assets_env.register('css', css)
    top_js = Bundle(filters='yui_js', output='js/top.js', *top_js_content)
    assets_env.register('top_js', top_js)
    bottom_js = Bundle(filters='yui_js', output='js/bottom.js', *bottom_js_content)
    assets_env.register('bottom_js', bottom_js)
    return assets_env