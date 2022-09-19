import os
from turtle import st
import numpy as np
from csv import reader

directory_files = 'C:/Users/Gustavo Blas/Desktop/CONTRATOS_GENERADOS'

with open('src\\data_names.csv', encoding='utf-8') as csv_file:
        csv_reader = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        print(list_of_rows)

for i in range(len(list_of_rows)):
    name = str(list_of_rows[i][0]).replace('\ufeff', '').replace('Ã±','Ñ').replace('Ã‰','É').replace('Ã‘','Ñ')
    new_name = str(list_of_rows[i][1]).replace('Ã±','Ñ').replace('Ã‰','É').replace('Ã‘','Ñ')
    os.rename(directory_files + '/' + str(name), directory_files + '_RENOMBRADOS/' + new_name)
    
