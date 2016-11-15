# APYE

[![Build Status](https://travis-ci.org/adalsa91/APYE.svg?branch=master)](https://travis-ci.org/adalsa91/APYE)

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
	export APP_SETTINGS="config.DevelopmentConfig"
	export DATABASE_URL="postgresql://<user>:<password>@localhost/apye_users"
	export SECRET_KEY="SuperSecretKey"
```

##Automaticación
Se han definido algunas reglas en el fichero [Makefile](https://github.com/adalsa91/APYE/blob/master/Makefile) para automatizar algunas tareas:

- **install**: instalara los requirimiento necesarios para la aplicación mediante *pip*.
- **test**: ejecuta todos los test.
- **run**: lanza la aplicación.
    
##Integración continua
Para la integración continua se ha utilizado [Travis CI](https://travis-ci.org/adalsa91/APYE), para más información sobre los tests y el proceso de integración continua consultar la [documentación del proyecto](https://adalsa91.github.io/APYE/).



[Página web del proyecto](https://adalsa91.github.io/APYE/ "Página web del proyecto")

>Adrián Álvarez Sáez
