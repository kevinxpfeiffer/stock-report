# pdf.py
# Copyright 2021 Kevin Pfeiffer
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
        self.pdf.write(4, f"{self.name} ({self.ticker})")
        self.pdf.ln(10)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.write(4, f"Created: {self.date}")
        self.pdf.ln(5)


    def create_box_key_figures(self):
        """
        Creates box for Key figures
        :return:
        """
        self.pdf.line(10, 75, 10, 200)
        self.pdf.line(10, 75, self.width / 2, 75)
        self.pdf.line(self.width / 2, 200, 10, 200)
        self.pdf.line(self.width / 2, 200, self.width / 2, 75)
        self.pdf.set_font("Arial", "b", 14)
        self.pdf.set_xy(11, 80)
        self.pdf.cell(0, txt="Key figures")


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


    def kff(self, key, value, y):
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
        self.pdf.set_xy(70, y)
        self.pdf.cell(0, txt=f"{value}")


    def key_figures(self):
        """

        """
        self.kff("market price !", 0, 90)
        self.kff("currency", self.data.fundamental("Currency"), 95)
        self.kff("exchange", self.data.fundamental("Exchange"), 100)
        #self.kff("sector", self.data.fundamental("Sector"), 105)
        #self.kff("country", self.data.fundamental("Country"), 115)
        self.kff("ebitda", self.data.fundamental("EBITDA"), 120)
        self.kff("revenue", self.data.fundamental("RevenueTTM"), 125)
        self.kff("ESG", self.esg, 130) #!

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
