# pdf.py
# stock-report
# Copyright 2022 Kevin Pfeiffer
# MIT License


import os
from fpdf import FPDF
from datetime import date


class PDF:
    def __init__(self, data, name, ticker):
        """
        Inherit PDF class with its default arguments.
        """
        self.date = date.today()
        self.data = data
        self.name = name
        self.ticker = ticker
        self.width = 210
        self.height = 297


    # Formats A4 Letter
    pdf = FPDF("P", "mm", "A4")


    def new_page(self):
        """
        Creates a new pdf page with default header and footer.
        """
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 12)
        
        this_dir, this_filename = os.path.split(__file__)
        
        header = os.path.join(this_dir, "resources", "header.png")
        footer = os.path.join(this_dir, "resources", "footer.png")
        
        self.pdf.image(header, 0, 0, self.width)
        self.pdf.image(footer, 0, 252, self.width)


    def create_title(self):
        """
        Creates title with stock name and date created.
        """
        self.pdf.set_font("Arial", "b", 40)
        self.pdf.ln(30)
        self.pdf.write(4, f"{self.name}")
        self.pdf.ln(10)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.write(4, f"Created: {self.date}")
        self.pdf.ln(5)
    
    
    def create_heading(self, headline):
        """
        Creates heading for a page with ticker.
        :param headline: text as a string
        """
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("Arial", "b", 20)
        self.pdf.ln(30)
        self.pdf.write(4, f"{headline}")
        self.pdf.ln(5)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.write(4, f"Symbol: {self.ticker}")
        self.pdf.ln(5)


    def no_data_available(self):
            """
            Creates heading for a page with ticker.
            :param headline: text as a string
            """
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.set_font("Arial", "b", 40)
            self.pdf.ln(100)
            self.pdf.write(4, "No data available")

    def category_key_figures(self, data, category):
        """
        Returns data by category.
        :param data: data from Alpha Vantage as pandas dataframe
        :param category: category by Alpha Vantage as a string
        :return: data from a category as a string
        """
        category_data = data
        category_data = category_data[category].values[0]
        return category_data


    def category_annual_report(self, data, year ,category):
        """
        Returns data by category and year.
        :param data: data from Alpha Vantage as pandas dataframe
        :param year: takes integer, latest year = 0, second latest year = 1 ...
        :param category: category by Alpha Vantage as a string
        :return: data from a category and year as a string
        """
        end = year + 1
        category_annual_report = data
        category_annual_report = category_annual_report.iloc[year:end , :]
        category_annual_report = category_annual_report[category].values[0]
        return category_annual_report
    
    
    def kff(self, data, key, category, y, key_style="", value_style="", left_position=True, thousands_character=False):
        """
        Creates Template for key_figures().
        :param data: data from Alpha Vantage as pandas dataframe
        :param key: name of key as string
        :param category: category by Alpha Vantage as a string
        :param y: y position of text as integer
        :param key_style: style of key text as string, b: bold, i: italic, u: underline
        :param key_style: style of value text as string, b: bold, i: italic, u: underline
        :param left_position: takes boolean for left or right position on paper
        :param thousands_character: takes boolean for thousands separator
        """
        # x position
        if left_position:
            x_key = 10
            x_value = 70
        else:
            x_key = 115
            x_value = 175
        
        # format of key
        self.pdf.set_font("Arial", key_style, 12)
        self.pdf.set_xy(x_key, y)
        self.pdf.cell(0, txt=f"{key}")
        
        # set value
        value = self.category_key_figures(data, category)
        
        # thousands character for value
        if thousands_character:
            try:
                value = int(value)
                value = f'{value:,}'
            except:
                value = value
        else: 
            value = value
        
        # format of value
        self.pdf.set_font("Arial", value_style, 12)
        self.pdf.set_xy(x_value, y)
        self.pdf.cell(0, txt=f"{value}")
        self.pdf.set_text_color(0, 0, 0)
        
            
    def arf(self, data, key, category, y, key_style="", value_style=""):
        """
        Creates Template for income_statment(), balance_sheet() and cash_flow().
        :param data: data from Alpha Vantage as pandas dataframe
        :param key: name of key as string
        :param category: category by Alpha Vantage as a string
        :param y: y position of text as integer
        :param key_style: style of key text as string, b: bold, i: italic, u: underline
        :param key_style: style of value text as string, b: bold, i: italic, u: underline
        """
        # format of key
        self.pdf.set_font("Arial", key_style, 12)
        self.pdf.set_xy(10, y)
        self.pdf.cell(0, txt=f"{key}")
        self.pdf.set_font("Arial", value_style, 12) 
        
        # format of value
        self.pdf.set_xy(95, y)
        value_1 = self.category_annual_report(data, 0, category)
        try:
            value_1 = int(value_1) # for seperation
            value_1 = f'{value_1:,}'
        except:
            value_1 = value_1
        self.pdf.cell(0, txt=f"{value_1}")
        
        self.pdf.set_xy(135, y)
        value_2 = self.category_annual_report(data, 1, category)
        try:
            value_2 = int(value_2)
            value_2 = f'{value_2:,}'
        except:
            value_2 = value_2
        self.pdf.cell(0, txt=f"{value_2}")
        
        self.pdf.set_xy(175, y)
        value_3 = self.category_annual_report(data, 2, category)
        try:
            value_3 = int(value_3)
            value_3 = f'{value_3:,}'
        except:
            value_3 = value_3
        self.pdf.cell(0, txt=f"{value_3}")


    def key_figures(self):
        """
        Creates key figures on pdf page.
        """
        try:
            # access data
            data_co = self.data.company_overview()
            
            # set elements
            self.kff(data_co, "Industry", "Industry", 70)
            self.kff(data_co, "Sector", "Sector", 75)
            self.kff(data_co, "Country", "Country", 80)
            self.kff(data_co, "Exchange", "Exchange", 85)
            self.kff(data_co, "Currency", "Currency", 90)
            self.kff(data_co, "Fiscal Year End", "FiscalYearEnd", 95)
            self.kff(data_co, "Latest Quarter", "LatestQuarter", 100)
            
            self.kff(data_co, "Market Capitalization", "MarketCapitalization", 110, thousands_character=True)
            self.kff(data_co, "Shares Outstanding", "SharesOutstanding", 115, thousands_character=True)
            
            self.kff(data_co, "Revenue", "RevenueTTM", 125, thousands_character=True)
            self.kff(data_co, "Gross Profit", "GrossProfitTTM", 130, thousands_character=True)
            self.kff(data_co, "EBITDA", "EBITDA", 135, thousands_character=True)
            
            self.kff(data_co, "Earnings per Share", "EPS", 145)
            self.kff(data_co, "Quarterly Earnings Growth", "QuarterlyEarningsGrowthYOY", 150)
            self.kff(data_co, "Revenue per Share", "RevenuePerShareTTM", 155)
            self.kff(data_co, "Quarterly Revenue Growth", "QuarterlyRevenueGrowthYOY", 160)
            
            self.kff(data_co, "Return on Assets", "ReturnOnAssetsTTM", 170)
            self.kff(data_co, "Return on Equity", "ReturnOnEquityTTM", 175)
            
            self.kff(data_co, "Profit Margin", "ProfitMargin", 185)
            self.kff(data_co, "Operating Margin", "OperatingMarginTTM", 190)
            
            self.kff(data_co, "Price to Earnings", "PERatio", 200)
            self.kff(data_co, "PE Forward", "ForwardPE", 205)
            self.kff(data_co, "Price to Earnings Growth", "PEGRatio", 210)
            self.kff(data_co, "Enterprise Value to Revenue", "EVToRevenue", 215)
            self.kff(data_co, "Enterprise Value to EBITDA", "EVToEBITDA", 220)
            self.kff(data_co, "Price to Sales", "PriceToSalesRatioTTM", 225)
            self.kff(data_co, "Price to Book", "PriceToBookRatio", 230)
            self.kff(data_co, "Book Value", "BookValue", 235)
            self.kff(data_co, "Beta", "Beta", 240)
            
            self.kff(data_co, "52 Week High", "52WeekHigh", 160, left_position=False)
            self.kff(data_co, "52 Week Low", "52WeekLow", 165, left_position=False)
            self.kff(data_co, "50 Day Moving Average", "50DayMovingAverage", 170, left_position=False)
            self.kff(data_co, "200 Day Moving Average", "200DayMovingAverage", 175, left_position=False)
            
            self.kff(data_co, "Analyst Target Price", "AnalystTargetPrice", 185, left_position=False)
            
            self.kff(data_co, "Dividend per Share", "DividendPerShare", 195, left_position=False)
            self.kff(data_co, "Dividend Yield", "DividendYield", 200, left_position=False)
            self.kff(data_co, "Dividend Date", "DividendDate", 205, left_position=False)
            self.kff(data_co, "Ex Dividend Date", "ExDividendDate", 210, left_position=False)
        except:
            pass
            
        try:
            # access data
            data_qu = self.data.quote()
            
            self.kff(data_qu, "Price", "05. price", 110, "b", "b", left_position=False)
            self.kff(data_qu, "Change", "09. change", 115, left_position=False)
            self.kff(data_qu, "Percent Change", "10. change percent", 120, left_position=False)
            
            self.kff(data_qu, "Open", "02. open", 130, left_position=False)
            self.kff(data_qu, "High", "03. high", 135, left_position=False)
            self.kff(data_qu, "Low", "04. low", 140, left_position=False)
            self.kff(data_qu, "Previous Close", "08. previous close", 145, left_position=False)
            self.kff(data_qu, "Volume", "06. volume", 150, thousands_character=True, left_position=False)
        except:
            self.no_data_available()
        
        
    def income_statement(self):
        '''
        Creates income statement on pdf page.
        '''
        try:
            # access data
            data_in = self.data.income_statement()
            
            # set elements
            self.arf(data_in, "", "fiscalDateEnding", 60)
            self.arf(data_in, "", "reportedCurrency", 65)
            
            self.arf(data_in, "Revenue", "totalRevenue", 75)
            self.arf(data_in, "Cost of Revenue", "costOfRevenue", 80)
            self.arf(data_in, "Gross Profit", "grossProfit", 85, "b", "b")
            
            self.arf(data_in, "Operating Expense", "operatingExpenses", 95)
            self.arf(data_in, "Selling General and Administrativ", "sellingGeneralAndAdministrative", 100)
            self.arf(data_in, "Research Development", "researchAndDevelopment", 105)
            self.arf(data_in, "EBITDA", "ebitda", 110, "b", "b")
            
            self.arf(data_in, "Deprecation and Amortiziation", "depreciationAndAmortization", 120)
            self.arf(data_in, "Deprecation", "depreciation", 125)
            self.arf(data_in, "Operating Income", "operatingIncome", 130, "b", "b")
            
            self.arf(data_in, "Interest Income", "interestIncome", 140)
            self.arf(data_in, "Other non Operating Income or Expense", "otherNonOperatingIncome", 145)
            self.arf(data_in, "EBIT", "ebit", 150, "b", "b")
            
            self.arf(data_in, "Interest Expense", "interestExpense", 160)
            self.arf(data_in, "EBT", "incomeBeforeTax", 165, "b", "b")
            
            self.arf(data_in, "Income Tax Expense", "incomeTaxExpense", 175)
            self.arf(data_in, "Net Income from Continuing Operations", "netIncomeFromContinuingOperations", 180)
            self.arf(data_in, "Net Income", "netIncome", 185, "b", "b")
            
            self.arf(data_in, "Net Investment Income", "investmentIncomeNet", 205)
            self.arf(data_in, "Net Interest Income", "netInterestIncome", 210)
            self.arf(data_in, "Non Interest Income", "nonInterestIncome", 215)
            self.arf(data_in, "Interest and Dept Expense", "interestAndDebtExpense", 220)
            self.arf(data_in, "Comprehensive Income Net of Tax", "comprehensiveIncomeNetOfTax", 225)
            self.arf(data_in, "Cost of Goods and Services Sold", "costofGoodsAndServicesSold", 230)
        except:
            self.no_data_available()
        
    def balance_sheet(self):
        '''
        Creates balance sheet on pdf page.
        '''
        try:
            # access data
            data_bs = self.data.balance_sheet()
            
            # set elements
            self.arf(data_bs, "", "fiscalDateEnding", 60)
            self.arf(data_bs, "", "reportedCurrency", 65)
            
            self.arf(data_bs, "Total Assets", "totalAssets", 75, "b", "b")
            
            self.arf(data_bs, "Current Assets", "totalCurrentAssets", 80, "b", "b")
            self.arf(data_bs, "Cash and Short Term Investments", "cashAndShortTermInvestments", 85)
            self.arf(data_bs, "Cash and Cash Equivalents at CaVa", "cashAndCashEquivalentsAtCarryingValue", 90)
            self.arf(data_bs, "Short Term Investments", "shortTermInvestments", 95)
            self.arf(data_bs, "Current Net Receivable", "currentNetReceivables", 100)
            self.arf(data_bs, "Inventory", "inventory", 105)
            self.arf(data_bs, "Other Current Assets", "otherCurrentAssets", 110)
            
            self.arf(data_bs, "Non Current Assets", "totalNonCurrentAssets", 115, "b", "b")
            self.arf(data_bs, "Property Plant Equipment", "propertyPlantEquipment", 120)
            self.arf(data_bs, "Accumulated Depreciation Amortization PPE", "accumulatedDepreciationAmortizationPPE", 125)
            self.arf(data_bs, "Intangible Assets", "intangibleAssets", 130)
            self.arf(data_bs, "Goodwill", "goodwill", 135)
            self.arf(data_bs, "Intangible Assets Excluding Goodwill", "intangibleAssetsExcludingGoodwill", 140)
            self.arf(data_bs, "Long Term Investments", "longTermInvestments", 145)
            self.arf(data_bs, "Other Non Current Assets", "otherNonCurrrentAssets", 150)
            
            self.arf(data_bs, "Total Liabilities", "totalLiabilities", 160, "b", "b")
            
            self.arf(data_bs, "Current Liabilities", "totalCurrentLiabilities", 165, "b", "b")
            self.arf(data_bs, "Current Accounts Payable", "currentAccountsPayable", 170)
            self.arf(data_bs, "Short Term Debt", "shortTermDebt", 175)
            self.arf(data_bs, "Deferred Revenue", "deferredRevenue", 180)
            self.arf(data_bs, "Current Long Term Debt", "currentLongTermDebt", 185)
            self.arf(data_bs, "Other Current Liabilities", "otherCurrentLiabilities", 190)
            
            self.arf(data_bs, "Non Current Liabilities", "totalNonCurrentLiabilities", 195, "b", "b")
            self.arf(data_bs, "Long Term Debt Non Current", "longTermDebtNoncurrent", 200)
            self.arf(data_bs, "Other Non Current Liabilities", "otherNonCurrentLiabilities", 205)
            
            self.arf(data_bs, "Shareholder Equity", "totalShareholderEquity", 215, "b", "b")
            self.arf(data_bs, "Common Stock", "commonStock", 220)
            self.arf(data_bs, "Treasury Stock", "treasuryStock",225)
            self.arf(data_bs, "Retained Earnings", "retainedEarnings", 230)
            self.arf(data_bs, "Common Stock Shares Outstanding", "commonStockSharesOutstanding", 235)
        except:
            self.no_data_available()
        
        
    def cash_flow(self):
        '''
        Creates cash flow on pdf page.
        '''
        try:
            # access data
            data_cs = self.data.cash_flow()
            
            # set elements
            self.arf(data_cs, "", "fiscalDateEnding", 60)
            self.arf(data_cs, "", "reportedCurrency", 65)
            
            self.arf(data_cs, "Operating Cashflow", "operatingCashflow", 75, "b", "b")
            self.arf(data_cs, "Net Income", "netIncome", 80)
            self.arf(data_cs, "Payments for Operating Activities", "paymentsForOperatingActivities", 85)
            self.arf(data_cs, "Proceeds from Operating Activities", "proceedsFromOperatingActivities", 90)
            self.arf(data_cs, "Depreciation Depletion and Amortization", "depreciationDepletionAndAmortization", 95)
            self.arf(data_cs, "Change in Operating Liabilities", "changeInOperatingLiabilities", 100)
            self.arf(data_cs, "Change in Operating Assets", "changeInOperatingAssets", 105)
            self.arf(data_cs, "Change in Receivables", "changeInReceivables", 110)
            self.arf(data_cs, "Change in Inventory", "changeInInventory", 115)
            
            self.arf(data_cs, "Cashflow from Investment", "cashflowFromInvestment", 125, "b", "b")
            self.arf(data_cs, "Capital Expenditures", "capitalExpenditures", 130)
            
            self.arf(data_cs, "Cashflow from Financing", "cashflowFromFinancing", 140, "b", "b")
            self.arf(data_cs, "Dividend Payout", "dividendPayout", 145)
            self.arf(data_cs, "Dividend Payout Common Stock", "dividendPayoutCommonStock", 150)
            self.arf(data_cs, "Dividend Payout Preferred Stock", "operatingCashflow", 155)
            self.arf(data_cs, "Payments for Repurchase of Common Stock", "paymentsForRepurchaseOfCommonStock", 160)
            self.arf(data_cs, "Payments for Repurchase of Equity", "paymentsForRepurchaseOfEquity", 165)
            self.arf(data_cs, "Payments for Repurchase of Preferred Stock", "paymentsForRepurchaseOfPreferredStock", 170)
            self.arf(data_cs, "Proceeds from Repayments of Short Term D.", "proceedsFromRepaymentsOfShortTermDebt", 175)
            self.arf(data_cs, "Proceeds from Issuance of Common Stock", "proceedsFromIssuanceOfCommonStock", 180)
            self.arf(data_cs, "Proceeds from Issuance of Long Term Debt", "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet", 185)
            self.arf(data_cs, "Proceeds from Issuance of Preferred Stock", "proceedsFromIssuanceOfPreferredStock", 190)
            self.arf(data_cs, "Proceeds from Repurchase of Equity", "proceedsFromRepurchaseOfEquity", 195)
            self.arf(data_cs, "Proceeds from Sale of Treasury Stock", "proceedsFromSaleOfTreasuryStock", 200)
            
            self.arf(data_cs, "Change in Cash and Cash Equivalents", "changeInCashAndCashEquivalents", 210)
            self.arf(data_cs, "Change in Exchange Rate", "changeInExchangeRate", 215)
        except:
            self.no_data_available()
        

    def technical_analysis(self):
        """
        Insert plots in pdf
        """
        download_folder = os.path.expanduser("~")+"/Downloads/"
        
        self.pdf.image(f"{download_folder}/stock-report_sma.png", 5, 55, self.width - 10)
        self.pdf.image(f"{download_folder}/stock-report_bb.png", 5, 150, self.width - 10)
        self.new_page()
        self.pdf.image(f"{download_folder}/stock-report_macd.png", 5, 55, self.width - 10)
        self.pdf.image(f"{download_folder}/stock-report_rsi.png", 5, 150, self.width - 10)
        self.new_page()
        self.pdf.image(f"{download_folder}/stock-report_dpc.png", 5, 55, self.width - 10)
        self.pdf.image(f"{download_folder}/stock-report_md.png", 5, 150, self.width - 10)
        
        os.remove(f"{download_folder}/stock-report_sma.png")
        os.remove(f"{download_folder}/stock-report_bb.png")
        os.remove(f"{download_folder}/stock-report_macd.png")
        os.remove(f"{download_folder}/stock-report_rsi.png")
        os.remove(f"{download_folder}/stock-report_dpc.png")
        os.remove(f"{download_folder}/stock-report_md.png")