# main.py
# stock-report
# Copyright 2022 Kevin Pfeiffer
# MIT License

import shutil
import os
import time
from stock_report import data
from stock_report import analysis
from stock_report import pdf


print("")
print("Welcome to Stock Report...")
print("Here you can carry out an automatic analysis of a share of your choice and receive the result as a PDF.")
print("")

while True:
        print('Which company should be analyzed?')
        name = str(input(">>> "))
        print("")
        
        d = data.DATA(name=name, ticker="AAPL") # Create object data for search
        
        #try:
        print(d.symbol_search(keyword=name)) # Print searche
        print("")
                
        print("What's the company's ticker?")
        ticker = str(input(">>> "))
        print("")
                
        print('One moment please, PDF is being generated...')
        print("")
                        
        d = data.DATA(name=name, ticker=ticker) # Create object data
        a = analysis.ANALYSIS(data=d) # Create object analysis
                        
        a.main() # run analysis
                        
        p = pdf.PDF(data=d, name=name, ticker=ticker) # Create object pdf
                        
        p.new_page()
        p.create_title()
        p.key_figures()
                        
        time.sleep(60) # time sleep for alpha vantage api
                
        p.new_page()
        p.create_heading("Income Statement")
        p.income_statement()
                        
        p.new_page()
        p.create_heading("Balance Sheet")
        p.balance_sheet()
                        
        p.new_page()
        p.create_heading("Cashflow")
        p.cash_flow()
                        
        p.new_page()
        p.create_heading("Technical Analysis")
        p.technical_analysis()

        p.pdf.output(f'{name}.pdf', 'F') # Create pdf
                
        download_folder = os.path.expanduser("~")+"/Downloads/"
        shutil.move(f'{name}.pdf', download_folder) # Move pdf to output folder
        
                                
        print('PDF is ready!!!')
        print("You can quit with ctrl + c everytime.")
        print("")
        #except:
               # print("Something must have gone wrong :(")
               # print("Try again or quit with ctrl + c")
               # print("")  