import os
import os.path
import json
import csv

def all_keys(dict_obj,parent_name=''):
    ''' This function generates all keys of
        a nested dictionary. 
    '''
    # Iterate over all keys of the dictionary
    for key , value in dict_obj.items():
        # If value is of dictionary type then yield all keys
        # in that nested dictionary
        if isinstance(value, dict):
            for k in all_keys(value,key):
                yield k
        else:
            if parent_name != '':
                parent_name = parent_name + '_'
            yield [parent_name+key,value]

def main():
    jsonfiles=[]
    for dirpath, dirnames, filenames in os.walk("data"):
        for filename in [f for f in filenames if f.endswith(".json")]:
            jsonfiles.append(os.path.join(dirpath, filename))
    
    for jf in jsonfiles:
        jf_file = open(jf)
        jf_data = json.load(jf_file)
        jf_file.close()

        count = 0

        header = []
        data = []

        for i in all_keys(jf_data):
            # Writing headers of CSV file
            header.append(i[0])
            data.append(i[1])

        output_csv_filename = os.path.basename(jf).replace('json','csv')
        if os.path.exists(output_csv_filename):
            os.remove(output_csv_filename)
        output_csv_file = open(output_csv_filename,'w', newline='')
        csv_writer = csv.writer(output_csv_file)
        csv_writer.writerow(header)
        csv_writer.writerow(data)
        output_csv_file.close()

if __name__ == '__main__':
    main()
