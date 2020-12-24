# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: J:\workspace\python\haf\haf\ext\jinjia2report\report.py
# Compiled at: 2020-03-21 04:56:32
# Size of source mod 2**32: 4057 bytes
import os, traceback
from jinja2 import Environment, FileSystemLoader
from jinja2.environment import TemplateStream
from haf.common.log import Log
from haf.result import EndResult
from haf.utils import Utils
logger = Log.getLogger(__name__)

class Jinja2Report(object):
    __doc__ = '\n    generate report by jinja2\n    '

    def __init__(self):
        pass

    @staticmethod
    def get_template_customer(path_: str) -> None:
        path, template = Utils.get_path(path_)
        j2r = FileSystemLoader((f"{path}"))
        j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        j2r_t = j2r_e.get_template(template)
        return j2r_t

    @staticmethod
    def get_template(key: str) -> None:
        """
        get template by the key
        key :                 template:
        None/base/online      base.html
        online-app, base_app  base_app.html
        online-web, base_web  base_app.html
        base_email            base_eamil.html
        third-pary            find the template in the path

        :param key:
        :return:
        """
        if key == 'base' or key == 'online':
            template = 'base.html'
        else:
            if key in ('online-app', 'base_app', 'online-web', 'base_web'):
                template = 'base_app.html'
            else:
                if key == 'base_email':
                    template = 'base_email.html'
                else:
                    template = key
                    if os.path.exists(template):
                        try:
                            logger.info(f"try using customer template {template}", __name__)
                            return Jinja2Report.get_template_customer(template)
                        except Exception as e:
                            try:
                                logger.error(f"Jinja2Report Customer Template Error : {traceback.format_exc()}", __name__)
                                logger.info('continue using default template to generate report !!!', __name__)
                            finally:
                                e = None
                                del e

                    template = 'base.html'
        local_dir = os.path.dirname(__file__)
        j2r = FileSystemLoader(f"{local_dir}/../resource/report/")
        j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        j2r_t = j2r_e.get_template(template)
        return j2r_t

    @staticmethod
    def report(results: EndResult, name='base'):
        """
        generate report

        :param results:
        :param name:
        :return: generate report by template and results
        """
        if results is None:
            return {'status':'error', 
             'msg':'results is None'}
        if not name:
            name = 'base'
        logger.info(f"using {name} as template", __name__)
        template = Jinja2Report.get_template(name)
        return template.generate(results=results)

    @staticmethod
    def write_report_to_file(info, report_path: str):
        """
        write stream to file
        :param info:
        :param report_path:
        :return: None
        """
        try:
            logger.info(f"generate report to {report_path}", __name__)
            stream = TemplateStream(info)
            stream.dump(report_path)
        except Exception as e:
            try:
                logger.error(e, __name__)
                traceback.print_exc()
            finally:
                e = None
                del e

    @staticmethod
    def report_online(results: EndResult):
        """
        generate online report stream
        :param results:
        :return:
        """
        if results is None:
            return {'status':'error', 
             'msg':'results is None'}
        template = Jinja2Report.get_template('online')
        return template.render(results=results)

    @staticmethod
    def report_online_app(results: EndResult):
        """
        generate online app report stream
        :param results:
        :return:
        """
        if results is None:
            return {'status':'error', 
             'msg':'results is None'}
        template = Jinja2Report.get_template('online-app')
        return template.render(results=results)