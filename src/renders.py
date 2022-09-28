from cmath import isnan
from distutils.dir_util import mkpath
from tkinter.messagebox import NO
import numbers_to_letter
import os, sys
from pickle import FALSE  
from docxtpl import DocxTemplate
import pandas as pd
import pyodbc
import math

carta = pd.read_csv('C:\\GeneracionContratos\\info_render.csv',encoding = 'utf-8')


meses = ['','Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

for dt in carta.index:
  #print(dt)
  anexo1 = DocxTemplate("layouts/A N E X O 1. Solicitud_VF_DATOS.docx") 
  anexo2 = DocxTemplate("layouts/A N E X O 2. Datos Generales del Crédito_VF.docx") 
  anexo3 = DocxTemplate("layouts/A N E X O 3. Adendum ENCO_VF.docx") 
  anexo4 = DocxTemplate("layouts/A N E X O 4. Adendum CAS_VF.docx") 
  anexo5 = DocxTemplate("layouts/A N E X O 5. Comisiones_VF.docx") 
  anexo6 = DocxTemplate("layouts/A N E X O 6. Preceptos Legales_VF.docx") 
  caratula_en_ruta = DocxTemplate("layouts/Carátula_EN RUTA (XXXI-I-2022)_VF.docx") 
  carta_finiquito = DocxTemplate("layouts/Carta finiquito TEMPLATE_EN RUTA.docx") 
  preautorizacion = DocxTemplate("layouts/CARTA_Preautorización PV (XXXI-I-2022)_VF.docx") 
  programa = DocxTemplate("layouts/CARTA_PROGRAMA_FINSUS_(XXXI-I-2022)_VF.docx") 
  apertura = DocxTemplate("layouts/CONTRATO DE APERTURA DE CRÉDITO SIMPLE CON GARANT╓A PRENDARIA (XXXI-I-2022)_VF.docx") 
  dacion = DocxTemplate("layouts/Dación en Pago_EN RUTA_(XXXI-I-2022)_VF.docx") 
  actualizacion = DocxTemplate("layouts/FORMATO DE ACTUALIZACIÓN DE DATOS_CLIENTE (XXXI-I-2022)_VF.docx") 
  obligado = DocxTemplate("layouts/FORMATO DE ACTUALIZACIÓN DE DATOS_OBLIGADO SOLIDARIO  (XXXI-I-2022)_VF.docx") 
  suscripcion = DocxTemplate("layouts/FORMATO DE AUTORIZACION DE SUSCRIPCION  (XXXI-I-2022)_VF.docx") 
  domiciliacion = DocxTemplate("layouts/Formato_Domiciliación (XXXI-I-2022)_VF.docx") 
  enruta = DocxTemplate("layouts/2022 02 06 Paquete de Firmas Sin Telefono 2.docx") 
  convenioMod = DocxTemplate("layouts/CONVENIO MOD_ACCESORIOS (25-VII-2022)_ LVM_FIRMADO (subsiste seguro de vida) CORRESPONDIDO.docx") 
  
  
  EnrutaMasConvenioModificatorio = DocxTemplate("layouts/2022 02 06 Paquete de Firmas Sin Telefono 2 MAS CONVENIO MODIFICATORIO.docx")
  EnrutaMasConvenioModificatorioCartaCondonacion = DocxTemplate("layouts/2022 02 06 Paquete de Firmas Sin Telefono 2 MAS CONVENIO MODIFICATORIO - CARTA_CONDONACION.docx")

  fecha_text = carta['fechaape'][dt].split('/')
  fecha_nac = carta['fechanacimiento'][dt].split('/')
  reca = '13916-439-035811/01-00414-0122'
  
  #print(str(carta['referencia'][dt]).zfill(10))
  monto_total = (carta['mensualidad'][dt] * (carta['plazo'][dt] -1)) + carta['bullet'][dt]
  context = {        
        'credito': carta['credito'][dt],
        'pais': 'México',
        'fecha_texto': fecha_text[0]+ ' de '+ meses[int(fecha_text[1])]+' de '+fecha_text[2],
        'nombre_completo' : carta['nombre'][dt].strip(),
        'ruta' : carta['ruta'][dt].strip(),
        'cuenta_2001' : carta['cuenta_2001'][dt].strip(),
        'direccion_completa': carta['direccion_completa'][dt],
        'pais_nacimiento': ' ',
        'entidad_nacimiento': ' ',
        'nacionalidad': ' ',
        'fecha_nacimiento_texto': fecha_nac[0]+ ' de '+ meses[int(fecha_nac[1])]+' de '+fecha_nac[2],
        'edad': carta['edad'][dt],
        'sexo': carta['sexo'][dt],
        'curp': carta['curp'][dt],
        'ocupacion': carta['ocupacion'][dt],
        'monto_max_formato': '{:,.2f}'.format(carta['mensualidad'][dt]),
        #'monto_max_texto': carta['mensualidad_formato'][dt],
        'fecha_apertura_texto': fecha_text[0]+ ' de '+ meses[int(fecha_text[1])]+' de '+fecha_text[2],
        'motor' : carta['motor'][dt],
        'vin': carta['vin'][dt],
        'marca': carta['marca'][dt],
        'modelo': int(carta['modelo'][dt]),
        'modelo_formato': carta['modelo'][dt],
        'color': carta['color'][dt],
        'saldo_insoluto_formato': '{:,.2f}'.format(carta['saldo_insoluto_formato'][dt]),
        'saldo_insoluto_texto': carta['saldo_insoluto_texto'][dt],
        'referencia_bancaria' : str(carta['referencia'][dt]).zfill(10),
        'celular' : carta['celular'][dt],
        'telefono_fijo' : carta['telefono_fijo'][dt],
        'reca': reca,
        'nombre_obligado_solidario' : '',
        'nombre_aseguradora': '',
        'cat' : carta['cat'][dt],
        'interes_moratorio': '20 %',
        'plazo': carta['plazo'][dt],
        'monto_total' : '{:,.2f}'.format(monto_total),
        'mensualidad': carta['mensualidad'][dt],
        'fecha_corte': 'Pendiente' ,
        'fecha_vencimiento':  carta['fecha_vencimiento'][dt],
        'bullet' : '{:,.2f}'.format(carta['bullet'][dt]),
        'correo' :carta['email'][dt],
        'descripcion_camioneta': carta['descripcion'][dt]+ ' Modelo ' +str(carta['modelo'][dt])+ ' con número de motor ' + carta['motor'][dt]+ ' VIN ' + carta['vin'][dt],
        'rfc': carta['rfc'][dt]
        #'condonacion_letra' :  carta['condonacion_formato'][dt]  
  }
  
  if  str(carta['condonacion'][dt]) != "NO APLICA":
    # AGREGAMOS VALORES DE CONDONACION
    #print((numbers_to_letter.numero_a_letras(int(float(carta['condonacion'][dt]))).upper()).replace("(",''))
    context['cond'] = str(float(carta['condonacion'][dt]))
    context['cond_letra'] = "({} PESOS {}/100 M/N)".format(
      #(numbers_to_letter.numero_a_letras(int(float(carta['condonacion'][dt]))).upper()).replace("(",''), 
      numbers_to_letter.numero_a_letras(int(float(carta['condonacion'][dt]))).upper(),
      str(carta['condonacion'][dt]).split('.')[1])
    context['monto_max_texto'] = "({} PESOS 0/100 M/N)".format(numbers_to_letter.numero_a_letras(int(float(carta['mensualidad'][dt]))))



  nombreRuta = carta['ruta'][dt].replace("..","")
  for r in ('"', ".", "/","..","\""):
    nombreRuta = nombreRuta.replace(r, "")
    
  fileDir = 'contratos/'
  
  #print(nombreRuta)
  try:
    os.stat('contratos/')
  except:
    os.mkdir('contratos/')
  
  try:
    os.stat(fileDir)
  except:
    os.mkdir(fileDir)

  
  #print(math.isnan(carta['cat'][dt]) )
    
  if(math.isnan(carta['cat'][dt]) == FALSE ):
    anexo1.render(context)  
    anexo1.save(fileDir+"/anexo1_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    anexo2.render(context)
    anexo2.save(fileDir+"/anexo2_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    anexo3.render(context)
    anexo3.save(fileDir+"/anexo3_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    anexo4.render(context)
    anexo4.save(fileDir+"/anexo4_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    anexo5.render(context)
    anexo5.save(fileDir+"/anexo5_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    anexo6.render(context)
    anexo6.save(fileDir+"/anexo6_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    caratula_en_ruta.render(context)
    caratula_en_ruta.save(fileDir+"/caratula_en_ruta_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    carta_finiquito.render(context)
    carta_finiquito.save(fileDir+"/carta_finiquito_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    preautorizacion.render(context)
    preautorizacion.save(fileDir+"/preautorizacion_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    programa.render(context)
    programa.save(fileDir+"/programa_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    apertura.render(context)
    apertura.save(fileDir+"/apertura_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    dacion.render(context)
    dacion.save(fileDir+"/dacion_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    actualizacion.render(context)
    actualizacion.save(fileDir+"/actualizacion_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    obligado.render(context)
    obligado.save(fileDir+"/obligado_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    suscripcion.render(context)
    suscripcion.save(fileDir+"/suscripcion_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    domiciliacion.render(context)
    domiciliacion.save(fileDir+"/domiciliacion_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
    convenioMod.render(context)
    convenioMod.save(fileDir+"/convenioMod_"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")

  #enruta.render(context)
  #enruta.save(fileDir+"/En_Ruta"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+carta['credito'][dt]+".docx")
  #print(context)
  if 'cond' in context:
    #print(context['cond_letra'])
    #print("Se agrega carta de condoniación")
    EnrutaMasConvenioModificatorioCartaCondonacion.render(context)
    EnrutaMasConvenioModificatorioCartaCondonacion.save(fileDir+"/"+str(carta['nombre'][dt]).strip()+"_"+str(carta['credito'][dt])+"_"+str(carta['vin'][dt])+"_"+str(carta['mensualidad'][dt])+".docx")
    print("[" + str(dt) + "] >>> " + str(carta['nombre'][dt]).strip()+"_"+str(carta['credito'][dt])+"_"+str(carta['vin'][dt])+"_"+str(carta['mensualidad'][dt])+".docx")
  else:
    EnrutaMasConvenioModificatorio.render(context)
    #EnrutaMasConvenioModificatorio.save(fileDir+"/En_Ruta"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+"("+str(dt)+")"+"_"+carta['credito'][dt]+".docx")
    EnrutaMasConvenioModificatorio.save(fileDir+"/"+str(carta['nombre'][dt]).strip()+"_"+str(carta['credito'][dt])+"_"+str(carta['vin'][dt])+"_"+str(carta['mensualidad'][dt])+".docx")
    print("[" + str(dt) + "] >>> " + str(carta['nombre'][dt]).strip()+"_"+str(carta['credito'][dt])+"_"+str(carta['vin'][dt])+"_"+str(carta['mensualidad'][dt])+".docx")
#EnrutaMasConvenioModificatorio.save("C:\\GeneracionContratos"+"/En_Ruta"+str(carta['idrol'][dt])+"_"+carta['nombre'][dt]+"_"+"("+str(dt)+")"+"_"+str(carta['credito'][dt])+".docx")
