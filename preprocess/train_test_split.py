import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split

# Parameters
random_state=102
test_size=0.2
train_set_path='data/train_reto_precios.csv'
test_set_path='data/test_reto_precios.csv'


departamentos=pd.read_csv("data/reto_precios_procesado.csv")
# Quit duplicated departments
departamentos=departamentos.drop_duplicates(subset=["main_name","price","lat","lon"])

numerical_columns=['since_value',
       'days_on_site', 'amenities', 'age_in_years', 'bathrooms', 'cellars',
       'num_floors', 'monthly_fee', 'apartments_per_floor',
       'parking_lots', 'floor_situated', 'num_bedrooms',
        'm2', 'universo_act_legislativas',
       'universo_agricultura', 'universo_alojamiento_alimentos_y_bebidas',
       'universo_comercio_mayoreo', 'universo_comercio_al_por_menor',
       'universo_construccion', 'universo_corporativos',
       'universo_electricidad_agua_y_gas', 'universo_ind_manofactura',
       'universo_inf_medios_masivos', 'universo_mineria',
       'universo_servicios_excepto_gubernamentales',
       'universo_servicios_cientificos', 'universo_servicios_educacion',
       'universo_servicios_financieros_y_seguros',
       'universo_servicios_inmobiliarios_y_alquiler',
       'universo_servicios_negocios', 'universo_servicios_recreativos',
       'universo_servicios_salud',
       'universo_transporte_correos_y_almacenamiento',
       'delitos_contra_patrimonio', 'delitos_contra_familia',
       'delitos_contra_libertad_personal', 'delitos_contra_seguridad_sexual',
       'delitos_contra_la_sociedad',
       'delitos_contra_la_vida_y_la_integridad_corporal',
       'delitos_contra_otros_bienes_juridicos', 'total', 'pobtot', 'pobfem',
       'pobmas', 'población de 15 años o más analfabeta',
       'población de 6 a 14 años que no asiste a la escuela',
       'población de 15 años y más con educación básica incompleta',
       'población sin derechohabiencia a servicios de salud',
       'viviendas con piso de tierra',
       'viviendas que no disponen de excusado o sanitario',
       'viviendas que no disponen de agua entubada de la red pública',
       'viviendas que no disponen de drenaje',
       'viviendas que no disponen de energía eléctrica',
       'viviendas que no disponen de lavadora',
       'viviendas que no disponen de refrigerador', 'irs',
       'lugar_que_ocupa_en_el_contexto_nacional',
       'distancia_al_metro_mas_cercano']

categorical_columns=['department_type']
response_variable="price_square_meter"

# One Hot Encoding categorical varable
departamentos["department_type_loft"]=np.where(departamentos["department_type"]=="Loft",1,0)
dataset=departamentos[numerical_columns+["department_type_loft"]+[response_variable]]

# Split data
train, test=train_test_split(dataset,test_size=test_size, random_state=random_state)

# Save data
train.to_csv(train_set_path,index=False)
test.to_csv(test_set_path,index=False)
print("Train, test datasets saved!")

