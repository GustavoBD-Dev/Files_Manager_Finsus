"""
    This code generate contract PV, get data table of pay.
    dataPV.csv
    col[0]  : number of credit (antecedente)
    col[1]  : date of pay (antecedente)
    col[2]  : number of credit (now)
"""

from multiprocessing import context
import pandas as pd
import re, os, camelot
from PyPDF2 import PdfFileReader
from pathlib import Path
import os
from docxtpl import DocxTemplate
import pandas as pd
from csv import reader


def getDataPay():

    # directory of template file Word
    convenioPV = DocxTemplate("layouts/CONVENIO MODIFICATORIO_ARRENDAMIENTO PV_SUBSISTE SEGURO DE VIDA.docx") 

    files = "C:\\Files_Manager_Finsus\\inputs_PV\\" # route to find files PDF
    dirFiles = os.listdir(files) # list files in route

    with open('C:\\Files_Manager_Finsus\\src\\dataPV.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        #print(list_of_rows)


    # name of columns to get data 
    meses = ['','Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']


    for fichero in dirFiles: # each file to do

        ficheropath = os.path.join(files, fichero) # complete route of file
        filename = Path(ficheropath).stem

        if os.path.isfile(ficheropath) and (fichero.endswith('.pdf') or fichero.endswith('.PDF')):  # validate PDF

            temp = open(os.path.join(files, fichero), 'rb')
            PDF_read = PdfFileReader(temp)
            first_page = PDF_read.getPage(0)
            second_page = PDF_read.getPage(1)
            text = str(first_page.extractText()) # get text of file
            text_2 = str(second_page.extractText()) # get text of file

            index = text.find("FINANCIERA SUSTENTABLE DE")  # reference to find credit 

            parts = text.split()
            #for i in range(len(parts)):
            #    print(i, ' - ', parts[i])

            parts2 = text_2.split()
            #for i in range(len(parts2)):
            #    print(i, ' - ', parts2[i]) 

            # fin the numer of client
            start_nclient = text.find('M.N.)')
            end_nclient = text.find('1-6')
            N_CLIENT = text[start_nclient+5 : end_nclient]

            # find name of document, betwen the words continuacion y "suscriptor"
            start_name = text.find('continuación:')
            end_name = text.find('"Suscriptor"')
            NOMBRE = text[start_name+13: end_name] 

            # find amount 
            start_amount = text.find('"Beneficiario"')
            end_amount = text.find('M.N.)')
            #print(">>>>>>>>",start_amount)
            #print(end_amount)
            AMOUNT = text[start_amount+16: end_amount+5] 

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

            #print(df_out)

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

            #print(partial_income_table)
            #print(NOMBRE)
            #print(AMOUNT)
            #print(MONTHS_NUMBER)
            #print(MONTHS_TEXT)
            #print(N_CLIENT)
            #print(credito)

            dataValues = [] # list of dictionaries 
            
            # iterate the matrix of values
            for row in partial_income_table:
                aux_dic = {}                # crate the dictionary
                aux_dic['cols'] = row       # add value 'list' with the key 
                dataValues.append(aux_dic)  # add dictionary in the list

            # get data 'ANTECEDENTES'
            DATE_HISTORICAL = '______'
            CREDIT_HISTORICAL = '______'
            for i in range(len(list_of_rows)):
                for j in range(len(list_of_rows[i])):
                    #print(list_of_rows[i][j], end=' ')
                    if list_of_rows[i][2] == credito:
                        DATE_HISTORICAL = list_of_rows[i][1]
                        CREDIT_HISTORICAL = list_of_rows[i][0]
                #print()

            if DATE_HISTORICAL == '______' or CREDIT_HISTORICAL == '______':
                print(credito, ' NO CUENTA CON ANTECEDENTES')
            else:
                DATE_VALUES = DATE_HISTORICAL.split('/')
                DATE_HISTORICAL = DATE_VALUES[0]+ ' de '+ meses[int(DATE_VALUES[1])]+' de '+ DATE_VALUES[2]

                 # build context with data of the PDF
                context = {
                    'nombre' : NOMBRE,
                    'monto'  : '$ {}'.format(AMOUNT),
                    'plazo_texto'  : MONTHS_TEXT,
                    'plazo_numero'  : MONTHS_NUMBER,
                    'fecha'  : '01 de septiembre de 2022',
                    'tbl_data' : dataValues,
                    'fecha_antecedentes': DATE_HISTORICAL,
                    'no_arrendamiento': CREDIT_HISTORICAL
                }

                # generate the files Word with the data file PDF (table and other variables)
                fileDir = 'contratos/'
                convenioPV.render(context)
                convenioPV.save(fileDir+"/PV_"+str(NOMBRE).strip()+"_"+str(credito)+"_"+str(cliente)+"_.docx")
            

if __name__ == '__main__' :
    getDataPay()
