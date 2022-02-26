![Logo StockReport](https://github.com/pfeiffer-dev/stock-report/blob/main/resources/logo.png "Logo Stock Report")

**StockReport is a Phyton program that allows you to simply create an automated PDF report about a stock.**

---

## Installation
Before starting please install the following packages:
```
pip install alpha_vantage
pip install pandas
pip install fpdf
pip install plotly
```
Then install stock-report:
```
pip install stock-report
```

## Usage
### Alpha Vantage
This project is build with the [Alpha Vantage API ](https://www.alphavantage.co)

You can request a free key at the following link: [Claim API Key](https://www.alphavantage.co/support/#api-key)

### Save your key as an environment variable

***Mac***
1. From your terminal, type in: `export ALPHAVANTAGE_API_KEY=xxx`
2. Make sure to use your actual API key for the value. You can confirm that the environment variable is saved by typing in the following which should display your API key:
`echo $ALPHAVANTAGE_API_KEY`
   
or

1. From your terminal, type in: `nano .zshenv`
3. In nano insert `export ALPHAVANTAGE_API_KEY=xxx`
4. Close nano
5. Restart

***Windows***
1. Click Start and type in `environment variables`. You should see an option to Edit environment variables for your account.
2. In the new window that pops up, click New under the User variables section.
3. Your variable name should be `ALPHAVANTAGE_API_KEY` and the variable value is where you can paste in your key.

### Run
Run with:
```
python3 -m stock-report
```

## Examples
You can view the examples [here](https://github.com/pfeiffer-dev/stock-report/tree/main/examples).

## License
MIT
[See here](https://github.com/pfeiffer-dev/stock-report/blob/main/LICENSE)