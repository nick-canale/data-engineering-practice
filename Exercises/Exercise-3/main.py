from fileinput import filename
import boto3
import os
import gzip
from urllib.parse import urlparse
from io import StringIO

def downloads3file(Bucket, FilePath :str, FileName, s3_client) -> StringIO:
    if not FilePath.endswith('/'):
        FilePath = FilePath + '/'
    if not os.path.exists(FileName):
        s3_client.download_file(Bucket, f'{FilePath}{FileName}', FileName)
    else:
        print(f'File already exists ({FileName})')
    return f

def main():
    session = boto3.Session(profile_name='default')
    s3_client = session.client('s3')
    Bucket = 'commoncrawl'
    FilePath = 'crawl-data/CC-MAIN-2022-05/'
    FileName = 'wet.paths.gz'

    
    # Get the file
    f = downloads3file(Bucket, FilePath, FileName, s3_client)

    #Extract the file
    with gzip.open(FileName) as f:
        file_header = f.readline()

    Bucket = 'commoncrawl'
    FileName = os.path.basename(urlparse(file_header).path)
    FilePath = os.path.dirname(urlparse(file_header).path)
    
    # Get the file
    downloads3file(Bucket, FilePath.decode("utf-8"), FileName.decode("utf-8"), s3_client)


    f = open(FileName, 'rb')
    lines = f.readlines()
    for l in lines:
        print(l)

if __name__ == '__main__':
    main()

