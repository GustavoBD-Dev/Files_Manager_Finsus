"""
    Se obtiene un layout a partir de dos archivos txt que son generados
    a partir de una consulta en la base de datos
"""

table = []


with open('C:/Files_Manager_Finsus/src/carga_1.txt', 'r', encoding="utf8") as fichero:
    for linea in fichero:

        # split rows in columns
        row = linea.split('|')

        # delete 
        for column in range(len(row)):
            row[column] = row[column].strip()

        table.append(row)
        #print(linea, end='')

print(table)




