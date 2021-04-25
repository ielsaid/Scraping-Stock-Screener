import pandas as pd
import numpy as npy
from bs4 import BeautifulSoup
import urllib.request
from decimal import *


place_to_search = input("Which Index to search (if multiple seperate by space)?\n1. S&P 500\n2. Nasdaq 100\n3. Dow Jones\n4. Russell 1000\n")

if len(place_to_search)>1:
    list_selection = place_to_search.split(' ')
else:
    list_selection = [place_to_search]

tickers = []


if '1' in list_selection:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    website = urllib.request.urlopen(url)
    data = website.read()
    soup = BeautifulSoup(data, 'html.parser')
    
    tables = soup.findAll('table')
    for table in tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:

            ticker = row.find_all('td')
            list_row = [cell.text.strip() for cell in ticker]
            if len(list_row) > 1:
                if list_row[0].isupper():
                    tickers.append(list_row[0])
elif '2' in list_selection:
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    website = urllib.request.urlopen(url)
    data = website.read()
    soup = BeautifulSoup(data, 'html.parser')

    tables = soup.findAll('table')
    for table in tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:
            ticker = row.find_all('td')
            list_row = [cell.text.strip() for cell in ticker]
        
            if len(list_row) > 1:
                if list_row[1].isupper():
                    tickers.append(list_row[1])
elif '3' in list_selection:
    url = "https://www.investopedia.com/terms/d/djia.asp"
    website = urllib.request.urlopen(url)
    data = website.read()
    soup = BeautifulSoup(data, 'html.parser')
    tables = soup.findAll('table')
    
    for table in tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
    
        for row in rows:
            ticker = row.find_all('td')
            list_row = [cell.text.strip() for cell in ticker]
            tickers.append(list_row[1])
elif '4' in list_selection:
    url = "https://en.wikipedia.org/wiki/Russell_1000_Index"
    website = urllib.request.urlopen(url)
    data = website.read()
    soup = BeautifulSoup(data, 'html.parser')

    tables = soup.findAll('table')
    for table in tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        
        for row in rows:
            ticker = row.find_all('td')
            list_row = [cell.text.strip() for cell in ticker]
            if len(list_row) > 1:
                if list_row[1].isupper():
                    tickers.append(list_row[1])

tickers = list(dict.fromkeys(tickers))

url = 'https://finance.yahoo.com/quote/'+tickers[0]+'/key-statistics?p='+tickers[0]
website = urllib.request.urlopen(url)
data = website.read()
soup = BeautifulSoup(data, 'html.parser')
technicals = {}
tables = soup.findAll('table', {"class": 'W(100%) Bdcl(c)'})

for table in tables:
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        col_name = row.find_all('span')
        col_name = [cell.text.strip() for cell in col_name]

        col_val = row.find_all('td')
        col_val = [cell.text.strip() for cell in col_val]
        
        if col_val[1][-1] == 'T':
            new_int = float(Decimal(col_val[1][0:-1]))
            converted = new_int*1000000
            technicals[col_name[0]+' (in Ms)'] = [converted]
        elif col_val[1][-1] == 'B':
            new_int = float(Decimal(col_val[1][0:-1]))
            converted = new_int*1000
            technicals[col_name[0]+' (in Ms)'] = [converted]
        elif col_val[1][-1] == 'M':
            new_int = float(Decimal(col_val[1][0:-1]))
            converted = new_int*1
            technicals[col_name[0]+' (in Ms)'] = [converted]
        elif col_val[1][-1] == '%':
            new_int = float(Decimal(col_val[1][0:-1]))
            converted = new_int/100
            technicals[col_name[0]] = [converted]
        else:
            try:
                isinstance(int(col_val[1][0]), int)
                new_int = float(Decimal(col_val[1]))
                technicals[col_name[0]] = [new_int]
            except ValueError:
                technicals[col_name[0]] = [col_val[1]]
            except InvalidOperation:
                technicals[col_name[0]] = [col_val[1]]

