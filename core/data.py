# data.py
# Copyright 2021 Kevin Pfeiffer
# MIT License

import os
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.foreignexchange import ForeignExchange


class DATA:
    def __init__(self, name, ticker):
        self.name = name
        self.ticker = ticker
    
    # Get Alpha Vantage Key
    api_key = os.getenv("ALPHAVANTAGE_API_KEY_1")

    # Define various Alpha Vantage classes
    ts = TimeSeries(key=api_key, output_format="pandas")
    fd = FundamentalData(key=api_key, output_format="pandas")
    fo = ForeignExchange(key=api_key, output_format="pandas")

    #Company Data
    def company_overview(self):
        """
        help function to get fundamental data by category
        :param category: Alpha Vantage category name as string
        :return: selected fundamental data
        """
        company_data = self.fd.get_company_overview(symbol=self.ticker)
        return company_data

    # Balance sheet
    def balance(self):
        balance_sheet = self.fd.get_balance_sheet_quarterly(symbol=self.ticker)
        # Wie am besten einbinden? https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo


    # USD in Euro
    def exchange(self):
        usd_eur = self.fo.get_currency_exchange_rate(from_currency="USD", to_currency="EUR")
        usd_eur_rate = usd_eur[0]
        usd_eur_rate = usd_eur_rate["5. Exchange Rate"].values[0]


    # Stock Time Series
    def prices(self):
        stock_prices = self.ts.get_daily(symbol=self.ticker, outputsize="full")
        stock_prices = stock_prices[0]
        return stock_prices