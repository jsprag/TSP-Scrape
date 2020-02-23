
#!/usr/bin/python
# script to scrape tsp fund prices from tsp.gov
# adapted from Python 2 script created by user Simbills on Bogleheads.org
# https://www.bogleheads.org/forum/viewtopic.php?f=1&t=108388

import requests
import csv
from datetime import datetime, timedelta, date
import sys

fundTag = {
    'L Income' : 'TSPLINCOME',
    'L 2020' : 'TSPL2020',
    'L 2030' : 'TSPL2030',
    'L 2040' : 'TSPL2040',
    'L 2050' : 'TSPL2050',
    'G Fund' : 'TSPGFUND',
    'F Fund' : 'TSPFFUND',
    'C Fund' : 'TSPCFUND',
    'S Fund' : 'TSPSFUND',
    'I Fund' : 'TSPIFUND'}

priceHistoryFile = 'tspQuicken.csv'

lastDate = ''
try:
    quickenReader = csv.reader(open(priceHistoryFile, 'r'))
    lastDate = [row for row in quickenReader][-1][2]
except:
    lastDate = '06/01/2003'
startDate = (datetime.strptime(lastDate, '%m/%d/%Y') + timedelta(1)).strftime('%m/%d/%Y')
endDate = date.today().strftime('%m/%d/%Y')
if lastDate == endDate:
    print('already have prices through', endDate)
    sys.exit()

print('checking for new prices starting on', startDate)
tspSharePricePageUrl = 'https://www.tsp.gov/InvestmentFunds/FundPerformance/index.html'
postData = {'startdate' : startDate, 'enddate' : endDate, 'whichButton' : 'CSV'}

page = requests.post(tspSharePricePageUrl, data = postData)

reader = csv.reader(page.text.splitlines(), delimiter=',')
rows = [row for row in reader if len(row) > 0]
tagRow = rows[0]
foundNew = False

newRows = []
for row in rows[:0:-1]:
    currDate = datetime.strptime(row[0], '%Y-%m-%d').strftime('%m/%d/%Y')
    for i in range(1, len(row)):
        tag = tagRow[i].lstrip()
        if tag in fundTag:
            try:
                price = float(row[i])
            except:
                continue
            newRows.append([fundTag[tag], price, currDate])
            foundNew = True
            print('found', [fundTag[tag], price, currDate])

if foundNew:
    with open(priceHistoryFile, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(newRows)

sys.exit()