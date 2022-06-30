################################################################################
###      Procesar las bases de denue para que sean útiles a nivel ageb       ###
################################################################################
# By: Salvador Barcenas Valladolid

library(stringr)
setwd("/Users/salvadorbarcenas/Documents/reto/DENUE")

crear_llave_ageb<- function(base){
  
  base$cve_ent<- str_pad(base$cve_ent, 2, side = c("left"), pad = "0")
  base$cve_mun<- str_pad(base$cve_mun, 3, side = c("left"), pad = "0")
  base$cve_loc<- str_pad(base$cve_loc, 4, side = c("left"), pad = "0")
  base$ageb<- str_pad(base$ageb, 4, side = c("left"), pad = "0")
  
  
  base$LLAVE_AGEB<- paste0(base$cve_ent,base$cve_mun,base$cve_loc,base$ageb)
  
  return(base)
}


obtener_universo_tipo_establecimiento<- function(base,tipo_establecimiento){
  base<-aggregate(id~LLAVE_AGEB,base,length)
  names(base)<- c("LLAVE_AGEB",paste0("UNIVERSO_",tipo_establecimiento))
  
  return(base)
  
}


act_legislativas<- read.csv("Act_legislativas.csv")
act_legislativas<- crear_llave_ageb(act_legislativas)
act_legislativas<-obtener_universo_tipo_establecimiento(act_legislativas,"ACT_LEGISLATIVAS")

agricultura<- read.csv("Agricultura.csv")
agricultura<- crear_llave_ageb(agricultura)
agricultura<-obtener_universo_tipo_establecimiento(agricultura,"AGRICULTURA")


alimentos_1<- read.csv("Alojamiento_alimentos_y_bebidas_1.csv")
alimentos_2<- read.csv("Alojamiento_alimentos_y_bebidas_2.csv")
alimentos<- rbind(alimentos_1,alimentos_2)
alimentos<- crear_llave_ageb(alimentos)
alimentos<-obtener_universo_tipo_establecimiento(alimentos,"ALOJAMIENTO_ALIMENTOS_Y_BEBIDAS")
rm(alimentos_1,alimentos_2)


comercio_mayoreo<- read.csv("Comercio_al_por_mayor.csv")
comercio_mayoreo<- crear_llave_ageb(comercio_mayoreo)
comercio_mayoreo<-obtener_universo_tipo_establecimiento(comercio_mayoreo,"COMERCIO_MAYOREO")

comercio_menudeo_1<- read.csv("Comercio_al_por_menor_1.csv")
comercio_menudeo_2<- read.csv("Comercio_al_por_menor_2.csv")
comercio_menudeo_3<- read.csv("Comercio_al_por_menor_3.csv")
comercio_menudeo_4<- read.csv("Comercio_al_por_menor_4.csv")
comercio_menudeo<- rbind(comercio_menudeo_1,comercio_menudeo_2,
                         comercio_menudeo_3,comercio_menudeo_4)
rm(comercio_menudeo_1,comercio_menudeo_2
   ,comercio_menudeo_3,comercio_menudeo_4)

comercio_menudeo<- crear_llave_ageb(comercio_menudeo)
comercio_menudeo<-obtener_universo_tipo_establecimiento(comercio_menudeo,"COMERCIO_AL_POR_MENOR")


construccion<- read.csv("Construccion.csv")
construccion<- crear_llave_ageb(construccion)
construccion<-obtener_universo_tipo_establecimiento(construccion,"CONSTRUCCION")

corporativos<- read.csv("Corporativos.csv")
corporativos<- crear_llave_ageb(corporativos)
corporativos<-obtener_universo_tipo_establecimiento(corporativos,"CORPORATIVOS")


electricidad<- read.csv("Electricidad_agua_y_gas.csv",stringsAsFactors=FALSE, fileEncoding="latin1")
electricidad<- crear_llave_ageb(electricidad)
electricidad<-obtener_universo_tipo_establecimiento(electricidad,"ELECTRICIDAD_AGUA_Y_GAS")

ind_manofactureras<- read.csv("Ind_manofactureras.csv")
ind_manofactureras<- crear_llave_ageb(ind_manofactureras)
ind_manofactureras<-obtener_universo_tipo_establecimiento(ind_manofactureras,"IND_MANOFACTURA")

inf_medios_masivos<- read.csv("Inf_medios_masivos.csv")
inf_medios_masivos<- crear_llave_ageb(inf_medios_masivos)
inf_medios_masivos<-obtener_universo_tipo_establecimiento(inf_medios_masivos,"INF_MEDIOS_MASIVOS")


mineria<- read.csv("Mineria.csv")
mineria<- crear_llave_ageb(mineria)
mineria<-obtener_universo_tipo_establecimiento(mineria,"MINERIA")

