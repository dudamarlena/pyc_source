# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/newsParser/articleParser.py
# Compiled at: 2019-09-02 23:55:41
import requests, re, math, chardet

class AriticleParser(object):

    def __init__(self):
        self._title = re.compile('<title>(.*?)</title>', re.I | re.S)
        self._keyword = re.compile('<\\s*meta\\s*name="?Keywords"?\\s+content="?(.*?)"?\\s*[/]?>', re.I | re.S)
        self._description = re.compile('<\\s*meta\\s*name="?Description"?\\s+content="?(.*?)"?\\s*[/]?>', re.I | re.S)
        self._link = re.compile('<a(.*?)>|</a>')
        self._link_mark = '|ABC|'
        self._space = re.compile('\\s+')
        self._stopword = re.compile('备\\d+号|Copyright\\s*©|版权所有|all rights reserved|广告|推广|回复|评论|关于我们|链接|About|广告|下载|href=|本网|言论|内容合作|法律法规|原创|许可证|营业执照|合作伙伴|备案', re.I | re.S)
        self._punc = re.compile(',|\\?|!|:|;|。|，|？|！|：|；|《|》|%|、|“|”', re.I | re.S)
        self._special_list = [(re.compile('&quot;', re.I | re.S), '"'),
         (
          re.compile('&amp;', re.I | re.S), '&'),
         (
          re.compile('&lt;', re.I | re.S), '<'),
         (
          re.compile('&gt;', re.I | re.S), '>'),
         (
          re.compile('&nbsp;', re.I | re.S), ' '),
         (
          re.compile('&#34;', re.I | re.S), '"'),
         (
          re.compile('&#38;', re.I | re.S), '&'),
         (
          re.compile('&#60;', re.I | re.S), '<'),
         (
          re.compile('&#62;', re.I | re.S), '>'),
         (
          re.compile('&#160;', re.I | re.S), ' ')]

    def extract_offline(self, html):
        title = self.extract_title(html)
        description = self.extract_description(html)
        keyword = self.extract_keywords(html)
        content = self.extract_content(html, title)
        return {'title': title, 
           'description': description, 
           'keyword': keyword, 
           'content': content}

    def extract_online(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            if r.encoding == 'ISO-8859-1':
                r.encoding = chardet.detect(r.content)['encoding']
            html = r.text
            title = self.extract_title(html)
            description = self.extract_description(html)
            keyword = self.extract_keywords(html)
            content = self.extract_content(html, title)
            return {'title': title, 
               'description': description, 
               'keyword': keyword, 
               'content': content}
        return {}

    def extract_title(self, html):
        title = self._title.search(html)
        if title:
            title = title.groups()[0]
        else:
            return ''
        titleArr = re.split('_', title)
        newTitle = titleArr[0]
        for subTitle in titleArr:
            if len(subTitle) > len(newTitle):
                newTitle = subTitle

        return newTitle

    def extract_keywords(self, html):
        keyword = self._keyword.search(html)
        if keyword:
            keyword = keyword.groups()[0]
        else:
            return ''
        keyword = self._space.sub(' ', keyword)
        return keyword

    def extract_description(self, html):
        description = self._description.search(html)
        if description:
            keyword = description.groups()[0]
        else:
            return ''
        keyword = self._space.sub(' ', keyword)
        return keyword

    def extract_content(self, html, title):
        lines = self.remove_tag(html)
        blocks = self.get_blocks(lines)
        blockScores = self.block_scores(lines, blocks, title)
        res = ''
        if len(blockScores) != 0:
            maxScore = max(blockScores)
            if maxScore > 1000:
                blockIndex = blockScores.index(maxScore)
                lineStart, lineEnd = blocks[blockIndex]
                nextIndex = blockIndex + 1
                while nextIndex < len(blocks):
                    if self.detBlockLenght(lines, blocks, nextIndex) < 30:
                        break
                    newBlock = (
                     lineStart, blocks[nextIndex][1])
                    score = self.block_scores(lines, [newBlock], title)[0]
                    if score > maxScore:
                        lineEnd = blocks[nextIndex][1]
                        maxScore = score
                    else:
                        break

                lastIndex = blockIndex - 1
                while lastIndex >= 0:
                    if self.detBlockLenght(lines, blocks, nextIndex) < 30:
                        break
                    newBlock = (
                     blocks[lastIndex][0], lineEnd)
                    score = self.block_scores(lines, [newBlock], title)[0]
                    if score > maxScore:
                        lineEnd = blocks[nextIndex][1]
                        maxScore = score
                    else:
                        break

                res += ('').join(lines[lineStart:lineEnd])
                res = re.sub('\\|ABC\\|(.*?)\\|ABC\\|', '', res, 0, re.I | re.S)
        return res

    def detBlockLenght(self, lines, blocks, index):
        if len(blocks) <= index:
            return 0
        lineStart, lineEnd = blocks[index]
        block = ('').join(lines[lineStart:lineEnd])
        block = re.sub('\\|ABC\\|(.*?)\\|ABC\\|', '', block, 0, re.I | re.S)
        return len(block)

    def get_blocks(self, lines):
        linesLen = [ len(line) for line in lines ]
        totalLen = len(lines)
        blocks = []
        indexStart = 0
        while indexStart < totalLen and linesLen[indexStart] < 30:
            indexStart += 1

        for indexEnd in range(totalLen):
            if indexEnd > indexStart and linesLen[indexEnd] == 0 and indexEnd + 1 < totalLen and linesLen[(indexEnd + 1)] <= 30 and indexEnd + 2 < totalLen and linesLen[(indexEnd + 2)] <= 30:
                blocks.append((indexStart, indexEnd))
                indexStart = indexEnd + 3
                while indexStart < totalLen and linesLen[indexStart] <= 30:
                    indexStart += 1

        return blocks

    def block_scores(self, lines, blocks, title):
        blockScores = []
        for indexStart, indexEnd in blocks:
            blockLinesLen = indexEnd - indexStart + 1.0
            block = ('').join(lines[indexStart:indexEnd])
            cleanBlock = block.replace(self._link_mark, '')
            linkScale = (block.count(self._link_mark) + 1.0) / blockLinesLen
            lineScale = (len(lines) - indexStart + 1.0) / (len(lines) + 1.0)
            stopScale = (len(self._stopword.findall(block)) + 1.0) / blockLinesLen
            titleMatchScale = len(set(title) & set(cleanBlock)) / (len(title) + 1.0)
            puncScale = (len(self._punc.findall(block)) + 1.0) / blockLinesLen
            textScale = (len(cleanBlock) + 1.0) / blockLinesLen
            chineseScale = len(re.findall('[\\u4e00-\\u9fa5]', block)) / len(block)
            score = chineseScale * textScale * lineScale * puncScale * (1.0 + titleMatchScale) / linkScale / math.pow(stopScale, 0.5)
            blockScores.append(score)

        return blockScores

    def remove_tag(self, html):
        for r, c in self._special_list:
            text = r.sub(c, html)

        text = re.sub('<script(.*?)>(.*?)</script>', '', text, 0, re.I | re.S)
        text = re.sub('<!--(.*?)-->', '', text, 0, re.I | re.S)
        text = re.sub('<style(.*?)>(.*?)</style>', '', text, 0, re.I | re.S)
        text = re.sub('&.{2,6};|&#.{2,5};', '', text)
        text = re.sub('<a(.*?)>|</a>', self._link_mark, text, 0, re.I | re.S)
        text = re.sub('<[^>]*?>', '', text, 0, re.I | re.S)
        lines = text.split('\n')
        for lineIndex in range(len(lines)):
            lines[lineIndex] = re.sub('\\s+', '', lines[lineIndex])

        return lines


if __name__ == '__main__':
    urls = [
     'http://society.people.com.cn/n1/2019/0902/c1008-31330284.html']
    parser = AriticleParser()
    for url in urls:
        print parser.extract_online(url)