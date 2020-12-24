# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fred/Documents/GitHub/GeoCode/geopytool/ImportDependence.py
# Compiled at: 2020-05-08 01:32:39
import matplotlib
matplotlib.use('Qt5Agg')
import importlib, pip, subprocess, webbrowser, sys, sklearn as sk, scipy.stats as st
from scipy.interpolate import make_interp_spline, BSpline
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import requests, re, random, pandas as pd, os, numpy as np, matplotlib.pyplot as plt
from matplotlib import path
import matplotlib.patches as patches, matplotlib.image as mpimg, matplotlib.font_manager as font_manager, matplotlib.backends.backend_pdf, math, csv
from xml.dom import minidom
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer, Binarizer, LabelEncoder, OneHotEncoder, PolynomialFeatures, FunctionTransformer
from sklearn.neighbors import NearestNeighbors, KernelDensity
from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.decomposition import PCA, FastICA, FactorAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn import svm
from sklearn import tree
from sklearn import datasets
from scipy.stats import mode, gaussian_kde
from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy as hc
from scipy.signal import find_peaks, find_peaks_cwt, fftconvolve
from itertools import product, combinations, permutations, repeat
from PyQt5.QtWidgets import QMainWindow, QMenu, QSizePolicy, QMessageBox, QWidget, QFileDialog, QAction, QTextEdit, QLineEdit, QApplication, QPushButton, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QProxyStyle, QStyle, qApp, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import vstack, array, nan, mean, median, ptp, var, std, cov, corrcoef, arange, sin, pi, nanmean, nanmedian, nanvar, nanstd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import ttfFontProperty
import matplotlib.tri as tri
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from matplotlib import colors
from matplotlib import cm
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib import ft2font
from bs4 import BeautifulSoup
LocationOfMySelf = os.path.dirname(__file__)
fpath = LocationOfMySelf + '/wqy.ttf'
font = ft2font.FT2Font(fpath)
fprop = font_manager.FontProperties(fname=fpath)
ttfFontProp = ttfFontProperty(font)
fontprop = font_manager.FontProperties(family='sans-serif', size=9, fname=ttfFontProp.fname, stretch=ttfFontProp.stretch, style=ttfFontProp.style, variant=ttfFontProp.variant, weight=ttfFontProp.weight)
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 'truetype'
plt.rcParams['axes.unicode_minus'] = False
_translate = QtCore.QCoreApplication.translate