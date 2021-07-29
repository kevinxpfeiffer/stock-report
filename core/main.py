import pdf as p
import data as d
import analysis
import shutil

# create hole pdf document
p.new_page()
p.create_title()
p.create_box_key_figures()
p.key_figures()
p.create_box_score()
p.score()
p.new_page()
p.plots()

p.pdf.output(f'{d.name}.pdf', 'F')
# two variants:
shutil.move(f'{d.name}.pdf', '/Users/kevinpfeiffer/Downloads')
# shutil.move(f'{d.stock_name}.pdf', './examples')
print('PDF is ready!!!')


# ? Versiedene Comments
# ! Warning
# TODO This is a ToDo
# * Other method
# ! WARNING


