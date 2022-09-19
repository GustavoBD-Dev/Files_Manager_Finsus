
from ast import Try
from tkinter.messagebox import NO


def getTableFile_txt(fileName):
    # get file in directory
    file = open(fileName, "r", encoding='utf-8')
    # the data in file is save in the matrix
    rows = []
    # read all lines
    fileTable = file.readlines()
    # print line to line
    for row in fileTable:
        lineComplete = row.split('|')
        for i in range(len(lineComplete)):
            lineComplete[i] = lineComplete[i].strip()
        rows.append(lineComplete)
    # delete the second and the latest two rows
    rows.pop(1)
    rows.pop(len(rows)-1)  # length o list decrement
    rows.pop(len(rows)-1)  # the penultimate is now last
    # close the file
    file.close
    return rows


def getTableFile_csv(fileName):
    from csv import reader
    # the data in file is save in the matrix
    rows = []
    with open(fileName, 'r') as csv_file:
        csv_reader = reader(csv_file)  # default delimiter = ','
        # Passing the cav_reader object to list() to get a list of lists
        rows = list(csv_reader)
    return rows


def buildLayout(listOne, listTwo, listThird, listFour):
    print(listOne)
    print(listTwo)
    print(listThird)
    print(listFour)

    body = []

    # vin1
    body.append(listTwo[0])
    # nombre
    body.append(listOne[0])
    # referencia
    body.append(listOne[1])
    # cliente
    body.append(listOne[2])
    # idrol
    body.append(listOne[3])
    # credito
    body.append(listOne[4])
    # saldo_insoluto
    body.append(listOne[5])
    # saldo_insoluto_formato
    body.append('"{}"'.format(listOne[6])) ######
    # tipo_proceso
    body.append(listOne[7])
    # empresa
    body.append(listOne[8])
    # direccion_completa
    body.append('"{}"'.format(str(listOne[9]))) ##
    # telefono_fijo
    body.append(listOne[10])
    # email
    body.append(listOne[11])
    # celular
    body.append(listOne[12])
    # fechaape
    body.append(listOne[13])
    # plazo
    body.append(listFour[0])
    # mensualidad
    body.append(listFour[1])
    # bullet
    body.append(listFour[2])
    # fecha_vencimiento
    body.append(listFour[3])
    # cuenta_2001
    body.append(listThird[3])
    # lugarnacimiento
    body.append(listOne[14])
    # sexo
    body.append(listOne[15])
    # rfc
    body.append(listOne[16])
    # curp
    body.append(listOne[17])
    # ocupacion
    body.append(listOne[18])
    # fechanacimiento
    body.append(listOne[19])
    # ruta
    body.append('"{}"'.format(str(listOne[20])))
    # edad
    body.append(listOne[21])
    # vin
    body.append(listTwo[0])
    # modelo
    body.append(listTwo[1])
    # marca
    body.append(listTwo[2])
    # motor
    body.append(listTwo[3])
    # descripcion
    body.append(listTwo[4])
    # color
    body.append(listTwo[5])
    # cat
    body.append('')
    # saldo_insoluto_texto
    body.append(listOne[22])

    return body

def saveLayoutInCSV(layout):
    import numpy as np 
    np.savetxt("C:\Files_Manager_Finsus\outputs\info_error.csv", layout, delimiter =",",fmt ='% s', format="utf-8")

if __name__ == "__main__":
    firstTable = getTableFile_txt("src\\data\\datos_hilda.txt")
    secondTabe = getTableFile_txt("src\\data\\vin_datos_hilda.txt")
    thirdTable = getTableFile_csv("src\\layout_contract.csv")
    fourTable = getTableFile_csv("C:\\Files_Manager_Finsus\\outputs\\DataFilesPayPDF_ALETTIA.csv")

    
    # print the values of list
    """print(firstTable)
    print('\n\n')
    print(secondTabe)
    print('\n\n')
    print(thirdTable)
    print('\n\n')
    print(fourTable)
    print('\n\n\n\n')
    print(firstTable[0][4]) # key -> number of credit
    print(secondTabe[0][0]) # key -> value of vin
    print(thirdTable[0][0]) # 
    print(fourTable[0][4])  # key -> number of credit"""

    layoutComplete = []

    head = ["vin1", "nombre", "referencia", "cliente", "idrol", "credito", "saldo_insoluto", "saldo_insoluto_formato", "tipo_proceso","empresa", "direccion_completa", "telefono_fijo", "email", "celular", "fechaape", "plazo", "mensualidad",
            "bullet", "fecha_vencimiento", "cuenta_2001", "lugarnacimiento", "sexo", "rfc", "curp", "ocupacion", "fechanacimiento", "ruta", "edad", "vin", "modelo", "marca", "motor", "descripcion", "color", "cat", "saldo_insoluto_texto"]
    layoutComplete.append(head)

    # delete the first row, contains the name of columns
    thirdTable.pop(0)

    try:
        # iterate to third table, all values
        for element in range(len(thirdTable)):

            listOne = None
            listTwo = None
            listThird = None
            listFour = None

            # print(thirdTable[element])
            listThird = thirdTable[element]

            # get data in first table
            # find the row that contanins the value (number of credit)
            for credit in range(len(firstTable)):
                # print(firstTable[credit][4], " >>>>>>>>>> ", thirdTable[element][0])
                if firstTable[credit][4] == thirdTable[element][0]:
                    # print(firstTable[credit])
                    listOne = firstTable[credit]

            # get data in second table
            # find the row that contains the value (vin)
            for vin in range(len(secondTabe)):
                if secondTabe[vin][0] == thirdTable[element][2]:
                    #print(secondTabe[vin])
                    listTwo = secondTabe[vin]

            # get data in the four table
            # find the ro that contains the value (number of credit)
            for credit in range(len(fourTable)):
                if fourTable[credit][4] == thirdTable[element][0]:
                    print(fourTable[credit])
                    listFour = fourTable[credit]

            if listOne == None :
                print(" NO SE ENCUENTRAN DATOS DE TABLA CREDITOS COMPLETOS !!!")
                break
            elif listTwo == None :
                print(" NO SE ENCUENTRAN DATOS DE VIN COMPLETOS !!!")
                break
            elif listThird == None :
                print(" REVISAR TABLA DE SOLICITUD")
                break
            elif listFour == None :
                print("NO SE ENCUENTRAN DATOS DE PAGARÉS COMPLETOS")
                break
            else:
                # built layout with the data in lists
                layoutComplete.append(buildLayout(listOne, listTwo, listThird, listFour))

        print('\n\n')
        print(layoutComplete)
        saveLayoutInCSV(layoutComplete)
    except:
        print('HA OCURRIDO UN ERROR')

    

    