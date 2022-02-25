# data.py
# stock-report
# Copyright 2022 Kevin Pfeiffer
# MIT License

import os
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange


class DATA:
    def __init__(self, name, ticker):
        """
        Inherit DATA class with its default arguments.
        """
        self.name = name
        self.ticker = ticker
    
    
    # Get Alpha Vantage Keys
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    
    
    # Define Alpha Vantage classes
    fd = FundamentalData(key=api_key, output_format="pandas")
    ts = TimeSeries(key=api_key, output_format="pandas")
    fo = ForeignExchange(key=api_key, output_format="pandas")
    

    def company_overview(self):
        """
        Returns the company information, financial ratios, 
        and other key metrics for the equity specified. 
        Data is generally refreshed on the same day a company reports its latest 
        earnings and financials.
        :return: company overview data as pandas dataframe
        """
        company_overview_data = self.fd.get_company_overview(symbol=self.ticker)
        company_overview_data = company_overview_data[0]
        return company_overview_data
    
    
    def income_statement(self):
        """
        Returns the annual income statements for the company of interest. 
        Data is generally refreshed on the same day a company reports its latest 
        earnings and financials.
        :return: income statement data as pandas dataframe
        """
        income_statement_data = self.fd.get_income_statement_annual(symbol=self.ticker)
        income_statement_data = income_statement_data[0]
        income_statement_data = income_statement_data.reset_index()
        income_statement_data = income_statement_data.iloc[: , 1:]
        return income_statement_data
    
    
    def balance_sheet(self):
        """
        Returns the annual balance sheets for the company of interest.
        Data is generally refreshed on the same day a company reports its latest 
        earnings and financials.
        :return: balance sheet data as pandas dataframe
        """
        balance_sheet_data = self.fd.get_balance_sheet_annual(symbol=self.ticker)
        balance_sheet_data = balance_sheet_data[0]
        balance_sheet_data = balance_sheet_data.reset_index()
        balance_sheet_data = balance_sheet_data.iloc[: , 1:]
        return balance_sheet_data
    
    
    def cash_flow(self):
        """
        Returns the annual cash flows for the company of interest.
        Data is generally refreshed on the same day a company reports its latest 
        earnings and financials.
        :return: cashflow data as pandas dataframe
        """
        cash_flow_data = self.fd.get_cash_flow_annual(symbol=self.ticker)
        cash_flow_data = cash_flow_data[0]
        cash_flow_data = cash_flow_data.reset_index()
        cash_flow_data = cash_flow_data.iloc[: , 1:]
        return cash_flow_data
    
    
    def daily_prices(self):
        """ 
        Return daily time series in two json objects as data and
        meta data. It raises ValueError when problems arise.
        :return: daily prices data as pandas dataframe
        """
        daily_prices_data = self.ts.get_daily(symbol=self.ticker, outputsize="full")
        daily_prices_data = daily_prices_data[0]
        return daily_prices_data
    
    
    def quote(self):
        """ 
        Return the latest price and volume information for a
        security of your choice.
        :return: quote data as pandas dataframe
        """
        quote_data = self.ts.get_quote_endpoint(symbol=self.ticker)
        quote_data = quote_data[0]
        return quote_data
    
    
    def exchange_rate(self, from_currency, to_currency):
        """ 
        Returns the realtime exchange rate for any pair of physical
        currency (e.g., EUR) or physical currency (e.g., USD).
        :param from_currency: he currency you would like to get the exchange rate
            for. It can either be a physical currency or digital/crypto currency.
            For example: from_currency=USD or from_currency=BTC.
        :param to_currency: The destination currency for the exchange rate.
            It can either be a physical currency or digital/crypto currency.
            For example: to_currency=USD or to_currency=BTC.     
        :return: exchange rate data as a string
        """
        exchange_rate_data = self.fo.get_currency_exchange_rate(from_currency=from_currency, to_currency=to_currency)
        exchange_rate_data = exchange_rate_data[0]
        exchange_rate_data = exchange_rate_data["5. Exchange Rate"].values[0]
        return exchange_rate_data
    
    
    def symbol_search(self, keyword):
        """ 
        Return best matching symbols and market information
        based on keywords. It raises ValueError when problems arise.
        :param keyword: name of company as string
        :return: symbol search data as pandas dataframe
        """
        symbol_search_data = self.ts.get_symbol_search(keywords=keyword)
        symbol_search_data = symbol_search_data[0]
        symbol_search_data = symbol_search_data.reset_index()
        symbol_search_data = symbol_search_data[["1. symbol", "2. name", "3. type", "8. currency"]]
        symbol_search_data = symbol_search_data.rename({"1. symbol": "symbol", "2. name": "name", "8. currency": "currency", "3. type": "type"}, axis="columns")
        return symbol_search_data