# APYE

[![Build Status](https://travis-ci.org/adalsa91/APYE.svg?branch=master)](https://travis-ci.org/adalsa91/APYE)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
[![Docker](https://camo.githubusercontent.com/8a4737bc02fcfeb36a2d7cfb9d3e886e9baf37ad/687474703a2f2f693632382e70686f746f6275636b65742e636f6d2f616c62756d732f7575362f726f6d696c67696c646f2f646f636b657269636f6e5f7a7073776a3369667772772e706e67)](https://hub.docker.com/r/adalsa91/apye/)

Proyecto para la asignatura de Infraestructura Virtual 2016-2017

##Descripción
La aplicación consiste en un gestor de ficheros que junto a un editor de texto permitirá al usuario la creación y edición de scripts de python, quedando estos almacenados permanentemente entre sesiones, posibilitando la opción de ejecutar estos scripts en un entorno virtual y seguro que devolverá los resultados del programa en pantalla.

##Herramientas
  - Framework Python (Flask)
  - Tecnología de virtualización de contenedores (Docker)
  - IaaS(e.g. Azure)

##Requisitos principales
  - Python 3
  - PostgreSQL
  - pip

##Instalación en local
```bash
	#Clonar repositorio
	$ git clone git@github.com:adalsa91/APYE.git
	$ cd APYE
	#Instalar dependencias
	$ make install
```

Es necesario definir tres variables de entorno:
```bash
	$ export APP_SETTINGS="config.DevelopmentConfig"
	$ export DATABASE_URL="postgresql://<user>:<password>@localhost/<db_name>"
	$ export SECRET_KEY="SuperSecretKey"
```

Una vez definidas las variables de entorno podemos ejecutar la aplicación.

```bash
	$ make run
```

Si todo ha ido bien se podrá acceder a la aplicación a través de la dirección [http://127.0.0.1:5000](http://127.0.0.1:5000)

##Automaticación
Se han definido algunas reglas en el fichero [Makefile](https://github.com/adalsa91/APYE/blob/master/Makefile) para automatizar algunas tareas:

- **install**: instalara los requirimiento necesarios para la aplicación mediante *pip*.
- **test**: ejecuta todos los test.
- **run**: lanza la aplicación.

##Integración continua
Para la integración continua se ha utilizado [Travis CI](https://travis-ci.org/adalsa91/APYE), para más información sobre los tests y el proceso de integración continua consultar la [documentación del proyecto](https://adalsa91.github.io/APYE/).

##Despliegue en un PaaS
Para el despliegue en un Paas he elegido [Heroku](https://dashboard.heroku.com/), ya que era el PaaS que mejores servicios gratuitos ofrecía, una interfaz web muy intuitiva y fácil de usar además disponía de unas herramientas de CLI muy completas para tareas más complejas, otro motivo de peso es la posibilidad de usar de forma gratuita el addon de PostgreSQL, ya que es el que usa mi aplicación me ahorro externalizar la base de datos. Además ofrece un servicio de *pipelines* que permite crear un flujo de trabajo entre entornos estilo `dev ---> staging ---> production` y por supuesto el soporte a Flask que es el framework que estoy usando para desarrollar la aplicación. Pensando en probar los *pipelines* he creado dos apps: [apye-stage](https://apye-stage.herokuapp.com/) y [apye-pro](https://apye-pro.herokuapp.com/).

**Para más información sobre como se ha realizado el despliegue consultar la [documentación del proyecto](https://adalsa91.github.io/APYE/)**

Si deseas desplegar este proyecto en Heroku utiliza el siguiente botón.
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

[Página web del proyecto](https://adalsa91.github.io/APYE/ "Página web del proyecto")


##Docker
Para crear la imagen de docker solo es necesario ejecutar el siguiente comando en la carpeta raíz del repositorio:

```bash
    $ docker build -t apye .
```

También es posible descargar la imagen directamente de los repositorios de Docker Hub [adalsa91/apye](https://hub.docker.com/r/adalsa91/apye/).

La aplicación necesita PostgreSQL para la persistencia de datos, como por ejemplo los datos de los usuarios, sin embargo este no se incluye en la imagen **adalsa91/apye**, la aplicación es independiente de como se decida instalar PostgreSQL, solo necesita conocer las credenciales y dirección del host a través de la variable de entorno `DATABASE_URL` que se detalla más adelante.

Se puede utilizar la imagen de PostgreSQL que hay disponible en los [repositorios oficiales de Docker Hub](https://hub.docker.com/_/postgres/), solo sería necesario ejecutar el siguiente comando:

```bash
    $ docker run --name postgresql_container -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=db_name -d postgres
```

###Variables de entorno
Para ejecutar la aplicación es necesario definir tres variables de entorno:
- **APP_SETTINGS**: indica el contexto de ejecución de la aplicación, puede tomar los siguientes valores:
    - **config.ProductionConfig**: para entornos de producción
    - **config DevelopmentConfig**: para desarrollo, habilita recarga automática de archivos python por parte del servidor integrado de Flask y además activa el depurador.
    - **config TestingConfig**: para realizar tests.
- **DATABASE_URL**: indica la url de la base de datos postgresql a usar. El formato de la url es: `postgresql://user:password@host/db_name`

- **SECRET_KEY**: clave secreta para cifrar sesiones.
 puede descargar y lanzar la imagen con el sigueinte comando:

###Lanzar container
Para descargar y lanzar la imagen fijando las variables de entorno se puede usar el siguiente comando:

```bash
    $ docker run --name apye --link postgresql_container:postgresql -d -e APP_SETTINGS="config.DevelopmentConfig" -e DATABASE_URL="postgresql://apye:password@postgresql/apye" -e SECRET_KEY="Sql1D00WTF." -p 5000:5000 adalsa91/apye
```

- La opción `--link postgresql_container:postgresql` solo será necesaria si hemos creado un contenedor para postgreSQL, esta opción crea un enlace entre los contenedores, creando entre otras cosas una entrada en `/etc/hosts` con el nombre **postgres** y la dirección asociada del contenedor de nombre **postgresql_container**, de esta forma el contenedor podrá resolver la dirección del host de la url de la base de datos pasada como variable de entorno.

- La opción `-p 5000:5000` crea un reenvío de puertos del contenedor al host, para poder acceder a la aplicación.

###Punto de entrada
La imagen está configurada para arrancar la aplicación automáticamente, para ello tiene fijado como punto de entrada el comando `python3 manage.py` y como comandos por omisión `runserver --host 0.0.0.0`. Si se desea utilizar otro punto de entrada al arrancar el contenedor para por ejemplo arrancar un terminal se puede usar la opcíon `--entrypoint /bin/bash`, por ejemplo:
```bash
    $ docker run --name apye -i --entrypoint /bin/bash --link postgresql_container:postgresql -d -e APP_SETTINGS="config.DevelopmentConfig" -e DATABASE_URL="postgresql://apye:password@postgresql/apye" -e SECRET_KEY="Sql1D00WTF." -p 5000:5000 adalsa91/apye
```
###Creación tablas
Para crear las tablas necesarias para la aplicación en la base de datos de PostgreSQL debemos ejecutar el siguiente comando en el contenedor de la aplicación:

```bash
    $ python3 migrate.py db upgrade
```

>Adrián Álvarez Sáez
