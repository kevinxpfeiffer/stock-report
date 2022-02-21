# main.py
# stock-report
# Copyright 2022 Kevin Pfeiffer
# MIT License

import shutil
import data
import analysis
import pdf
import esg


print("")
print("Welcome to Stock Report...")
print("Here you can carry out an automatic analysis of a share of your choice and receive the result as a PDF.")
print("")

while True:
        print('Which company should be analyzed?')
        name = str(input(">>> "))
        print("")
        
        d = data.DATA(name=name, ticker="AAPL") # Create object data for search
        
        print(d.symbol_search(keyword=name)) # Print searche
        print("")
        
        print("What's the company's ticker?")
        ticker = str(input(">>> "))
        print("")
        
        try:
                print('One moment please, PDF is being generated...')
                print("")
                
                d = data.DATA(name=name, ticker=ticker) # Create object data
                e = esg.ESG(name=name).esg() # Create object esg
                a = analysis.ANALYSIS(data=d) # Create object analysis
                
                a.main() # run analysis
                
                p = pdf.PDF(data=d, esg=e, name=name, ticker=ticker) # Create object pdf
                
                p.new_page()
                p.create_title()
                p.create_box_key_figures()
                p.key_figures()
                p.create_box_score()
                p.score()
                p.new_page()
                p.plots()

                p.pdf.output(f'{name}.pdf', 'F') # Create pdf
                shutil.move(f'{name}.pdf', '/Users/kevinpfeiffer/Downloads') # Move pdf to output folder
                        
                print('PDF is ready!!!')
                print("You can quit with ctrl + c everytime.")
                print("")
        except:
                print("Something must have gone wrong :(")
                print("Try again or quit with ctrl + c")
                print("")    