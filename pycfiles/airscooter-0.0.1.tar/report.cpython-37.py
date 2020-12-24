# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mengwei/workspace/mine/airtest_run/airrun/report/report.py
# Compiled at: 2020-04-15 05:15:24
# Size of source mod 2**32: 25446 bytes
import json, os, io, re, six, sys
from PIL import Image
import shutil, jinja2, traceback
from copy import deepcopy
from datetime import datetime
from jinja2 import evalcontextfilter, Markup, escape
from airtest.aircv import imread, get_resolution
import airtest.core.settings as ST
from airtest.aircv.utils import compress_image
from airtest.utils.compat import decode_path, script_dir_name
from airtest.cli.info import get_script_info
from six import PY3
LOGDIR = 'log'
LOGFILE = 'log.txt'
HTML_TPL = 'log_template.html'
HTML_FILE = 'log.html'
STATIC_DIR = os.path.dirname(__file__)
_paragraph_re = re.compile('(?:\\r\\n|\\r|\\n){2,}')

@evalcontextfilter
def nl2br(eval_ctx, value):
    result = '\n\n'.join(('<p>%s</p>' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value))))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def timefmt(timestamp):
    """
    Formatting of timestamp in Jinja2 templates
    :param timestamp: timestamp of steps
    :return: "%Y-%m-%d %H:%M:%S"
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


class LogToHtml(object):
    """LogToHtml"""
    scale = 0.5

    def __init__(self, script_root, log_root='', static_root='', export_dir=None, script_name='', logfile=LOGFILE, lang='en', plugins=None, device=None, package_name=None, test_name=None):
        self.log = []
        self.script_root = script_root
        self.script_name = script_name
        self.log_root = log_root
        self.static_root = static_root or 
        self.test_result = True
        self.run_start = None
        self.run_end = None
        self.export_dir = export_dir
        self.test_name = test_name.strip().split(',') if test_name is not None else []
        self.logfile = {}
        self.lang = lang
        self.init_plugin_modules(plugins)
        self.device = device
        self.package_name = package_name
        self.get_all_tests_name()

    @staticmethod
    def init_plugin_modules(plugins):
        if not plugins:
            return
        for plugin_name in plugins:
            print('try loading plugin: %s' % plugin_name)
            try:
                __import__(plugin_name)
            except:
                traceback.print_exc()

    def _load(self, logfile):
        logfile = logfile.encode(sys.getfilesystemencoding()) if not PY3 else logfile
        logs = []
        with io.open(logfile, encoding='utf-8') as (f):
            for line in f.readlines():
                logs.append(json.loads(line))

        return logs

    def _analyse(self, logs):
        """ 解析log成可渲染的dict """
        steps = []
        children_steps = []
        for log in logs:
            depth = log['depth']
            if not self.run_start:
                self.run_start = log.get('data', {}).get('start_time', '') or 
            self.run_end = log['time']
            if depth == 0:
                steps.append(log)
            elif depth == 1:
                step = deepcopy(log)
                step['__children__'] = children_steps
                steps.append(step)
                children_steps = []
            else:
                children_steps.insert(0, log)

        translated_steps = []
        for step in steps:
            translated_steps.append(self._translate_step(step))

        return translated_steps

    def _translate_step(self, step):
        """translate single step"""
        name = step['data']['name']
        title = self._translate_title(name, step)
        code = self._translate_code(step)
        desc = self._translate_desc(step, code)
        screen = self._translate_screen(step, code)
        traceback = self._translate_traceback(step)
        assertion = self._translate_assertion(step)
        if traceback:
            self.test_result = False
        translated = {'title':title, 
         'time':step['time'], 
         'code':code, 
         'screen':screen, 
         'desc':desc, 
         'traceback':traceback, 
         'assert':assertion}
        return translated

    def _translate_assertion(self, step):
        if 'assert' in step['data']['name']:
            if 'msg' in step['data']['call_args']:
                return step['data']['call_args']['msg']

    def _translate_screen(self, step, code):
        if step['tag'] != 'function':
            return
        screen = {'src':None,  'rect':[],  'pos':[],  'vector':[],  'confidence':None}
        for item in step['__children__']:
            if item['data']['name'] == 'try_log_screen':
                snapshot = item['data'].get('ret', None)
                if isinstance(snapshot, six.text_type):
                    src = snapshot
                elif isinstance(snapshot, dict):
                    src = snapshot['screen']
                    screen['resolution'] = snapshot['resolution']
                else:
                    continue
                if self.export_dir:
                    screen['_filepath'] = os.path.join(LOGDIR, src)
                else:
                    screen['_filepath'] = os.path.abspath(os.path.join(self.log_root, src))
                screen['src'] = screen['_filepath']
                self.get_thumbnail(os.path.join(self.log_root, src))
                screen['thumbnail'] = self.get_small_name(screen['src'])
                break

        display_pos = None
        for item in step['__children__']:
            if item['data']['name'] == '_cv_match':
                if isinstance(item['data'].get('ret'), dict):
                    cv_result = item['data']['ret']
                    pos = cv_result['result']
                    if self.is_pos(pos):
                        display_pos = [
                         round(pos[0]), round(pos[1])]
                rect = self.div_rect(cv_result['rectangle'])
                screen['rect'].append(rect)
                screen['confidence'] = cv_result['confidence']
                break

        if step['data']['name'] in ('touch', 'assert_exists', 'wait', 'exists'):
            if self.is_pos(step['data'].get('ret')):
                display_pos = step['data']['ret']
            elif self.is_pos(step['data']['call_args'].get('v')):
                display_pos = step['data']['call_args']['v']
        elif step['data']['name'] == 'swipe':
            if 'ret' in step['data']:
                screen['pos'].append(step['data']['ret'][0])
                target_pos = step['data']['ret'][1]
                origin_pos = step['data']['ret'][0]
                screen['vector'].append([target_pos[0] - origin_pos[0], target_pos[1] - origin_pos[1]])
        if display_pos:
            screen['pos'].append(display_pos)
        return screen

    @classmethod
    def get_thumbnail(cls, path):
        """compress screenshot"""
        new_path = cls.get_small_name(path)
        if not os.path.isfile(new_path):
            try:
                img = Image.open(path)
                compress_image(img, new_path, ST.SNAPSHOT_QUALITY)
            except Exception:
                traceback.print_exc()

            return new_path
        return

    @classmethod
    def get_small_name(cls, filename):
        name, ext = os.path.splitext(filename)
        return '%s_small%s' % (name, ext)

    def _translate_traceback(self, step):
        if 'traceback' in step['data']:
            return step['data']['traceback']

    def _translate_code(self, step):
        if step['tag'] != 'function':
            return
        step_data = step['data']
        args = []
        code = {'name':step_data['name'], 
         'args':args}
        for key, value in step_data['call_args'].items():
            args.append({'key':key, 
             'value':value})

        for k, arg in enumerate(args):
            value = arg['value']
            if isinstance(value, dict):
                if value.get('__class__') == 'Template':
                    if self.export_dir:
                        image_path = value['filename']
                        if not os.path.isfile(os.path.join(self.script_root, image_path)):
                            if value['_filepath']:
                                shutil.copyfile(value['_filepath'], os.path.join(self.script_root, value['filename']))
                            else:
                                image_path = os.path.abspath(value['_filepath'] or )
                        arg['image'] = image_path
                        if not value['_filepath']:
                            if not os.path.exists(value['filename']):
                                crop_img = imread(os.path.join(self.script_root, value['filename']))
                    else:
                        crop_img = imread(value['_filepath'] or )
                arg['resolution'] = get_resolution(crop_img)

        return code

    @staticmethod
    def div_rect(r):
        """count rect for js use"""
        xs = [p[0] for p in r]
        ys = [p[1] for p in r]
        left = min(xs)
        top = min(ys)
        w = max(xs) - left
        h = max(ys) - top
        return {'left':left, 
         'top':top,  'width':w,  'height':h}

    def _translate_desc(self, step, code):
        """ 函数描述 """
        if step['tag'] != 'function':
            return
        name = step['data']['name']
        res = step['data'].get('ret')
        args = {i['key']:i['value'] for i in code['args']}
        desc = {'snapshot':lambda : 'Screenshot description: %s' % args.get('msg'), 
         'touch':lambda : 'Touch %s' % ('target image' if isinstance(args['v'], dict) else 'coordinates %s' % args['v']), 
         'swipe':'Swipe on screen', 
         'wait':'Wait for target image to appear', 
         'exists':lambda : 'Image %s exists' % ('' if res else 'not'), 
         'text':lambda : 'Input text:%s' % args.get('text'), 
         'keyevent':lambda : 'Click [%s] button' % args.get('keyname'), 
         'sleep':lambda : 'Wait for %s seconds' % args.get('secs'), 
         'assert_exists':'Assert target image exists', 
         'assert_not_exists':'Assert target image does not exists'}
        desc_zh = {'snapshot':lambda : '截图描述: %s' % args.get('msg'), 
         'touch':lambda : '点击 %s' % ('目标图片' if isinstance(args['v'], dict) else '屏幕坐标 %s' % args['v']), 
         'swipe':'滑动操作', 
         'wait':'等待目标图片出现', 
         'exists':lambda : '图片%s存在' % ('' if res else '不'), 
         'text':lambda : '输入文字:%s' % args.get('text'), 
         'keyevent':lambda : '点击[%s]按键' % args.get('keyname'), 
         'sleep':lambda : '等待%s秒' % args.get('secs'), 
         'assert_exists':'断言目标图片存在', 
         'assert_not_exists':'断言目标图片不存在'}
        if self.lang == 'zh':
            desc = desc_zh
        ret = desc.get(name)
        if callable(ret):
            ret = ret()
        return ret

    def _translate_title(self, name, step):
        title = {'touch':'Touch', 
         'swipe':'Swipe', 
         'wait':'Wait', 
         'exists':'Exists', 
         'text':'Text', 
         'keyevent':'Keyevent', 
         'sleep':'Sleep', 
         'assert_exists':'Assert exists', 
         'assert_not_exists':'Assert not exists', 
         'snapshot':'Snapshot', 
         'assert_equal':'Assert equal', 
         'assert_not_equal':'Assert not equal'}
        return title.get(name, name)

    @staticmethod
    def _render(template_name, output_file=None, all_case_data=[], **template_vars):
        """ 用jinja2渲染html"""
        env = jinja2.Environment(loader=(jinja2.FileSystemLoader(STATIC_DIR)),
          extensions=(),
          autoescape=True)
        env.filters['nl2br'] = nl2br
        env.filters['datetime'] = timefmt
        template = env.get_template(template_name)
        html = (template.render)(all_case_data=all_case_data, **template_vars)
        if output_file:
            with io.open(output_file, 'w', encoding='utf-8') as (f):
                f.write(html)
            print(output_file)
        return html

    def is_pos(self, v):
        return isinstance(v, (list, tuple))

    def copy_tree(self, src, dst, ignore=None):
        try:
            shutil.copytree(src, dst, ignore=ignore)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    def _make_export_dir(self):
        """mkdir & copy /staticfiles/screenshots"""
        dirname = '.'
        dirpath = os.path.join(self.export_dir, dirname)
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath, ignore_errors=True)

        def ignore_export_dir(dirname, filenames):
            if os.path.commonprefix([dirpath, dirname]) == dirpath:
                return filenames
            return []

        self.copy_tree((self.script_root), dirpath, ignore=ignore_export_dir)
        logpath = os.path.join(dirpath, LOGDIR)
        if os.path.normpath(logpath) != os.path.normpath(self.log_root):
            if os.path.isdir(logpath):
                shutil.rmtree(logpath, ignore_errors=True)
            self.copy_tree((self.log_root), logpath, ignore=(shutil.ignore_patterns(dirname)))
        if not self.static_root.startswith('http'):
            for subdir in ('css', 'fonts', 'image', 'js'):
                self.copy_tree(os.path.join(self.static_root, subdir), os.path.join(dirpath, 'static', subdir))

        return (dirpath, logpath)

    def get_relative_log(self, output_file):
        try:
            html_dir = os.path.dirname(output_file)
            return os.path.relpath(os.path.join(self.log_root, 'log.txt'), html_dir)
        except Exception:
            traceback.print_exc()
            return ''

    def get_console(self, output_file):
        html_dir = os.path.dirname(output_file)
        file = os.path.join(html_dir, 'console.txt')
        content = ''
        if os.path.isfile(file):
            try:
                content = self.readFile(file)
            except Exception:
                try:
                    content = self.readFile(file, 'gbk')
                except Exception:
                    content = traceback.format_exc() + content
                    content = content + 'Can not read console.txt. Please check file in:\n' + file

        return content

    def readFile(self, filename, code='utf-8'):
        content = ''
        with io.open(filename, encoding=code) as (f):
            for line in f.readlines():
                content = content + line

        return content

    def get_all_tests_name(self):
        try:
            data_file = os.path.join(self.log_root, 'cpu_memory.json')
            print(data_file)
            if os.path.exists(data_file):
                with open(data_file, 'r') as (f):
                    temp = json.load(f)
                    self.test_name = list(temp.keys())
        except Exception as e:
            try:
                print(e)
                traceback.print_exc()
            finally:
                e = None
                del e

    def get_cpu_memory(self, test_name):
        cpu_memory_rev = {'time_line_x':[],  'cpu_y':[],  'heap_size_y':[],  'heap_alloc_y':[]}
        try:
            data_file = os.path.join(self.log_root, 'cpu_memory.json')
            all_data = {}
            if os.path.exists(data_file):
                with open(data_file, 'r') as (f):
                    temp = json.load(f)
                    if test_name not in ('all', '_all'):
                        all_data = temp.get(test_name).get('data')
                    else:
                        for value in temp.values():
                            all_data.update(value.get('data'))

                cpu_memory = all_data
                cpu_memory_rev = {'time_line_x':list(cpu_memory.keys()), 
                 'cpu_y':[float(cpu.get('cpu')) for cpu in cpu_memory.values()], 
                 'heap_size_y':[cpu.get('heap_size') / 1024 for cpu in cpu_memory.values()], 
                 'heap_alloc_y':[cpu.get('heap_alloc') / 1024 for cpu in cpu_memory.values()]}
        except Exception as e:
            try:
                print(e)
                traceback.print_exc()
            finally:
                e = None
                del e

        return cpu_memory_rev

    def report_data(self, output_file=None, record_list=None, logfile=None, test_name=None, script_name=None):
        """
        Generate data for the report page
        :param output_file: The file name or full path of the output file, default HTML_FILE
        :param record_list: List of screen recording files
        :return:
        """
        logs = self._load(logfile)
        steps = self._analyse(logs)
        script_path = os.path.join(self.script_root, script_name or )
        info = json.loads(get_script_info(script_path))
        records = [os.path.join(LOGDIR, f) if self.export_dir else os.path.abspath(os.path.join(self.log_root, f)) for f in record_list]
        if not self.static_root.endswith(os.path.sep):
            self.static_root = self.static_root.replace('\\', '/')
            self.static_root += '/'
        data = {}
        data['steps'] = steps
        data['name'] = self.script_root
        data['scale'] = self.scale
        data['test_result'] = self.test_result
        data['run_end'] = self.run_end
        data['run_start'] = self.run_start
        data['static_root'] = self.static_root
        data['lang'] = self.lang
        data['records'] = records
        data['info'] = info
        data['log'] = self.get_relative_log(output_file)
        data['console'] = self.get_console(output_file)
        data['device'] = self.device
        data['cpu_memory'] = self.get_cpu_memory(test_name)
        data['package'] = self.package_name
        data['test_name'] = test_name
        data['data'] = json.dumps(data)
        return data

    def split_outfile(self, output_file):
        output_file = output_file.encode(sys.getfilesystemencoding()) if not PY3 else output_file
        all = []
        with io.open(output_file, encoding='utf-8') as (f):
            for line in f.readlines():
                all.append(line)

        output_file_parent = os.path.dirname(output_file)
        i = 0
        la = len(all)
        for test_name in self.test_name:
            test_log = []
            stop_count = 0
            log_file = os.path.join(output_file_parent, f"{test_name}_log.txt")
            self.logfile[test_name] = log_file
            if len(self.test_name) == 1:
                test_log = all
            elif len(self.test_name) > 1:
                while i < la:
                    json_i = json.loads(all[i])
                    if json_i['data']['name'] == 'stop_app':
                        stop_count += 1
                    test_log.append(all[i])
                    i += 1
                    if stop_count == 2:
                        break

            with open(log_file, 'w') as (f):
                f.writelines(test_log)

    def report(self, template_name=HTML_TPL, output_file=None, record_list=None):
        """
        Generate the report page, you can add custom data and overload it if needed
        :param template_name: default is HTML_TPL
        :param output_file: The file name or full path of the output file, default HTML_FILE
        :param record_list: List of screen recording files
        :return:
        """
        if not self.script_name:
            path, self.script_name = script_dir_name(self.script_root)
        else:
            if self.export_dir:
                self.script_root, self.log_root = self._make_export_dir()
                output_file = output_file if (output_file and os.path.isabs(output_file)) else (os.path.join(self.script_root, output_file or ))
                if not self.static_root.startswith('http'):
                    self.static_root = 'static/'
            log_all_file = os.path.join(self.log_root, 'log.txt')
            self.split_outfile(log_all_file)
            record_list = record_list or [f for f in os.listdir(self.log_root) if f.endswith('.mp4')]
        all_case_data = []
        for test_name in self.test_name:
            data = self.report_data(output_file=output_file, record_list=record_list, logfile=(self.logfile[test_name]), test_name=test_name,
              script_name=f"{test_name}.py")
            all_case_data.append(data)

        data_all = self.report_data(output_file=output_file, record_list=record_list, logfile=log_all_file, test_name='all')
        return (self._render)(template_name, output_file, all_case_data=all_case_data, **data_all)


def simple_report(filepath, logpath=True, logfile=LOGFILE, output=HTML_FILE):
    path, name = script_dir_name(filepath)
    if logpath is True:
        logpath = os.path.join(path, LOGDIR)
    rpt = LogToHtml(path, logpath, logfile=logfile, script_name=name)
    rpt.report(HTML_TPL, output_file=output)


def get_parger(ap):
    ap.add_argument('script', help='script filepath')
    ap.add_argument('--outfile', help='output html filepath, default to be log.html', default=HTML_FILE)
    ap.add_argument('--static_root', help='static files root dir')
    ap.add_argument('--log_root', help='log & screen data root dir, logfile should be log_root/log.txt')
    ap.add_argument('--record', help='custom screen record file path', nargs='+')
    ap.add_argument('--export', help='export a portable report dir containing all resources')
    ap.add_argument('--lang', help='report language', default='en')
    ap.add_argument('--plugins', help='load reporter plugins', nargs='+')
    ap.add_argument('--report', help='placeholder for report cmd', default=True, nargs='?')
    ap.add_argument('--device', help='device information', default='Android', nargs='?')
    ap.add_argument('--package', help='package information', default='com.xihu.shihuimiao', nargs='?')
    ap.add_argument('--test_name', help='test name information', default='test_4', nargs='?')
    return ap


def main(args):
    path, name = script_dir_name(args.script)
    record_list = args.record or 
    log_root = decode_path(args.log_root) or 
    static_root = args.static_root or 
    static_root = decode_path(static_root)
    export = decode_path(args.export) if args.export else None
    lang = args.lang if args.lang in ('zh', 'en') else 'en'
    plugins = args.plugins
    device = args.device
    package_name = args.package
    test_name = args.test_name
    print(static_root, export)
    rpt = LogToHtml(path, log_root, static_root, export_dir=export, script_name=name, lang=lang, plugins=plugins, device=device,
      package_name=package_name,
      test_name=test_name)
    rpt.report(HTML_TPL, output_file=(args.outfile), record_list=record_list)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    args = get_parger(ap).parse_args()
    main(args)