column_names = list(dict.fromkeys(technicals))
technicals_df = pd.DataFrame(technicals, index=[0])
technicals_df['Stock'] = tickers[0]
technicals_df.set_index('Stock', inplace=True)
#print(column_names)
i=1
while i < len(tickers):
    url = 'https://finance.yahoo.com/quote/'+tickers[i]+'/key-statistics?p='+tickers[i]
    website = urllib.request.urlopen(url)
    data = website.read()
    soup = BeautifulSoup(data, 'html.parser')
    technicals = {}
    tables = soup.findAll('table', {"class": 'W(100%) Bdcl(c)'})

    for table in tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:
            col_name = row.find_all('span')
            col_name = [cell.text.strip() for cell in col_name]

            col_val = row.find_all('td')
            col_val = [cell.text.strip() for cell in col_val]
            
            if col_val[1] == 'N/A':
                technicals[col_name[0]] = float('Nan')
            elif col_val[1][-1] == 'T':
                new_int = float(Decimal(col_val[1][0:-1]))
                converted = new_int*1000000
                technicals[col_name[0]+' (in Ms)'] = [converted]
            elif col_val[1][-1] == 'B':
                new_int = float(Decimal(col_val[1][0:-1]))
                converted = new_int*1000
                technicals[col_name[0]+' (in Ms)'] = [converted]
            elif col_val[1][-1] == 'M':
                new_int = float(Decimal(col_val[1][0:-1]))
                converted = new_int*1
                technicals[col_name[0]+' (in Ms)'] = [converted]
            elif col_val[1][-1] == '%':
                if ',' in col_val[1]:
                    col_val[1] = col_val[1].replace(',','')
                    
                    if col_val[1][0] == '-':
                        new_int = float(Decimal(col_val[1][1:-1]))
                        converted = -(new_int/100)
                        technicals[col_name[0]] = [converted]
                    else:
                        new_int = float(Decimal(col_val[1][0:-1]))
                        converted = new_int/100
                        technicals[col_name[0]] = [converted]
                else:
                    if col_val[1][0] == '-':
                        new_int = float(Decimal(col_val[1][1:-1]))
                        converted = -(new_int/100)
                        technicals[col_name[0]] = [converted]
                    else:
                        new_int = float(Decimal(col_val[1][0:-1]))
                        converted = new_int/100
                        technicals[col_name[0]] = [converted]
            else:
                try:
                    isinstance(int(col_val[1][0]), int)
                    new_int = float(Decimal(col_val[1]))
                    technicals[col_name[0]] = [new_int]
                except ValueError:
                    technicals[col_name[0]] = [col_val[1]]
                except InvalidOperation:
                    technicals[col_name[0]] = [col_val[1]]


    append_df = pd.DataFrame(technicals, index=[i])
    append_df['Stock'] = tickers[i]
    append_df.set_index('Stock', inplace=True)
    technicals_df = pd.concat([technicals_df, append_df], join='outer')
    i+=1



while input('Start screening? (Y or N)\n') != 'N':
    df_to_merge = []
    columns_to_screen = input("Which fundamental to screen?\n1. Trailing P/E\n2. Forward P/E\n3. P/B\n4. Beta\n5. past dividend\n6. Market Cap\n")

    if len(columns_to_screen) > 1:                    
        selected = columns_to_screen.split(' ')
    else:
        selected = [columns_to_screen]
        
    if '1' in selected:
        criteria = input("Trailing P/E greater than or less than?\n1. Greater than\n2. Less than\n")
        number = int(input('What value?\n'))
        if criteria == '1':
            trailing_PE = pd.DataFrame(technicals_df[technicals_df['Trailing P/E'] >= number]['Trailing P/E'])
            print(trailing_PE)
            df_to_merge.append(trailing_PE)
        else:
            trailing_PE = pd.DataFrame(technicals_df[technicals_df['Trailing P/E'] <= number]['Trailing P/E'])
            print(trailing_PE)
            df_to_merge.append(trailing_PE)

    if '2' in selected:
        criteria = input("Forward P/E greater than or less than?\n1. Greater than\n2. Less than\n")
        number = int(input('What value?\n'))
        if criteria == '1':
            forward_PE = pd.DataFrame(technicals_df[technicals_df['Forward P/E'] >= number]['Forward P/E'])
            df_to_merge.append(forward_PE)
        else:
            forward_PE = pd.DataFrame(technicals_df[technicals_df['Forward P/E'] <= number]['Forward P/E'])
            df_to_merge.append(forward_PE)

    if '3' in selected:
        criteria = input("P/B Greater than or less than?\n1. Greater than\n2. Less than\n")
        number = int(input('What value?\n'))
        if criteria == '1':
            PB = pd.DataFrame(technicals_df[technicals_df['Price/Book'] >= number]['Price/Book'])
            df_to_merge.append(PB)
        else:
            PB = pd.DataFrame(technicals_df[technicals_df['Price/Book'] <= number]['Price/Book'])
            df_to_merge.append(PB)

    if '4' in selected:
        criteria = input("Beta Greater than or less than?\n1. Greater than\n2. Less than\n")
        number = float(Decimal(input('What value?\n')))
        if criteria == '1':
            beta = pd.DataFrame(technicals_df[technicals_df['Beta (5Y Monthly)'] >= number]['Beta (5Y Monthly)'])
            df_to_merge.append(beta)
        else:
            beta = pd.DataFrame(technicals_df[technicals_df['Beta (5Y Monthly)'] <= number]['Beta (5Y Monthly)'])
            df_to_merge.append(beta)

    if '5' in selected:
        criteria = input("Dividend Greater than or less than?\n1. Greater than\n2. Less than\n")
        number = float(Decimal(input('What value?\n')))
        if criteria == '1':
            div = pd.DataFrame(technicals_df[technicals_df['Trailing Annual Dividend Rate'] >= number]['Trailing Annual Dividend Rate'])
            df_to_merge.append(div)
        else:
            div = pd.DataFrame(technicals_df[technicals_df['Trailing Annual Dividend Rate'] <= number]['Trailing Annual Dividend Rate'])
            df_to_merge.append(div)
            
    if '6' in selected:
        criteria = input("Market cap (in millions) Greater than or less than?\n1. Greater than\n2. Less than\n")
        number = int(input('What value?\n'))
        if criteria == '1':
            mktcap = pd.DataFrame(technicals_df[technicals_df['Market Cap (intraday) (in Ms)'] >= number]['Market Cap (intraday) (in Ms)'])
            df_to_merge.append(mktcap)
        else:
            mktcap = pd.DataFrame(technicals_df[technicals_df['Market Cap (intraday) (in Ms)'] <= number]['Market Cap (intraday) (in Ms)'])
            df_to_merge.append(mktcap)

    cleaned = pd.concat(df_to_merge, axis=1, join='inner')
    print(cleaned)


