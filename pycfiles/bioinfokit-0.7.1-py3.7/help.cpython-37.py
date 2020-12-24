# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bioinfokit/help.py
# Compiled at: 2020-04-16 23:04:47
# Size of source mod 2**32: 3059 bytes


class format:

    def __init__(self):
        pass

    @staticmethod
    def fq_qual_var():
        text = '\n            <b>FASTQ quality format detection</b>\n\n            `bioinfokit.analys.format.fq_qual_var(file)`\n                \n             Parameters:\n             ------------\n             file : FASTQ file to detect quality format [deafult: None]\n            \n            Returns:\n            Quality format encoding name for FASTQ file\n            (Supports only Sanger, Illumina 1.8+ and Illumina  1.3/1.4)\n\n            <a href="https://reneshbedre.github.io/blog/fqqualfmt.html" target="_blank">Working Example</a>\n            '
        print(text)


class stat:

    def __init__(self):
        pass

    @staticmethod
    def lin_reg():
        text = '\n            <b>Linear regression analysis</b>\n\n            `bioinfokit.analys.stat.linearreg(file)`\n\n             Parameters:\n             ------------\n             df: Pandas dataframe object\n             x : Name of column having independent X variables [list][default:None]\n             y : Name of column having dependent Y variables [list][default:None]\n\n            Returns:\n            Regression analysis summary\n\n            <a href="https://reneshbedre.github.io/blog/linearreg.html" target="_blank">Working Example</a>\n            '
        print(text)

    @staticmethod
    def regplot():
        text = '\n                <b>Regression plot</b>\n\n                `bioinfokit.visuz.stat.regplot(df, x, y, yhat, dim, colordot, colorline, r, ar, dotsize, markerdot, linewidth, \n                    valphaline, valphadot)`\n\n                 Parameters:\n                 ------------\n                 df        : Pandas dataframe object\n                 x         : Name of column having independent X variables [string][default:None]\n                 y         : Name of column having dependent Y variables [string][default:None]\n                 yhat      : Name of column having predicted response of Y variable (y_hat) from regression [string][default:None]\n                 dim       : Figure size [tuple of two floats (width, height) in inches][default: (6, 4)]\n                 r         : Figure resolution in dpi [int][default: 300]\n                 ar        : Rotation of X-axis labels [float][default: 0]\n                 dotsize   : The size of the dots in the plot [float][default: 6]\n                 markerdot : Shape of the dot marker. See more options at  https://matplotlib.org/3.1.1/api/markers_api.html [string][default: "o"]\n                valphaline : Transparency of regression line on plot [float (between 0 and 1)][default: 1]\n                valphadot  : Transparency of dots on plot [float (between 0 and 1)][default: 1]\n                linewidth  : Width of regression line [float][default: 1]\n\n                Returns:\n\n                Regression plot image in same directory (reg_plot.png)\n\n                <a href="https://reneshbedre.github.io/blog/linearreg.html" target="_blank">Working Example</a>\n                '
        print(text)