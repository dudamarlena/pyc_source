# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/LeslieZhu/.pyenv/versions/2.7.15/Python.framework/Versions/2.7/lib/python2.7/site-packages/orgnote/config.py
# Compiled at: 2019-11-27 20:06:24
"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""
from __future__ import absolute_import
from yaml import load, dump, FullLoader
import os, os.path

class Config(object):
    _default_yml = '# OrgNote Configuration\n## Docs: https://orgnote.readthedocs.io/zh_CN/latest/\n## Source: https://github.com/LeslieZhu/OrgNote\n\n# Site\ntitle: OrgNote\nsubtitle: "A simple org-mode blog, write blog by org-mode in Emacs"\n\nauthor: OrgNote\nemail: pythonisland@gmail.com\n\nlanguage: zh-CN\n\n# About this blog\ndescription: "Use OrgNote."\nkeywords: "OrgNote,Emacs,org-mode,blog,python,geek"\n\n# URL\n## If your site is put in a subdirectory, set url as \'http://yoursite.com/child\' and root as \'/child/\'\nurl: http://yoursite.com\nroot: /\n\n\n# Directory\n# if the source_dir is ./notes, then set \'source_dir\' as \'notes\', not include the \'/\'\npublic_dir: public\nsource_dir: notes\nimages_dir: images\nfiles_dir: data\n\n\n# Category & Tag\ndefault_tag: "默认"\n\n# Nopublic Tab\n# public: start with \'-\'\n# nopublic: start with \'+\'\nnopublic_tag: "暂不公开"\nreading_mode_keyword: "随笔"\n\n# Theme\n# the default is \'freemind\' and it\'s only theme for OrgNote now\ntheme: freemind\n\n# css highlight\n# the defaulit is \'default\'\n# pygments: manni igor xcode vim autumn vs rrt native perldoc borland tango\n# emacs friendly monokai paraiso-dark colorful murphy bw pastie paraiso-light trac default fruity \ncss_highlight: default\n\n# Pagination\n## the note num of each page\nper_page: 6\n\n\n# duoshuo\nduoshuo_shortname:\n\n# https://utteranc.es/\nutteranc_repo:\n\n# WeChat Official Accounts\nweixin_name:\n#weixin_public: images/weixin.jpg\n\n# donate\n#disable: set name as blank\n# "赞赏支持"\ndonate_name: "" \ndonate_wechatpay: images/wechatpay.png\ndonate_alipay: images/alipay.png\n\n\n# RSS\n# ReadMore|ReadAll\nrss_type: "ReadMore"\n\n\n# layout\n## 1: enable\n## 0: disable\n### if \'sidebar_show` is disable, igore all `sidebar` option\n### the sidebar item display as the config order, sidebar items list:\n### sidebar_latest,sidebar_tags,sidebar_time,sidebar_weibo,sidebar_link\n###\n### sidebar_show_page: if show sidebar in each note page,default enable\n### sidebar_contain_name: the contain title in sidebar\n### sidebar_contact: the contain text in sidebar\n\nsidebar_show: 1\nsidebar_show_page: 0\n\nsidebar_contain_name: "联系/反馈"\nsidebar_contact: ""\n\nsidebar:\n  - sidebar_weixin\n  - sidebar_latest\n  - sidebar_tags\n  - sidebar_duoshuo\n  - sidebar_time\n  - sidebar_link\n\n\n# sidebar links, each link should setting url,name,icon\nslinks_name: "友情链接"\n\n# format: url,name,icon\n# e.g: https://github.com/LeslieZhu/OrgNote,OrgNote,fa fa-github\n# e.g: https://github.com/LeslieZhu/OrgNote,OrgNote\n# e.g: https://github.com/LeslieZhu/OrgNote\nslinks_file: slinks.org\n\n# links, add links on menu page\n# format: url,name\n# e.g: https://github.com/LeslieZhu/OrgNote,OrgNote\n# e.g: https://github.com/LeslieZhu/OrgNote\nlinks_name: "觅链"\nlinks_file: links.org\n\ndeploy_type: git\ndeploy_url:\ndeploy_branch: master\n\n\n# calendar\n# disable calendar, just keep as blank\ncalendar_name: "日历"\n\n# calendar job\n# job time: %Y/%m/%d %H:%M\n# job name: text\n# job type: by_once,by_day,by_week,by_month,by_quarter,by_year\n# job link(optional): url\n# job layout: type,time,name,link\n# e.g: by_once,2019/11/12 09:30,查看新闻,www.weibo.com\ncalendar_jobfile: calendar.org\n\n# shift hour for calendar job\n# default: 0h\nshift_hour: 0\n'

    def __init__(self, cfgfile='_config.yml'):
        self.cfgfile = cfgfile
        self.cfg = dict()
        if not os.path.exists(self.cfgfile):
            self.cfg = load(self._default_yml, Loader=FullLoader)
        else:
            self.update()

    def update(self):
        import os.path
        if not os.path.exists(self.cfgfile):
            self.default()
        fp = open(self.cfgfile, 'r')
        self.cfg.update(load(fp, Loader=FullLoader))
        fp.close()

    def dump(self):
        self.update()
        fp = open(self.cfgfile, 'w')
        dump(self.cfg, fp)
        fp.close()

    def default(self):
        fp = open(self.cfgfile, 'w')
        fp.write(self._default_yml)
        fp.close()

    def display(self):
        """display the _config.yml contents"""
        for key in sorted(self.cfg):
            if isinstance(self.cfg[key], dict):
                print key
                for key2 in sorted(self.cfg[key]):
                    print (
                     '\t', key2, ':', self.cfg[key][key2])

            else:
                print (
                 key, ':', self.cfg[key])


def main(args=None):
    cfg = Config()
    cfg.update()
    cfg.display()


if __name__ == '__main__':
    import sys
    sys.exit(main())