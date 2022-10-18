from ast import Bytes
from io import StringIO,BytesIO,TextIOWrapper
from zipfile import ZipFile
from os import walk
from frictionless import describe, Resource

def extract_zip(input_zip):
    input_zip=ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def ConvertFrictionlessTypeToPostgres(FrictionlessTypeName : str) -> str:
    if FrictionlessTypeName == 'integer': return 'int'
    if FrictionlessTypeName == 'string': return 'varchar(200)'
    if FrictionlessTypeName == 'datetime': return 'datetime'

def GetPostgresCreateTableSQLFromFields(TableName: str, Fields: str, IncludeForeignKeys: bool=False) -> str:
    ct = f'drop table if exists {TableName} cascade;\r\n\r\n'
    ct += f'create table {TableName}(\r\n'

    for i, field in enumerate(Fields): # build the create table script
        k=''
        if field.name.endswith('_id'): 
            if(i==0):# if it's the first column and it ends in _id then make it a primary key
                k = ' primary key'
            elif(IncludeForeignKeys): #otherwise make it a foreign key
                tablename = field.name.replace('_id','s')
                k = f' ,constraint fk_{field.name} foreign key({field.name}) references {tablename}({field.name})'
        ct+= f'{field.name} {ConvertFrictionlessTypeToPostgres(field.type)}{k},\r\n'
    ct = f'{ct[:len(ct)-3]});\r\n\r\n' # when done, get rid of trailing comma
    return ct

def main():
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
    
    for csvfile in csvfiles:
        #should probably validate it's really a csv file on this line
        with Resource(csvfile[1], format='csv') as resource:
            sql = GetPostgresCreateTableSQLFromFields(csvfile[0].replace('.csv',''), resource.schema.fields)
            print(sql)
            

if __name__ == '__main__':
    main()