# APYE

[![Build Status](https://travis-ci.org/adalsa91/APYE.svg?branch=master)](https://travis-ci.org/adalsa91/APYE)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

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

>Adrián Álvarez Sáez
