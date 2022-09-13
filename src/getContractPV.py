from datetime import date
from itertools import count
from lib2to3.pgen2.token import NAME
from multiprocessing import context
from tokenize import Double
import pandas as pd
import numpy as np
import re, os, camelot
from PyPDF2 import PdfFileReader
from pathlib import Path
from distutils.dir_util import mkpath
import os
from pickle import FALSE  
from docxtpl import DocxTemplate
import pandas as pd
import math


def getDataPay():

    # directory of template file Word
    convenioPV = DocxTemplate("layouts/CONVENIO MODIFICATORIO_ARRENDAMIENTO PV_SUBSISTE SEGURO DE VIDA.docx") 

    files = "C:\\GeneracionContratos\\inputs_PV\\" # route to find files PDF
    dirFiles = os.listdir(files) # list files in route

    # name of columns to get data 
    columnas = ['Pagos de Amortizacion','Fecha de Vencimiento','monto total a pagar']

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
            start_name = text.find('continuación:')
            end_name = text.find('"Suscriptor"')
            NOMBRE = text[start_name+13: end_name] 

            # find amount 
            start_amount = text.find('"Beneficiario"')
            end_amount = text.find('60/100')
            AMOUNT = text[start_amount+16: end_amount+6] 

            # find number of months
            start_months = text.find('durante')
            end_months = text.find('sucesivas')
            MONTHS_TEXT = text[start_months+12: end_months-7] 
            # get number of months in text
            MONTHS_NUMBER = text[start_months+8: start_months+10] 

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

            print(df_out)

            # get number of pay
            pay =  re.split("\\n| ", df_out[0][1])

            # get date of pay
            dates = re.split("\\n| ", df_out[1][1])

            # get month pay
            months =  re.split("\\n| ", df_out[2][1])

            # generate table with the list 
            table_data = []
            table_data.append(pay)
            table_data.append(dates)
            table_data.append(months)

            partial_income_table = []

            # build the data matrix, list of lists
            for i in range(len(table_data[0])):
                    aux = []
                    aux.append(table_data[0][i])
                    aux.append(table_data[1][i])
                    aux.append(table_data[2][i])
                    partial_income_table.append(aux)

            print(partial_income_table)
            print(NOMBRE)
            print(AMOUNT)
            print(MONTHS_NUMBER)
            print(MONTHS_TEXT)

            dataValues = [] # list of dictionaries 
            
            # iterate the matrix of values
            for row in partial_income_table:
                aux_dic = {}                # crate the dictionary
                aux_dic['cols'] = row       # add value 'list' with the key 
                dataValues.append(aux_dic)  # add dictionary in the list

            # build context with data of the PDF
            context = {
                'nombre' : NOMBRE,
                'monto'  : '$ {}'.format(AMOUNT),
                'plazo_texto'  : MONTHS_TEXT,
                'plazo_numero'  : MONTHS_NUMBER,
                'fecha'  : '01 de septiembre de 2022',
                'tbl_data' : dataValues
            }

            # generate the files Word with the data file PDF (table and other variables)
            fileDir = 'contratos/'
            convenioPV.render(context)
            convenioPV.save(fileDir+"/_(PRUEBA)_CONVENIO MODIFICATORIO_ARRENDAMIENTO PV_SUBSISTE SEGURO DE VIDA "+str(NAME)+".docx")
            

if __name__ == '__main__' :
    getDataPay()
