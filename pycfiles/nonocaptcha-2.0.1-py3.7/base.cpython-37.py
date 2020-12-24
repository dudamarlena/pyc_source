# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/nonocaptcha/base.py
# Compiled at: 2018-12-25 20:47:59
# Size of source mod 2**32: 3870 bytes
""" Base module. """
import asyncio, logging, os, random
from nonocaptcha import package_dir
from nonocaptcha.exceptions import SafePassage, TryAgain
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
try:
    import yaml
    with open('nonocaptcha.yaml') as (f):
        settings = yaml.load(f)
except FileNotFoundError:
    print("Solver can't run without a configuration file!\nAn example (nonocaptcha.example.yaml) has been copied to your folder.")
    import sys
    from shutil import copyfile
    copyfile(f"{package_dir}/nonocaptcha.example.yaml", 'nonocaptcha.example.yaml')
    sys.exit(0)

class Clicker:

    @staticmethod
    async def click_button(button):
        click_delay = random.uniform(30, 170)
        await button.click(delay=click_delay)


class Base(Clicker):
    logger = logging.getLogger(__name__)
    if settings['debug']:
        logger.setLevel('DEBUG')
    proc_id = 0
    headless = settings['headless']
    should_block_images = settings['block_images']
    page_load_timeout = settings['timeout']['page_load'] * 1000
    iframe_timeout = settings['timeout']['iframe'] * 1000
    animation_timeout = settings['timeout']['animation'] * 1000
    speech_service = settings['speech']['service']
    deface_data = os.path.join(package_dir, settings['data']['deface_html'])
    jquery_data = os.path.join(package_dir, settings['data']['jquery_js'])
    override_data = os.path.join(package_dir, settings['data']['override_js'])

    async def get_frames(self):
        self.checkbox_frame = next((frame for frame in self.page.frames if 'api2/anchor' in frame.url))
        self.image_frame = next((frame for frame in self.page.frames if 'api2/bframe' in frame.url))

    async def click_reload_button(self):
        reload_button = await self.image_frame.J('#recaptcha-reload-button')
        await self.click_button(reload_button)

    async def check_detection(self, timeout):
        """Checks if "Try again later", "please solve more" modal appears
        or success"""
        func = '(function() {\n    checkbox_frame = parent.window.jQuery(\n        "iframe[src*=\'api2/anchor\']").contents();\n    image_frame = parent.window.jQuery(\n        "iframe[src*=\'api2/bframe\']").contents();\n\n    var bot_header = jQuery(".rc-doscaptcha-header-text", image_frame)\n    if(bot_header.length){\n        if(bot_header.text().indexOf("Try again later") > -1){\n            parent.window.wasdetected = true;\n            return true;\n        }\n    }\n\n    var try_again_header = jQuery(\n        ".rc-audiochallenge-error-message", image_frame)\n    if(try_again_header.length){\n        if(try_again_header.text().indexOf("please solve more") > -1){\n            try_again_header.text(\'Trying again...\')\n            parent.window.tryagain = true;\n            return true;\n        }\n    }\n\n    var checkbox_anchor = jQuery("#recaptcha-anchor", checkbox_frame);\n    if(checkbox_anchor.attr("aria-checked") === "true"){\n        parent.window.success = true;\n        return true;\n    }\n\n})()'
        try:
            await self.page.waitForFunction(func, timeout=timeout)
        except asyncio.TimeoutError:
            raise SafePassage()
        else:
            if await self.page.evaluate('parent.window.wasdetected === true;'):
                status = 'detected'
            else:
                if await self.page.evaluate('parent.window.success === true'):
                    status = 'success'
                else:
                    if await self.page.evaluate('parent.window.tryagain === true'):
                        await self.page.evaluate('parent.window.tryagain = false;')
                        raise TryAgain()
            return {'status': status}

    def log(self, message):
        self.logger.debug(f"{self.proc_id} {message}")