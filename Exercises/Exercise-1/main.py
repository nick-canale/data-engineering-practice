from fileinput import filename
import requests
import validators
import os
import zipfile
from urllib.parse import urlparse
import asyncio
import time
import aiohttp
import platform

download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

async def DownloadZipFile(ZipFileURL, session) -> str:
    print(f'Downloading {ZipFileURL}')
    SaveFileLocation = os.path.basename(urlparse(ZipFileURL).path)
    if os.path.exists(SaveFileLocation):
        print(f'Already retrieved file {SaveFileLocation}, skipping')
        return
    if validators.url(ZipFileURL):
        async with session.get(ZipFileURL) as resp:
            r = await resp.read()
    else:
        print(f'Malformed URL: {ZipFileURL}')
        return
    with open(SaveFileLocation, 'wb') as f:
        f.write(r) 
    return SaveFileLocation

async def ExtractZipFile(ZipFilePath, session) -> list:
    print(f'Attempting to unzip {ZipFilePath}')
    if zipfile.is_zipfile(ZipFilePath):
        f = zipfile.ZipFile(ZipFilePath)
    else:
        print(f'{ZipFilePath} is not a valid zip file')
        os.remove(ZipFilePath)
        return
    ExtractedFiles = []
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
        ExtractedFiles.append(csv.filename)
    f.close()
    os.remove(ZipFilePath)
    return ExtractedFiles

async def ProcessURIs(URI: str, session) -> None:
    start = time.perf_counter()
    ZipFile = await DownloadZipFile(URI, session)
    ExtractedFileNames = await ExtractZipFile(ZipFile, session)
    end = time.perf_counter() - start
    print(f"-->Processing {URI} (took {end:0.2f} seconds).")
    if ExtractedFileNames is not None:
        for fn in ExtractedFileNames:
            print(f"Extracted: {fn}")

async def main():
    # Create the downloads directory
    if not os.path.exists('Downloads'):
        os.mkdir('Downloads')
    os.chdir('Downloads')
    
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(ProcessURIs(n, session) for n in download_uris))


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
