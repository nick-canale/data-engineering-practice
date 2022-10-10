from fileinput import filename
import requests
import pandas
import os
import time
import validators
import numpy


def main():
    # Get the html if it doesn't already exist
    if not os.path.exists('cdata.html'):
        with open('cdata.html', 'w') as f:
            f.write(requests.get('https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/').text) 

    
    header = ['Name','Last Modified','Size']
    datarows = []

    # Find the row with the given date
    with open('cdata.html') as f:
        for line in f.readlines():
            if '.csv' in line:
                datarows.append([line[34:49],line[76:92],line[117:121]])
    df = pandas.DataFrame(columns=header, data=datarows)
    FileName = df.loc[df['Last Modified'] == '2022-02-07 14:03'].max()[0]

    # Download the file if we haven't already
    URL = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/{FileName}'
    if os.path.exists(FileName):
        print(f'Already retrieved file {FileName}, skipping')
    else:
        if validators.url(URL):
            print(f'downloading {URL}')
            r = requests.get(URL)
        else:
            print(f'Malformed URL: {URL}')
            return
        with open(FileName, 'wb') as f:
            print(f'{URL} successfully downloaded, saving to disk.')
            f.write(r.content)


    
    # Read in the file and put it in pandas - this is the old and bad way
    # header2 = []
    # datarows2 = []
    # with open(FileName) as f:
    #     csvfile = csv.reader(f, delimiter=',', quotechar='"')
    #     for index, row in enumerate(csvfile, start=1):
    #         if(index == 1):
    #             header2 = row
    #         else:
    #             datarows2.append(row)
    
    df2 = pandas.read_csv(FileName)
    maxtemp = 0
    # this field has shit values in it like '82s' so it stored the values
    # as an object instead of float so max does not work
    for dbtemp in df2['HourlyDryBulbTemperature']:
        try:
            floatemp = float(dbtemp)
            if(floatemp > maxtemp):
                maxtemp = floatemp
        except:
            pass

    print(f'The max temp that is not a fucking shit bad data value is: {maxtemp}')

if __name__ == '__main__':
    main()
