import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

import pandas as pd
import numpy as np
import re
import geopy.distance


Departamentos=pd.read_csv("data/reto_precios_con_AGEB.csv")
# Impute missing values

Departamentos["address"]=Departamentos["address"].fillna("No Address")
Departamentos["amenities"]=Departamentos["amenities"].fillna(0)
Departamentos["cellars"]=Departamentos["cellars"].fillna(0)
Departamentos["num_floors"]=Departamentos["num_floors"].fillna(0)
Departamentos["monthly_fee"]=Departamentos["monthly_fee"].fillna("0 MXN")
Departamentos["monthly_fee"]=Departamentos["monthly_fee"].apply(lambda x: int(re.search('[0-9]+', x).group(0)))
Departamentos["apartments_per_floor"]=Departamentos["apartments_per_floor"].fillna(0)
Departamentos["disposition"]=Departamentos["disposition"].fillna("No Info")
Departamentos["floor_situated"]=Departamentos["floor_situated"].fillna(0)
Departamentos["orientation"]=Departamentos["orientation"].fillna("No Info")
Departamentos["department_type"]=Departamentos["department_type"].fillna("No Info")

# Geographical information
Departamentos["CVE_MUN"]=Departamentos["AGEB"].apply(lambda x: x[0:5])
Departamentos["CVE_LOC"]=Departamentos["AGEB"].apply(lambda x: x[0:9])

### EXTERNAL DATA

# DENUE
DENUE=pd.read_csv("DENUE/Datos_denue_procesados.csv")
Departamentos=Departamentos.merge(DENUE,left_on="AGEB",right_on="LLAVE_AGEB")

# Criminal data
Delitos=pd.read_csv("data/Delitos_por_municipio.csv")
Delitos["CVE_MUN"]=Delitos["CVE_MUN"].apply(lambda x: str(x).rjust(5, '0'))
Departamentos=Departamentos.merge(Delitos)

# INEGI Census
Poblacion=pd.read_csv("data/Poblacion_CDMX.csv")
Poblacion["ENTIDAD"]=Poblacion["ENTIDAD"].apply(lambda x: str(x).rjust(2, '0'))
Poblacion["MUN"]=Poblacion["MUN"].apply(lambda x: str(x).rjust(3, '0'))
Poblacion["LOC"]=Poblacion["LOC"].apply(lambda x: str(x).rjust(4, '0'))
Poblacion["AGEB"]=Poblacion["AGEB"].apply(lambda x: str(x).rjust(4, '0'))

Poblacion["LLAVE_AGEB"]=Poblacion["ENTIDAD"]+Poblacion["MUN"]+Poblacion["LOC"]+Poblacion["AGEB"]
Poblacion=Poblacion[["LLAVE_AGEB","POBTOT","POBFEM","POBMAS"]]

Poblacion.loc[Poblacion["POBFEM"]=="*","POBFEM"]="0"
Poblacion.loc[Poblacion["POBMAS"]=="*","POBMAS"]="0"
Poblacion["POBFEM"]=Poblacion["POBFEM"].astype(int)
Poblacion["POBMAS"]=Poblacion["POBMAS"].astype(int)

Poblacion=pd.DataFrame(Poblacion.groupby("LLAVE_AGEB")[["POBTOT","POBFEM","POBMAS"]].sum()).reset_index()
Departamentos=Departamentos.merge(Poblacion)

