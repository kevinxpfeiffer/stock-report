# Python Libraries
from fpdf import FPDF
from datetime import date

# Package Libraries
import data as d

# Formats A4 Letter
WIDTH = 210
HEIGHT = 297
pdf = FPDF('P', 'mm', 'A4')

# get date
date = date.today()


def new_page():
    """
    Creates a new PDF page
    :return:
    """
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.image("./resources/header.png", 0, 0, WIDTH)
    pdf.image("./resources/footer.png", 0, 252, WIDTH)


def create_title():
    """
    Creates title with name and ticker
    :return:
    """
    pdf.set_font('Arial', 'b', 40)
    pdf.ln(30)
    pdf.write(4, f"{d.name} ({d.ticker})")
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    pdf.write(4, f'Created: {date}')
    pdf.ln(5)


def create_box_key_figures():
    """
    Creates box for Key figures
    :return:
    """
    pdf.line(10, 75, 10, 200)
    pdf.line(10, 75, WIDTH / 2, 75)
    pdf.line(WIDTH / 2, 200, 10, 200)
    pdf.line(WIDTH / 2, 200, WIDTH / 2, 75)
    pdf.set_font('Arial', 'b', 14)
    pdf.set_xy(11, 80)
    pdf.cell(0, txt='Key figures')


def create_box_score():
    """
    creates box for Score
    :return:
    """
    pdf.line(WIDTH / 2 + 10, 75, WIDTH / 2 + 10, 100)
    pdf.line(WIDTH / 2 + 10, 75, 200, 75)
    pdf.line(200, 100, WIDTH / 2 + 10, 100)
    pdf.line(200, 100, 200, 75)
    pdf.set_font('Arial', 'b', 14)
    pdf.set_xy(WIDTH / 2 + 11, 80)
    pdf.cell(0, txt='Score')


def kff(key, value, y):
    """
    Creates Template for key_figures()
    :param key: name of key as string
    :param value: value of key
    :param y: position of y in mm
    :return:
    """
    pdf.set_font('Arial', 'b', 12)
    pdf.set_xy(15, y)
    pdf.cell(0, txt=f'{key}')
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(70, y)
    pdf.cell(0, txt=f'{value}')


def key_figures():
    """

    """
    kff('market price !', 0, 90)
    kff('currency', d.currency, 95)
    kff('exchange', d.exchange, 100)
    kff('sector', d.sector, 105)
    kff('country', d.country, 115)
    kff('ebitda', d.ebitda, 120)
    kff('revenue', d.revenue, 125)
    kff('week high 52', d.week_high_52, 130)
    kff('week low 52', d.week_low_52, 135)
    kff('ebitda', d.ebitda, 140)
    kff('PE ratio', d.pe, 145)
    kff('PEG ratio', d.peg, 150)
    kff('dividend', d.dividend, 155)
    kff('EPS', d.eps, 160)
    kff('short', d.shares_short, 165)
    kff('institutions', d.percent_institutions, 170)
    kff('last split', d.last_split_date, 175)


def score():
    """
    Creates score for Score Box
    :return:
    """
    analysed_score = 5  # Score insert analysis data
    pdf.set_font('Arial', 'b', 30)
    pdf.set_xy(WIDTH - 30, 90)
    if analysed_score > 7:
        pdf.set_text_color(0, 204, 0)
    elif 7 >= analysed_score > 5:
        pdf.set_text_color(255, 204, 0)
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(0, txt=f'{analysed_score}')


def plots():
    """
    Insert plots in PDF
    """
    pdf.image("./resources/sma.png", 5, 55, WIDTH - 10)
    pdf.image("./resources/bb.png", 5, 150, WIDTH - 10)
    new_page()
    pdf.image("./resources/macd.png", 5, 55, WIDTH - 10)
    pdf.image("./resources/rsi.png", 5, 150, WIDTH - 10)
    new_page()
    pdf.image("./resources/dpc.png", 5, 55, WIDTH - 10)
    pdf.image("./resources/md.png", 5, 150, WIDTH - 10)
