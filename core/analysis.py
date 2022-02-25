# analysis.py
# stock-report
# Copyright 2022 Kevin Pfeiffer
# MIT License

from scipy.stats import norm
import plotly.express as px
import pandas as pd


class ANALYSIS:
    def __init__(self, data):
        self.data = data.daily_prices()

    def main(self):
        
        pd.options.mode.chained_assignment = None  # Disable SettingWithCopyWarning
        
        data = self.data[['4. close']]
        ticker = data[::-1]  # reverse dataframe for better calculation
            
        '''MACD'''
        exp1 = ticker['4. close'].ewm(span=12, adjust=False).mean()
        exp2 = ticker['4. close'].ewm(span=26, adjust=False).mean()

        ticker['MACD'] = exp1 - exp2
        ticker['Signal Line'] = ticker['MACD'].ewm(span=9, adjust=False).mean()

        '''SMA'''
        ticker['SMA 30 Days'] = ticker['4. close'].rolling(window=30).mean()
        ticker['SMA 100 Days'] = ticker['4. close'].rolling(window=100).mean()

        '''RSI'''
        delta = ticker['4. close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=13, adjust=False).mean()
        ema_down = down.ewm(com=13, adjust=False).mean()
        rs = ema_up / ema_down

        ticker['RSI'] = 100 - (100 / (1 + rs))
        # Skip first 14 days to have real values


        '''Bollinger Bands'''
        ticker['Moving Average 30 Days'] = ticker['4. close'].rolling(window=20).mean()
        ticker['Standard Deviation 30 Days'] = ticker['4. close'].rolling(window=20).std()
        ticker['Upper Band'] = ticker['Moving Average 30 Days'] + (ticker['Standard Deviation 30 Days'] * 2)
        ticker['Lower Band'] = ticker['Moving Average 30 Days'] - (ticker['Standard Deviation 30 Days'] * 2)

        '''Max Drawdown'''
        ticker['Daily Percentage Change'] = ticker['4. close'].pct_change()
        ticker['Wealth Index'] = 1000 * (1 + ticker['Daily Percentage Change'][2:]).cumprod()
        ticker['Previous Peaks'] = ticker['Wealth Index'].cummax()
        ticker['Maximal Drawdown'] = (ticker['Wealth Index'] - ticker['Previous Peaks']) / ticker['Previous Peaks']

        '''

        ERK-RISK-Kit_Methods

        '''

        # calculate returns
        r = ticker['4. close'].pct_change()
        r_mean = r.mean()

        '''Semideviation'''
        semideviation = r[r < 0].std(ddof=0)

        '''Standarddeviation'''
        volatility = r.std()
        
        '''skewness and kurtosis'''
        demeaned_r = r - r.mean()
        # use the population standard deviation, so set dof=0
        sigma_r = r.std(ddof=0)
        exp = (demeaned_r ** 3).mean()

        skewness = exp / sigma_r ** 3
        kurtosis = exp / sigma_r ** 4
        
        '''CVar'''
       

        # set Level for function
        level = 5

        z = norm.ppf(level / 100)
        s = skewness
        k = kurtosis
        z = (z +
        (z ** 2 - 1) * s / 6 +
        (z ** 3 - 3 * z) * (k - 3) / 24 -
        (2 * z ** 3 - 5 * z) * (s ** 2) / 36
        )

        cvar = -(r.mean() + z * r.std(ddof=0))

        # Create plots

        plot_data = ticker[::-1]  # reverse dataframe for better displaying

        # Plot of MACD
        plot_macd = px.line(data_frame=plot_data[0:365],
                        y=['MACD', 'Signal Line'],
                        title='MACD')
        #plot_macd.show()
        plot_macd.write_image('./resources/macd.png', format='png', width=1000, height=500)

        # Plot of SMA
        plot_sma = px.line(data_frame=plot_data[0:365],
                        y=['4. close', 'SMA 30 Days', 'SMA 100 Days'],
                        title='Simple Moving Average')
        #plot_sma.show()
        plot_sma.write_image('./resources/sma.png', format='png', width=1000, height=500)

        # Plot of RSI
        plot_rsi = px.line(data_frame=plot_data[0:365],
                                y=['RSI'],
                                title='Relative Strength Index')
        plot_rsi.add_hline(y=30, line_width=3, line_dash="dash", line_color="green")
        plot_rsi.add_hline(y=70, line_width=3, line_dash="dash", line_color="red")
        #plot_rsi.show()
        plot_rsi.write_image('./resources/rsi.png', format='png', width=1000, height=500)

        # Plot of Bollinger Bands
        plot_bb = px.line(data_frame=plot_data[0:365],
                        y=['4. close', 'Moving Average 30 Days', 'Upper Band', 'Lower Band'],
                        title='Bolinger Bands')
        #plot_bb.show()
        plot_bb.write_image('./resources/bb.png', format='png', width=1000, height=500)

        # Plot of Maximal Drawdown
        plot_md = px.line(data_frame=plot_data[0:365],
                        y=['Maximal Drawdown'],
                        title='Maximal Drawdown')
        #plot_md.show()
        plot_md.write_image('./resources/md.png', format='png', width=1000, height=500)

        # Plot of Daily Percentage Change
        plot_dpc = px.line(data_frame=plot_data[0:365],
                        y=['Daily Percentage Change'],
                        title='Daily Percentage Change')
        #plot_dpc.show()
        plot_dpc.write_image('./resources/dpc.png', format='png', width=1000, height=500)