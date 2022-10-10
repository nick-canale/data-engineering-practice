from fileinput import filename
import boto3
import os
import gzip
from urllib.parse import urlparse
from io import BytesIO

def downloads3file(Bucket, Key) -> BytesIO:
    session = boto3.Session(profile_name='default')
    s3 = session.resource('s3')
    object = s3.Object(bucket_name=Bucket, key=Key)

    file_stream = BytesIO()

    # Get the file in memory
    object.download_fileobj(file_stream)

    return file_stream

def main():

    Bucket = 'commoncrawl'
    Key = 'crawl-data/CC-MAIN-2022-05/wet.paths.gz'
    
    # Get the first file
    file_stream = downloads3file(Bucket,Key)

    # Extract the file
    file_stream.seek(0)
    decompressedFile = gzip.GzipFile(fileobj=file_stream, mode='rb')

    # Get the second file
    Bucket = 'commoncrawl'
    Key = decompressedFile.readline().decode().replace('\n','')
    file_stream = downloads3file(Bucket,Key)

    # Extract the second file
    file_stream.seek(0)
    decompressedFile = gzip.GzipFile(fileobj=file_stream, mode='rb')

    for l in decompressedFile:
        print(l)


if __name__ == '__main__':
    main()

