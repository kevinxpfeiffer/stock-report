# Python Libraries
import os
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.foreignexchange import ForeignExchange


# Get name and ticker
print('Which company should be analyzed?')
name = str(input("--> "))
print("What's the company's ticker?")
ticker = str(input("--> "))
print('One moment please, PDF is being generated...')


# Get Alpha Vantage Key
api_key = os.getenv('ALPHAVANTAGE_API_KEY')


# Define various Alpha Vantage classes
ts = TimeSeries(key=api_key, output_format='pandas')
fd = FundamentalData(key=api_key, output_format='pandas')
fo = ForeignExchange(key=api_key, output_format='pandas')


# Fundamental Data
fundamental_data = fd.get_company_overview(symbol=ticker)


def fundamental(category):
    """
    help function to get fundamental data by category
    :param category: Alpha Vantage category name as string
    :return: selected fundamental data
    """
    fun_data = fundamental_data[0]
    fun_data = fun_data[category].values[0]
    return fun_data


exchange = fundamental("Exchange")
currency = fundamental("Currency")
country = fundamental("Country")
sector = fundamental("Sector")
industry = fundamental("Industry")
address = fundamental("Address")
fiscal_year_end = fundamental("FiscalYearEnd")
latest_quarter = fundamental("LatestQuarter")
market_cap = fundamental('MarketCapitalization')
ebitda = fundamental("EBITDA")
pe = fundamental("PERatio")
peg = fundamental("PEGRatio")
book_value = fundamental("BookValue")
dividend = fundamental("DividendPerShare")
dividend_yield = fundamental("DividendYield")
eps = fundamental("EPS")
revenue_per_share = fundamental("RevenuePerShareTTM")
profit_margin = fundamental("ProfitMargin")
operating_margin = fundamental("OperatingMarginTTM")
return_on_assets = fundamental("ReturnOnAssetsTTM")
return_on_equity = fundamental("ReturnOnEquityTTM")
revenue = fundamental("RevenueTTM")
gross_profit = fundamental("GrossProfitTTM")
diluted_eps = fundamental("DilutedEPSTTM")
q_earnings_growth = fundamental("QuarterlyEarningsGrowthYOY")
q_revenue_growth = fundamental("QuarterlyRevenueGrowthYOY")
analyst_target_price = fundamental("AnalystTargetPrice")
trailing_pe = fundamental("TrailingPE")
forward_pe = fundamental("ForwardPE")
price_to_sales_ratio = fundamental("PriceToSalesRatioTTM")
price_to_book_ratio = fundamental("PriceToBookRatio")
evt_revenue = fundamental("EVToRevenue")
evt_ebitda = fundamental("EVToEBITDA")
beta = fundamental("Beta")
week_high_52 = fundamental("52WeekHigh")
week_low_52 = fundamental("52WeekLow")
day_moving_average_50 = fundamental("50DayMovingAverage")
day_moving_average_200 = fundamental("200DayMovingAverage")
shares_outstanding = fundamental("SharesOutstanding")
shares_float = fundamental("SharesFloat")
shares_short = fundamental("SharesShort")
shares_short_prior_month = fundamental("SharesShortPriorMonth")
short_ratio = fundamental("ShortRatio")
short_percentage_outstanding = fundamental("ShortPercentOutstanding")
short_percent_float = fundamental("ShortPercentFloat")
percent_insiders = fundamental("PercentInsiders")
percent_institutions = fundamental("PercentInstitutions")
forward_annual_dividend_rate = fundamental("ForwardAnnualDividendRate")
forward_annual_dividend_yield = fundamental("ForwardAnnualDividendYield")
payout_ratio = fundamental("PayoutRatio")
dividend_rate = fundamental("DividendDate")
ex_dividend_date = fundamental("ExDividendDate")
last_split_factor = fundamental("LastSplitFactor")
last_split_date = fundamental("LastSplitDate")


# Balance sheet
balance_sheet = fd.get_balance_sheet_quarterly(symbol=ticker)
# Wie am besten einbinden? https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo


# USD in Euro
usd_eur = fo.get_currency_exchange_rate(from_currency='USD', to_currency='EUR')
usd_eur_rate = usd_eur[0]
usd_eur_rate = usd_eur_rate["5. Exchange Rate"].values[0]


# Stock Time Series
stock_prices = ts.get_daily(symbol=ticker, outputsize='full')
stock_prices = stock_prices[0]
