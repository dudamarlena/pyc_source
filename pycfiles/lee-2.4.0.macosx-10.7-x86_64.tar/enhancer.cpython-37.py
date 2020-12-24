# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zk/anaconda3/lib/python3.7/site-packages/lee/enhancer.py
# Compiled at: 2020-02-12 10:49:21
# Size of source mod 2**32: 6422 bytes
from termcolor import colored
import logging, json, os
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import PythonLexer, CppLexer, MarkdownLexer
import pygments.formatters as tf
import html2markdown
from .exts_map import ext2language, language2extAndComemnt
from .utils import jsonp
from .highlight_lexer import terminal_print
logger = logging.getLogger(__name__)

def red(str):
    return colored(str, 'red')


def green(str):
    return colored(str, 'green')


def yellow(str):
    return colored(str, 'yellow')


def blue(str):
    return colored(str, 'blue')


def cyan(str):
    return colored(str, 'cyan')


def white(str):
    return colored(str, 'white')


def purple(str):
    return colored(str, 'purple')


class Enhancer:

    def __init__(self, cli, mainArgs):
        self.cli = cli
        self.mainArgs = mainArgs

    @staticmethod
    def parse_id(qid):
        if qid:
            if qid.find(',') > 0:
                for i in qid.split(','):
                    yield i

            else:
                if qid.find('-') > 0:
                    smaller = int(qid.split('-')[0])
                    bigger = int(qid.split('-')[1])
                    for i in range(bigger, smaller - 1, -1):
                        yield i

                else:
                    yield qid

    def pull(self, qid):
        for q in Enhancer.parse_id(qid):
            self.generate(q, self.mainArgs)

    def extractFileInfo(self, filePath):
        qid = int(os.path.basename(filePath).split('.')[0])
        ext = os.path.basename(filePath).split('.')[(-1)]
        content = ''
        with open(filePath, 'r') as (f):
            content = f.read()
        language = ext2language(ext)
        return (qid, content, language)

    def login(self):
        self.cli.loginPrompt()

    def show(self, qids=None):
        difficulty = {1:white('Easy'), 
         2:blue('Medium'), 
         3:red('Hard')}
        import re

        def howManyChinese(s):
            match = re.findall('[\\u4e00-\\u9fff]', s)
            return len(match)

        def nonAsciiBack(str1):
            return '\x08' * howManyChinese(str1)

        def pp(q):
            mark = green('✓') if (q.status and 'a' in q.status) else ' '
            line_new = '{}{:<3}{:<8}{:<40}{:<5}'.format(mark, '$' if q.paid_only else ' ', q.qid, q.chs_name, nonAsciiBack(q.chs_name) + difficulty[q._difficilty_level])
            print(line_new)

        if qids != 'all':
            q = None
            for qid in Enhancer.parse_id(qids):
                q = self.cli.find(qid)
                if q:
                    pp(q)

            if ',' not in qids:
                if '-' not in qids:
                    print('\n\n')
                    q = self.cli.question_detail(qid)
                    translatedContent = q.translatedContent
                    if translatedContent:
                        coment_translatedContent = '\n'.join([x for x in BeautifulSoup(translatedContent, features='lxml').get_text().split('\n')]) + '\n\n'
                        print(coment_translatedContent)
        else:
            for q in self.cli.findAll():
                if q:
                    pp(q)

    def highlight(self, content):
        print(highlight(content, PythonLexer(), tf()))

    def solution(self, qids, topK, markdown, language='python'):
        assert qids
        for qid in Enhancer.parse_id(qids):
            for s in self.cli.solution(qid, topK, language):
                self.highlight(s.content)
                if markdown:
                    question_detail = self.cli.question_detail(qid)
                    eng_name = question_detail.eng_name
                    with open(f"{qid}-solution-{s.votes}-{s.author_name}-{language}.md", 'w') as (f):
                        f.write('author: ' + s.author_name + '\n\n')
                        f.write('voteCount: ' + str(s.votes) + '\n\n')
                        f.write('language: ' + language + '\n\n')
                        f.write(f"discuss: https://leetcode.com/problems/{eng_name}/discuss/{s.qid}\n\n\n")
                        f.write('--- \n\n\n')
                        f.write(s.content)

    def get_cli(self):
        return self.cli

    def submit(self, filePath):
        qid, content, language = self.extractFileInfo(filePath)
        ret = self.cli.submit(qid, content, language)
        jsonp(ret)
        return ret

    def test(self, filePath):
        qid, content, language = self.extractFileInfo(filePath)
        ret = self.cli.test(qid, content, language)
        jsonp(ret)
        return ret

    def write_local(self, full_path, content):
        with open(full_path, 'w') as (f):
            f.write(content)

    def generate(self, qid, args):
        directory = args.output
        ext, commentType = language2extAndComemnt(args.language.lower())
        q = self.cli.question_detail(qid)
        codeDefinition = q.get_code_defination(args.language)
        translatedContent = q.translatedContent
        if not os.path.exists(directory):
            os.makedirs(directory)
        sourcePath = os.path.join(directory, f"{qid}.{q.eng_name}.{ext}")
        with open(sourcePath, 'w') as (f):
            coment_translatedContent = '\n'.join([f"{commentType} " + x for x in BeautifulSoup(translatedContent, features='lxml').get_text().split('\n')]) + '\n\n'
            f.write(coment_translatedContent)
            f.write(q.get_code_defination(args.language))
            print(green(sourcePath), ' generated!')
        if args.markdown:
            mdPath = os.path.join(directory, f"{qid}.{q.eng_name}.md")
            self.write_local(mdPath, html2markdown.convert(translatedContent))
        if args.html:
            htmlPath = os.path.join(directory, f"{qid}.{q.eng_name}.html")
            self.write_local(htmlPath, translatedContent)