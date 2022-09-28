"""
    Obtienen los datos del pagare dentro de una carpeta y se guardan en una archivo CSV
    - monto a pagar
    - monto final
    - ultima fecha de pago
    - No. total de pagos
    - No. de credito
    - Nombre
"""


# los datos se encuentran en la tabla por lo que debemos obtener la tabla del archivo
# analizando la tabla, los datos se encuentran en las siguientes posiciones
#    - monto a pagar (primer fila de la columna MONTO A PAGAR)
#    - monto final (ultim fila de la columna MONTO A PAGAR)
#    - ultima fecha de pago (ultima fila de la columna FECHA DE PAGO)
#    - No. total de pagos (ultima fila de la columna No DE PAGO)

from tokenize import Double
import pandas as pd
import numpy as np
import re, os, camelot
from PyPDF2 import PdfFileReader
from pathlib import Path
import numpy

files = "C:\\GeneracionContratos\\inputs" # route to find files PDF
dirFiles = os.listdir(files) # list files in route

DATA_FILES_PDF =  []    # list to save data in files PDF

# name of columns to get data 
columnas = ['TOTAL PAGOS','MONTO A PAGAR','MONTO TOTAL','FECHA FINAL' ,'NO CREDITO','NOMBRE','MONTO_LETRA']
DATA_FILES_PDF.append(columnas)

# name of variables to get  
MONTO_A_PAGAR = None
MONTO_TOTAL = None
FECHA_FINAL = None
TOTAL_PAGOS = None
NO_CREDITO = None
NOMBRE = None

# data frame
dfs = []

producto_fin = ""

for fichero in dirFiles: # each file to do

    ficheropath = os.path.join(files, fichero) # complete route of file
    filename = Path(ficheropath).stem

    if os.path.isfile(ficheropath) and (fichero.endswith('.pdf') or fichero.endswith('.PDF')):  # validate PDF

        temp = open(os.path.join(files, fichero), 'rb')
        PDF_read = PdfFileReader(temp)
        first_page = PDF_read.getPage(0)
        text = str(first_page.extractText()) # get text of file

        index = text.find("FINANCIERA SUSTENTABLE DE")  # reference to find credit 

        parts = text.split()
        for i in range(len(parts)):
            print(i, ' - ', parts[i])

        # find name of document, betwen the words continuacion y "suscriptor"
        start_name = text.find('Suscriptor')
        end_name = text.find('Obligado')
        NOMBRE = text[start_name+10: end_name-3]    

        # find the amount
        start_amount = text.find('$')
        end_amount = text.find('M.N.)"Beneficiario"')
        AMOUNT = text[start_amount+1: end_amount+5]   
        print(AMOUNT) 
        print(type(AMOUNT)) 

        if(index < 0):
            index = text.find("POSIBILIDADES  VERDES  S.A")

        cc = text[index-30:index]

        index = cc.find("-")
        cc = cc[index-1:-1]

        index = cc.rfind("-")
        index = cc.rfind("-", 0, index)
        credito = cc[index-1:len(cc)]
        cliente = cc[0:index-1]
        print(credito + " & " + cliente + " & " + cc)

        tables = camelot.read_pdf(os.path.join(files, fichero)) # find tables in PDF

        df = tables[0].df # in the pays, the tables is in first page
        df_out = pd.DataFrame(df)  

        # get index of latest element, this is the latest row 
        END_DATA = 0
        for i in range(len(df_out)):
            #print(df_out[1][i])
            if df_out[1][i].strip() == '':
                END_DATA = i
                #print(i)
                break

        # the date latest is in latest row
        FECHA_FINAL = df_out[1][END_DATA - 1]

        # total of elements
        TOTAL_PAGOS = END_DATA - 1

        # amount to pay monthly
        MONTO_A_PAGAR = df_out[9][1]

        # amount total
        MONTO_TOTAL = df_out[9][END_DATA - 1]

        # number of credit and name
        NO_CREDITO = credito 

        data_in_file = [TOTAL_PAGOS, str(MONTO_A_PAGAR).replace(',',''), str(MONTO_TOTAL).replace(',',''), FECHA_FINAL, NO_CREDITO, NOMBRE, AMOUNT]
        DATA_FILES_PDF.append(data_in_file)

# save data in file CSV
np.savetxt("C:\\GeneracionContratos\\outputs\\DataPDF_28-09-2022.csv", DATA_FILES_PDF, delimiter =",",fmt ='% s')
