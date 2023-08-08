# Proyecto steam
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2048px-Steam_icon_logo.svg.png" alt="La imagen no puede cargarse" width="500" height="500">

# Kevin Bonnin

En este proyecto se nos planteo tomar el rol de cientifico de datos en nuestro primer trabajo, en el cual nos an pedido que realicemos un modelo de machine-learning que prediga el precio de un videojuego, para cumplir con ese fín, encare el proyecto en las siguientes etapas.

# ETL

Lo primero es descargar las librerias necesarias junto con el archivo que se nos fué entregado y transformarlo en un dataframe para poder leerlo, interpretarlo y manipularlo.

Después de eso se crea una nueva columna llamada Year a partir de la columna release_date con el objetivo de tener disponibles solamente el año de lanzamiento de cada juego.

Y como última medida de esta parte, se disponibiliza el dataframe en un archivo .csv

# EDA

El EDA lo pensé con el fin de preparar los datos solamente para el modelo, ya que consideré que con el ETL ya se podía cumplir con los gets requeridos sin problemas.

Lo primero que se hizo fué importar las librerias necesarias y el archivo al igual que en el ETL.

Luego se revisó la correlación de las variables para determinar cuales eran las mas óptimas para el modelo, se decidió que estas variables eran 'genres' y 'specs'. También fueron consideradas 'tags' y 'metascore', pero una tenía demaciadas variables distintas y podía realentizar demaciado el modelo, mientras que la otra tenía muy pocos registros en comparación como para ser determinante. También se descartó 'discount_price' ya que a pesar de tener una fuerte correlación, es una variable que depende de la variable objetivo y no al revéz.

Una vez terminado eso se procedió a eliminar las filas en las que ubiera datos nulos, ya que se consideró que afectarían de mala manera al modelo.

Después de eso se desglosó las filas que contenían datos concatenados para que el modelo lo tome como variables independientes, esto se hizo creando una columna binaria por cada valor independiente que aperecía en esas filas, columnas en las que si ese juego poseía ese atributo se le colocó un 1 y donde no lo tenía, un 0.

Luego de eso se entrenó el modelo y se calculó el RMSE solicitado, y por último se diponibilizó esto en un archivo .pkl.

# main

En el main se realizó la creación de los gets y la función de prediccion.

En los gets se realizron códigos capaces de cumplir con las consignas puestas por los instructores, al igual que en la predicción, donde se utilizó Enum para tener disponibilizada en una lista de opciones de los generos y especificaciones utilizables en este modelo.

# Links

Repositorio de GitHub: https://github.com/KevinBonnin/proyecto-steam.git
Render: https://proyecto-steam.onrender.com/docs#/
Video: https://www.youtube.com/watch?v=XAHsTh-ZiOc