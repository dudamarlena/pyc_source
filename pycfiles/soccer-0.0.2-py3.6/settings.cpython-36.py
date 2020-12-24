# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\tm\settings.py
# Compiled at: 2018-02-09 12:03:39
# Size of source mod 2**32: 7920 bytes
BOT_NAME = 'tm'
SPIDER_MODULES = [
 'tm.spiders']
NEWSPIDER_MODULE = 'tm.spiders'
ROBOTSTXT_OBEY = True
HTTPERROR_ALLOWED_CODES = [
 500]
DOWNLOADER_MIDDLEWARES = {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, 
 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware':400}
ITEM_PIPELINES = {'tm.pipelines.ValidateItemPipeline':700, 
 'tm.pipelines.MongoDBPipeline':800}
DUPEFILTER_DEBUG = True
LOG_LEVEL = 'WARNING'
POINT_RULES = [
 '2p', '3p']
COMPETITION_DATA = {'BL1':{'point_rules':[
   {'season_to':1994, 
    'rule':'2p'},
   {'season_from':1995, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS',
   'POINTS_H2H',
   'GOAL_DIFFERENCE_H2H',
   'AWAY_GOALS_H2H',
   'AWAY_GOALS']}, 
 'BL2':{'point_rules':[
   {'season_to':1994, 
    'rule':'2p'},
   {'season_from':1995, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS',
   'POINTS_H2H',
   'GOAL_DIFFERENCE_H2H',
   'AWAY_GOALS_H2H',
   'AWAY_GOALS']}, 
 'BL3':{'point_rules':[
   {'season_from':2008, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS',
   'POINTS_H2H',
   'GOAL_DIFFERENCE_H2H',
   'AWAY_GOALS_H2H',
   'AWAY_GOALS']}, 
 'PL':{'point_rules':[
   {'season_from':1992, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'ELC':{'point_rules':[
   {'season_from':2004, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'EL1':{'point_rules':[
   {'season_from':2004, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'SA':{'point_rules':[
   {'season_to':1993, 
    'rule':'2p'},
   {'season_from':1994, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'POINTS_H2H',
   'GOAL_DIFFERENCE_H2H',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'SB':{'point_rules':[
   {'season_to':1993, 
    'rule':'2p'},
   {'season_from':1994, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'POINTS_H2H',
   'GOAL_DIFFERENCE_H2H',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'FL1':{'point_rules':[
   {'season_to':1993, 
    'rule':'2p'},
   {'season_from':1994, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'FL2':{'point_rules':[
   {'season_to':1993, 
    'rule':'2p'},
   {'season_from':1994, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'PD':{'point_rules':[
   {'season_to':1994, 
    'rule':'2p'},
   {'season_from':1995, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'POINTS_H2H',
   'GOAL_DIFFERENCE_H2H',
   'GOALS_H2H',
   'GOAL_DIFFERENCE',
   'GOALS']}, 
 'SD':{'point_rules':[
   {'season_to':1994, 
    'rule':'2p'},
   {'season_from':1995, 
    'rule':'3p'}], 
  'tie_break_rules':[
   'POINTS',
   'POINTS_H2H',
   'GOAL_DIFFERENCE_H2H',
   'GOALS_H2H',
   'GOAL_DIFFERENCE',
   'GOALS']}}