# Social backwardness index
Indice_Rezago_Social=pd.read_csv("data/IRS_localidades_2020 - CDMX.csv")
Indice_Rezago_Social["Población de 15 años o más analfabeta"]=Indice_Rezago_Social["Población de 15 años o más analfabeta"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Población de 6 a 14 años que no asiste a la escuela"]=Indice_Rezago_Social["Población de 6 a 14 años que no asiste a la escuela"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Población de 15 años y más con educación básica incompleta"]=Indice_Rezago_Social["Población de 15 años y más con educación básica incompleta"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Población sin derechohabiencia a servicios de salud"]=Indice_Rezago_Social["Población sin derechohabiencia a servicios de salud"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Viviendas con piso de tierra"]=Indice_Rezago_Social["Viviendas con piso de tierra"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Viviendas que no disponen de excusado o sanitario"]=Indice_Rezago_Social["Viviendas que no disponen de excusado o sanitario"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Viviendas que no disponen de agua entubada de la red pública"]=Indice_Rezago_Social["Viviendas que no disponen de agua entubada de la red pública"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Viviendas que no disponen de drenaje"]=Indice_Rezago_Social["Viviendas que no disponen de drenaje"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Viviendas que no disponen de energía eléctrica"]=Indice_Rezago_Social["Viviendas que no disponen de energía eléctrica"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Viviendas que no disponen de lavadora"]=Indice_Rezago_Social["Viviendas que no disponen de lavadora"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["Viviendas que no disponen de refrigerador"]=Indice_Rezago_Social["Viviendas que no disponen de refrigerador"].apply(lambda x: re.sub(',',  '.',x))
Indice_Rezago_Social["IRS"]=Indice_Rezago_Social["IRS"].apply(lambda x: re.sub(',',  '.',x))

Indice_Rezago_Social[['Población de 15 años o más analfabeta',
       'Población de 6 a 14 años que no asiste a la escuela',
       'Población de 15 años y más con educación básica incompleta',
       'Población sin derechohabiencia a servicios de salud',
       'Viviendas con piso de tierra',
       'Viviendas que no disponen de excusado o sanitario',
       'Viviendas que no disponen de agua entubada de la red pública',
       'Viviendas que no disponen de drenaje',
       'Viviendas que no disponen de energía eléctrica',
       'Viviendas que no disponen de lavadora',
       'Viviendas que no disponen de refrigerador', 'IRS']]=Indice_Rezago_Social[['Población de 15 años o más analfabeta',
       'Población de 6 a 14 años que no asiste a la escuela',
       'Población de 15 años y más con educación básica incompleta',
       'Población sin derechohabiencia a servicios de salud',
       'Viviendas con piso de tierra',
       'Viviendas que no disponen de excusado o sanitario',
       'Viviendas que no disponen de agua entubada de la red pública',
       'Viviendas que no disponen de drenaje',
       'Viviendas que no disponen de energía eléctrica',
       'Viviendas que no disponen de lavadora',
       'Viviendas que no disponen de refrigerador', 'IRS']].astype(float)

Indice_Rezago_Social["CVE_LOC"]=Indice_Rezago_Social["CVE_LOC"].apply(lambda x: str(x).rjust(9, '0'))
Departamentos=Departamentos.merge(Indice_Rezago_Social)

# Nearest subway
coordenadas_departamentos=pd.read_csv("data/reto_precios.csv")
Departamentos=Departamentos.merge(coordenadas_departamentos[["id","lat","lon"]])

metro_cdmx=pd.read_csv("data/lineasmetro2.csv")
metro_cdmx["lat"]=metro_cdmx["lat"].apply(lambda x: re.sub(',',  '.',x))
metro_cdmx["lon"]=metro_cdmx["lon"].apply(lambda x: re.sub(',',  '.',x))
metro_cdmx["lat"]=metro_cdmx["lat"].astype(float)
metro_cdmx["lon"]=metro_cdmx["lon"].astype(float)

def distance_to_closest_subway(coordinates):
    distances=[]
    for i in range(0,len(metro_cdmx)):
        coords_1=(coordinates["lat"],coordinates["lon"])
        coords_2=(metro_cdmx.loc[i,"lat"],metro_cdmx.loc[i,"lon"])
        distances.append(geopy.distance.geodesic(coords_1, coords_2).km*1000)
        
    return min(distances)

Departamentos["DISTANCIA_AL_METRO_MAS_CERCANO"]=Departamentos[["lat","lon"]].apply(lambda x: distance_to_closest_subway(x),
                                                                                  axis=1)

# Save the data
Departamentos.columns=list(map(str.lower, Departamentos.columns))
Departamentos.to_csv("data/reto_precios_procesado.csv",index=False)


