################################################################################
### Asignar llave de ageb a cada departamento dependiendo de las coordenadas ###
################################################################################
# By: Salvador Barcenas Valladolid

library(sf)
library(stringr)
setwd("/Users/salvadorbarcenas/Documents/reto")


AGEBS<- read_sf("shape_agebs/00a.shp")

Departamentos<- read.csv("reto_precios.csv")
Departamentos <- st_as_sf(Departamentos,coords = c('lon',"lat"))
st_crs(Departamentos)<- 4326
Departamentos <- st_transform(Departamentos, crs = st_crs(AGEBS))


Departamentos$AGEB <- apply(st_intersects(AGEBS, Departamentos, sparse = FALSE), 2, 
                                function(col) {AGEBS[which(col), ]$CVEGEO}) 

Departamentos$geometry<- NULL

write.csv(Departamentos,"data/reto_precios_con_AGEB.csv",row.names = FALSE)

