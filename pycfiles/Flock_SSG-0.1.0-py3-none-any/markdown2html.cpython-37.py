# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\converter\markdown2html.py
# Compiled at: 2018-12-05 20:22:22
# Size of source mod 2**32: 5592 bytes
from .. import settings
import os, markdown, Flock.src.converter.markdown_extensions
FLOCK_HEADER_CODE = '<!DOCTYPE html>\n<html><head>\n<meta charset="utf-8"/>\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" type="text/css" media="screen" href="styles.css"/>\n</head></html>\n<body>'
FLOCK_FOOTER_CODE = '\n<a href="https://github.com/rdall96/Flock_SSG" target="blank" style="text-decoration:none;color:inherit;">\n<div class="FlockFooter">\n<p> Created using Flock   \n<img src="flock_icon.png"/>\n</p></div></a>\n</body>'
EXTENSIONS_FILE = 'src/converter/markdown_extensions.py'
EXECUTE_SUCCESSFULLY = False

def getFileName(fileName):
    name = fileName[:-3]
    settings.LOG('File name: ' + name)
    return name


def generateHTMLHeader(file, mode):
    if mode == 'o':
        file.write(FLOCK_HEADER_CODE)
    else:
        if mode == 'c':
            file.write(FLOCK_FOOTER_CODE)
            file.close()
    return file


def createHTML(fileName):
    settings.LOG('Creating HTML file...')
    htmlName = getFileName(fileName) + '.html'
    html = open(htmlName, 'w+')
    html = generateHTMLHeader(html, 'o')
    return html


def parseMarkdown(mFile, htmlFile):
    try:
        settings.LOG('--- ' + mFile)
        input_file = open(mFile, 'r')
        text = input_file.read()
        html = markdown.markdown(text)
        htmlFile.write(html)
        EXECUTE_SUCCESSFULLY = True
    except OSError as err:
        try:
            settings.LOG('Cannot open the target file: ' + mFile)
            settings.LOG('Perhaps the path to the file is incorrect?')
            EXECUTE_SUCCESSFULLY = False
            settings.LOG(err)
        finally:
            err = None
            del err

    except ValueError:
        settings.LOG("Couldn't read the contents of the file")
        EXECUTE_SUCCESSFULLY = False
    except:
        settings.LOG('Unexpected error, could not convert the file')
        EXECUTE_SUCCESSFULLY = False

    return htmlFile


def markdown2html(inputFile):
    settings.LOG('- Markdown to HTML Python Translator -\n')
    htmlFile = createHTML(inputFile)
    outputFile = parseMarkdown(inputFile, htmlFile)
    generateHTMLHeader(outputFile, 'c')
    return EXECUTE_SUCCESSFULLY


def checkIfValid(filePath):
    fileExtension = filePath[:3]
    if fileExtension != '.md':
        settings.LOG('Selected file does not have a markdown (.md) extension')
        return False
    try:
        tempHTML = open('testHTML.html', 'w+')
        tempHTML = parseMarkdown(filePath, tempHTML)
        if os.stat(tempHTML).st_stat < 1:
            settings.LOG('Selected file is not a valid Markdown file')
            return False
        return True
    except:
        print('Unexpected error occured during valid markdown verification')

    tempHTML.close()
    os.remove('testHTML.html')
    return True


def convertAllMarkdown(folder):
    filesConverted = 0
    for root, dirs, files in os.walk(folder):
        for fileName in files:
            if fileName.endswith('.md'):
                filePath = os.path.join(root, fileName)
                markdown2html(filePath)
                filesConverted += 1

    settings.LOG('Converted ' + str(filesConverted) + ' files')
    return filesConverted