servicios_negocios<- read.csv("Servicios_apoyo_negocios.csv")
servicios_negocios<- crear_llave_ageb(servicios_negocios)
servicios_negocios<-obtener_universo_tipo_establecimiento(servicios_negocios,"SERVICIOS_NEGOCIOS")

servicios_cientificos<- read.csv("Servicios_cientificos.csv")
servicios_cientificos<- crear_llave_ageb(servicios_cientificos)
servicios_cientificos<-obtener_universo_tipo_establecimiento(servicios_cientificos,"SERVICIOS_CIENTIFICOS")

servicios_salud<- read.csv("Servicios_de_salud.csv")
servicios_salud<- crear_llave_ageb(servicios_salud)
servicios_salud<-obtener_universo_tipo_establecimiento(servicios_salud,"SERVICIOS_SALUD")


servicios_educacion<- read.csv("Servicios_educativos.csv")
servicios_educacion<- crear_llave_ageb(servicios_educacion)
servicios_educacion<-obtener_universo_tipo_establecimiento(servicios_educacion,"SERVICIOS_EDUCACION")


servcios_no_gobierno_1<- read.csv("Servicios_excepto_gubernamentales_1.csv")
servcios_no_gobierno_2<- read.csv("Servicios_excepto_gubernamentales_2.csv")
servcios_no_gobierno<- rbind(servcios_no_gobierno_1,servcios_no_gobierno_2)
rm(servcios_no_gobierno_1,servcios_no_gobierno_2)
servcios_no_gobierno<- crear_llave_ageb(servcios_no_gobierno)
servcios_no_gobierno<-obtener_universo_tipo_establecimiento(servcios_no_gobierno,"SERVICIOS_EXCEPTO_GUBERNAMENTALES")


servicios_financieros<- read.csv("Servicios_financieros_y_seguros.csv")
servicios_financieros<- crear_llave_ageb(servicios_financieros)
servicios_financieros<-obtener_universo_tipo_establecimiento(servicios_financieros,"SERVICIOS_FINANCIEROS_Y_SEGUROS")


servicios_inmobiliarios<- read.csv("Servicios_inmobiliarios_y_de_alquiler.csv")
servicios_inmobiliarios<- crear_llave_ageb(servicios_inmobiliarios)
servicios_inmobiliarios<-obtener_universo_tipo_establecimiento(servicios_inmobiliarios,"SERVICIOS_INMOBILIARIOS_Y_ALQUILER")


servicios_recreativos<- read.csv("Servicios_recreativos.csv")
servicios_recreativos<- crear_llave_ageb(servicios_recreativos)
servicios_recreativos<-obtener_universo_tipo_establecimiento(servicios_recreativos,"SERVICIOS_RECREATIVOS")

transporte<- read.csv("Transportes_correos_y_almacenamiento.csv",stringsAsFactors=FALSE, fileEncoding="latin1")
transporte<- crear_llave_ageb(transporte)
transporte<-obtener_universo_tipo_establecimiento(transporte,"TRANSPORTE_CORREOS_Y_ALMACENAMIENTO")

### Unimos toda la data
base_final<- merge(act_legislativas,agricultura,all=TRUE)
base_final<- merge(base_final,alimentos,all=TRUE)
base_final<- merge(base_final,comercio_mayoreo,all=TRUE)
base_final<- merge(base_final,comercio_menudeo,all=TRUE)
base_final<- merge(base_final,construccion,all=TRUE)
base_final<- merge(base_final,corporativos,all=TRUE)
base_final<- merge(base_final,electricidad,all=TRUE)
base_final<- merge(base_final,ind_manofactureras,all=TRUE)
base_final<- merge(base_final,inf_medios_masivos,all=TRUE)
base_final<- merge(base_final,mineria,all=TRUE)
base_final<- merge(base_final,servcios_no_gobierno,all=TRUE)
base_final<- merge(base_final,servicios_cientificos,all=TRUE)
base_final<- merge(base_final,servicios_educacion,all=TRUE)
base_final<- merge(base_final,servicios_financieros,all=TRUE)
base_final<- merge(base_final,servicios_inmobiliarios,all=TRUE)
base_final<- merge(base_final,servicios_negocios,all=TRUE)
base_final<- merge(base_final,servicios_recreativos,all=TRUE)
base_final<- merge(base_final,servicios_salud,all=TRUE)
base_final<- merge(base_final,transporte,all=TRUE)


base_final[is.na(base_final)] <- 0


write.csv(base_final,"/Users/salvadorbarcenas/Documents/reto/data/Datos_denue_procesados.csv",row.names = FALSE)

