from pyspark.sql import SparkSession
from os import walk
from frictionless import describe, Resource
from zipfile import ZipFile

def extract_zip(input_zip):
    input_zip=ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def main():
    spark = SparkSession.builder.appName('Exercise6') \
        .enableHiveSupport().getOrCreate()
    csvfiles =[]
    for (dirpath, dirnames, filenames) in walk("data"):
        for zipfile in filenames:
            if not zipfile.endswith('.zip'):
                continue
            for extractedfile in extract_zip(dirpath+"\\"+zipfile).items():
                filename = extractedfile[0]
                if not filename.endswith('.csv') or '__MACOSX' in filename:
                    continue
                filedata = extractedfile[1]
                csvfiles.append([filename, filedata])
    print(csvfiles)


if __name__ == '__main__':
    main()
