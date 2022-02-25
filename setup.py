from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='stock-report',
    version='0.0.4',
    description='StockReport is a Phyton program that allows you to simply create an automated PDF report about a stock.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pfeiffer-dev/stock-report',
    author='Kevin Pfeiffer',
    author_email='pfeiffer.kevin@gmx.de',
    classifiers=[ 
        'Development Status :: 5 - Production/Stable',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    keywords='stock-market, pandas, pdf, report, fpdf, alpha-vantage, plotly-express',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'shutil',
        'os',
        'datetime',
        'alpha-vantage',
        'pandas',
        'fpdf',
        'plotly'
    ],
    package_data={ 
        'stock-report': [],
    },
    # data_files=[('my_data', ['/resources'])], 

    project_urls={ 
        'Bug Reports': 'https://github.com/pfeiffer-dev/stock-report/issues',
        'Source': 'https://github.com/pfeiffer-dev/stock-report',
    },
)