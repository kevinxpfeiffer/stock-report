# pdf.py
# stock-report
# Copyright 2022 Kevin Pfeiffer
# MIT License

from fpdf import FPDF
from datetime import date


class PDF: # PDF(FPDF)
    def __init__(self, data, esg, name, ticker):
        self.date = date.today()
        self.data = data
        self.esg = esg
        self.name = name
        self.ticker = ticker
        self.width = 210
        self.height = 297

    # Formats A4 Letter
    pdf = FPDF("P", "mm", "A4")

    def new_page(self):
        """
        Creates a new PDF page
        :return:
        """
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.image("./resources/header.png", 0, 0, self.width)
        self.pdf.image("./resources/footer.png", 0, 252, self.width)

    def create_title(self):
        """
        Creates title with name and ticker
        :return:
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
        Creates title with name and ticker
        :return:
        """
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("Arial", "b", 20)
        self.pdf.ln(30)
        self.pdf.write(4, f"{headline}")
        self.pdf.ln(5)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.write(4, f"Symbol: {self.ticker}")
        self.pdf.ln(5)

    def create_box_score(self):
        """
        creates box for Score
        :return:
        """
        self.pdf.line(self.width / 2 + 10, 75, self.width / 2 + 10, 100)
        self.pdf.line(self.width / 2 + 10, 75, 200, 75)
        self.pdf.line(200, 100, self.width / 2 + 10, 100)
        self.pdf.line(200, 100, 200, 75)
        self.pdf.set_font("Arial", "b", 14)
        self.pdf.set_xy(self.width / 2 + 11, 80)
        self.pdf.cell(0, txt="Score")

    def category_key_figures(self, data, category):
        category_data = data
        category_data = category_data[category].values[0]
        return category_data

    def category_annual_report(self, data, year ,category):
    # year -> start with 0 for latest year
        end = year + 1
        category_annual_report = data
        category_annual_report = category_annual_report.iloc[year:end , :]
        category_annual_report = category_annual_report[category].values[0]
        return category_annual_report

    def kff(self, data, key, category, y):
        """
        Creates Template for key_figures()
        :param key: name of key as string
        :param value: value of key
        :param y: position of y in mm
        :return:
        """
        self.pdf.set_font("Arial", "b", 12)
        self.pdf.set_xy(15, y)
        self.pdf.cell(0, txt=f"{key}")
        
        self.pdf.set_font("Arial", "", 12)
        value = self.category_key_figures(data, category)
        self.pdf.set_xy(70, y)
        self.pdf.cell(0, txt=f"{value}")

    def key_figures(self):
        """

        """
        # acces data
        data_co = self.data.company_overview()
        data_qu = self.data.quote()
        
        # y abstand immer 5
        self.kff(data_qu, "price", "05. price", 70)
        self.kff(data_qu, "change", "09. change", 75)
        self.kff(data_qu, "change %", "10. change percent", 80)
        self.kff(data_qu, "volume", "06. volume", 85)
        
        self.kff(data_qu, "symbol", "01. symbol", 90)
        self.kff(data_co, "exchange", "Exchange", 95)
        self.kff(data_co, "currency", "Currency", 100)
        self.kff(data_co, "exchange", "Exchange", 105)
   
        self.kff(data_co, "sector", "Sector", 110)
        self.kff(data_co, "industry", "Industry", 115)
    
        self.kff(data_co, "ebitda", "EBITDA", 125)
        self.kff(data_co, "revenue", "RevenueTTM", 130)
    
    def arf(self, data, key, category, y, key_style="", value_style=""):
        self.pdf.set_font("Arial", key_style, 12)
        self.pdf.set_xy(10, y)
        self.pdf.cell(0, txt=f"{key}")
        self.pdf.set_font("Arial", value_style, 12) # style b: bold, i: italic, u: underline
        
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
    
        
    def income_statement_pdf(self):
        '''
        
        '''
        data_in = self.data.income_statement()
        
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
        
        
    def balance_sheet_pdf(self):
        '''
        '''
        data_bs = self.data.balance_sheet()
        
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
        
        
    def cash_flow_pdf(self):
        '''
        '''
        data_cs = self.data.cash_flow()
        
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
        
        
    def score(self):
        """
        Creates score for Score Box
        :return:
        """
        analysed_score = 5  # Score insert analysis data
        self.pdf.set_font("Arial", "b", 30)
        self.pdf.set_xy(self.width - 30, 90)
        if analysed_score > 7:
            self.pdf.set_text_color(0, 204, 0)
        elif 7 >= analysed_score > 5:
            self.pdf.set_text_color(255, 204, 0)
        else:
            self.pdf.set_text_color(255, 0, 0)
        self.pdf.cell(0, txt=f"{analysed_score}")

    def plots(self):
        """
        Insert plots in PDF
        """
        self.pdf.image("./resources/sma.png", 5, 55, self.width - 10)
        self.pdf.image("./resources/bb.png", 5, 150, self.width - 10)
        self.new_page()
        self.pdf.image("./resources/macd.png", 5, 55, self.width - 10)
        self.pdf.image("./resources/rsi.png", 5, 150, self.width - 10)
        self.new_page()
        self.pdf.image("./resources/dpc.png", 5, 55, self.width - 10)
        self.pdf.image("./resources/md.png", 5, 150, self.width - 10)
