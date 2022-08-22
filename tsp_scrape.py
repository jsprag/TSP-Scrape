#!/usr/bin/env python
# script to scrape tsp fund prices from tsp.gov
# adapted from Python 2 script created by user Simbilis on Bogleheads.org
# https://www.bogleheads.org/forum/viewtopic.php?f=1&t=108388

import requests
import csv
from datetime import datetime, timedelta, date
import sys
import platform

fundTag = {
    'L Income'  : 'TSPLINCOME',
    'L 2025' : 'TSPL2025',
    'L 2030' : 'TSPL2030',
    'L 2035' : 'TSPL2035',
    'L 2040' : 'TSPL2040',
    'L 2045' : 'TSPL2045',
    'L 2050' : 'TSPL2050',
    'L 2055' : 'TSPL2055',
    'L 2060' : 'TSPL2060',
    'L 2065' : 'TSPL2065',
    'G Fund' : 'TSPGFUND',
    'F Fund' : 'TSPFFUND',
    'C Fund' : 'TSPCFUND',
    'S Fund' : 'TSPSFUND',
    'I Fund' : 'TSPIFUND'}

priceHistoryFile = 'tspQuicken.csv'

# quicken file dates are: m/dd/yyyy
# tsp URL dates are: yyyy-mm-dd
quicken_lastDate = ''
try:
    quickenReader = csv.reader(open(priceHistoryFile, 'r'))
    quicken_lastDate = [row for row in quickenReader][-1][2]
except:
    quicken_lastDate = '01/01/2003'

quicken_endDate = date.today().strftime('%m/%d/%Y')
if quicken_lastDate == quicken_endDate:
    print('already have prices through', quicken_endDate)
    sys.exit()

tsp_startDate = (datetime.strptime(quicken_lastDate, '%m/%d/%Y') + timedelta(1)).strftime('%Y-%m-%d')
tsp_endDate = date.today().strftime('%Y-%m-%d')

print('checking for new prices starting on', tsp_startDate)
tspSharePricePageUrl = f'https://www.tsp.gov/data/fund-price-history.csv?startdate={tsp_startDate}&enddate={tsp_endDate}&Lfunds=1&InvFunds=1&download=0'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}

page = requests.get(tspSharePricePageUrl, headers=headers)

reader = csv.reader(page.text.splitlines(), delimiter=',')
rows = [row for row in reader if len(row) > 0]
tagRow = rows[0]
foundNew = False

newRows = []
for row in rows[1:]:
    tsp_curDate = row[0]
    if tsp_curDate >= tsp_startDate:
        quicken_curDate = datetime.strptime(tsp_curDate, '%Y-%m-%d').strftime('%m/%d/%Y')
        for i in range(1, len(row)):
            tag = tagRow[i].lstrip()
            if tag in fundTag:
                try:
                    price = float(row[i])
                except:
                    continue
                newRows.append([tsp_curDate, fundTag[tag], price, quicken_curDate])
                foundNew = True
                #print('found', [fundTag[tag], price, quicken_curDate])

if foundNew:
    with open(priceHistoryFile, "a", newline='') as file:
        writer = csv.writer(file)
        # sort by tsp_curDate (yyyy-mm-dd) to ensure most recent record is last
        newRows = [row[1:] for row in sorted(newRows)]
        writer.writerows(newRows)

if platform.system() == 'Darwin':
    # Quicken for Mac can only import prices for a single Security
    #   Windows> Securities> (Double click a Security)> Price History> Import History From CSV File...
    #   Required Header: Date, Open, Close, High, Low, Volume
    #   Required Columns: Date, Close
    #   Unknown columns are ignored by Quicken
    # convert multi-Security priceHistoryFile to multiple single-Security security.csv
    print(f'Converting {priceHistoryFile} to multiple security.csv as required by Quicken For Mac...\n')
    try:
        import pandas as pd
        df_in = pd.read_csv(priceHistoryFile, names='Ticker Close Date'.split())
        df_in['Open High Low Volume'.split()] = ''
        for ticker, df in df_in.groupby('Ticker'):
            csv_name = f'{ticker}.csv'
            print(csv_name)
            df.to_csv(csv_name, index=False)
    except ImportError as e:
        print(repr(e), '\nMacOS conversion requires pandas:\n\tpip install pandas')

sys.exit()
