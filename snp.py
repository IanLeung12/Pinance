import bs4 as bs
import pickle
import requests
import os
import pandas as pd
import yfinance as web
import datetime as dt

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text,'html.parser')
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:  # Skip the header row
        # Find all <td> elements (table columns)
        columns = row.findAll('td')

        # Check if the row has at least one <td> element
        if len(columns) > 0:
            ticker = columns[1].text.strip() # Get the ticker symbol, remove extra spaces
            tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as file:
        pickle.dump(tickers, file)

    print(tickers)

    return tickers

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as file:
            tickers = pickle.load(file)

    tickers = [ticker for ticker in tickers if ticker.strip()]

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2024,12,31)

    for ticker in tickers:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.download(ticker,start,end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

def compile_data():
    with open('sp500tickers.pickle', 'rb') as file:
        tickers = pickle.load(file)

    tickers = [ticker for ticker in tickers if ticker.strip()]
    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df = df[['Date', 'Adj Close']].copy()
        df.set_index('Date', inplace=True)

        df.rename(columns = {'Adj Close': ticker}, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count%10 == 0:
            print(count)

        print(main_df.head())
        main_df.to_csv('sp500_joined_closes.csv')

compile_data()
#get_data_from_yahoo()
#save_sp500_tickers()