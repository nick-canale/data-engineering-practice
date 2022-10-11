import psycopg2
from frictionless import describe
import os
import csv

def ConvertFrictionlessTypeToPostgres(FrictionlessTypeName : str) -> str:
    if FrictionlessTypeName == 'integer': return 'int'
    if FrictionlessTypeName == 'string': return 'varchar(200)'
    #if FrictionlessTypeName == 'integer': return int

def main():
    host = 'postgres'
    database = 'postgres'
    user = 'postgres'
    pas = 'postgres'
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)

    # your code here 
    os.chdir('data')

    for file in os.listdir(os.getcwd()):
        if file.endswith('.csv'):
            #should probably validate it's really a csv file on this line
            package = describe(file, type="package")
            TableName = package.resources[0].name
            ct = f'drop table if exists {TableName} cascade;\r\n\r\n'
            ct += f'create table {TableName}(\r\n'

            for i, field in enumerate(package.resources[0].schema.fields): # build the create table script
                k=''
                if field.name.endswith('_id'): 
                    if(i==0):# if it's the first column and it ends in _id then make it a primary key
                        k = ' primary key'
                    else: #otherwise make it a foreign key
                        tablename = field.name.replace('_id','s')
                        k = f' ,constraint fk_{field.name} foreign key({field.name}) references {tablename}({field.name})'
                ct+= f'{field.name} {ConvertFrictionlessTypeToPostgres(field.type)}{k},\r\n'
            ct = f'{ct[:len(ct)-3]});\r\n\r\n' # when done, get rid of trailing comma
            # print(package.to_yaml())
            print(ct)

            #Create the table in postgres
            with conn:
                with conn.cursor() as cur:
                    cur.execute(ct)

            #Load the data
            with open(file, newline='') as csvfile:
                reader = csv.reader(csvfile, skipinitialspace=True)
                for i,row in enumerate(reader):
                    if i==0:
                        Columns = str(tuple(row)).replace("'","")
                    else:
                        Data = str(row).replace('[','(').replace(']',')')
                        with conn:
                            with conn.cursor() as cur:
                                cur.execute(f'insert into {TableName} {Columns} values {Data}')

            

if __name__ == '__main__':
    main()
