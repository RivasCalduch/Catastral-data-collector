# author Jose Luis Rivas Calduch
# name Datos Catastro V 1
# date 2020.02.04
# -*- coding: utf-8 -*-

# Librerias

import urllib
from xml.dom import minidom
import datetime
import time
import pandas as pd

# Inicia el cronometro
started_at = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
print("Empiezo a:" + started_at)

# Crea output en excel
col_names = ['referencia','error','pc1','pc2','xcen', 'ycen','ldt']
my_df = pd.DataFrame(columns=col_names)

# leer excel
df = pd.read_excel('../data/input.xlsx')
search_items = df["referencia"].tolist()
 
for item in search_items:

    #Duerme un segundo
    time.sleep(1)

    # API DESCARGA INFORMACION DE GEOLOCALIZACION
    
    # Dirección del API para la descarga de los datos XML de geolocalización
    url = 'http://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_CPMRC?Provincia=&Municipio=&SRS=EPSG:4326&RC='
 
    # Referencia catastral matriz (14 caracteres)
    #referencia = '9076901BE7N'
    #referencia = '9076901BE4397N'
    referencia14 = item[0:14:]
 
    # Crea la url completa
    urlcompleta = url + referencia14

    try:

        # Descarga de la API la información XML
        sourceCode = urllib.request.urlopen(urlcompleta).read().decode('utf8')

        #Parsea la información
        doc = minidom.parseString(sourceCode)

        # Comprueba que la información es correcta
        controlgeo = doc.getElementsByTagName("cucoor")[0]
        controlgeo2 = doc.getElementsByTagName("cuerr")[0]

        controlgeoStr = controlgeo.firstChild.data
        controlgeoStr2 = controlgeo2.firstChild.data

        if controlgeoStr == '0':

            #Captura el tipo de error
            error = doc.getElementsByTagName("des")[0]
            errorStr = error.firstChild.data
            print(errorStr)

            #Carga variables en blanco

            pc1Str = "ND"
            pc2Str = "ND"
            xcenStr = "ND"
            ycenStr = "ND"
            ldtStr = "ND"

        else:

            #Captura los datos de la geolocalizacion

            pc1 = doc.getElementsByTagName("pc1")[0]
            pc2 = doc.getElementsByTagName("pc2")[0]
            xcen = doc.getElementsByTagName("xcen")[0]
            ycen = doc.getElementsByTagName("ycen")[0]
            ldt = doc.getElementsByTagName("ldt")[0]

            #Carga la variables en formato string
            pc1Str = pc1.firstChild.data
            pc2Str = pc2.firstChild.data
            xcenStr = xcen.firstChild.data
            ycenStr = ycen.firstChild.data
            ldtStr = ldt.firstChild.data

            #Carga varible error
            errorStr = "NO"

        #Imprime resultado de la consulta la consulta
        print(item + "-" + pc1Str + "-" + pc2Str + "-" + xcenStr + "-" + ycenStr + "-" + ldtStr)
        my_df = my_df.append(pd.Series([item,errorStr,pc1Str,pc2Str,xcenStr,ycenStr,ldtStr], index=my_df.columns), ignore_index=True)    

    except:
    
        print("Error de conexion!!!!!")

        # Fija el tiempo de finalizacion
        ended_at = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print("Termino a:" + ended_at)

        #Guarda el output
        my_df.to_excel("../outcomes/output.xlsx")
   
#Guarda el output
my_df.to_excel("../outcomes/output.xlsx")

#Mensaje de finalizacion con exito
print("He terminado con exito!!!!")

# Fija el tiempo de finalizacion
ended_at = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
print("Termino a:" + ended_at)
