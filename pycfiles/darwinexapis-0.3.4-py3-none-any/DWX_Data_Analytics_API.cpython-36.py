# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eriz/Desktop/darwinexapis/darwinexapis/API/DarwinDataAnalyticsAPI/DWX_Data_Analytics_API.py
# Compiled at: 2020-05-13 05:34:50
# Size of source mod 2**32: 19127 bytes
"""
    dwx_analytics.py - Pythonic access to raw DARWIN analytics data via FTP
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: October 17, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import gzip, json, os, pandas as pd
from tqdm import tqdm
from ftplib import FTP
from io import BytesIO
from matplotlib import pyplot as plt
import logging
logger = logging.getLogger()

class DWX_Darwin_Data_Analytics_API:
    __doc__ = 'This API has the ability to download DARWIN data and analyze it.'

    def __init__(self, dwx_ftp_user, dwx_ftp_pass, dwx_ftp_hostname, dwx_ftp_port):
        """Initialize variables, setup byte buffer and FTP connection.
        
        Parameters
        ----------
        ftp_server : str
            FTP server that houses raw DARWIN data
            
        ftp_username : str
            Your Darwinex username
            
        ftp_password : str
            Your FTP password (NOT your Darwinex password)
            
        ftp_port : int
            Port to connect to FTP server on.
        --
        """
        self.analytics_headers = {'AVG_LEVERAGE':[
          'timestamp', 'periods', 'darwin_vs_eurusd_volatility'], 
         'ORDER_DIVERGENCE':[
          'timestamp', 'instrument', 'usd_volume', 'latency', 'divergence'], 
         'RETURN_DIVERGENCE':[
          'timestamp', 'quote', 'quote_after_avg_divergence'], 
         'MONTHLY_DIVERGENCE':[
          'timestamp', 'average_divergence', 'monthly_divergence'], 
         'DAILY_FIXED_DIVERGENCE':[
          'timestamp', 'profit_difference'], 
         'DAILY_REAL_DIVERGENCE':[
          'timestamp', 'profit_difference']}
        self.retbuf = BytesIO()
        self.mode = 0
        try:
            self.server = FTP(dwx_ftp_hostname)
            self.server.login(dwx_ftp_user, dwx_ftp_pass)
            if str(self.server.lastresp).startswith('2'):
                logger.warning('[KERNEL] FTP Connection Successful. Data will now be pulled from Darwinex FTP Server.')
                self.mode = 1
            logger.warning(f"[KERNEL] Last FTP Status Code: {self.server.lastresp} | Please consult https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes for code definitions.")
        except Exception as ex:
            logger.warning(f"Exception: {ex}")
            exit(-1)

    def parse_line(self, line):
        for start, end in [['[[', ']]'], ['[', ']']]:
            if start in line:
                ls = line.split(start)
                ls1 = ls[1].split(end)
                return ls[0].split(',')[:-1] + [json.loads(start + ls1[0].replace("'", '"') + end)] + ls1[1].split(',')[1:]

        return line.split(',')

    def get_data_from_ftp(self, darwin, data_type):
        """Connect to FTP server and download requested data for DARWIN.
        
        For example, darwin='PLF' and data_type='AVG_LEVERAGE' results in this
        code retrieving the file 'PLF/AVG_LEVERAGE' from the FTP server.
        
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        data_type : str
            Must be a key in self.analytics_headers dictionary.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        self.retbuf = BytesIO()
        self.server.retrbinary(f"RETR {darwin}/{data_type}", self.retbuf.write)
        self.retbuf.seek(0)
        ret = []
        while True:
            line = self.retbuf.readline()
            if len(line) > 1:
                ret.append(self.parse_line(line.strip().decode()))
            else:
                break

        return pd.DataFrame(ret)

    def get_data_from_file(self, darwin, data_type):
        """Read data from local file stored in path darwin/filename
        
        For example, darwin='PLF' and data_type='AVG_LEVERAGE' results in this
        code retrieving the file 'PLF/AVG_LEVERAGE' from the current directory.
        
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        data_type : str
            Must be a key in self.analytics_headers dictionary.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        if self.mode == 0:
            logger.warning(f"Retrieving data from file for DARWIN {darwin}...")
            return pd.read_csv(f"{str(darwin).upper()}/{str(data_type).upper()}", header=None)
        else:
            logger.warning(f"Retrieving data from FTP Server for DARWIN {darwin}...")
            return self.get_data_from_ftp(str(darwin).upper(), str(data_type).upper())

    def save_data_to_csv(self, dataframe_to_save, which_path, filename):
        if which_path:
            dataframe_to_save.to_csv(which_path + filename + '.csv')
        else:
            dataframe_to_save.to_csv(filename + '.csv')

    def get_analytics(self, darwin, data_type):
        """Get, index and prepare requested data.
        
        For example, darwin='PLF' and data_type='AVG_LEVERAGE' results in:
            
            - the code retrieving the file 'PLF/AVG_LEVERAGE'
            - converting millisecond timestamps column to Pandas datetime
            - Setting the above converted timestamps as the index
            - Dropping the timestamp column itself.            
        
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        data_type : str
            Must be a key in self.analytics_headers dictionary.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        df = self.get_data_from_file(darwin, data_type)
        df.columns = self.analytics_headers[data_type]
        df.set_index(pd.to_datetime((df['timestamp']), unit='ms'), inplace=True)
        df.drop(['timestamp'], axis=1, inplace=True)
        return df

    def get_darwin_vs_eurusd_volatility(self, darwin, plot=True):
        """Get the evolution of the given DARWIN's volatility vs that of the EUR/USD.
                
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        plot : bool
            If true, produce a chart as defined in the method.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        data_type = 'AVG_LEVERAGE'
        df = self.get_analytics(darwin, data_type)
        df.loc[:, self.analytics_headers[data_type][(-1)]] = df.loc[:, self.analytics_headers[data_type][(-1)]].apply(eval).apply(lambda x: x[(-1)])
        if plot:
            df['darwin_vs_eurusd_volatility'].plot(title=f"${darwin}: DARWIN vs EUR/USD Volatility", figsize=(10,
                                                                                                              8))
        return df

    def get_order_divergence(self, darwin, plot=True):
        """Get the evolution of the given DARWIN's replication latency and investor
        divergence, per order executed by the trader.
                
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        plot : bool
            If true, produce a chart as defined in the method.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        data_type = 'ORDER_DIVERGENCE'
        df = self.get_analytics(darwin, data_type)
        df[['latency', 'usd_volume', 'divergence']] = df[['latency', 'usd_volume', 'divergence']].apply((pd.to_numeric), errors='coerce')
        if plot:
            fig = plt.figure(figsize=(10, 12))
            ax1 = fig.add_subplot(211)
            ax1.xaxis.set_label_text('Replication Latency (ms)')
            ax2 = fig.add_subplot(212)
            ax2.xaxis.set_label_text('Investor Divergence')
            df.groupby('instrument').latency.median().sort_values(ascending=True).plot(kind='barh', title=f"${darwin} | Median Order Replication Latency (ms)",
              ax=ax1)
            df.groupby('instrument').divergence.median().sort_values(ascending=True).plot(kind='barh', title=f"${darwin} | Median Investor Divergence per Order",
              ax=ax2)
            fig.subplots_adjust(hspace=0.2)
        return df.dropna()

    def get_return_divergence(self, darwin, plot=True):
        """Get the evolution of the given DARWIN's Quote and Quote after applying
        average investors' divergence.
                
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        plot : bool
            If true, produce a chart as defined in the method.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        data_type = 'RETURN_DIVERGENCE'
        df = self.get_analytics(darwin, data_type).apply((pd.to_numeric), errors='coerce')
        if plot:
            df.plot(title=f"${darwin} | Quote vs Quote with Average Divergence", figsize=(10,
                                                                                          8))
        return df

    def get_monthly_divergence(self, darwin):
        """Get the evolution of the given DARWIN's average and monthly divergence.
                
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        data_type = 'MONTHLY_DIVERGENCE'
        df = self.get_analytics(darwin, data_type).apply((pd.to_numeric), errors='coerce')
        return df

    def get_daily_fixed_divergence(self, darwin, plot=True):
        """Analyses the effect of applying a fixed divergence (10e-5) on the profit.
                
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        plot : bool
            If true, produce a chart as defined in the method.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        data_type = 'DAILY_FIXED_DIVERGENCE'
        df = self.get_analytics(darwin, data_type).apply((pd.to_numeric), errors='coerce')
        if plot:
            df.plot(title=f"${darwin} | Effect of 10e-5 Fixed Divergence on profit", figsize=(10,
                                                                                              8))
        return df

    def get_daily_real_divergence(self, darwin, plot=True):
        """Analyse the effect of applying the investors' divergence on the profit.
                
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        plot : bool
            If true, produce a chart as defined in the method.
            
        Returns
        -------
        df
            Pandas DataFrame
        --
        """
        data_type = 'DAILY_REAL_DIVERGENCE'
        df = self.get_analytics(darwin, data_type).apply((pd.to_numeric), errors='coerce')
        if plot:
            df.plot(title=f"${darwin} | Effect of Investor Divergence on profit", figsize=(10,
                                                                                           8))
        return df

    def get_quotes_from_ftp(self, darwin='PLF', suffix='4.1', monthly=True, month='01', year='2019'):
        """Download Quote data for any DARWIN directly via FTP.
                
        Parameters
        ----------
        darwin : str
            DARWIN ticker symbol, e.g. $PLF
            
        suffix : str
            Reflects risk, '4.1' being for 10% VaR DARWIN assets.
            
        monthly : bool
            If set to True, month and year arguments are ignored, and ALL 
            data available for the DARWIN is downloaded.
            
        month : str
            Data on the FTP server has the following directory structure:    
                DARWIN_Symbol -> {year}-{month} -> *.csv.gz files
                e.g. PLF/2019-01/PLF....csv.gz
                
                Specifies month for {year}-{month} tuple as above.
        
        year : str
            Data on the FTP server has the following directory structure:    
                DARWIN_Symbol -> {year}-{month} -> *.csv.gz files
                e.g. PLF/2019-01/PLF....csv.gz
                
                Specifies year for {year}-{month} tuple as above.
            
        Returns
        -------
        df
            Pandas DataFrame containing Quotes, indexed by timeframe.
        --
        """
        quote_files = []
        roots = []
        if monthly:
            tqdm.write(f"\n[KERNEL] Searching for Quote data for DARWIN {darwin}, please wait..", end='')
            self.server.retrlines(f"NLST {darwin}/quotes/", roots.append)
            roots_pbar = tqdm(roots, position=0, leave=True)
            for root in roots_pbar:
                try:
                    roots_pbar.set_description('Getting filenames for month: %s' % root)
                    root_files = []
                    self.server.retrlines(f"NLST {darwin}/quotes/{root}", root_files.append)
                    quote_files += [f"{darwin}/quotes/{root}/{root_file}" for root_file in root_files if '{}.{}'.format(darwin, suffix) in root_file]
                except Exception as ex:
                    logger.warning(ex)
                    return

        elif pd.to_numeric(month) > 0 and pd.to_numeric(year) > 2010:
            tqdm.write(f"\n[KERNEL] Asserting data for month {year}-{month}, please wait..", end='')
            quote_files = []
            try:
                self.server.retrlines(f"NLST {darwin}/quotes/{year}-{month}/", quote_files.append)
                quote_files = [f"{darwin}/quotes/{year}-{month}/{quote_file}" for quote_file in quote_files if '{}.{}'.format(darwin, suffix) in quote_file]
            except Exception as ex:
                logger.warning(ex)
                return

        else:
            logger.warning('\n[ERROR] Please either set monthly=True or ensure both month and year have integer values')
            return
        tqdm.write(f"\n[KERNEL] {len(quote_files)} files retrieved.. post-processing now, please wait..", end='')
        ticks_df = pd.DataFrame()
        ticks_pbar = tqdm(quote_files, position=0, leave=True)
        for tick_file in ticks_pbar:
            try:
                ticks_pbar.set_description('Processing %s' % tick_file)
                self.retbuf = BytesIO()
                self.server.retrbinary(f"RETR {tick_file}", self.retbuf.write)
                self.retbuf.seek(0)
                ret = [line.strip().decode().split(',') for line in gzip.open(self.retbuf)]
                ticks_df = pd.concat([ticks_df, pd.DataFrame(ret[1:])], axis=0)
            except Exception as ex:
                logger.warning(ex)

        ticks_df.columns = ['timestamp', 'quote']
        ticks_df.timestamp = ticks_df.timestamp.apply(pd.to_numeric)
        ticks_df.set_index('timestamp', drop=True, inplace=True)
        ticks_df.index = pd.to_datetime((ticks_df.index), unit='ms')
        ticks_df.quote = ticks_df.quote.apply(pd.to_numeric)
        return ticks_df.dropna()