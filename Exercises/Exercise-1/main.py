from fileinput import filename
import requests
import validators
import os
import zipfile
from urllib.parse import urlparse

download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]


def main():
    # Create the downloads directory
    if not os.path.exists('Downloads'):
        os.mkdir('Downloads')
    os.chdir('Downloads')

    #loop through the list and download the files, then write them to disk
    for i in download_uris:
        print(f'Downloading {i}')
        if os.path.exists(os.path.basename(urlparse(i).path)):
            print(f'Already retrieved file {os.path.basename(urlparse(i).path)}, skipping')
            continue
        if validators.url(i):
            r = requests.get(i)
        else:
            print(f'Malformed URL: {i}')
            continue
        with open(os.path.basename(urlparse(i).path), 'wb') as f:
            f.write(r.content)
    
    #Now extract the zip files
    for i in os.listdir():
        print(f'Attempting to unzip {i}')
        if zipfile.is_zipfile(i):
            f = zipfile.ZipFile(i)
        else:
            print(f'{i} is not a valid zip file')
            os.remove(i)
            continue
        for csv in f.infolist():
            if os.path.exists(csv.filename):
                print(f'Already unzipped file {csv.filename}, skipping')
                continue
            if not csv.filename.endswith('.csv'):
                print(f'{csv.filename} is not a CSV file')
                continue
            if csv.filename.startswith('__MACOSX'):
                print(f'I fucking hate macs')
                continue
            f.extract(csv)
        f.close()
        os.remove(i)
        
    
    pass


if __name__ == '__main__':
    main()
