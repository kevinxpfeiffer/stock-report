# main.py
# Copyright 2021 Kevin Pfeiffer
# MIT License

import shutil
import data
import esg
import pdf


loop = True

while loop:
        print('Which company should be analyzed?')
        name = str(input("--> "))
        print("What's the company's ticker?")
        ticker = str(input("--> "))
        print('One moment please, PDF is being generated...')
        
        
        d = data.DATA(name=name, ticker=ticker)
        e = esg.ESG(name=name).esg()
        p = pdf.PDF(data=d, esg=e, name=name, ticker=ticker)
        
        p.new_page()
        p.create_title()
        p.create_box_key_figures()
        p.key_figures()
        p.create_box_score()
        p.score()
        p.new_page()
        p.plots()

        p.pdf.output(f'{name}.pdf', 'F')
                # two variants:
        shutil.move(f'{name}.pdf', '/Users/kevinpfeiffer/Downloads')
                # shutil.move(f'{d.stock_name}.pdf', './examples')
        print('PDF is ready!!!')





