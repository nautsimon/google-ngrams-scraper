import pandas as pd
import requests
import time
from pandas import DataFrame
import json
data = []

# enter the desired temporal bound to the query (as a string)
# note: the upper bound is non inclusive
startYear = "1920"
endYear = "2021"

# enter the path to the excel file with the words you want to query
excelPath = 'names.xlsx'
df = pd.read_excel(excelPath, index_col=0)

# If querying ever gets interrupted, restart at a certain excel index with the var below.
startAt = 0

# select the corpus
corpus = "26"

data = []
count = 0
qUrl = 'https://books.google.com/ngrams/json?content=' + \
    str(row[0])+'&year_start='+str(startYear) + \
    '&year_end='+str(endYear)+'&corpus='+str(corpus)
for row in df.iterrows():
    count += 1
    if count < startAt:
        continue

    response = requests.get(qUrl)
    time.sleep(1)
    jRep = json.loads(response.content)
    timeseries = jRep[0]['timeseries']
    newRow = [row[0]]
    for freq in timeseries:
        newRow.append(freq)
    data.append(newRow)
    print(newRow)

# create output csv
columns = ['Name']
for year in range(int(startYear), int(endYear)-1):
    print(year)
    columns.append(str(year))

outDf = DataFrame(data, columns=columns)
outDf.to_csv('ngrams.csv', encoding='utf-8')
