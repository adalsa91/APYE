##Hito 4

###Dockerfile
El **Dockerfile** utilizado para crear la imagen de la aplicación es el siguiente:

```
FROM debian:jessie

MAINTAINER Adrián Álvarez

#Sincronizamos el indice e instalamos dependencias
RUN apt-get update -y
RUN apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i es_ES -c -f UTF-8 -A /usr/share/locale/locale.alias es_ES.UTF-8
ENV LANG es_ES.utf8
RUN apt-get update -y &&  apt-get install -y libpq-dev python3-dev python3-pip git

#Descargamos apliccaión e instalamos requisitos con pip
RUN git clone https://github.com/adalsa91/APYE.git
WORKDIR /APYE
RUN pip3 install -r requirements.txt

EXPOSE 5000

#Fijamos el punto de entrada y el comando a ejecutar
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "--host" , "0.0.0.0"]

```

Tiene como base la imagen de *Debian Jessie* del [repositorio oficial](https://hub.docker.com/_/debian/), en primer lugar instalamos los locales de español a la imagen, después instalamos las dependencias mínimamente necesarias para la ejecución de la aplicación, en este caso: *libpq-dev python3-dev python3-pip y git*. Una vez configurado el sistema base procedemos a descargar la aplicación del repositorio de GitHub y seleccionamos como directorio de trabajo la raíz del repositorio, a continuación instalamos los requisitos de la aplicación con *pip*. Exponemos el puerto que utiliza el servidor incorporado en *Flask* (5000) al resto de contenedores, aunque este puerto se expondrá automáticamente al realizar el reenvío de puertos hacia el host es conveniente declararlo en el *Dockerfile* para más claridad. Por último fijamos el punto de entrada en `python3 manage.py` de está forma podremos lanzar directamente comándos a la aplicación desde el cliente de docker, en caso de que no se proporcione ningún comando se ejecutará `runserver --host 0.0.0.0` que deja la aplicación lista para funcionar.

Para crear la imagen con este *Dockerfile* ejecutamos el siguiente comando en la raíz del repositorio:

```bash
    $ docker build -t apye .
```

Si la operación se ha realizado con éxito podremos ver una nueva imagen ejecutando el comando `docker images`.

![Listado de imágenes](images/hito4/image1.png "Listado de imágenes")


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
 puede descargar y lanzar la imagen con el siguiente comando:

###Lanzar container
Para descargar y lanzar la imagen fijando las variables de entorno se puede usar el siguiente comando:

```bash
    $ docker run --name apye --link postgresql_container:postgresql -d -e APP_SETTINGS="config.DevelopmentConfig" -e DATABASE_URL="postgresql://apye:password@postgresql/apye" -e SECRET_KEY="Sql1D00WTF." -p 5000:5000 adalsa91/apye
```

- La opción `--link postgresql_container:postgresql` solo será necesaria si hemos creado un contenedor para postgreSQL, esta opción crea un enlace entre los contenedores, creando entre otras cosas una entrada en `/etc/hosts` con el nombre **postgres** y la dirección asociada del contenedor de nombre **postgresql_container**, de esta forma el contenedor podrá resolver la dirección del host de la url de la base de datos pasada como variable de entorno.

- La opción `-p 5000:5000` crea un reenvío de puertos del contenedor al host, para poder acceder a la aplicación.

###Punto de entrada
La imagen está configurada para arrancar la aplicación automáticamente, para ello tiene fijado como punto de entrada el comando `python3 manage.py` y como comándos por omisión `runserver --host 0.0.0.0`. Si se desea utilizar otro punto de entrada al arrancar el contenedor para por ejemplo arrancar un terminal se puede usar la opcíon `--entrypoint /bin/bash`, por ejemplo:
```bash
    $ docker run --name apye -i --entrypoint /bin/bash --link postgresql_container:postgresql -d -e APP_SETTINGS="config.DevelopmentConfig" -e DATABASE_URL="postgresql://apye:password@postgresql/apye" -e SECRET_KEY="Sql1D00WTF." -p 5000:5000 adalsa91/apye
```
###Creación tablas
Para crear las tablas necesarias para la aplicación en la base de datos de PostgreSQL debemos ejecutar el siguiente comando en el contenedor de la aplicación:

```bash
    $ python3 migrate.py db upgrade
```
###Docker Hub
Para subir nuestra imagen en primer lugar debemos crear una nueva [cuenta](https://hub.docker.com/r/adalsa91/) en Docker Hub. Una vez creada la cuenta creamos un [repositorio](https://hub.docker.com/r/adalsa91/apye/) donde alojaremos la imagen.

Una vez creada la cuenta y el repositorio tenemos que crear un tag para la imagen que queremos subir, este tag debe ser de la forma <dockerhub_user>/<repository>, para crear el tag usamos el siguiente comando:

``` bash
    $ docker tag <image_id> <dockerhub_user>/<repository>:latest
```

Con el comando `docker images` podemos comprobar que el nuevo tag se ha establecido correctamente.

![Listado de imágenes con tag](images/hito4/image2.png "Listado de imágenes con tag")

Ahora solo queda subirlo, para ello en primer lugar iniciamos sesión con `docker login` y a continuación ejecutamos el siguiente comando:

```bash
    $ docker push adalsa91/apye
```
![Subiendo imagen](images/hito4/image3.png "Subiendo imagen")

Si accedemos a nuesta cuenta de *Docker Hub* podemos comprobar que hay una nueva imagen.

![Imágenes cuenta Docker Hub](images/hito4/image5.png "Imágenes cuenta Docker Hub")

En el panel principal de nuestra cuenta podemos ver cuantas veces se ha descargado nuestra imagen.

![Número de descargas cuenta Docker Hub](images/hito4/image5.png "Número de descargas cuenta Docker Hub")
